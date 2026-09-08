#!/usr/bin/env python3
"""Generate the derived parts of the site: log pages, feed, sitemap, timestamps.

Everything this script writes is derived from three sources of truth:

  * ``content/log/*.html`` — one hand-authored fragment per research-log entry.
  * ``data/components.json`` — the implementation status of every stage of the
    volatility system.
  * ``data/evidence/*.json`` — one published diagnostic report per file, each
    the ingest box's own output under a required provenance envelope.
  * ``git`` — the commit history, which supplies every ``lastmod`` and
    ``dateModified`` on the site.

Nothing here invents a date. That matters more than it sounds: freshness is a
real ranking input for both conventional search and AI answer engines, so a
hand-typed "last updated" is an incentive to lie. Deriving it from the commit
that actually changed the file removes the temptation and makes the claim
checkable by anyone with the repository.

Outputs (all generated, none hand-edited):

  * ``log/<entry>.html``   — one page per entry, with BlogPosting metadata
  * ``log/index.html``     — entry list, injected between BUILD markers
  * ``feed.xml``           — Atom feed of the research log
  * ``sitemap.xml``        — every indexable page, with real lastmod values
  * ``llms.txt``           — log section, injected between BUILD markers
  * ``index.html``         — build-status strip, injected between BUILD markers
  * ``vol/index.html``     — architecture grid, injected between BUILD markers
  * ``vol/build-status.html`` — pipeline, evidence and milestone, injected
  * ``vol/evidence/<slug>.html`` — one page per published diagnostic
  * timestamps stamped into every page's metadata

The component manifest exists because hand-written status prose is how this
site came to advertise a volatility surface fit that no code implemented: the
public pages were edited and the handbook, which was correct, was not. One
manifest, rendered everywhere status appears, makes that particular mistake
structurally harder — a status is changed in one place or not at all.

Usage:

    python3 scripts/build_site.py            # write
    python3 scripts/build_site.py --check    # exit 1 if anything is stale

``--check`` is what CI runs, so a push that edits a page without rebuilding is
caught rather than silently shipping a stale sitemap.

Exit codes: 0 ok, 1 stale (--check) or refused, 2 could not run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import html
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://bradlasater.com"
AUTHOR = "Brad Lasater"
AUTHOR_EMAIL = "brad@bradlasater.com"

# Commits made by this script are skipped when computing a file's modification
# date. Without that exclusion, stamping a date into a file changes the file,
# which changes its last-commit date, which demands another stamp — the build
# would never reach a fixed point.
BUILD_COMMIT_SUBJECT = "chore: rebuild derived site metadata"

# Hand-authored pages that belong in the sitemap, in the order a reader would
# meet them. 404.html is deliberately absent: it carries noindex and must never
# be submitted for indexing. The handbook under handbook/ is also absent, but
# for a different reason — see handbook_pages() below.
STATIC_PAGES = [
    "index.html",
    "vol/index.html",
    "vol/build-status.html",
    "vol/methodology.html",
    "vol/track-record.html",
    "log/index.html",
    "cv.html",
]

ENTRY_SRC_DIR = ROOT / "content" / "log"

# Every page that carries the site header and footer, with the nav state it
# should show: (primary active, primary ancestor, section-bar active).
# index.html marks nothing current — "Work" and "Contact" are anchors on it,
# and aria-current on a link to the page you are already on is noise.
# 404.html appears here but not in STATIC_PAGES: it needs the same chrome as
# every other page but carries noindex and must never reach the sitemap.
CHROME_PAGES: dict[str, tuple[str, str, str]] = {
    "index.html":              ("",    "",    ""),
    "cv.html":                 ("cv",  "",    ""),
    "404.html":                ("",    "",    ""),
    "log/index.html":          ("log", "",    ""),
    "vol/index.html":          ("vol", "",    "vol-overview"),
    "vol/build-status.html":   ("",    "vol", "vol-build-status"),
    "vol/methodology.html":    ("",    "vol", "vol-methodology"),
    "vol/track-record.html":   ("",    "vol", "vol-track-record"),
}

COMPONENTS_PATH = ROOT / "data" / "components.json"
EVIDENCE_SRC_DIR = ROOT / "data" / "evidence"
EVIDENCE_OUT_DIR = ROOT / "vol" / "evidence"

# How a published diagnostic was derived. This is required on every report and
# is not cosmetic: with no option NBBO entitlement, every analytic this project
# produces comes from traded prices, and a reader who assumed a quote midpoint
# would draw the wrong conclusion from an identical-looking number.
INPUT_TYPES = {
    "last_trade_else_day_close": "Traded prices — last trade, else day close. No quote midpoint.",
    "day_bars": "Session aggregates from the option day-bar archive.",
    "nbbo_mid": "Quote midpoints. Requires an option NBBO entitlement.",
    "mixed": "More than one input kind; see the report's own limitations.",
}

# The four implementation states, in the order a component moves through them.
# Each maps to a label and the badge classes that render it. A badge is never
# the whole claim: every component also carries current_behaviour and
# design_intent as separate required fields, so a reader can tell what a stage
# does today from what it is designed to do eventually.
STATES: dict[str, tuple[str, str]] = {
    "operational": ("Operational", "badge badge--live badge--dot"),
    "implemented_unvalidated": ("Implemented — under validation", "badge badge--active badge--dot"),
    "in_progress": ("In progress", "badge badge--progress badge--dot"),
    "planned": ("Planned", "badge"),
}

MARKER = re.compile(
    r"(<!-- BUILD:(?P<name>[A-Z-]+):START -->)(?P<body>.*?)(<!-- BUILD:(?P=name):END -->)",
    re.DOTALL,
)


# ---------------------------------------------------------------------------
# git
# ---------------------------------------------------------------------------

def git(*args: str) -> str:
    """Run git, returning stdout. Raises on failure so problems are loud."""
    proc = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


@functools.lru_cache(maxsize=None)
def last_modified(relpath: str) -> dt.datetime:
    """The commit date of the last non-build commit to touch ``relpath``.

    Falls back to the current time for a file git has never seen — a brand new
    entry being previewed locally, typically. Never fabricates a past date.

    A git *failure* (not a repository, corrupt index, git missing) is not the
    fallback case: ``git log`` on an untracked path exits 0 with empty output,
    so an empty result genuinely means "never committed". Letting the error
    propagate keeps a broken checkout from silently stamping every page with
    the build time. Cached because render_feed and render_sitemap each ask for
    every entry's date again, and each call is a git subprocess.
    """
    out = git(
        "log", "-1", "--format=%cI", "--no-merges",
        "--invert-grep", f"--grep=^{BUILD_COMMIT_SUBJECT}",
        "--", relpath,
    ).strip()
    if not out:
        return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    return dt.datetime.fromisoformat(out).replace(microsecond=0)


# ---------------------------------------------------------------------------
# entries
# ---------------------------------------------------------------------------

class Entry:
    """One research-log entry, parsed from a hand-authored fragment."""

    REQUIRED = ("title", "date", "summary")

    def __init__(self, path: pathlib.Path):
        self.path = path
        self.src_rel = str(path.relative_to(ROOT))
        raw = path.read_text(encoding="utf-8")

        match = re.match(r"\s*<!--meta\s*\n(.*?)\n\s*-->\s*\n", raw, re.DOTALL)
        if not match:
            raise SystemExit(
                f"{self.src_rel}: missing the <!--meta ... --> block at the top of the file."
            )

        self.meta: dict[str, str] = {}
        for line in match.group(1).splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                raise SystemExit(f"{self.src_rel}: cannot parse meta line {line!r}.")
            key, value = line.split(":", 1)
            self.meta[key.strip()] = value.strip()

        missing = [k for k in self.REQUIRED if not self.meta.get(k)]
        if missing:
            raise SystemExit(f"{self.src_rel}: meta block missing {', '.join(missing)}.")

        self.body = raw[match.end():].strip()
        if not self.body:
            raise SystemExit(f"{self.src_rel}: no body content after the meta block.")

        try:
            self.date = dt.date.fromisoformat(self.meta["date"])
        except ValueError:
            raise SystemExit(
                f"{self.src_rel}: date {self.meta['date']!r} is not ISO YYYY-MM-DD."
            ) from None
        if self.date > dt.date.today():
            raise SystemExit(f"{self.src_rel}: date {self.date} is in the future.")

        self.slug = path.stem
        if self.slug == "index":
            # log/index.html is the entry list; an entry with this slug would
            # be silently overwritten by the index injection in main().
            raise SystemExit(
                f"{self.src_rel}: 'index' is reserved for the log index page; rename the file."
            )
        if not re.fullmatch(r"[A-Za-z0-9._~-]+", self.slug):
            # The slug is interpolated unescaped into URLs, HTML attributes,
            # the Atom feed, and the sitemap. RFC 3986 unreserved characters
            # are the only ones safe in all of those contexts.
            raise SystemExit(
                f"{self.src_rel}: filename slug {self.slug!r} is not URL-safe "
                "(use letters, digits, and - . _ ~ only); rename the file."
            )
        self.title = self.meta["title"]
        self.summary = self.meta["summary"]
        self.stage = self.meta.get("stage", "")

    @property
    def url(self) -> str:
        return f"{SITE}/log/{self.slug}.html"

    @property
    def out_rel(self) -> str:
        return f"log/{self.slug}.html"

    @property
    def modified(self) -> dt.datetime:
        return last_modified(self.src_rel)

    @property
    def published(self) -> dt.datetime:
        # Midday UTC: the entry records a day, not a moment, and noon keeps the
        # rendered date identical either side of the date line.
        return dt.datetime(self.date.year, self.date.month, self.date.day, 12, tzinfo=dt.timezone.utc)


def load_entries() -> list[Entry]:
    if not ENTRY_SRC_DIR.is_dir():
        return []
    entries = [Entry(p) for p in sorted(ENTRY_SRC_DIR.glob("*.html"))]
    slugs = [e.slug for e in entries]
    duplicate = {s for s in slugs if slugs.count(s) > 1}
    if duplicate:
        raise SystemExit(f"duplicate entry slugs: {', '.join(sorted(duplicate))}")
    entries.sort(key=lambda e: (e.date, e.slug), reverse=True)
    return entries


# ---------------------------------------------------------------------------
# components
# ---------------------------------------------------------------------------

class Component:
    """One stage of the volatility system, parsed from data/components.json.

    The manifest is the single source of implementation status for the whole
    site: the homepage status strip, the architecture grid on /vol/, and the
    build-status table all render from it. Hand-written status prose is how
    the site came to claim a surface fit that no code implemented, so the only
    defence is that there is one place to change and every surface follows it.
    """

    REQUIRED_TEXT = (
        "id", "name", "layer", "state", "summary",
        "current_behaviour", "design_intent", "inputs", "outputs",
        "next_acceptance",
    )

    def __init__(self, raw: dict, index: int):
        where = f"data/components.json[{index}]"

        for key in self.REQUIRED_TEXT:
            value = raw.get(key)
            if not isinstance(value, str) or not value.strip():
                raise SystemExit(f"{where}: {key!r} must be a non-empty string.")

        self.id = raw["id"]
        if not re.fullmatch(r"[a-z0-9-]+", self.id):
            # Interpolated into DOM ids and fragment links unescaped.
            raise SystemExit(f"{where}: id {self.id!r} must be lowercase letters, digits and hyphens.")

        if raw["state"] not in STATES:
            raise SystemExit(
                f"{where}: state {raw['state']!r} is not one of {', '.join(STATES)}."
            )

        order = raw.get("order")
        if not isinstance(order, int) or isinstance(order, bool) or order < 1:
            raise SystemExit(f"{where}: 'order' must be a positive integer.")

        validated = raw.get("validated_on")
        if validated is not None:
            if not isinstance(validated, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", validated):
                raise SystemExit(f"{where}: 'validated_on' must be null or ISO YYYY-MM-DD.")
            try:
                parsed = dt.date.fromisoformat(validated)
            except ValueError:
                raise SystemExit(f"{where}: 'validated_on' {validated!r} is not a real date.") from None
            if parsed > dt.date.today():
                raise SystemExit(f"{where}: 'validated_on' {validated} is in the future.")

        blocked = raw.get("blocked_by")
        if blocked is not None and (not isinstance(blocked, str) or not blocked.strip()):
            raise SystemExit(f"{where}: 'blocked_by' must be null or a non-empty string.")

        evidence = raw.get("evidence", [])
        if not isinstance(evidence, list):
            raise SystemExit(f"{where}: 'evidence' must be a list.")
        for item in evidence:
            if not isinstance(item, dict) or not item.get("label") or not item.get("href"):
                raise SystemExit(f"{where}: every evidence entry needs a label and an href.")

        unknown = set(raw) - set(self.REQUIRED_TEXT) - {"order", "validated_on", "blocked_by", "evidence"}
        if unknown:
            # A typo in a key would otherwise be silently dropped, and the page
            # would render as though the field had never been written.
            raise SystemExit(f"{where}: unknown field(s) {', '.join(sorted(unknown))}.")

        self.order = order
        self.name = raw["name"]
        self.layer = raw["layer"]
        self.state = raw["state"]
        self.summary = raw["summary"]
        self.current_behaviour = raw["current_behaviour"]
        self.design_intent = raw["design_intent"]
        self.inputs = raw["inputs"]
        self.outputs = raw["outputs"]
        self.next_acceptance = raw["next_acceptance"]
        self.validated_on = validated
        self.blocked_by = blocked
        self.evidence = evidence

    @property
    def label(self) -> str:
        return STATES[self.state][0]

    @property
    def badge_class(self) -> str:
        return STATES[self.state][1]

    @property
    def runs_today(self) -> bool:
        return self.state in ("operational", "implemented_unvalidated")

    def live_evidence(self, pending: frozenset[str] = frozenset()) -> list[dict]:
        """Evidence links whose target exists, or is being generated this build.

        The manifest names the artifact a component will publish before it has
        been published, so that the next acceptance test is legible. Rendering
        those links regardless would ship 404s from the one page whose whole
        purpose is that its claims can be checked.

        ``pending`` carries the hrefs this build is about to write. Without it a
        report's first build would drop its own link — the page does not exist
        on disk at the moment the check runs — and only the *second* build would
        pick it up, which makes --check fail in CI on the run that adds a report.
        """
        out = []
        for item in self.evidence:
            href = item["href"]
            if href.startswith("/vol/evidence/"):
                # This directory is generated in full from data/evidence, so the
                # pending set is the complete truth about it. Consulting disk
                # here would be wrong in both directions: a report's first build
                # has not written the page yet, and a withdrawn report's page is
                # still on disk at this point and is deleted later in the pass.
                if href not in pending:
                    continue
            elif href.startswith("/"):
                target = ROOT / href.lstrip("/")
                if target.suffix and not target.exists():
                    continue
            out.append(item)
        return out


def load_components() -> list[Component]:
    if not COMPONENTS_PATH.exists():
        raise SystemExit("data/components.json is missing.")
    try:
        doc = json.loads(COMPONENTS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"data/components.json: {exc}") from None

    if doc.get("schema_version") != 1 or isinstance(doc.get("schema_version"), bool):
        raise SystemExit("data/components.json: schema_version must be 1.")
    raw = doc.get("components")
    if not isinstance(raw, list) or not raw:
        raise SystemExit("data/components.json: 'components' must be a non-empty list.")

    components = [Component(item, i) for i, item in enumerate(raw)]

    ids = [c.id for c in components]
    duplicate = {i for i in ids if ids.count(i) > 1}
    if duplicate:
        raise SystemExit(f"data/components.json: duplicate ids {', '.join(sorted(duplicate))}.")
    orders = [c.order for c in components]
    if len(set(orders)) != len(orders):
        raise SystemExit("data/components.json: 'order' values must be unique.")

    components.sort(key=lambda c: c.order)
    return components


# ---------------------------------------------------------------------------
# evidence
# ---------------------------------------------------------------------------

class Evidence:
    """One published diagnostic report, parsed from data/evidence/<slug>.json.

    The ``report`` object is the box's own output, copied in verbatim; this
    class validates only the envelope around it. Four envelope fields are
    required because a diagnostic without them is not checkable: when the data
    was from, what kind of input produced it, which revision of the code
    computed it, and what it does not establish.
    """

    REQUIRED = ("title", "summary", "component", "data_timestamp", "input_type", "code_version")

    def __init__(self, path: pathlib.Path, component_ids: set[str]):
        self.src_rel = str(path.relative_to(ROOT))
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{self.src_rel}: {exc}") from None

        if doc.get("schema_version") != 1 or isinstance(doc.get("schema_version"), bool):
            raise SystemExit(f"{self.src_rel}: schema_version must be 1.")

        for key in self.REQUIRED:
            if not isinstance(doc.get(key), str) or not doc[key].strip():
                raise SystemExit(f"{self.src_rel}: {key!r} must be a non-empty string.")

        self.slug = path.stem
        if not re.fullmatch(r"[a-z0-9-]+", self.slug):
            raise SystemExit(
                f"{self.src_rel}: filename slug {self.slug!r} must be lowercase letters, "
                "digits and hyphens; it becomes the URL."
            )

        if doc["component"] not in component_ids:
            raise SystemExit(
                f"{self.src_rel}: component {doc['component']!r} is not in data/components.json. "
                "A report that names no component cannot be shown as that component's evidence."
            )

        if doc["input_type"] not in INPUT_TYPES:
            raise SystemExit(
                f"{self.src_rel}: input_type {doc['input_type']!r} is not one of "
                f"{', '.join(INPUT_TYPES)}."
            )

        try:
            stamp_dt = dt.datetime.fromisoformat(doc["data_timestamp"].replace("Z", "+00:00"))
        except ValueError:
            raise SystemExit(
                f"{self.src_rel}: data_timestamp {doc['data_timestamp']!r} is not an ISO timestamp."
            ) from None
        if stamp_dt.tzinfo is None:
            raise SystemExit(f"{self.src_rel}: data_timestamp needs a timezone offset.")
        now = dt.datetime.now(dt.timezone.utc)
        if stamp_dt > now:
            raise SystemExit(f"{self.src_rel}: data_timestamp {doc['data_timestamp']} is in the future.")

        limitations = doc.get("known_limitations", [])
        if not isinstance(limitations, list) or not limitations:
            raise SystemExit(
                f"{self.src_rel}: 'known_limitations' must be a non-empty list. Every report "
                "states what it does not establish; if there is genuinely nothing, say so "
                "explicitly rather than omitting the field."
            )
        for item in limitations:
            if not isinstance(item, str) or not item.strip():
                raise SystemExit(f"{self.src_rel}: every known_limitations entry must be a string.")

        report = doc.get("report")
        if not isinstance(report, dict) or not report:
            raise SystemExit(f"{self.src_rel}: 'report' must be a non-empty object.")

        unknown = set(doc) - set(self.REQUIRED) - {"schema_version", "known_limitations", "report"}
        if unknown:
            raise SystemExit(f"{self.src_rel}: unknown field(s) {', '.join(sorted(unknown))}.")

        self.title = doc["title"]
        self.summary = doc["summary"]
        self.component = doc["component"]
        self.data_timestamp = doc["data_timestamp"]
        self.data_moment = stamp_dt
        self.input_type = doc["input_type"]
        self.code_version = doc["code_version"]
        self.known_limitations = limitations
        self.report = report

    @property
    def out_rel(self) -> str:
        return f"vol/evidence/{self.slug}.html"

    @property
    def url(self) -> str:
        return f"{SITE}/vol/evidence/{self.slug}.html"


def load_evidence(components: list[Component]) -> list[Evidence]:
    if not EVIDENCE_SRC_DIR.is_dir():
        return []
    ids = {c.id for c in components}
    reports = [Evidence(p, ids) for p in sorted(EVIDENCE_SRC_DIR.glob("*.json"))]
    reports.sort(key=lambda e: (e.data_moment, e.slug), reverse=True)
    return reports


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------

def esc(text: str) -> str:
    return html.escape(text, quote=True)


# strftime('%B') follows the process locale, so a non-English dev machine would
# render different month names than CI and desync --check. Fixed table instead.
_MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)


def human_date(value: dt.date | dt.datetime) -> str:
    return f"{_MONTHS[value.month - 1]} {value.day}, {value.year}"


# The primary bar, in the order a visitor needs them: who this is, the project,
# the working record, the credential, the way to make contact. Build Status,
# the Methodology and the Handbook are all *inside* the volatility system and
# reached from its section bar rather than competing for a top-level slot —
# seven top-level items made the section look like seven unrelated sites.
NAV_ITEMS = [
    ("/#work", "Work", "work"),
    ("/vol/", "Volatility System", "vol"),
    ("/log/", "Research Log", "log"),
    ("/cv.html", "CV", "cv"),
    ("/#contact", "Contact", "contact"),
]

GITHUB_URL = "https://github.com/bradlasater/Crack-the-Sky"

# The volatility system's own bar. Appears on every page under /vol/ and on no
# other page, so a reader who arrives at the handbook or the build status can
# see where they are without going back to the top level.
SECTION_ITEMS = [
    ("/vol/", "Overview", "vol-overview"),
    ("/vol/build-status.html", "Build Status", "vol-build-status"),
    ("/vol/methodology.html", "Evaluation Protocol", "vol-methodology"),
    ("/vol/track-record.html", "Trading Record", "vol-track-record"),
    ("/handbook/", "Handbook", "vol-handbook"),
]


def nav(active: str, ancestor: str = "") -> str:
    """The primary nav list items.

    ``active`` marks the page itself with ``aria-current="page"``; ``ancestor``
    marks a section the page belongs to but is not, with ``aria-current="true"``
    — used by every page under /vol/, which highlights Volatility System while
    navigating somewhere else.
    """
    lis = []
    for href, label, key in NAV_ITEMS:
        if key == active:
            current = ' aria-current="page"'
        elif key == ancestor:
            current = ' aria-current="true"'
        else:
            current = ""
        lis.append(f'        <li><a href="{href}"{current}>{label}</a></li>')
    # GitHub closes the bar but is not a section of this site: it never takes
    # aria-current, and it carries its own separator so it does not read as one
    # more page to visit. It is in the header at all because a hiring manager
    # looks for the code first and should not have to scroll to find it.
    lis.append(
        '        <li class="site-nav__ext">'
        f'<a href="{GITHUB_URL}" target="_blank" rel="noopener">GitHub</a></li>'
    )
    return "\n".join(lis)


def section_nav(active: str) -> str:
    """The /vol/ section bar. Empty string for pages outside the section."""
    if not active:
        return ""
    lis = []
    for href, label, key in SECTION_ITEMS:
        current = ' aria-current="page"' if key == active else ""
        lis.append(f'      <li><a href="{href}"{current}>{label}</a></li>')
    return (
        "\n"
        '  <nav class="section-nav" aria-label="Volatility system">\n'
        '    <div class="shell section-nav__inner">\n'
        '      <span class="section-nav__label">Volatility system</span>\n'
        "      <ul>\n" + "\n".join(lis) + "\n      </ul>\n"
        "    </div>\n"
        "  </nav>\n"
    )


def site_footer() -> str:
    """One footer for every page.

    There were five distinct footers across seven pages, and 404.html — the page
    that most needs wayfinding — carried a single mailto link.
    """
    links = [
        ("/", "Home"),
        ("/vol/", "Volatility System"),
        ("/vol/build-status.html", "Build Status"),
        ("/handbook/", "Handbook"),
        ("/log/", "Research Log"),
        ("/cv.html", "CV"),
        (GITHUB_URL, "GitHub"),
        ("https://www.linkedin.com/in/bradlasater", "LinkedIn"),
        ("mailto:brad@bradlasater.com", "Email"),
        ("/feed.xml", "Feed"),
    ]
    lis = []
    for href, label in links:
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        lis.append(f'      <li><a href="{href}"{ext}>{label}</a></li>')
    return (
        "\n"
        '    <span>&copy; 2026 Brad Lasater</span>\n'
        "    <ul>\n" + "\n".join(lis) + "\n    </ul>\n"
        "  "
    )


ENTRY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_esc} — Research Log — Brad Lasater</title>
<meta name="description" content="{summary_esc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#14171c">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">

<meta property="og:type" content="article">
<meta property="og:site_name" content="Brad Lasater">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title_esc}">
<meta property="og:description" content="{summary_esc}">
<meta property="og:image" content="{site}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="article:published_time" content="{published}">
<meta property="article:modified_time" content="{modified}">
<meta property="article:author" content="Brad Lasater">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/atom+xml" title="Brad Lasater — Research Log" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400..700&family=JetBrains+Mono:wght@400;500&family=Newsreader:opsz,wght@6..72,400..600&display=swap">
<link rel="stylesheet" href="/assets/css/site.css">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BlogPosting",
      "@id": "{url}#post",
      "isPartOf": {{ "@id": "{site}/log/#blog" }},
      "mainEntityOfPage": "{url}",
      "headline": {title_json},
      "description": {summary_json},
      "datePublished": "{published}",
      "dateModified": "{modified}",
      "inLanguage": "en-US",
      "author": {{ "@id": "{site}/#brad" }},
      "publisher": {{ "@id": "{site}/#brad" }},
      "image": "{site}/assets/og.png",
      "keywords": {keywords_json}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{site}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Research Log", "item": "{site}/log/" }},
        {{ "@type": "ListItem", "position": 3, "name": {title_json} }}
      ]
    }}
  ]
}}
</script>
<script src="/assets/js/analytics.js" defer></script>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="shell site-header__inner">
    <a class="brand" href="/">Brad Lasater<span class="brand__dot">.</span></a>
    <nav class="site-nav" aria-label="Primary">
      <ul>
{nav}
      </ul>
    </nav>
  </div>
</header>

<main id="main">

  <article class="shell shell--narrow section">

    <div class="role__meta" style="margin-bottom: var(--sp-3);">
      <time class="badge" datetime="{date_iso}">{date_human}</time>
{stage_badge}    </div>

    <h1 class="hero__name" style="font-size: var(--step-3);">{title_esc}</h1>

    <p class="hero__bio" style="margin-top: var(--sp-4);">{summary_esc}</p>

    <div class="prose" style="margin-top: var(--sp-6);">
{body}
    </div>

    <p class="muted" style="margin-top: var(--sp-7);">
      Published <time datetime="{date_iso}">{date_human}</time>.{revised}
      This entry follows the pre-committed
      <a href="/vol/methodology.html">evaluation protocol</a>; it is versioned in the
      repository, and any later correction appears as a dated commit rather than a silent edit.
    </p>

    <nav class="actions" aria-label="More research-log entries">
{pager}    </nav>

  </article>

</main>

<footer class="site-footer">
  <div class="shell site-footer__inner">{footer}</div>
</footer>

</body>
</html>
"""


def json_str(value: str) -> str:
    """A JSON string literal, safe to drop into a <script> block."""
    return json.dumps(value).replace("</", "<\\/")


def render_entry(entry: Entry, newer: Entry | None, older: Entry | None) -> str:
    stage_badge = ""
    if entry.stage:
        stage_badge = f'      <span class="badge">{esc(entry.stage)}</span>\n'

    keywords = ["volatility trading", "systematic trading", "quantitative research"]
    if entry.stage:
        keywords.insert(0, entry.stage.lower())

    pager_bits = []
    if older:
        pager_bits.append(f'      <a class="btn" href="/log/{older.slug}.html">&larr; {esc(older.title)}</a>\n')
    pager_bits.append('      <a class="btn btn--primary" href="/log/">All entries</a>\n')
    if newer:
        pager_bits.append(f'      <a class="btn" href="/log/{newer.slug}.html">{esc(newer.title)} &rarr;</a>\n')

    body = "\n".join("      " + line if line.strip() else line
                     for line in entry.body.splitlines())

    modified = entry.modified

    # Only claim a revision when one actually happened. Same-day edits before
    # first publication are not revisions.
    revised = ""
    if modified.date() > entry.date:
        revised = (f'\n      Last revised <time class="page-updated__time" '
                   f'datetime="{modified.isoformat()}">{human_date(modified)}</time>.')

    return ENTRY_TEMPLATE.format(
        site=SITE,
        url=entry.url,
        title_esc=esc(entry.title),
        title_json=json_str(entry.title),
        summary_esc=esc(entry.summary),
        summary_json=json_str(entry.summary),
        keywords_json=json_str(", ".join(keywords)),
        published=entry.published.isoformat(),
        modified=modified.isoformat(),
        modified_human=human_date(modified),
        revised=revised,
        date_iso=entry.date.isoformat(),
        date_human=human_date(entry.date),
        stage_badge=stage_badge,
        body=body,
        pager="".join(pager_bits),
        nav=nav("log"),
        footer=site_footer(),
    )


def render_log_index_list(entries: list[Entry]) -> str:
    if not entries:
        return (
            "\n    <div class=\"pending\">\n"
            "      <strong>No entries yet</strong>\n"
            "      The first entries land as the data and surface-construction stages come together.\n"
            "      Each one follows the same structure: expected, observed, diagnosis, changed as a result.\n"
            "    </div>\n"
        )

    cards = []
    for entry in entries:
        stage = f'\n        <span class="badge">{esc(entry.stage)}</span>' if entry.stage else ""
        cards.append(
            f"""
    <article class="card card--link" style="margin-bottom: var(--sp-5);">
      <div class="role__meta">
        <time class="badge" datetime="{entry.date.isoformat()}">{human_date(entry.date)}</time>{stage}
      </div>
      <h2 class="card__title" style="margin-top: var(--sp-3);">
        <a href="/log/{entry.slug}.html">{esc(entry.title)}</a>
      </h2>
      <div class="card__body">
        <p>{esc(entry.summary)}</p>
      </div>
    </article>
"""
        )
    return "".join(cards)


def render_llms_log_section(entries: list[Entry]) -> str:
    if not entries:
        return "\n"
    lines = ["\n## Research log entries\n"]
    for entry in entries:
        lines.append(
            f"- [{entry.title}]({entry.url}): {entry.summary} (published {entry.date.isoformat()})"
        )
    return "\n".join(lines) + "\n\n"


def render_architecture(components: list[Component]) -> str:
    """The stage grid on /vol/ — status, what runs, what is designed.

    Deliberately lighter than the build-status table: inputs, outputs,
    evidence and acceptance tests live there, and each card links across.
    """
    cards = []
    for c in components:
        rows = [
            f'          <div class="stage__field">\n'
            f'            <dt>Runs today</dt>\n'
            f'            <dd>{esc(c.current_behaviour)}</dd>\n'
            f'          </div>',
            f'          <div class="stage__field">\n'
            f'            <dt>Designed to</dt>\n'
            f'            <dd>{esc(c.design_intent)}</dd>\n'
            f'          </div>',
        ]
        if c.blocked_by:
            rows.append(
                f'          <div class="stage__field stage__field--blocked">\n'
                f'            <dt>Blocked by</dt>\n'
                f'            <dd>{esc(c.blocked_by)}</dd>\n'
                f'          </div>'
            )
        fields = "\n".join(rows)
        cards.append(
            f'      <article class="card stage" id="stage-{c.id}" aria-labelledby="stage-{c.id}-title">\n'
            f'        <p class="stage__order"><span class="stage__num">{c.order:02d}</span> {esc(c.layer)}</p>\n'
            f'        <h3 class="card__title" id="stage-{c.id}-title">{esc(c.name)}</h3>\n'
            f'        <p class="card__status"><span class="{c.badge_class}">{esc(c.label)}</span></p>\n'
            f'        <div class="card__body">\n'
            f'          <p class="stage__summary">{esc(c.summary)}</p>\n'
            f'          <dl class="stage__fields">\n{fields}\n          </dl>\n'
            f'          <p class="stage__more">'
            f'<a href="/vol/build-status.html#stage-{c.id}">Inputs, outputs and acceptance test &rarr;</a></p>\n'
            f'        </div>\n'
            f'      </article>'
        )
    return "\n\n" + "\n\n".join(cards) + "\n\n    "


def render_report_value(value, depth: int = 0) -> str:
    """Render one JSON value from a box report.

    Generic rather than bespoke per report, because these payloads are the
    box's own dataclasses and will gain fields without asking this renderer
    first. A renderer that only knew today's fields would silently drop
    tomorrow's, which for a page whose purpose is checkability is the one
    failure mode that matters.
    """
    if isinstance(value, bool):
        return "yes" if value else "no"
    if value is None:
        return "&mdash;"
    if isinstance(value, (int, float)):
        return esc(f"{value:,.6g}" if isinstance(value, float) else f"{value:,}")
    if isinstance(value, str):
        return esc(value)
    if isinstance(value, list):
        if not value:
            return "<span class=\"report__none\">none</span>"
        items = "".join(f"<li>{render_report_value(v, depth + 1)}</li>" for v in value)
        return f"<ul class=\"report__list\">{items}</ul>"
    if isinstance(value, dict):
        if not value:
            return "<span class=\"report__none\">none</span>"
        rows = "".join(
            f"<tr><th scope=\"row\">{esc(str(k))}</th>"
            f"<td>{render_report_value(v, depth + 1)}</td></tr>"
            for k, v in value.items()
        )
        return f"<table class=\"report__table\"><tbody>{rows}</tbody></table>"
    return esc(str(value))


def render_evidence_section(components: list[Component], reports: list[Evidence]) -> str:
    """The diagnostic-reports block on the build-status page.

    A component with no published report shows its acceptance test instead of a
    number, which is the same rule the trading-record page already follows: an
    empty state says it is empty rather than showing a placeholder.
    """
    by_component = {c.id: c for c in components}
    published = {}
    for r in reports:
        published.setdefault(r.component, []).append(r)

    cards = []
    for c in components:
        owned = published.get(c.id, [])
        if owned:
            for r in owned:
                cards.append(
                    f'      <article class="card">\n'
                    f'        <p class="proof__kicker">{esc(c.name)}</p>\n'
                    f'        <h3 class="card__title"><a href="/{r.out_rel}">{esc(r.title)}</a></h3>\n'
                    f'        <p class="card__status">'
                    f'<span class="badge badge--live badge--dot">Published</span></p>\n'
                    f'        <div class="card__body">\n'
                    f'          <p>{esc(r.summary)}</p>\n'
                    f'          <p class="report__meta">Data as of {esc(human_date(r.data_moment))} '
                    f'&middot; {esc(INPUT_TYPES[r.input_type])}</p>\n'
                    f'        </div>\n'
                    f'      </article>'
                )
        elif c.evidence:
            # The component names an artifact it intends to publish.
            names = ", ".join(esc(item["label"]) for item in c.evidence)
            cards.append(
                f'      <article class="card">\n'
                f'        <p class="proof__kicker">{esc(c.name)}</p>\n'
                f'        <h3 class="card__title">{names}</h3>\n'
                f'        <p class="card__status"><span class="badge">Not yet published</span></p>\n'
                f'        <div class="card__body">\n'
                f'          <p><strong>What would make it publishable:</strong> '
                f'{esc(c.next_acceptance)}</p>\n'
                f'        </div>\n'
                f'      </article>'
            )
    if not cards:
        return (
            '\n    <p class="pending"><strong>No diagnostics yet</strong>'
            'No component names an artifact to publish.</p>\n  '
        )
    return "\n" + '    <div class="grid">\n' + "\n".join(cards) + "\n    </div>\n  "


EVIDENCE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_esc} — Diagnostic — Brad Lasater</title>
<meta name="description" content="{summary_attr}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#14171c">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400..700&family=JetBrains+Mono:wght@400;500&family=Newsreader:opsz,wght@6..72,400..600&display=swap">
<link rel="stylesheet" href="/assets/css/site.css">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title_attr}">
<meta property="og:description" content="{summary_attr}">
<meta property="og:image" content="https://bradlasater.com/assets/og.png">
<meta property="og:site_name" content="Brad Lasater">
<meta property="article:modified_time" content="{modified}">
<meta name="twitter:card" content="summary_large_image">
<script src="/assets/js/analytics.js" defer></script>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="shell site-header__inner">
    <a class="brand" href="/">Brad Lasater<span class="brand__dot">.</span></a>
    <nav class="site-nav" aria-label="Primary">
      <ul>
{nav}
      </ul>
    </nav>
  </div>
</header>
{section_nav}
<main id="main">

  <section class="shell hero">
    <p class="hero__role">Volatility System · Diagnostic · {component_name}</p>
    <h1 class="hero__name" style="font-size: var(--step-3); margin-top: var(--sp-3);">{title_esc}</h1>
    <p class="hero__bio">{summary_esc}</p>
    <div class="actions">
      <a class="btn btn--primary" href="/vol/build-status.html">Build status</a>
      <a class="btn" href="/data/evidence/{slug}.json">Raw report</a>
    </div>
  </section>

  <section class="shell section" aria-labelledby="provenance-title">
    <div class="section__head">
      <span class="section__eyebrow">Provenance</span>
      <h2 class="section__title" id="provenance-title">Where this came from</h2>
    </div>
    <dl class="statusstrip">
      <div class="statusstrip__item">
        <dt>Data timestamp</dt>
        <dd>{data_timestamp_esc}</dd>
      </div>
      <div class="statusstrip__item">
        <dt>Input type</dt>
        <dd>{input_type_desc}</dd>
      </div>
      <div class="statusstrip__item">
        <dt>Code version</dt>
        <dd><code>{code_version_esc}</code></dd>
      </div>
    </dl>
  </section>

  <section class="shell section" aria-labelledby="limits-title">
    <div class="section__head">
      <span class="section__eyebrow">Limitations</span>
      <h2 class="section__title" id="limits-title">What this does not establish</h2>
    </div>
    <div class="prose">
      <ul>
{limitations}
      </ul>
    </div>
  </section>

  <section class="shell section" aria-labelledby="report-title">
    <div class="section__head">
      <span class="section__eyebrow">Report</span>
      <h2 class="section__title" id="report-title">The output, as produced</h2>
      <p class="section__lede">
        Rendered from the job's own output without reshaping, so that this page and
        <a href="/data/evidence/{slug}.json">the raw file</a> cannot disagree.
      </p>
    </div>
    <div class="table-wrap">
{report}
    </div>
  </section>

  <section class="shell section" aria-label="Page metadata">
    <div class="prose">
      <p class="page-updated">
        This page was last updated <time class="page-updated__time" datetime="{modified}">{modified_human}</time>.
      </p>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="shell site-footer__inner">{footer}</div>
</footer>

</body>
</html>
"""


def render_evidence_page(report: Evidence, components: list[Component]) -> str:
    component = next(c for c in components if c.id == report.component)
    modified = last_modified(report.src_rel)
    limitations = "\n".join(f"        <li>{esc(x)}</li>" for x in report.known_limitations)
    return EVIDENCE_TEMPLATE.format(
        title_esc=esc(report.title),
        title_attr=esc(report.title),
        summary_esc=esc(report.summary),
        summary_attr=esc(report.summary),
        url=report.url,
        slug=report.slug,
        component_name=esc(component.name),
        data_timestamp_esc=esc(report.data_timestamp),
        input_type_desc=esc(INPUT_TYPES[report.input_type]),
        code_version_esc=esc(report.code_version),
        limitations=limitations,
        report=render_report_value(report.report),
        nav=nav("", "vol"),
        section_nav=section_nav("vol-build-status"),
        footer=site_footer(),
        modified=modified.isoformat(),
        modified_human=human_date(modified),
    )


def render_component_table(components: list[Component], reports: list[Evidence]) -> str:
    """The full pipeline on the build-status page: contracts, evidence, tests.

    An ordered list rather than a table or a drawn diagram. A table of ten rows
    by nine columns is unreadable on a phone, and a diagram shrunk to phone
    width is worse — an ordered list is already the correct mobile form, and
    numbering it carries the one thing the card grid on /vol/ cannot: that
    these stages are a sequence, each consuming the one above it.
    """
    pending = frozenset(f"/{r.out_rel}" for r in reports)
    rows = []
    for c in components:
        fields = [
            ("Runs today", esc(c.current_behaviour), ""),
            ("Designed to", esc(c.design_intent), ""),
        ]
        if c.blocked_by:
            fields.append(("Blocked by", esc(c.blocked_by), " stage__field--blocked"))
        fields.extend([
            ("Inputs", esc(c.inputs), ""),
            ("Outputs", esc(c.outputs), ""),
        ])

        evidence = c.live_evidence(pending)
        if evidence:
            links = ", ".join(
                f'<a href="{esc(item["href"])}">{esc(item["label"])}</a>' for item in evidence
            )
        else:
            links = "None published yet."
        fields.append(("Validation evidence", links, ""))

        if c.validated_on:
            fields.append(
                ("Last validated", esc(human_date(dt.date.fromisoformat(c.validated_on))), "")
            )

        fields.append(("Next acceptance test", esc(c.next_acceptance), " stage__field--next"))

        body = "\n".join(
            f'            <div class="stage__field{extra}">\n'
            f'              <dt>{esc(label)}</dt>\n'
            f'              <dd>{value}</dd>\n'
            f'            </div>'
            for label, value, extra in fields
        )
        running = " is-running" if c.runs_today else ""
        rows.append(
            f'        <li class="pipeline__row{running}" id="stage-{c.id}">\n'
            f'          <div class="pipeline__head">\n'
            f'            <span class="pipeline__num">{c.order:02d}</span>\n'
            f'            <h3 class="pipeline__name">{esc(c.name)}</h3>\n'
            f'            <span class="pipeline__layer">{esc(c.layer)}</span>\n'
            f'            <span class="{c.badge_class}">{esc(c.label)}</span>\n'
            f'          </div>\n'
            f'          <p class="pipeline__summary">{esc(c.summary)}</p>\n'
            f'          <dl class="stage__fields">\n{body}\n          </dl>\n'
            f'        </li>'
        )

    running_count = sum(1 for c in components if c.runs_today)
    return (
        "\n"
        '      <ol class="pipeline">\n'
        + "\n".join(rows)
        + "\n      </ol>\n"
        '      <p class="pipeline__empty">'
        f"{running_count} of {len(components)} stages run today. "
        "Switch to the target system to see the rest.</p>\n"
        "    "
    )


def render_next_milestone(components: list[Component]) -> str:
    """The frontier stage's acceptance test, stated in full."""
    frontier = next((c for c in components if not c.runs_today), components[-1])
    return (
        "\n"
        '    <div class="verdict verdict--pending">\n'
        f'      <p class="verdict__label">{esc(frontier.name)}</p>\n'
        f'      <p class="verdict__text">{esc(frontier.next_acceptance)}</p>\n'
        f'      <p class="verdict__note">This is the first stage in the pipeline that does not yet '
        f'run, which is what makes it the frontier. Its status and this test are both read from '
        f'<a href="/data/components.json">the manifest</a>; nothing on this page is typed by hand.</p>\n'
        "    </div>\n"
        "  "
    )


def first_sentence(text: str) -> str:
    """The opening sentence, for places too small for a full acceptance test.

    The strip is three cells wide; a paragraph in one of them unbalances the
    row and buries the other two facts. The full text is one click away on the
    build-status page, so the cell only has to carry the headline.
    """
    parts = re.split(r"(?<=[.?!])\s+", text.strip())
    out = parts[0]
    # A very short opener ("Nothing.") is a fragment rather than the claim;
    # take the next sentence with it so the cell says something.
    if len(out) < 60 and len(parts) > 1:
        out = f"{out} {parts[1]}"
    return out


def render_status_strip(components: list[Component]) -> str:
    """The homepage strip: where the build is, the latest evidence, what is next.

    Every figure here is counted from the manifest rather than typed, so the
    homepage cannot claim a build fraction the architecture page contradicts.
    """
    running = [c for c in components if c.runs_today]
    total = len(components)

    # The frontier is the first stage that is not yet running: what the build
    # is actually working towards, rather than a stage picked by hand.
    frontier = next((c for c in components if not c.runs_today), components[-1])

    dated = [c for c in components if c.validated_on]
    if dated:
        latest = max(dated, key=lambda c: c.validated_on)
        evidence_value = f"{esc(latest.name)} &middot; {esc(human_date(dt.date.fromisoformat(latest.validated_on)))}"
    else:
        evidence_value = "No component has a published validation date yet"

    items = [
        ("Build phase", f"{len(running)} of {total} stages run today; the rest are designed and not built"),
        ("Latest validated evidence", evidence_value),
        ("Next milestone", f"{esc(frontier.name)} &mdash; {esc(first_sentence(frontier.next_acceptance))}"),
    ]
    rendered = "\n".join(
        f'      <div class="statusstrip__item">\n'
        f'        <dt>{esc(label)}</dt>\n'
        f'        <dd>{value}</dd>\n'
        f'      </div>'
        for label, value in items
    )
    return (
        "\n"
        '    <dl class="statusstrip">\n'
        f"{rendered}\n"
        "    </dl>\n"
        '    <p class="statusstrip__note">'
        'Counted from <a href="/data/components.json">the component manifest</a>, '
        'which is what the <a href="/vol/">architecture</a> and '
        '<a href="/vol/build-status.html">build status</a> pages render from.</p>\n'
        "  "
    )


def render_feed(entries: list[Entry]) -> str:
    if entries:
        updated = max(e.modified for e in entries).isoformat()
    else:
        updated = last_modified("log/index.html").isoformat()

    items = []
    for entry in entries:
        items.append(f"""  <entry>
    <title>{esc(entry.title)}</title>
    <link href="{entry.url}" rel="alternate" type="text/html"/>
    <id>{entry.url}</id>
    <published>{entry.published.isoformat()}</published>
    <updated>{entry.modified.isoformat()}</updated>
    <summary type="text">{esc(entry.summary)}</summary>
    <author><name>{AUTHOR}</name></author>
  </entry>
""")

    return f"""<?xml version="1.0" encoding="utf-8"?>
<!-- Generated by scripts/build_site.py. Do not edit by hand. -->
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Brad Lasater — Research Log</title>
  <subtitle>Building a systematic volatility trading system in the open: what I tried, what I expected, what happened, and what I had wrong.</subtitle>
  <link href="{SITE}/feed.xml" rel="self" type="application/atom+xml"/>
  <link href="{SITE}/log/" rel="alternate" type="text/html"/>
  <id>{SITE}/log/</id>
  <updated>{updated}</updated>
  <author>
    <name>{AUTHOR}</name>
    <email>{AUTHOR_EMAIL}</email>
    <uri>{SITE}/</uri>
  </author>
  <rights>© {dt.date.today().year} {AUTHOR}</rights>
{"".join(items)}</feed>
"""


def handbook_pages() -> list[str]:
    """Handbook pages for the sitemap, overview first, then the rest by name.

    Discovered rather than declared. The handbook is synced from a separate
    repository by ``scripts/sync_docs.py`` and is still being written, so a page
    added upstream reaches the sitemap on the next sync instead of waiting on a
    second edit here that would be easy to forget.

    These stay out of ``STATIC_PAGES`` on purpose: they are not hand-authored in
    this repository, they carry none of the stamp markers, and this script must
    never write to a directory that ``sync_docs.py`` overwrites wholesale.
    """
    names = sorted(p.name for p in (ROOT / "handbook").glob("*.html"))
    if "index.html" in names:
        names.remove("index.html")
        names.insert(0, "index.html")
    return [f"handbook/{name}" for name in names]


def evidence_pages(reports: list[Evidence]) -> list[str]:
    """Published diagnostics, from the manifest rather than from the output dir.

    Deriving these from ``vol/evidence/*.html`` on disk would put the sitemap one
    build behind: on the run that first writes a report, the glob happens before
    the file exists, so the page would be generated and left out of the sitemap
    until some later build. Reading the source list makes one pass sufficient.
    """
    return sorted(r.out_rel for r in reports)


def sitemap_pages(reports: list[Evidence]) -> list[str]:
    """Every indexable page outside the log, in the order the nav presents it.

    ``docs/`` is unpublished working material (Jekyll-excluded in
    ``_config.yml``) and must never join this list. A page added there is a
    local note, not a public URL.
    """
    pages = list(STATIC_PAGES)
    after_status = pages.index("vol/build-status.html") + 1
    after_track = pages.index("vol/track-record.html") + 1
    return (
        pages[:after_status]
        + evidence_pages(reports)
        + pages[after_status:after_track]
        + handbook_pages()
        + pages[after_track:]
    )


def render_sitemap(entries: list[Entry], reports: list[Evidence]) -> str:
    urls = []
    for rel in sitemap_pages(reports):
        # "vol/index.html" is served at "/vol/"; the directory form is the
        # canonical URL declared on the page, so the sitemap must agree.
        loc = SITE + "/" + re.sub(r"(^|/)index\.html$", r"\1", rel)
        urls.append((loc, last_modified(rel)))
    for entry in entries:
        urls.append((entry.url, entry.modified))

    body = "".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod.date().isoformat()}</lastmod>\n  </url>\n"
        for loc, mod in urls
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<!-- Generated by scripts/build_site.py. Do not edit by hand. -->\n"
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}</urlset>\n"
    )


# ---------------------------------------------------------------------------
# stamping
# ---------------------------------------------------------------------------

STAMPS = (
    (re.compile(r'(<meta property="article:modified_time" content=")[^"]*(")'), "iso"),
    (re.compile(r'("dateModified":\s*")[^"]*(")'), "iso"),
    (re.compile(r'(<time class="page-updated__time" datetime=")[^"]*(")>[^<]*(</time>)'), "both"),
)


def stamp(text: str, moment: dt.datetime) -> str:
    iso = moment.isoformat()
    human = human_date(moment)
    for pattern, kind in STAMPS:
        if kind == "iso":
            text = pattern.sub(lambda m: f"{m.group(1)}{iso}{m.group(2)}", text)
        else:
            text = pattern.sub(lambda m: f"{m.group(1)}{iso}{m.group(2)}>{human}{m.group(3)}", text)
    return text


def inject(text: str, name: str, replacement: str) -> str:
    """Replace the body between a matching pair of BUILD markers."""
    found = False

    def repl(match: re.Match[str]) -> str:
        nonlocal found
        if match.group("name") != name:
            return match.group(0)
        found = True
        return match.group(1) + replacement + match.group(4)

    out = MARKER.sub(repl, text)
    if not found:
        raise SystemExit(f"marker BUILD:{name} not found")
    return out


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="do not write; exit 1 if any generated file is out of date",
    )
    args = parser.parse_args()

    entries = load_entries()
    components = load_components()
    reports = load_evidence(components)
    planned: dict[str, str] = {}

    # 1. One page per entry.
    for index, entry in enumerate(entries):
        newer = entries[index - 1] if index > 0 else None
        older = entries[index + 1] if index + 1 < len(entries) else None
        planned[entry.out_rel] = render_entry(entry, newer, older)

    # 2. The log index list.
    log_index = (ROOT / "log" / "index.html").read_text(encoding="utf-8")
    planned["log/index.html"] = inject(log_index, "LOG-ENTRIES", render_log_index_list(entries))

    # 3. Feed.
    planned["feed.xml"] = render_feed(entries)

    # 4. llms.txt log section.
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    planned["llms.txt"] = inject(llms, "LOG-ENTRIES", render_llms_log_section(entries))

    # 5. Implementation status, from data/components.json. One manifest drives
    #    the homepage strip and the architecture grid, so the two cannot
    #    disagree about what is built.
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    planned["index.html"] = inject(home, "STATUS-STRIP", render_status_strip(components))

    vol_index = (ROOT / "vol" / "index.html").read_text(encoding="utf-8")
    planned["vol/index.html"] = inject(vol_index, "ARCHITECTURE", render_architecture(components))

    build_status = (ROOT / "vol" / "build-status.html").read_text(encoding="utf-8")
    build_status = inject(build_status, "COMPONENT-TABLE", render_component_table(components, reports))
    build_status = inject(build_status, "EVIDENCE", render_evidence_section(components, reports))
    planned["vol/build-status.html"] = inject(
        build_status, "NEXT-MILESTONE", render_next_milestone(components)
    )

    for report in reports:
        planned[report.out_rel] = render_evidence_page(report, components)

    # 6. Site chrome. The nav used to be hand-maintained in seven HTML files and
    #    again in nav() here, and there were five different footers; both now
    #    come from one definition, so a nav change is a one-place edit.
    for rel, (active, ancestor, section) in CHROME_PAGES.items():
        text = planned.get(rel) or (ROOT / rel).read_text(encoding="utf-8")
        text = inject(text, "SITE-NAV", "\n" + nav(active, ancestor) + "\n      ")
        text = inject(text, "SITE-FOOTER", site_footer())
        if section:
            text = inject(text, "SECTION-NAV", section_nav(section))
        planned[rel] = text

    # 7. Timestamps on every hand-authored page. Generated entry pages already
    #    carry their own, so they are stamped from their source fragment above.
    for rel in STATIC_PAGES:
        text = planned.get(rel) or (ROOT / rel).read_text(encoding="utf-8")
        planned[rel] = stamp(text, last_modified(rel))

    # 8. Sitemap last, so it sees the final entry list.
    planned["sitemap.xml"] = render_sitemap(entries, reports)

    # Remove generated pages whose source is gone — a retracted log entry, or a
    # diagnostic whose JSON was withdrawn. A published report that no longer has
    # a source file must not keep serving.
    orphans = sorted(
        p for p in (ROOT / "log").glob("*.html")
        if p.name != "index.html" and f"log/{p.name}" not in planned
    )
    if EVIDENCE_OUT_DIR.is_dir():
        orphans += sorted(
            p for p in EVIDENCE_OUT_DIR.glob("*.html")
            if f"vol/evidence/{p.name}" not in planned
        )

    stale: list[str] = []
    for rel, content in sorted(planned.items()):
        path = ROOT / rel
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        stale.append(rel)
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    removed: list[str] = []
    for path in orphans:
        removed.append(str(path.relative_to(ROOT)))
        if not args.check:
            path.unlink()

    if args.check:
        if stale or removed:
            print("Derived files are out of date:", file=sys.stderr)
            for rel in stale:
                print(f"  stale:    {rel}", file=sys.stderr)
            for rel in removed:
                print(f"  orphaned: {rel}", file=sys.stderr)
            print("\nRun: python3 scripts/build_site.py", file=sys.stderr)
            return 1
        print(f"Up to date. {len(entries)} log entr{'y' if len(entries) == 1 else 'ies'}.")
        return 0

    for rel in stale:
        print(f"wrote   {rel}")
    for rel in removed:
        print(f"removed {rel}")
    if not stale and not removed:
        print("no changes")
    print(f"{len(entries)} log entr{'y' if len(entries) == 1 else 'ies'}.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - a build failure must be loud
        print(f"build failed: {exc}", file=sys.stderr)
        sys.exit(2)

#!/usr/bin/env python3
"""Generate the derived parts of the site: log pages, feed, sitemap, timestamps.

Everything this script writes is derived from two sources of truth:

  * ``content/log/*.html`` — one hand-authored fragment per research-log entry.
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
  * timestamps stamped into every page's metadata

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
    "vol/methodology.html",
    "vol/track-record.html",
    "log/index.html",
    "cv.html",
]

ENTRY_SRC_DIR = ROOT / "content" / "log"

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


def last_modified(relpath: str) -> dt.datetime:
    """The commit date of the last non-build commit to touch ``relpath``.

    Falls back to the current time for a file git has never seen — a brand new
    entry being previewed locally, typically. Never fabricates a past date.
    """
    try:
        out = git(
            "log", "-1", "--format=%cI", "--no-merges",
            "--invert-grep", f"--grep=^{BUILD_COMMIT_SUBJECT}",
            "--", relpath,
        ).strip()
    except RuntimeError:
        out = ""
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


def nav(active: str) -> str:
    items = [
        ("/vol/", "Volatility System", "vol"),
        ("/vol/track-record.html", "Build Status", "track"),
        ("/handbook/", "Handbook", "handbook"),
        ("/log/", "Research Log", "log"),
        ("/cv.html", "CV", "cv"),
        ("/#contact", "Contact", "contact"),
    ]
    lis = []
    for href, label, key in items:
        current = ' aria-current="page"' if key == active else ""
        lis.append(f'        <li><a href="{href}"{current}>{label}</a></li>')
    # GitHub closes the bar but is not a section of this site: it never takes
    # aria-current, and it carries its own separator so it does not read as one
    # more page to visit. It is in the header at all because a hiring manager
    # looks for the code first and should not have to scroll to find it.
    lis.append(
        '        <li class="site-nav__ext">'
        '<a href="https://github.com/bradlasater?tab=repositories">GitHub</a></li>'
    )
    return "\n".join(lis)


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
  <div class="shell site-footer__inner">
    <span>&copy; {year} Brad Lasater</span>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/log/">Research Log</a></li>
      <li><a href="/vol/">Volatility System</a></li>
      <li><a href="/handbook/">Handbook</a></li>
      <li><a href="/feed.xml">Feed</a></li>
      <li><a href="mailto:brad@bradlasater.com">Email</a></li>
    </ul>
  </div>
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
        year=dt.date.today().year,
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


def sitemap_pages() -> list[str]:
    """Every indexable page outside the log, in the order the nav presents it."""
    pages = list(STATIC_PAGES)
    after_track = pages.index("vol/track-record.html") + 1
    return pages[:after_track] + handbook_pages() + pages[after_track:]


def render_sitemap(entries: list[Entry]) -> str:
    urls = []
    for rel in sitemap_pages():
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

    # 5. Timestamps on every hand-authored page. Generated entry pages already
    #    carry their own, so they are stamped from their source fragment above.
    for rel in STATIC_PAGES:
        text = planned.get(rel) or (ROOT / rel).read_text(encoding="utf-8")
        planned[rel] = stamp(text, last_modified(rel))

    # 6. Sitemap last, so it sees the final entry list.
    planned["sitemap.xml"] = render_sitemap(entries)

    # Remove generated entry pages whose source fragment is gone.
    orphans = sorted(
        p for p in (ROOT / "log").glob("*.html")
        if p.name != "index.html" and f"log/{p.name}" not in planned
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

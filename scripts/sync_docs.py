#!/usr/bin/env python3
"""Copy the data_ingest_infra system handbook into ``handbook/`` and publish it.

The handbook is authored in a different, private repository. It is the design
document for the running ingest box, and it is kept next to the code it
describes so that the two are edited in the same commit — moving it here would
break exactly the property that makes it trustworthy.

So this script copies rather than moves, and treats ``handbook/`` as derived:
every file in it is overwritten from source on each run, and anything in it
that no longer exists upstream is deleted. Nothing in ``handbook/`` should ever
be hand-edited; the edit belongs in the source repository, followed by a sync.

At publish time the handbook is re-skinned into the site's design system — the
same OKLCH palette, the same Inter / JetBrains Mono / Newsreader faces, the
same theme colour — so reading it feels like reading the site rather than
stepping into a different one. The reskin is a string transform (FONT_MAP and
COLOR_MAP below) applied to every synced HTML and CSS file, diagrams and inline
styles included. Anything upstream introduces that the transform does not
recognise — a new hex colour, a new font — fails the sync loudly instead of
quietly drifting back into the old theme. Interaction behaviour that string
replacement cannot express (underlined content links, selection colour, focus
rings, corner radii) lives in assets/css/handbook-chrome.css, which is loaded
last on every handbook page and is never touched by this script.

What the sync adds on top of the reskin is only what a page needs in order to
be a public URL rather than a file on a laptop:

  * a canonical URL, so the directory and index.html forms do not compete
  * favicon, theme colour, and robots directives matching the rest of the site
  * Open Graph and Twitter card tags, so a link pasted into Slack or a DM
    renders a card instead of a bare URL
  * " — Brad Lasater" appended to the title, which is the site's convention
  * one link back out of the handbook, styled by assets/css/handbook-chrome.css

Usage:

    python3 scripts/sync_docs.py             # write
    python3 scripts/sync_docs.py --check     # exit 1 if handbook/ is stale
    python3 scripts/sync_docs.py --source DIR

``--check`` exits 0 when the source repository is not present, so it is safe to
run somewhere the private repository was never cloned — CI, for instance. It
cannot detect drift it cannot see, which is why CI does not rely on it.

Exit codes: 0 ok (or source absent), 1 stale (--check), 2 could not run.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://bradlasater.com"
DEST = ROOT / "handbook"
DEFAULT_SOURCE = ROOT.parent / "data_ingest_infra" / "docs"

BANNER = (
    "<!-- Synced from data_ingest_infra/docs by scripts/sync_docs.py. "
    "Do not edit by hand; edit the source repository and re-run the sync. -->"
)
CSS_BANNER = (
    "/* Synced from data_ingest_infra/docs by scripts/sync_docs.py.\n"
    "   Do not edit by hand; edit the source repository and re-run the sync. */\n"
)

TITLE_SUFFIX = " — Brad Lasater"

# --- The reskin -------------------------------------------------------------
# The handbook source carries its own warm palette and IBM Plex faces. Every
# value below is a token from assets/css/site.css copied as a literal, because
# handbook pages do not load site.css and so have no tokens to inherit. If
# site.css's :root block changes, change these (and handbook-chrome.css) to
# match.

FONT_MAP = {
    "IBM Plex Mono": "JetBrains Mono",
    "IBM Plex Sans": "Inter",
}

SITE_FONTS_URL = (
    "https://fonts.googleapis.com/css2?family=Inter:wght@400..700"
    "&family=JetBrains+Mono:wght@400;500"
    "&family=Newsreader:opsz,wght@6..72,400..600&display=swap"
)

COLOR_MAP = {
    # handbook token   site token it publishes as
    "#0e1114": "oklch(0.165 0.010 255)",   # --bg         → --c-bg
    "#0b0e11": "oklch(0.145 0.010 255)",   # sidebar bg   → a half-step below --c-bg
    "#161b20": "oklch(0.195 0.012 255)",   # --bg-2       → --c-bg-subtle
    "#1c2328": "oklch(0.215 0.013 255)",   # --bg-3       → --c-surface
    "#2a3238": "oklch(0.300 0.015 255)",   # --line       → --c-border
    "#6a6458": "oklch(0.520 0.018 255)",   # diagram grey → --c-border-strong
    "#e8e4d9": "oklch(0.955 0.004 255)",   # --ink        → --c-text
    "#d4cfc3": "oklch(0.790 0.011 255)",   # --body       → --c-text-secondary
    "#9a9386": "oklch(0.680 0.013 255)",   # --muted      → --c-text-muted
    "#d08c44": "oklch(0.745 0.135 232)",   # --copper     → --c-accent
    "#8a5c2a": "oklch(0.310 0.055 232)",   # --copper-dim → --c-accent-quiet
    "#1a1208": "oklch(0.165 0.020 255)",   # skip-link    → --c-on-accent
    "#8aaa78": "oklch(0.780 0.140 165)",   # --ok         → --c-pos
    "#c9a35a": "oklch(0.800 0.130 85)",    # --warn       → --c-warn
    "#c97a7a": "oklch(0.700 0.160 25)",    # --bad        → --c-neg
    "#c47d7d": "oklch(0.700 0.160 25)",    # --s3         → --c-neg (they were
                                           # already near-identical dusty reds)
    # Status-chip borders → the site's own badge-border idiom.
    "#3d5440": "color-mix(in oklch, oklch(0.780 0.140 165) 40%, transparent)",
    "#5c3a3a": "color-mix(in oklch, oklch(0.700 0.160 25) 40%, transparent)",
    "#5c4e2a": "color-mix(in oklch, oklch(0.800 0.130 85) 40%, transparent)",
    "#3d545c": "color-mix(in oklch, #7aa3b0 40%, transparent)",
    # Session-timeline bars: dimmed variants of the same hues.
    "#8a4d4d": "color-mix(in oklch, oklch(0.700 0.160 25) 45%, oklch(0.165 0.010 255))",
    "#5a6b52": "color-mix(in oklch, oklch(0.780 0.140 165) 40%, oklch(0.165 0.010 255))",
    # box-operations.html's inline status-tag washes.
    "rgba(138,170,120,0.15)": "color-mix(in oklch, oklch(0.780 0.140 165) 15%, transparent)",
    "rgba(201,163,90,0.15)": "color-mix(in oklch, oklch(0.800 0.130 85) 15%, transparent)",
    "rgba(201,122,122,0.12)": "color-mix(in oklch, oklch(0.700 0.160 25) 12%, transparent)",
}

# Categorical source colours that survive the reskin: they encode REST vs S3
# identity in the diagrams and session timeline, and both already sit inside
# the site's cool hue family.
ALLOWED_SOURCE_COLORS = {"#7aa3b0", "#4d7380"}

LEFTOVER_HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b")
FONTS_URL_RE = re.compile(r"https://fonts\.googleapis\.com/css2\?[^\"\s]+")

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL)
HEAD_END_RE = re.compile(r"([ \t]*)</head>")
DOCTYPE_RE = re.compile(r"(<!DOCTYPE html>\n)", re.IGNORECASE)
TOC_OPEN_RE = re.compile(r"(<nav class=\"toc\"[^>]*>)")
BODY_OPEN_RE = re.compile(r"(<body[^>]*>)")

BACK_LABEL = "&#8592; bradlasater.com"


def reskin(name: str, text: str) -> str:
    """Re-skin one synced file into the site's palette and faces.

    Fails loudly on anything unrecognised rather than publishing a page that
    has drifted back into the handbook's source theme.
    """
    for old, new in FONT_MAP.items():
        text = text.replace(old, new)
    for old, new in COLOR_MAP.items():
        if old.startswith("#"):
            text = re.sub(re.escape(old), lambda _: new, text, flags=re.IGNORECASE)
        else:
            text = text.replace(old, new)

    leftovers = {
        c for c in LEFTOVER_HEX_RE.findall(text)
        if c.lower() not in ALLOWED_SOURCE_COLORS
    }
    if leftovers:
        raise SystemExit(
            f"{name}: unmapped colours {sorted(leftovers)}. Add each to "
            "COLOR_MAP (with its site token) or ALLOWED_SOURCE_COLORS in "
            "scripts/sync_docs.py."
        )
    if "Plex" in text:
        raise SystemExit(
            f"{name}: an IBM Plex reference survived the font remap; "
            "extend FONT_MAP in scripts/sync_docs.py."
        )
    return text


def public_url(name: str) -> str:
    """The canonical URL for a handbook file served by GitHub Pages."""
    return f"{SITE}/handbook/" if name == "index.html" else f"{SITE}/handbook/{name}"


def head_block(name: str, title: str) -> str:
    """The metadata a handbook page needs once it is a public URL."""
    url = public_url(name)
    return "\n".join(
        [
            "",
            "  <!-- Added by scripts/sync_docs.py; not present in the source repository. -->",
            f'  <link rel="canonical" href="{url}">',
            '  <meta name="theme-color" content="#14171c">',
            '  <meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">',
            '  <meta property="og:type" content="article">',
            '  <meta property="og:site_name" content="Brad Lasater">',
            '  <meta property="og:locale" content="en_US">',
            f'  <meta property="og:url" content="{url}">',
            f'  <meta property="og:title" content="{title}">',
            f'  <meta property="og:image" content="{SITE}/assets/og.png">',
            '  <meta property="og:image:width" content="1200">',
            '  <meta property="og:image:height" content="630">',
            '  <meta name="twitter:card" content="summary_large_image">',
            '  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">',
            '  <link rel="stylesheet" href="/assets/css/handbook-chrome.css">',
            "",
        ]
    )


def transform_html(name: str, text: str) -> str:
    """Apply every source-to-published change for one handbook page."""
    if BANNER in text:
        raise SystemExit(f"{name}: source already carries the sync banner; refusing")

    # Swap the font stylesheet before reskin(): the handbook's css2 URL itself
    # names the IBM Plex faces and would trip the reskin's leftover scan.
    text, count = FONTS_URL_RE.subn(SITE_FONTS_URL, text, count=1)
    if not count:
        raise SystemExit(
            f"{name}: no Google Fonts stylesheet link; the reskin needs it "
            "to load the site's faces"
        )
    # Re-skin before any metadata injection: the tripwire in reskin() must
    # scan source content only, and the injected head block below carries
    # site values (the #14171c theme colour) it would otherwise flag.
    text = reskin(name, text)

    match = TITLE_RE.search(text)
    if not match:
        raise SystemExit(f"{name}: no <title>; cannot build canonical metadata")
    title = match.group(1).strip()
    if not title.endswith(TITLE_SUFFIX):
        title += TITLE_SUFFIX
        text = TITLE_RE.sub(lambda _: f"<title>{title}</title>", text, count=1)

    text, count = DOCTYPE_RE.subn(rf"\1{BANNER}\n", text, count=1)
    if not count:
        raise SystemExit(f"{name}: no doctype; refusing to publish an unmarked copy")

    text, count = HEAD_END_RE.subn(
        lambda m: head_block(name, title) + m.group(0), text, count=1
    )
    if not count:
        raise SystemExit(f"{name}: no </head>; cannot inject page metadata")

    # The sidebar pages get the back link as the first thing in the sidebar,
    # above the handbook's own kicker. box-operations.html has no sidebar, so it
    # gets it at the top of its single content column instead.
    link = f'<a class="hb-back" href="/">{BACK_LABEL}</a>'
    text, count = TOC_OPEN_RE.subn(rf"\1\n      {link}", text, count=1)
    if not count:
        plain = f'<a class="hb-back hb-back--plain" href="/">{BACK_LABEL}</a>'
        text, count = BODY_OPEN_RE.subn(rf"\1\n{plain}", text, count=1)
        if not count:
            raise SystemExit(f"{name}: no sidebar and no <body>; nowhere to link back")

    return text


def plan(source: pathlib.Path) -> dict[str, str]:
    """Every file the sync would write, keyed by name, with its final content."""
    planned: dict[str, str] = {}
    for path in sorted(source.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".html":
            planned[path.name] = transform_html(path.name, text)
        elif path.suffix == ".css":
            planned[path.name] = CSS_BANNER + reskin(path.name, text)
        else:
            raise SystemExit(
                f"{path.name}: unexpected file type in the handbook source. "
                "Add a rule for it here rather than copying it blind."
            )
    if "index.html" not in planned:
        raise SystemExit(f"{source}: no index.html; /handbook/ would 404")
    return planned


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="do not write; exit 1 if handbook/ differs from the source",
    )
    parser.add_argument(
        "--source", type=pathlib.Path, default=DEFAULT_SOURCE,
        help=f"handbook source directory (default: {DEFAULT_SOURCE})",
    )
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    if not source.is_dir():
        # Not an error: the source lives in a private repository that is not
        # cloned everywhere this repository is.
        print(f"Handbook source not found at {source}; nothing to sync.")
        return 0

    planned = plan(source)

    stale: list[str] = []
    for name, content in sorted(planned.items()):
        path = DEST / name
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        stale.append(name)
        if not args.check:
            DEST.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    removed: list[str] = []
    if DEST.is_dir():
        for path in sorted(DEST.iterdir()):
            if path.is_file() and path.name not in planned:
                removed.append(path.name)
                if not args.check:
                    path.unlink()

    if args.check:
        if stale or removed:
            print("handbook/ is out of date:", file=sys.stderr)
            for name in stale:
                print(f"  stale:    handbook/{name}", file=sys.stderr)
            for name in removed:
                print(f"  orphaned: handbook/{name}", file=sys.stderr)
            print("\nRun: python3 scripts/sync_docs.py", file=sys.stderr)
            return 1
        print(f"Up to date. {len(planned)} handbook files.")
        return 0

    for name in stale:
        print(f"wrote   handbook/{name}")
    for name in removed:
        print(f"removed handbook/{name}")
    if not stale and not removed:
        print("no changes")
    print(f"{len(planned)} handbook files from {source}.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)

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

The handbook keeps its own dark theme, its own sidebar, and its own layout. The
site does not restyle it — a system handbook that looks like a system handbook
is the point. What the sync adds is only what a page needs in order to be a
public URL rather than a file on a laptop:

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

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL)
HEAD_END_RE = re.compile(r"([ \t]*)</head>")
DOCTYPE_RE = re.compile(r"(<!DOCTYPE html>\n)", re.IGNORECASE)
TOC_OPEN_RE = re.compile(r"(<nav class=\"toc\"[^>]*>)")
BODY_OPEN_RE = re.compile(r"(<body[^>]*>)")

BACK_LABEL = "&#8592; bradlasater.com"


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
            '  <meta name="theme-color" content="#0e1114">',
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
            planned[path.name] = CSS_BANNER + text
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

#!/usr/bin/env python3
"""Rebuild the prompt table in ``journal-prompts.html`` from recent git activity.

Scheduled at 06:00 ET (04:00 local MT) via launchd
(``com.bradlasater.journal-prompts``) so the file is fresh when the morning
writing session starts: development happens at night, the entry gets written
the next morning.

Rows are grouped per repo per day from commits in the last 48 hours across the
repos listed below, plus one row for any repo with uncommitted work. Commits
whose only changes are log entries themselves are skipped — an entry about an
entry is noise. No activity is a valid row: "no surprise, no entry" is the rule
the page teaches.

Everything between ``<!-- PROMPTS:BEGIN -->`` and ``<!-- PROMPTS:END -->`` (and
the ``GENERATED`` stamp) is rewritten on each run; the rest of the file is
hand-authored. Missing markers fail loudly rather than clobbering the guide.

Usage: python3 scripts/journal_prompts.py
"""

from __future__ import annotations

import datetime as dt
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "journal-prompts.html"

REPOS = [
    ("site", ROOT),
    ("system", ROOT.parent / "data_ingest_infra"),
]

WINDOW = dt.timedelta(hours=48)

PROMPTS_BEGIN = "<!-- PROMPTS:BEGIN -->"
PROMPTS_END = "<!-- PROMPTS:END -->"
GENERATED_BEGIN = "<!-- GENERATED:BEGIN -->"
GENERATED_END = "<!-- GENERATED:END -->"

# Log-entry commits are the output of this process, not input to it. A log
# commit also lands the derived feed.xml and sitemap.xml, so those count as
# log artifacts too — otherwise every published entry still fills the table.
LOG_DIRS = ("content/log/", "log/")
LOG_FILES = ("feed.xml", "sitemap.xml")


def git(repo: pathlib.Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, check=True, timeout=60,
    ).stdout


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def prompt_for(subject: str) -> str:
    """The angle most likely to produce a defensible entry from this change."""
    word = subject.split(":", 1)[0].split(None, 1)[0].lower() if subject else ""
    if word.startswith(("fix", "bug", "hotfix", "repair")):
        return ("What did you expect, what did you observe, and what in the "
                "system now makes this class of bug loud instead of silent?")
    if word.startswith(("add", "feat", "build", "implement", "create", "wire")):
        return "What decision does this encode? What evidence would prove it wrong?"
    if word.startswith(("test", "cover")):
        return "What failure just became loud? What did it catch that you missed?"
    if word.startswith(("doc", "handbook", "readme")):
        return "What can a reader now verify that they couldn't before?"
    if word.startswith(("refactor", "chore", "clean", "bump")):
        return "Probably not an entry. If it is: what risk did this remove?"
    return "What assumption did this confirm or break?"


def is_log_only(repo: pathlib.Path, commit: str) -> bool:
    # splitlines, not split: a filename may contain spaces.
    files = [
        f
        for f in git(repo, "show", "--pretty=format:", "--name-only", commit).splitlines()
        if f
    ]
    return bool(files) and all(
        f.startswith(LOG_DIRS) or f in LOG_FILES for f in files
    )


def collect() -> list[str]:
    """One HTML <tr> per repo per evening, plus uncommitted-work rows.

    Grouped by (repo, day): a busy night can produce a dozen commits, and a
    morning prompt table that reads as a changelog has failed — the writer
    needs the shape of the session, not the commit list.
    """
    since = (dt.datetime.now() - WINDOW).strftime("%Y-%m-%dT%H:%M:%S")
    groups: dict[tuple[str, str], list[str]] = {}
    rows: list[str] = []

    for label, repo in REPOS:
        if not (repo / ".git").is_dir():
            continue
        # %cI: strict ISO 8601 (colon in the offset) — datetime.fromisoformat
        # accepts %ci's space separator and colon-less offset only on 3.11+.
        log = git(
            repo, "log", f"--since={since}",
            "--pretty=format:%h%x09%cI%x09%s", "--no-merges",
        ).strip()
        for line in log.splitlines():
            short, committed, subject = line.split("\t", 2)
            if is_log_only(repo, short):
                continue
            committed_dt = dt.datetime.fromisoformat(committed)
            # "%-d" is POSIX-only; f-string keeps this portable.
            day = f"{committed_dt:%a %b} {committed_dt.day}"
            groups.setdefault((label, day), []).append(subject)

        dirty = git(repo, "status", "--porcelain").strip()
        if dirty:
            count = len(dirty.splitlines())
            rows.append(
                "<tr>"
                '<td class="when">uncommitted</td>'
                f'<td class="repo">{esc(label)}</td>'
                f"<td>{count} file{'s' if count != 1 else ''} changed in the "
                "working tree</td>"
                '<td class="prompt">Last night\'s session isn\'t committed. '
                "What was it about — and did anything surprise you?</td>"
                "</tr>"
            )

    for (label, day), subjects in groups.items():
        shown = [f"<span class=\"hash\">{esc(s)}</span>" for s in subjects[:3]]
        more = f" …and {len(subjects) - 3} more" if len(subjects) > 3 else ""
        what = f"{len(subjects)} commit{'s' if len(subjects) != 1 else ''}: " + "; ".join(shown) + more
        rows.append(
            "<tr>"
            f'<td class="when">{esc(day)}</td>'
            f'<td class="repo">{esc(label)}</td>'
            f"<td>{what}</td>"
            f'<td class="prompt">{esc(prompt_for(subjects[0]))}</td>'
            "</tr>"
        )

    if not rows:
        rows.append(
            "<tr>"
            '<td class="when">—</td><td class="repo">—</td>'
            "<td>No commits and no uncommitted work in the last 48 hours</td>"
            '<td class="prompt">No surprise, no entry. If a standing seed below '
            "still isn't shipped, today is a fine day for it.</td>"
            "</tr>"
        )
    return rows


def replace_between(text: str, begin: str, end: str, body: str, name: str) -> str:
    pattern = re.compile(re.escape(begin) + ".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        raise SystemExit(f"{TARGET.name}: {name} markers missing; refusing to write")
    # Lambda replacement: body carries commit messages, and re.sub would
    # interpret backslashes in a plain replacement string as escapes.
    return pattern.sub(lambda _: f"{begin}\n{body}\n{end}", text, count=1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")
    rows = collect()
    table = (
        "<table>\n"
        "  <thead><tr><th>When</th><th>Repo</th><th>What landed</th>"
        "<th>Prompt angle</th></tr></thead>\n"
        "  <tbody>\n" + "\n".join(rows) + "\n  </tbody>\n</table>"
    )
    text = replace_between(text, PROMPTS_BEGIN, PROMPTS_END, table, "PROMPTS")
    stamp = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    text = replace_between(text, GENERATED_BEGIN, GENERATED_END, esc(stamp), "GENERATED")
    TARGET.write_text(text, encoding="utf-8")
    print(f"{TARGET.name}: {len(rows)} prompt row(s), stamped {stamp}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"error: git failed: {exc.stderr.strip()}", file=sys.stderr)
        raise SystemExit(2)
    except subprocess.TimeoutExpired:
        print("error: git timed out (60s); is another process holding the repo?", file=sys.stderr)
        raise SystemExit(2)
    except FileNotFoundError:
        print("error: git not found on PATH", file=sys.stderr)
        raise SystemExit(2)

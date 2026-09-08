#!/usr/bin/env python3
"""Append one day to data/track-record.json, or record a paper -> live change.

Usage:

    python3 scripts/append_observation.py \
        --date 2026-09-01 --nav 100123.45 \
        --gross-pnl 150.00 --costs 26.55 --positions 4 --mode paper \
        --record-kind forward_sim

    python3 scripts/append_observation.py \
        --mode-change live --date 2027-03-01 --note "Funded with real capital."

Add --commit to create the git commit as well.

The script only ever appends, and re-runs the full validator on the whole
document before writing, so a bad append never lands on disk.

It does NOT enforce the append-only guarantee — that lives in CI, in
validate_track_record.py --check-append-only, which compares against git
history. This script only sees the file in front of it, so a locally tampered
file will still append cleanly here and be rejected on push. That split is
deliberate: local tooling is convenience, CI is the guarantee.

Exit codes: 0 ok, 1 refused, 2 could not run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from validate_track_record import (  # noqa: E402
    DEFAULT_PATH,
    REPO_ROOT,
    VALID_RECORD_KINDS,
    CannotRun,
    Failure,
    _parse_date,
    load,
    validate_structure,
)

# Typed by hand at the end of a trading day, so the refusal has to explain the
# design decision rather than just list the legal values — "backtest" is the
# value a reasonable person expects to work, because the site's own copy names
# three kinds of record.
BACKTEST_REFUSAL = (
    "backtest days do not belong in this file. Its guarantee is that each day "
    "was published before its outcome was known, and a historical simulation "
    "is generated in bulk from data that was already in hand, so appending one "
    "here would borrow that guarantee without earning it. Publish the backtest "
    "as its own diagnostic report and let the page show the two side by side. "
    "See data/SCHEMA.md."
)


def write(doc: dict[str, Any], path: pathlib.Path) -> None:
    path.write_text(json.dumps(doc, indent=2) + "\n")


def append_observation(doc: dict[str, Any], args: argparse.Namespace) -> None:
    observations = doc.setdefault("observations", [])
    date = dt.date.fromisoformat(args.date)

    if observations:
        last = dt.date.fromisoformat(observations[-1]["date"])
        if date <= last:
            raise Failure(
                f"refusing to append {date}: the last published observation is "
                f"{last}. Observations are append-only and strictly ascending."
            )

    observations.append(
        {
            "date": args.date,
            "nav": round(float(args.nav), 2),
            "gross_pnl": round(float(args.gross_pnl), 2),
            "costs": round(float(args.costs), 2),
            "positions": int(args.positions),
            "mode": args.mode,
            "record_kind": args.record_kind,
        }
    )

    if doc.get("inception") is None:
        doc["inception"] = args.date


def append_mode_change(doc: dict[str, Any], args: argparse.Namespace) -> None:
    changes = doc.setdefault("mode_changes", [])
    current = changes[-1]["to"] if changes else "paper"
    date = dt.date.fromisoformat(args.date)

    if current == args.mode_change:
        raise Failure(f"mode is already {current!r}; nothing to record")

    # Same bounds the validator applies, checked here so the script fails with
    # a clear message instead of writing a file it is about to reject.
    if date > dt.date.today():
        raise Failure(f"refusing to record a transition dated {date}: it is in the future")
    if changes:
        last = dt.date.fromisoformat(changes[-1]["date"])
        if date <= last:
            raise Failure(
                f"refusing to record {date}: the last transition is {last}. "
                "Transitions are append-only and strictly ascending."
            )

    changes.append(
        {
            "date": args.date,
            "from": current,
            "to": args.mode_change,
            "note": args.note or "",
        }
    )


def git_commit(message: str, path: pathlib.Path) -> None:
    """Commit only `path`.

    The pathspec matters: a bare `git commit -m` would sweep whatever else
    happens to be staged into the observation commit, and the value of the
    history as a timestamp trail depends on those commits staying clean.
    """
    subprocess.run(
        ["git", "-C", str(REPO_ROOT), "commit", "-m", message, "--", str(path)],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--nav", type=float, help="net asset value at the close, after costs")
    parser.add_argument("--gross-pnl", type=float, default=None, help="P&L before frictions (required)")
    parser.add_argument("--costs", type=float, default=None, help="total frictions for the day (required)")
    parser.add_argument("--positions", type=int, default=0, help="open positions at the close")
    parser.add_argument("--mode", choices=("paper", "live"), default="paper")
    # Deliberately not an argparse `choices` list, unlike --mode: argparse would
    # answer "backtest" with a bare "invalid choice", and the reason backtests
    # are excluded is the one thing someone typing that needs to be told.
    # Checked in main() instead, so the refusal is exit 1 with the explanation.
    parser.add_argument(
        "--record-kind",
        default=None,
        help=(
            "how the day's numbers were produced (required): "
            + " | ".join(VALID_RECORD_KINDS)
        ),
    )
    parser.add_argument(
        "--mode-change",
        choices=("paper", "live"),
        help="record a capital-mode transition instead of appending an observation",
    )
    parser.add_argument("--note", help="note attached to a mode change")
    parser.add_argument("--commit", action="store_true", help="git commit the change")
    parser.add_argument("--path", type=pathlib.Path, default=DEFAULT_PATH)
    args = parser.parse_args()

    try:
        # The date is stored verbatim, so it must be checked against the same
        # strict YYYY-MM-DD rule the validator applies — a bare fromisoformat
        # would let "20260902" or a week date through and write it to disk.
        _parse_date(args.date, "--date")
    except Failure as exc:
        print(f"FAIL  {exc}", file=sys.stderr)
        return 1

    if args.mode_change is None:
        if args.nav is None or args.gross_pnl is None or args.costs is None:
            print(
                "FAIL  --nav, --gross-pnl and --costs are all required when "
                "appending an observation; an omitted cost would publish a "
                "plausible-looking $0-friction day",
                file=sys.stderr,
            )
            return 1

        # No default. A discriminator that guesses is worse than none at all:
        # whichever value it picked would be an unearned claim about how the
        # day's numbers were produced, made silently, on every append.
        if args.record_kind is None:
            print(
                "FAIL  --record-kind is required when appending an observation "
                f"({' | '.join(VALID_RECORD_KINDS)}); it says whether the day's "
                "numbers came from a simulator or from reconciled broker fills, "
                "and there is no honest default",
                file=sys.stderr,
            )
            return 1
        if args.record_kind not in VALID_RECORD_KINDS:
            detail = (
                BACKTEST_REFUSAL
                if args.record_kind == "backtest"
                else f"expected one of {list(VALID_RECORD_KINDS)}"
            )
            print(
                f"FAIL  --record-kind {args.record_kind!r} is not a valid record "
                f"kind: {detail}",
                file=sys.stderr,
            )
            return 1

    try:
        doc = load(args.path)
        if args.mode_change:
            append_mode_change(doc, args)
            message = f"track record: record transition to {args.mode_change} on {args.date}"
        else:
            append_observation(doc, args)
            message = (
                f"track record: add {args.date} (nav {args.nav}, "
                f"mode {args.mode}, {args.record_kind})"
            )

        # Validate the whole document before it is written, so a bad append
        # never lands on disk.
        notes = validate_structure(doc)
    except Failure as exc:
        print(f"FAIL  {exc}", file=sys.stderr)
        return 1
    except CannotRun as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2

    write(doc, args.path)
    print(f"OK    {message}")
    print(f"      {'; '.join(notes)}")

    if args.commit:
        try:
            git_commit(message, args.path)
        except subprocess.CalledProcessError as exc:
            print(f"FAIL  git commit failed: {exc}", file=sys.stderr)
            return 1
        print("      committed")

    return 0


if __name__ == "__main__":
    sys.exit(main())

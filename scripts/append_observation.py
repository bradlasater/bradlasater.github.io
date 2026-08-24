#!/usr/bin/env python3
"""Append one day to data/track-record.json, or record a paper -> live change.

Usage:

    python3 scripts/append_observation.py \
        --date 2026-09-01 --nav 100123.45 \
        --gross-pnl 150.00 --costs 26.55 --positions 4 --mode paper

    python3 scripts/append_observation.py \
        --mode-change live --date 2027-03-01 --note "Funded with real capital."

Add --commit to create the git commit as well.

The script refuses to touch anything already published: it only ever appends,
and it re-runs the full validator before writing. That is deliberate — the
track record's credibility rests on it being impossible to revise quietly.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from validate_track_record import Failure, validate_structure  # noqa: E402

PATH = pathlib.Path("data/track-record.json")


def read() -> dict:
    return json.loads(PATH.read_text())


def write(doc: dict) -> None:
    PATH.write_text(json.dumps(doc, indent=2) + "\n")


def append_observation(doc: dict, args: argparse.Namespace) -> str:
    observations = doc["observations"]
    date = dt.date.fromisoformat(args.date)

    if observations:
        last = dt.date.fromisoformat(observations[-1]["date"])
        if date <= last:
            raise Failure(
                f"refusing to append {date}: the last published observation is {last}. "
                "Observations are append-only and strictly ascending."
            )

    observations.append(
        {
            "date": args.date,
            "nav": round(float(args.nav), 2),
            "gross_pnl": round(float(args.gross_pnl), 2),
            "costs": round(float(args.costs), 2),
            "positions": int(args.positions),
            "mode": args.mode,
        }
    )

    if doc.get("inception") is None:
        doc["inception"] = args.date

    return f"track record: add {args.date} (nav {args.nav}, mode {args.mode})"


def append_mode_change(doc: dict, args: argparse.Namespace) -> str:
    changes = doc.setdefault("mode_changes", [])
    current = changes[-1]["to"] if changes else "paper"

    if current == args.mode_change:
        raise Failure(f"mode is already {current!r}; nothing to record")

    changes.append(
        {
            "date": args.date,
            "from": current,
            "to": args.mode_change,
            "note": args.note or "",
        }
    )
    return f"track record: record {current} -> {args.mode_change} on {args.date}"


def git_commit(message: str) -> None:
    subprocess.run(["git", "add", str(PATH)], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--nav", type=float, help="net asset value at the close, after costs")
    parser.add_argument("--gross-pnl", type=float, default=0.0, help="P&L before frictions")
    parser.add_argument("--costs", type=float, default=0.0, help="total frictions for the day")
    parser.add_argument("--positions", type=int, default=0, help="open positions at the close")
    parser.add_argument("--mode", choices=("paper", "live"), default="paper")
    parser.add_argument(
        "--mode-change",
        choices=("paper", "live"),
        help="record a capital-mode transition instead of appending an observation",
    )
    parser.add_argument("--note", help="note attached to a mode change")
    parser.add_argument("--commit", action="store_true", help="git commit the change")
    args = parser.parse_args()

    try:
        dt.date.fromisoformat(args.date)
    except ValueError:
        print(f"FAIL  --date {args.date!r} is not an ISO YYYY-MM-DD date", file=sys.stderr)
        return 1

    if args.mode_change is None and args.nav is None:
        print("FAIL  --nav is required when appending an observation", file=sys.stderr)
        return 1

    try:
        doc = read()
        message = (
            append_mode_change(doc, args)
            if args.mode_change
            else append_observation(doc, args)
        )
        # Validate the whole document before it is written, so a bad append
        # never lands on disk.
        notes = validate_structure(doc)
    except Failure as exc:
        print(f"FAIL  {exc}", file=sys.stderr)
        return 1

    write(doc)
    print(f"OK    {message}")
    print(f"      {'; '.join(notes)}")

    if args.commit:
        try:
            git_commit(message)
        except subprocess.CalledProcessError as exc:
            print(f"FAIL  git commit failed: {exc}", file=sys.stderr)
            return 1
        print("      committed")

    return 0


if __name__ == "__main__":
    sys.exit(main())

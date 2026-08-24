#!/usr/bin/env python3
"""Validate data/track-record.json.

Two jobs:

1. Structural validation — the file is well formed, observations are strictly
   ascending, nothing is dated in the future, values are sane.
2. Append-only enforcement (--check-append-only) — diff against the previous
   commit and fail if any already-published observation was modified, removed,
   or reordered. Appending is the only legal edit.

The second job is the point. A published track record is only evidence if it
cannot be quietly revised after the fact, so the check runs in CI on every push.

Exit codes: 0 ok, 1 validation failed, 2 could not run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys

DEFAULT_PATH = pathlib.Path("data/track-record.json")
VALID_MODES = {"paper", "live"}
OBS_REQUIRED = ("date", "nav", "gross_pnl", "costs", "positions", "mode")


class Failure(Exception):
    pass


def _parse_date(value: str, label: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        raise Failure(f"{label}: {value!r} is not an ISO YYYY-MM-DD date")


def load(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        raise Failure(f"{path} does not exist")
    except json.JSONDecodeError as exc:
        raise Failure(f"{path} is not valid JSON: {exc}")


def validate_structure(doc: dict) -> list[str]:
    """Return a list of human-readable notes; raise Failure on any hard error."""
    notes: list[str] = []

    if doc.get("schema_version") != 1:
        raise Failure(f"schema_version must be 1, got {doc.get('schema_version')!r}")

    periods = doc.get("periods_per_year")
    if not isinstance(periods, int) or periods <= 0:
        raise Failure("periods_per_year must be a positive integer")

    observations = doc.get("observations")
    if not isinstance(observations, list):
        raise Failure("observations must be an array")

    today = dt.date.today()
    previous: dt.date | None = None

    for index, obs in enumerate(observations):
        where = f"observations[{index}]"
        if not isinstance(obs, dict):
            raise Failure(f"{where} must be an object")

        missing = [key for key in OBS_REQUIRED if key not in obs]
        if missing:
            raise Failure(f"{where} is missing required field(s): {', '.join(missing)}")

        date = _parse_date(obs["date"], where)

        # Future-dated observations would let the record claim time it has not
        # actually accumulated, which is the whole asset being protected here.
        if date > today:
            raise Failure(f"{where}: {date} is in the future")

        if previous is not None and date <= previous:
            raise Failure(
                f"{where}: dates must be strictly ascending "
                f"({date} follows {previous})"
            )
        previous = date

        nav = obs["nav"]
        if not isinstance(nav, (int, float)) or isinstance(nav, bool) or nav <= 0:
            raise Failure(f"{where}: nav must be a positive number, got {nav!r}")

        costs = obs["costs"]
        if not isinstance(costs, (int, float)) or isinstance(costs, bool) or costs < 0:
            raise Failure(f"{where}: costs must be a non-negative number, got {costs!r}")

        gross = obs["gross_pnl"]
        if not isinstance(gross, (int, float)) or isinstance(gross, bool):
            raise Failure(f"{where}: gross_pnl must be a number, got {gross!r}")

        positions = obs["positions"]
        if not isinstance(positions, int) or isinstance(positions, bool) or positions < 0:
            raise Failure(f"{where}: positions must be a non-negative integer")

        if obs["mode"] not in VALID_MODES:
            raise Failure(
                f"{where}: mode must be one of {sorted(VALID_MODES)}, got {obs['mode']!r}"
            )

    inception = doc.get("inception")
    if observations:
        if inception is None:
            raise Failure("inception must be set once observations exist")
        inception_date = _parse_date(inception, "inception")
        first = _parse_date(observations[0]["date"], "observations[0]")
        if inception_date != first:
            raise Failure(
                f"inception ({inception_date}) must equal the first observation date ({first})"
            )
    elif inception is not None:
        raise Failure("inception must be null while there are no observations")

    for index, change in enumerate(doc.get("mode_changes", [])):
        where = f"mode_changes[{index}]"
        for key in ("date", "from", "to"):
            if key not in change:
                raise Failure(f"{where} is missing required field {key!r}")
        _parse_date(change["date"], where)
        if change["from"] not in VALID_MODES or change["to"] not in VALID_MODES:
            raise Failure(f"{where}: from/to must be one of {sorted(VALID_MODES)}")
        if change["from"] == change["to"]:
            raise Failure(f"{where}: from and to are both {change['from']!r}")

    notes.append(f"{len(observations)} observation(s)")
    if observations:
        notes.append(f"span {observations[0]['date']} to {observations[-1]['date']}")
    modes = {obs["mode"] for obs in observations}
    if modes:
        notes.append("mode(s): " + ", ".join(sorted(modes)))
    return notes


def _previous_version(path: pathlib.Path, ref: str) -> dict | None:
    """The file as of `ref`, or None if it did not exist there."""
    try:
        blob = subprocess.run(
            ["git", "show", f"{ref}:{path.as_posix()}"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise Failure(f"could not run git: {exc}")

    if blob.returncode != 0:
        return None
    try:
        return json.loads(blob.stdout)
    except json.JSONDecodeError:
        # An unparseable previous version cannot constrain the new one.
        return None


def validate_append_only(doc: dict, path: pathlib.Path, ref: str) -> list[str]:
    old = _previous_version(path, ref)
    if old is None:
        return [f"no previous version at {ref}; append-only check skipped"]

    old_obs = old.get("observations", [])
    new_obs = doc.get("observations", [])

    if len(new_obs) < len(old_obs):
        raise Failure(
            f"observations shrank from {len(old_obs)} to {len(new_obs)}; "
            "published observations may not be removed"
        )

    for index, previous in enumerate(old_obs):
        current = new_obs[index]
        if current != previous:
            changed = sorted(
                key
                for key in set(previous) | set(current)
                if previous.get(key) != current.get(key)
            )
            raise Failure(
                f"observations[{index}] (dated {previous.get('date')}) was modified; "
                f"changed field(s): {', '.join(changed)}. "
                "Published observations are append-only."
            )

    added = len(new_obs) - len(old_obs)
    return [f"append-only ok ({added} new observation(s) since {ref})"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=pathlib.Path, default=DEFAULT_PATH)
    parser.add_argument(
        "--check-append-only",
        action="store_true",
        help="also verify no published observation was modified or removed",
    )
    parser.add_argument(
        "--ref",
        default="HEAD^",
        help="git ref to diff against for the append-only check (default: HEAD^)",
    )
    args = parser.parse_args()

    try:
        doc = load(args.path)
        notes = validate_structure(doc)
        if args.check_append_only:
            notes += validate_append_only(doc, args.path, args.ref)
    except Failure as exc:
        print(f"FAIL  {args.path}: {exc}", file=sys.stderr)
        return 1

    print(f"OK    {args.path}: " + "; ".join(notes))
    return 0


if __name__ == "__main__":
    sys.exit(main())

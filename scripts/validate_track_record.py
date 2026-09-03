#!/usr/bin/env python3
"""Validate data/track-record.json and enforce that published history is immutable.

Two jobs:

1. Structural validation — the file is well formed, observations are strictly
   ascending, nothing is dated in the future, mode changes form a connected
   chain that agrees with the per-observation modes.

2. Append-only enforcement (--check-append-only) — walk every commit from a
   baseline ref up to HEAD, plus the working tree, and fail if any published
   observation or immutable metadata field changed at any step. Appending is
   the only legal edit.

The second job is the point. A published track record is only evidence if it
cannot be quietly revised after the fact.

Three design rules follow from that, and each exists because violating it
produced a working bypass:

- **Walk the whole range, not one hop.** A push carries many commits but fires
  one CI run at the tip. Checking only HEAD against HEAD^ lets an earlier
  commit in the same push rewrite history unseen.
- **Fail closed.** If the baseline cannot be read — git unavailable, ref
  unresolvable, baseline JSON corrupt — that is exit 2, never a silent pass.
  An attacker chooses whether the previous version parses.
- **Protect more than the observations list.** periods_per_year rescales every
  derived statistic, and mode_changes records which capital was real. Both are
  immutable once published.

Exit codes: 0 ok, 1 validation failed, 2 could not run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import pathlib
import re
import subprocess
import sys
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "data" / "track-record.json"

VALID_MODES = ("paper", "live")
OBS_REQUIRED = ("date", "nav", "gross_pnl", "costs", "positions", "mode")

# Changing any of these retroactively reinterprets numbers that are already
# published, so they are frozen once the first observation exists.
# periods_per_year is the dangerous one: it scales annualised return,
# annualised volatility, Sharpe, PSR and MinTRL all at once.
IMMUTABLE_TOP_LEVEL = (
    "schema_version",
    "strategy",
    "inception",
    "base_currency",
    "periods_per_year",
)


class Failure(Exception):
    """A validation error to report to the user. Not a bug in this script."""


class CannotRun(Exception):
    """The check could not be performed, so its result is unknown.

    Distinct from Failure because "I could not verify this" must never be
    reported, or exit, as "this is fine".
    """


# ---------------------------------------------------------------- loading --


_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _parse_date(value: Any, label: str) -> dt.date:
    # fromisoformat is lenient since Python 3.11 — it accepts "20260902" and
    # week dates like "2026-W36-3" — but the schema promises exactly
    # YYYY-MM-DD, the only form the page's JavaScript accepts.
    if not isinstance(value, str) or not _DATE_RE.fullmatch(value):
        raise Failure(f"{label}: {value!r} is not an ISO YYYY-MM-DD date")
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise Failure(f"{label}: {value!r} is not an ISO YYYY-MM-DD date") from None


def _as_document(raw: str, label: str) -> dict[str, Any]:
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise Failure(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(doc, dict):
        raise Failure(f"{label} must contain a JSON object, got {type(doc).__name__}")
    return doc


def load(path: pathlib.Path) -> dict[str, Any]:
    try:
        raw = path.read_text()
    except FileNotFoundError:
        raise Failure(f"{path} does not exist") from None
    except OSError as exc:
        raise CannotRun(f"could not read {path}: {exc}") from exc
    return _as_document(raw, str(path))


# ----------------------------------------------------------- structure ----


def _validate_observation(obs: Any, where: str, today: dt.date) -> dt.date:
    if not isinstance(obs, dict):
        raise Failure(f"{where} must be an object")

    missing = [key for key in OBS_REQUIRED if key not in obs]
    if missing:
        raise Failure(f"{where} is missing required field(s): {', '.join(missing)}")

    date = _parse_date(obs["date"], where)

    # A future-dated observation would let the record claim elapsed time it has
    # not actually accumulated, which is the asset this whole file protects.
    if date > today:
        raise Failure(f"{where}: {date} is in the future")

    # json.loads accepts NaN and Infinity by default, and comparisons against
    # them are always False, so without an explicit finiteness check both
    # would pass every numeric test below and poison the derived statistics.
    nav = obs["nav"]
    if (
        not isinstance(nav, (int, float))
        or isinstance(nav, bool)
        or not math.isfinite(nav)
        or nav <= 0
    ):
        raise Failure(f"{where}: nav must be a positive finite number, got {nav!r}")

    costs = obs["costs"]
    if (
        not isinstance(costs, (int, float))
        or isinstance(costs, bool)
        or not math.isfinite(costs)
        or costs < 0
    ):
        raise Failure(
            f"{where}: costs must be a non-negative finite number, got {costs!r}"
        )

    gross = obs["gross_pnl"]
    if (
        not isinstance(gross, (int, float))
        or isinstance(gross, bool)
        or not math.isfinite(gross)
    ):
        raise Failure(f"{where}: gross_pnl must be a finite number, got {gross!r}")

    positions = obs["positions"]
    if not isinstance(positions, int) or isinstance(positions, bool) or positions < 0:
        raise Failure(f"{where}: positions must be a non-negative integer")

    if obs["mode"] not in VALID_MODES:
        raise Failure(
            f"{where}: mode must be one of {list(VALID_MODES)}, got {obs['mode']!r}"
        )

    return date


def _validate_observations(doc: dict[str, Any], today: dt.date) -> list[dict[str, Any]]:
    observations = doc.get("observations")
    if not isinstance(observations, list):
        raise Failure("observations must be an array")

    previous: dt.date | None = None
    for index, obs in enumerate(observations):
        date = _validate_observation(obs, f"observations[{index}]", today)
        if previous is not None and date <= previous:
            raise Failure(
                f"observations[{index}]: dates must be strictly ascending "
                f"({date} follows {previous})"
            )
        previous = date

    return observations


def _validate_inception(doc: dict[str, Any], observations: list[dict[str, Any]]) -> None:
    inception = doc.get("inception")
    if observations:
        if inception is None:
            raise Failure("inception must be set once observations exist")
        inception_date = _parse_date(inception, "inception")
        first = _parse_date(observations[0]["date"], "observations[0]")
        if inception_date != first:
            raise Failure(
                f"inception ({inception_date}) must equal the first "
                f"observation date ({first})"
            )
    elif inception is not None:
        raise Failure("inception must be null while there are no observations")


def _validate_mode_changes(
    doc: dict[str, Any], observations: list[dict[str, Any]], today: dt.date
) -> None:
    """Check the capital-mode chain, and that observations agree with it.

    mode_changes and each observation's `mode` are two statements about the
    same fact — which capital a given day was traded with. If they are allowed
    to disagree, the record can show a day as simulated in one place and real
    in the other, which is precisely the silent swap the schema promises not to
    permit.
    """
    changes = doc.get("mode_changes", [])
    if not isinstance(changes, list):
        raise Failure("mode_changes must be an array")

    previous_date: dt.date | None = None
    expected_from = "paper"  # the record starts paper-traded by definition

    for index, change in enumerate(changes):
        where = f"mode_changes[{index}]"
        if not isinstance(change, dict):
            raise Failure(f"{where} must be an object")
        for key in ("date", "from", "to"):
            if key not in change:
                raise Failure(f"{where} is missing required field {key!r}")

        date = _parse_date(change["date"], where)
        if date > today:
            raise Failure(f"{where}: {date} is in the future")
        if previous_date is not None and date <= previous_date:
            raise Failure(
                f"{where}: dates must be strictly ascending "
                f"({date} follows {previous_date})"
            )
        previous_date = date

        if change["from"] not in VALID_MODES or change["to"] not in VALID_MODES:
            raise Failure(f"{where}: from/to must be one of {list(VALID_MODES)}")
        if change["from"] == change["to"]:
            raise Failure(f"{where}: from and to are both {change['from']!r}")
        if change["from"] != expected_from:
            raise Failure(
                f"{where}: from is {change['from']!r} but the mode in effect on "
                f"{date} is {expected_from!r}; the chain must connect"
            )
        expected_from = change["to"]

    if not observations:
        return

    # Replay the chain across the observations and require agreement.
    boundaries = [(_parse_date(c["date"], "mode_changes"), c["to"]) for c in changes]
    for index, obs in enumerate(observations):
        obs_date = _parse_date(obs["date"], f"observations[{index}]")
        implied = "paper"
        for boundary_date, to_mode in boundaries:
            if obs_date >= boundary_date:
                implied = to_mode
        if obs["mode"] != implied:
            raise Failure(
                f"observations[{index}] ({obs_date}) has mode {obs['mode']!r} but "
                f"mode_changes implies {implied!r}; record the transition in "
                "mode_changes rather than switching an observation's mode alone"
            )


def validate_structure(doc: dict[str, Any]) -> list[str]:
    """Validate the document in isolation. Raises Failure on any hard error."""
    # `True == 1` and `1.0 == 1` in Python, so a bare `!= 1` would let a
    # boolean or float through; the schema says integer.
    version = doc.get("schema_version")
    if not isinstance(version, int) or isinstance(version, bool) or version != 1:
        raise Failure(f"schema_version must be the integer 1, got {version!r}")

    for field in ("strategy", "base_currency"):
        if not isinstance(doc.get(field), str):
            raise Failure(f"{field} must be a string, got {doc.get(field)!r}")

    periods = doc.get("periods_per_year")
    if not isinstance(periods, int) or isinstance(periods, bool) or periods <= 0:
        raise Failure("periods_per_year must be a positive integer")

    today = dt.date.today()
    observations = _validate_observations(doc, today)
    _validate_inception(doc, observations)
    _validate_mode_changes(doc, observations, today)

    notes = [f"{len(observations)} observation(s)"]
    if observations:
        notes.append(f"span {observations[0]['date']} to {observations[-1]['date']}")
        notes.append("mode(s): " + ", ".join(sorted({o["mode"] for o in observations})))
    return notes


# ------------------------------------------------------------ git access --


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", "-C", str(REPO_ROOT), *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise CannotRun(f"could not run git: {exc}") from exc


def _rel_to_repo(path: pathlib.Path) -> str:
    """Path relative to the repo root — `git show ref:path` requires that."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        raise CannotRun(f"{path} is outside the repository at {REPO_ROOT}") from None


def _resolve(ref: str) -> str:
    result = _git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    if result.returncode != 0 or not result.stdout.strip():
        raise CannotRun(
            f"cannot resolve {ref!r}; the append-only check could not be performed"
        )
    return result.stdout.strip()


def _document_at(ref: str, rel_path: str) -> dict[str, Any] | None:
    """The document as of `ref`, or None only if it provably did not exist.

    Any other failure raises. A check that cannot read its baseline must fail
    the build, never quietly pass — an attacker gets to choose whether the
    baseline is readable.
    """
    _resolve(ref)  # raises CannotRun if the ref itself is unresolvable
    blob = _git("show", f"{ref}:{rel_path}")
    if blob.returncode != 0:
        stderr = blob.stderr.lower()
        if "does not exist" in stderr or "exists on disk, but not in" in stderr:
            return None  # genuine first publish
        raise CannotRun(f"could not read {rel_path} at {ref}: {blob.stderr.strip()}")
    return _as_document(blob.stdout, f"{rel_path} at {ref}")


# -------------------------------------------------------- append-only ----


def _check_list_append_only(
    old: list[Any], new: list[Any], label: str, context: str
) -> None:
    if len(new) < len(old):
        raise Failure(
            f"{context}: {label} shrank from {len(old)} to {len(new)}; "
            f"published entries may not be removed"
        )
    for index, previous in enumerate(old):
        current = new[index]
        if current == previous:
            continue
        changed = sorted(
            key
            for key in set(previous) | set(current)
            if previous.get(key) != current.get(key)
        ) if isinstance(previous, dict) and isinstance(current, dict) else []
        detail = f"; changed field(s): {', '.join(changed)}" if changed else ""
        raise Failure(
            f"{context}: {label}[{index}] was modified{detail}. "
            f"Published entries are append-only."
        )


def _compare(old: dict[str, Any] | None, new: dict[str, Any], context: str) -> None:
    """Fail if `new` revises anything `old` already published."""
    if old is None:
        return

    for field in IMMUTABLE_TOP_LEVEL:
        # Only frozen once something has actually been published under it.
        if not old.get("observations"):
            break
        if field in old and old[field] != new.get(field):
            raise Failure(
                f"{context}: {field} changed from {old[field]!r} to "
                f"{new.get(field)!r}; published metadata is immutable because "
                f"it reinterprets numbers that are already public"
            )

    _check_list_append_only(
        old.get("observations", []), new.get("observations", []), "observations", context
    )
    _check_list_append_only(
        old.get("mode_changes", []), new.get("mode_changes", []), "mode_changes", context
    )


def validate_append_only(
    doc: dict[str, Any], path: pathlib.Path, ref: str
) -> list[str]:
    """Walk every commit from `ref` to HEAD, then the working tree.

    Checking only the endpoints would miss a push whose intermediate commit
    tampers and whose final commit restores a plausible-looking file.
    """
    rel = _rel_to_repo(path)
    baseline = _resolve(ref)

    revs = _git("rev-list", "--reverse", f"{baseline}..HEAD")
    if revs.returncode != 0:
        raise CannotRun(f"could not enumerate commits: {revs.stderr.strip()}")
    commits = [line for line in revs.stdout.split() if line]

    baseline_doc = _document_at(baseline, rel)
    previous = baseline_doc
    steps = 0
    for commit in commits:
        current = _document_at(commit, rel)
        if current is None:
            if previous is not None:
                raise Failure(f"{commit[:8]}: {rel} was deleted")
            continue
        _compare(previous, current, commit[:8])
        previous = current
        steps += 1

    # Finally the working tree, which is what actually ships.
    _compare(previous, doc, "working tree")

    added = len(doc.get("observations", [])) - len(
        (baseline_doc or {}).get("observations", [])
    )
    return [
        f"append-only ok across {len(commits)} commit(s) since {ref} "
        f"({steps} touching {rel}; {added} new observation(s))"
    ]


# ------------------------------------------------------------------ main --


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=pathlib.Path, default=DEFAULT_PATH)
    parser.add_argument(
        "--check-append-only",
        action="store_true",
        help="also verify no published observation or metadata was revised",
    )
    parser.add_argument(
        "--ref",
        default="HEAD^",
        help=(
            "baseline commit for the append-only walk. In CI pass the pre-push "
            "SHA (github.event.before), not the default, so that every commit "
            "in the push is inspected."
        ),
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
    except CannotRun as exc:
        print(f"ERROR {args.path}: {exc}", file=sys.stderr)
        return 2

    print(f"OK    {args.path}: " + "; ".join(notes))
    return 0


if __name__ == "__main__":
    sys.exit(main())

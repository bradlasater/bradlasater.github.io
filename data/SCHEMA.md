# `track-record.json` — the data contract

This file is the single source of truth for the published out-of-sample track
record at `/vol/track-record.html`. The page computes every statistic it shows
from this file in the browser; nothing is precomputed and pasted in.

## Why the format is append-only

The value of a published track record is a function of elapsed time, and it only
holds if the record cannot be quietly revised after the fact. Two mechanisms
enforce that here:

1. **Every observation is a separate commit.** The git history is the timestamp
   trail. A reader can check when any given number first appeared.
2. **CI rejects edits to existing observations.** `.github/workflows/validate-track-record.yml`
   runs `scripts/validate_track_record.py --check-append-only` on every push and
   pull request that touches the data file, walking **every commit** from the
   merge-base with the base branch through HEAD — not just the previous commit —
   so tampering in an intermediate commit is caught too. The build fails if any
   already-published observation changed or disappeared, and the workflow
   rejects force-pushes it can see. Appending is the only legal edit.

Neither mechanism is worth anything if history gets rewritten. The workflow is
path-filtered, so the durable guard is branch protection: **force-pushes and
deletion are disabled on `main`, enforced for admins.** Never force-push this
repository.

## Top-level fields

| Field | Type | Notes |
|---|---|---|
| `schema_version` | integer | Currently `1`. Bump on any breaking change. |
| `strategy` | string | Human-readable name shown on the page. |
| `inception` | `YYYY-MM-DD` or `null` | Date tracking began. `null` until the first observation is appended, at which point the append script sets it. |
| `base_currency` | string | Display only. |
| `periods_per_year` | integer | Annualisation factor. `252` for daily observations. |
| `mode_changes` | array | Records each paper→live transition. See below. |
| `observations` | array | Append-only, strictly ascending by `date`. |

## `mode_changes`

The record starts paper-traded and may later move to real capital. That
transition is recorded rather than silently swapped, and the page draws it as a
labelled boundary on the equity curve so the simulated and live portions are
never visually conflated.

```json
{ "date": "2027-03-01", "from": "paper", "to": "live", "note": "Funded with real capital." }
```

## `observations[]`

One entry per trading day.

| Field | Type | Notes |
|---|---|---|
| `date` | `YYYY-MM-DD` | Strictly ascending, no duplicates, never in the future. |
| `nav` | number > 0 | Net asset value at the close, **after** costs. Returns are derived from this. |
| `gross_pnl` | number | That day's P&L before frictions. |
| `costs` | number ≥ 0 | That day's total frictions: spread paid, commissions, fees, borrow, hedging costs. |
| `positions` | integer ≥ 0 | Open positions at the close. |
| `mode` | `"paper"` \| `"live"` | Which capital this day was traded with. |
| `record_kind` | `"forward_sim"` \| `"broker_executed"` | Where this day's numbers came from. Required; see below. |

`gross_pnl` and `costs` exist so the page can show what share of gross P&L the
frictions consumed. That number is the honest one: a strategy whose edge is
mostly eaten by costs is reporting the error bar on its cost model.

## `record_kind`

`mode` says whose capital was at risk. `record_kind` says where the day's
numbers came from. They are independent axes and must never be conflated: a
paper-mode day can be forward simulation *or* broker-executed against a
broker's paper account, and the difference between those two is most of what a
reader needs in order to weight the number.

| Value | Meaning |
|---|---|
| `forward_sim` | Run against live market data with nothing at risk. Fills are modelled by this system, not obtained from a broker. |
| `broker_executed` | Reconciled against actual broker fills. |

The values are ordered by evidential strength, and that order is enforced.

### Why there is no `backtest` value

`/vol/track-record.html` names three kinds of result and only two of them are
in this file. That is deliberate, not an omission.

This file's guarantee is a timestamp. Every observation is a separate commit,
so a reader can check that a day was published *before* its outcome was known.
A backtest cannot meet that condition by construction: it is produced in bulk
from data that was already in hand, and it is legitimately re-run whenever the
model changes. Appending one here would let it borrow an append-only history it
did not earn — the single most misleading thing this file could do, on a page
whose entire argument is that it does not do things like that.

Two mechanical consequences point the same way. `inception` must equal the
first observation date and the page reports elapsed days from it, so a backtest
starting in 2015 would advertise ten years of elapsed track record. And
append-only forbids revision, so every re-run would have to land as an
additional series, which this file has no way to express.

Backtests are therefore published as their own diagnostic reports and read
*alongside* the record rather than inside it — which is what "reported
separately rather than joined into one curve" was always supposed to mean. If a
backtest ever does need to live here, that is a `schema_version` bump and a
structure of its own, not a third value quietly added to this field.

### Why the discriminator is per-observation

Three placements were possible. The other two are worse.

**A new immutable top-level field.** `IMMUTABLE_TOP_LEVEL` in the validator
freezes a field once the first observation exists. That is right for
`periods_per_year`, which retroactively rescales published numbers, and wrong
here: the record is *expected* to move from forward simulation to broker
execution — that is the point of building it. A frozen top-level kind would
make that move either an illegal edit or a reason to start a second file, and
abandoning the git history is abandoning the only thing that made the first
file worth reading. It would also put the label somewhere no individual day can
be checked against.

**A `mode_changes`-style chain of transitions.** A capital transition is an
event with a date of its own: funding lands on a Saturday whether or not a
trading day follows, and it carries a note explaining itself. A change of
record kind has no existence apart from an observation — it *is* the first day
whose numbers came from somewhere new. Recording it separately would create a
second statement about the same fact, and therefore a second way for the file
to contradict itself; `mode_changes` already needs a cross-check against every
observation's `mode` for exactly that reason. A second such structure would
double that surface and buy nothing, because the transition date is derivable
from the observations and cannot disagree with them.

**Per-observation, required — the choice made here.** The kind is a property of
how one day's numbers were produced, which is where it is known. It is frozen
the instant that observation is published, by the same append-only rule that
already protects `nav`, so no new immutable field is needed and nothing
top-level has to change when the record climbs.

It is required, and has no default. An optional discriminator would be filled
in by whatever the tooling picked, silently, on every append — a claim about
the provenance of a number that nobody actually made. `append_observation.py`
refuses to write an observation without `--record-kind`.

### The two rules the validator enforces

**The kind may never regress.** Once a `broker_executed` day is published, no
later day may be `forward_sim`. The page reports each kind as its own series,
so a fallback would put the weaker segment at the *end* of the record — the
part a reader weights most heavily — marked by nothing but a field in a JSON
file. A genuine return to simulation is a change in what the record means, and
has to be handled deliberately rather than appended.

**A `live` day must be `broker_executed`.** `forward_sim` is defined as running
with nothing at risk, so a day that both put real capital at risk and reported
simulator marks is describing itself incorrectly whichever field is wrong. The
rule is one-directional on purpose: `paper` + `broker_executed` is legitimate
and useful — a broker paper account produces its own execution reports to
reconcile against — and is the natural rung between the two. If unreconciled
live days ever need publishing, that is a third kind and a `schema_version`
bump, not a loosening of this rule.

### How the page uses it

`assets/js/track-record.js` splits the observations into one contiguous segment
per kind and computes every statistic — cumulative return, annualised return
and volatility, Sharpe, PSR, MinTRL, drawdown, cost share — within a single
segment. When both kinds are present the page shows a series selector,
defaulting to the newer and stronger one, and states directly above the figures
which kind they cover and how many observations they exclude. The table below
the charts stays complete and carries a Kind column.

Nothing is ever aggregated across kinds. One curve running from simulated marks
into real fills, with a single Sharpe over both, is a strictly worse number than
either half on its own.

## Appending a day

```bash
python3 scripts/append_observation.py \
  --date 2026-09-01 --nav 100123.45 \
  --gross-pnl 150.00 --costs 26.55 --positions 4 --mode paper \
  --record-kind forward_sim
```

The script validates before writing and refuses to modify or reorder anything
that already exists. Add `--commit` to have it create the commit for you.

To record a transition to real capital:

```bash
python3 scripts/append_observation.py --mode-change live --date 2027-03-01 \
  --note "Funded with real capital."
```

## Statistics the page derives

Computed in `assets/js/track-record.js` from the returns implied by `nav`,
always within one `record_kind` at a time:

- Cumulative and annualised return, annualised volatility.
- **Annualised Sharpe ratio**, reported but deliberately de-emphasised.
- **Probabilistic Sharpe Ratio (PSR)** — the probability the true Sharpe exceeds
  zero, given the observed skewness, kurtosis, and sample length.
- **Minimum Track Record Length (MinTRL)** — how many observations would be
  needed for the observed Sharpe to be statistically distinguishable from zero
  at 95% confidence. Shown against the actual count, so a track record that is
  too short to mean anything says so rather than implying otherwise.
- Maximum and current drawdown.
- Cost share of gross P&L.

Sharpe uses the sample standard deviation (`ddof=1`); skewness and kurtosis use
the standard moment estimators with raw (not excess) kurtosis, so a normal
distribution gives a kurtosis of 3, not 0. PSR and MinTRL follow Bailey & López de Prado.

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
   runs `scripts/validate_track_record.py --check-append-only`, which diffs the
   file against the previous commit and fails the build if any already-published
   observation changed or disappeared. Appending is the only legal edit.

Neither mechanism is worth anything if history gets rewritten, so **never
force-push this repository.**

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

`gross_pnl` and `costs` exist so the page can show what share of gross P&L the
frictions consumed. That number is the honest one: a strategy whose edge is
mostly eaten by costs is reporting the error bar on its cost model.

## Appending a day

```bash
python3 scripts/append_observation.py \
  --date 2026-09-01 --nav 100123.45 \
  --gross-pnl 150.00 --costs 26.55 --positions 4 --mode paper
```

The script validates before writing and refuses to modify or reorder anything
that already exists. Add `--commit` to have it create the commit for you.

To record a transition to real capital:

```bash
python3 scripts/append_observation.py --mode-change live --date 2027-03-01 \
  --note "Funded with real capital."
```

## Statistics the page derives

Computed in `assets/js/track-record.js` from the returns implied by `nav`:

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

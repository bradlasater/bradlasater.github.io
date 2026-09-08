# Published diagnostics

One JSON file per published report. The filename becomes the URL:
`coverage.json` renders to `/vol/evidence/coverage.html`.

These are the ingest box's own outputs, copied in verbatim under `report`.
On the box, `coverage_audit` writes `_meta/coverage.json` and `drift_check`
writes `_meta/drift_check.json`. Publishing one here is a deliberate act of
copying it in — nothing exports automatically, and nothing is invented. A
component with no report shows its next acceptance test instead of a number.

## Shape

```json
{
  "schema_version": 1,
  "title": "Daily pricing canary",
  "summary": "One sentence that stands alone; becomes the meta description.",
  "component": "pricing",
  "data_timestamp": "2026-09-05T20:40:00+00:00",
  "input_type": "last_trade_else_day_close",
  "code_version": "13985c5",
  "known_limitations": [
    "Put-call parity is skipped whenever either leg carries a last-trade price."
  ],
  "report": { }
}
```

| Field | Rule |
|---|---|
| `component` | Must be an `id` in `../components.json` |
| `data_timestamp` | ISO 8601 **with a timezone offset**, not in the future |
| `input_type` | One of `last_trade_else_day_close`, `day_bars`, `nbbo_mid`, `mixed` |
| `code_version` | A `Crack-the-Sky` commit SHA |
| `known_limitations` | Non-empty list. What the report does *not* establish |
| `report` | Non-empty object. The job's output, unreshaped |

`input_type` is the field that earns its place. With no option NBBO
entitlement, every analytic this project produces comes from traded prices;
a reader who assumed a quote midpoint would draw a different conclusion from
an identical-looking number.

The build refuses on a missing or malformed envelope, an unknown component, a
naive or future timestamp, an empty limitations list, or an unrecognised key.

## Adding one

```bash
cp /path/from/box/_meta/drift_check.json /tmp/r.json     # then wrap it
$EDITOR data/evidence/pricing-validation.json
python3 scripts/build_site.py
```

Withdrawing a report means deleting its JSON; the next build removes the page.

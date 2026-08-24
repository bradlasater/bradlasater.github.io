# bradlasater.com

Personal site for Brad Lasater, published at <https://bradlasater.com>. Static
HTML and CSS with two small vanilla-JS files, served by GitHub Pages from the
`main` branch at the repository root.

Its purpose is narrow: it is a recruiting instrument aimed at quantitative
finance roles, built around an end-to-end systematic volatility research and
execution platform — Phase 1 trades defined-risk SPX and XSP structures at
roughly 7–45 days to expiry — and, more importantly, the research process
behind it.

---

## Local development

```bash
python3 -m http.server 8000     # from the repository root
# then open http://localhost:8000
```

**Opening `index.html` over `file://` will not work.** Every stylesheet, script
and image path is root-relative, and `assets/js/track-record.js` uses `fetch()`,
which the `file://` origin blocks. Always go through a local server.

There is no bundler, no package manager and no dependency install step.

## Publishing

Push to `main`. GitHub Pages rebuilds automatically, typically within a minute.
There is no deploy script and no build artefact to commit beyond what
`scripts/build_site.py` generates (see below).

## Project structure

| Path | Purpose |
|---|---|
| `index.html` | Home — positioning, selected experience, capabilities, contact |
| `cv.html` | Full CV, including military and teaching service |
| `vol/index.html` | Volatility system overview: premise, architecture with per-stage status, sources |
| `vol/methodology.html` | The evaluation protocol, written before results exist |
| `vol/track-record.html` | Build status and live out-of-sample record (see below) |
| `log/index.html` | Research log index |
| `404.html` | Custom 404 (`noindex`) |
| `assets/css/site.css` | The entire design system — dark-only, OKLCH tokens |
| `assets/js/track-record.js` | Computes and renders every track-record statistic |
| `assets/js/analytics.js` | GoatCounter loader (see setup below) |
| `data/track-record.json` | The append-only track record. See `data/SCHEMA.md` |
| `scripts/append_observation.py` | Appends one day to the record |
| `scripts/validate_track_record.py` | Structural + append-only validation |
| `scripts/build_site.py` | Generates log entry pages and derived metadata |
| `content/log/*.html` | Hand-authored research-log entry fragments |

Only `vol/track-record.html` loads `track-record.js`; every page loads
`analytics.js`.

Data flows one way:
`append_observation.py` → `data/track-record.json` → CI validation →
`track-record.js` fetches it in the browser → `vol/track-record.html` renders.

Nothing is precomputed. The page derives its statistics client-side so that it
cannot disagree with the data file behind it.

---

## The append-only invariant

**This is the most important thing in the repository.** The track record's
entire value is that it cannot be revised after the fact, and the site says so
publicly on `/vol/track-record.html`. Three mechanisms back that claim:

1. Each observation lands as its own dated commit. The git history *is* the
   timestamp trail.
2. CI (`.github/workflows/validate-track-record.yml`) walks every commit in a
   push and fails the build if any published observation, `mode_changes` entry,
   or immutable metadata field was modified, removed or reordered.
3. Force-pushes are rejected by that workflow.

### Rules

- **Never force-push this repository.** Rewriting history destroys the evidence
  the whole record rests on, and no file-level check can detect it afterwards.
- **Never rebase or amend a commit that published an observation.**
- Append only. If a published number was wrong, append a correction and write
  up what happened — do not edit the original.

`periods_per_year` is frozen once the first observation exists, because it
rescales the annualised return, volatility, Sharpe, PSR and MinTRL all at once.

### Appending a day

```bash
python3 scripts/append_observation.py \
    --date 2026-09-01 --nav 100123.45 \
    --gross-pnl 150.00 --costs 26.55 --positions 4 --mode paper --commit
```

Run it from the repository root. It validates the whole document before writing,
refuses out-of-order and future-dated entries, and with `--commit` commits only
`data/track-record.json`.

Recording the move from paper to real capital:

```bash
python3 scripts/append_observation.py --mode-change live \
    --date 2027-03-01 --note "Funded with real capital."
```

**After a transition, every subsequent append must pass `--mode live`
explicitly.** The transition record and each observation's `mode` are
cross-checked; if they disagree, validation fails.

Full field reference: [`data/SCHEMA.md`](data/SCHEMA.md).

---

## Analytics — one open setup step

`assets/js/analytics.js` uses [GoatCounter](https://www.goatcounter.com): no
cookies, no consent banner, honours Do Not Track, and skips localhost.

It is **currently inert.** `CODE` is an empty string, so the script returns
before injecting anything — no pageviews and no events are being recorded. To
activate it, create a site at goatcounter.com and set `CODE` to your subdomain:

```js
var CODE = "bradlasater";   // for https://bradlasater.goatcounter.com
```

It also records `mailto:` clicks as a `contact-email` event and cross-origin
clicks as `outbound-<host>` — the two conversions that actually matter here.

---

## Infrastructure

Verified state, recorded here because nothing else in the repository captures it.

**Hosting.** GitHub Pages, legacy build, source `main` / root. `CNAME` contains
`bradlasater.com`; keep that file — Pages can drop the custom domain on a
rebuild without it.

**DNS** (registrar and nameservers: Porkbun):

- Apex `A` → the four GitHub Pages addresses
  (`185.199.108–111.153`)
- `www` `CNAME` → `bradlasater.github.io`
- HTTPS enforced; certificate covers apex and `www`

`www` and `bradlasater.github.io` both 301 to the apex, matching every
`<link rel="canonical">`.

**Email.** `brad@bradlasater.com` is deliverable — MX points at Porkbun
forwarding (`fwd1`/`fwd2.porkbun.com`) with a specific `brad@` alias, confirmed
by SMTP probe rather than assumed. Outbound appears to go via Zoho: SPF and
DKIM (`zmail._domainkey`) are both present.

**One real gap: there is no DMARC record.** Without
`_dmarc.bradlasater.com`, receivers have no published policy for SPF/DKIM
failures, which makes outbound mail to Gmail and Outlook more likely to be
filtered — i.e. mail to recruiters. Start monitor-only:

```
_dmarc.bradlasater.com  TXT  "v=DMARC1; p=none; rua=mailto:brad@bradlasater.com"
```

Tighten to `p=quarantine` after reviewing reports. The domain is also not
GitHub domain-verified (takeover protection); adding the
`_github-pages-challenge-bradlasater` TXT record would close that.

---

## Conventions

- **British spelling** in prose (`optimisation`, `modelling`). The deliberate
  exceptions are JSON-LD and the third-person "Who is Brad Lasater?" block on
  the homepage, which use American spelling for search reasons.
- The nav is hand-maintained in seven HTML files *and* in the `nav()` function
  of `scripts/build_site.py`. Changing it means editing both, or generated log
  pages will drift from the static ones.
- `aria-current="page"` marks the page you are on; `aria-current="true"` marks
  an ancestor section (used on `vol/methodology.html`, whose nav highlights
  `/vol/` but navigates away).
- Research-log entries are hand-authored fragments in `content/log/`; see
  `content/log/TEMPLATE.html.example`. Each follows the same four-part shape:
  **Expected · Observed · Diagnosis · Changed as a result.**
- Statistical conventions for the track record are documented at the top of
  `assets/js/track-record.js` — read them before changing any formula.

Outstanding work is tracked in [`ROADMAP.md`](ROADMAP.md).

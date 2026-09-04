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

### Pre-commit hook (one-time setup)

A pre-commit hook auto-runs `scripts/build_site.py` before every commit so
derived files stay in sync.  To activate it:

```bash
pip install pre-commit
pre-commit install
```

After that, `python3 scripts/build_site.py` runs automatically on each commit,
reducing the chance of the CI `check` job failing because derived files are out
of sync. If the hook rewrites files, re-stage them and re-run the commit so the
generated changes are included.

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
| `handbook/` | System handbook, synced from `data_ingest_infra` (see below) |
| `404.html` | Custom 404 (`noindex`) |
| `assets/css/site.css` | The entire design system — dark-only, OKLCH tokens |
| `assets/js/track-record.js` | Computes and renders every track-record statistic |
| `assets/css/handbook-chrome.css` | Site-owned interaction layer loaded last on every handbook page |
| `assets/js/analytics.js` | GoatCounter loader (see setup below) |
| `data/track-record.json` | The append-only track record. See `data/SCHEMA.md` |
| `scripts/append_observation.py` | Appends one day to the record |
| `scripts/validate_track_record.py` | Structural + append-only validation |
| `scripts/build_site.py` | Generates log entry pages and derived metadata |
| `scripts/sync_docs.py` | Copies the handbook in from `data_ingest_infra` |
| `content/log/*.html` | Hand-authored research-log entry fragments |

Only `vol/track-record.html` loads `track-record.js`; every page loads
`analytics.js`.

Data flows one way:
`append_observation.py` → `data/track-record.json` → CI validation →
`track-record.js` fetches it in the browser → `vol/track-record.html` renders.

Nothing is precomputed. The page derives its statistics client-side so that it
cannot disagree with the data file behind it.

---

## The handbook (`/handbook/`)

`handbook/` is the system handbook for the ingest and pricing box, published
here under the **Handbook** nav tab. It is **derived, not authored**: the source
of truth is `docs/` in the private `data_ingest_infra` repository, where it sits
next to the code it describes so the two are edited in the same commit. Copying
it here rather than moving it keeps that property.

Everything in `handbook/` is overwritten on each sync, so **never edit a file in
it**. Edit the source repository, then:

```bash
python3 scripts/sync_docs.py           # writes handbook/, deletes what is gone
python3 scripts/sync_docs.py --check   # exit 1 if handbook/ is stale
python3 scripts/build_site.py          # picks the pages up in sitemap.xml
```

The sync expects `data_ingest_infra` as a sibling of this repository; pass
`--source DIR` if it lives elsewhere. It is **not** wired into the pre-commit
hook or CI, and deliberately so: neither has the private repository, so neither
can tell a stale copy from a current one. `--check` exits 0 when the source is
absent for that reason — it reports drift it can see, and cannot be trusted to
prove there is none. Publishing a handbook change is a decision, so it stays a
command you run.

The handbook's layout is its own (a sidebar docs design), but its theme is the
site's: at publish time the sync rewrites every synced file's palette, font
names, and font stylesheet into the site's OKLCH tokens and Inter / JetBrains
Mono / Newsreader faces (`COLOR_MAP` / `FONT_MAP` in `scripts/sync_docs.py`),
and it fails loudly on any colour or font it does not recognise rather than
letting a page drift back into the source theme. Interaction behaviour that
string replacement cannot express — underlined content links, selection
colour, corner radii — lives in `assets/css/handbook-chrome.css`, which is
loaded last on every handbook page and is never touched by the sync. What else
the sync adds to each page is only what a file needs to become a public URL: a
canonical link, favicon and robots directives, Open Graph tags, the site's
title suffix, and one link back to the homepage.

`scripts/build_site.py` discovers handbook pages by globbing rather than from a
list, so a page added upstream reaches `sitemap.xml` on the next sync with no
second edit here. It never writes into `handbook/`.

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
3. `main` carries branch protection: force-pushes and deletion are disabled,
   enforced for admins. The workflow's `github.event.forced` check is a second
   layer for the paths it watches — it is path-filtered, so a force-push that
   left the watched files untouched would fire no run, and no file-level check
   can detect a rewrite after the fact. The branch rule is the durable guard.

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

## Analytics

`assets/js/analytics.js` uses [GoatCounter](https://www.goatcounter.com): no
cookies, no consent banner, honours Do Not Track and Global Privacy Control,
and skips localhost. It is **live** — `CODE` is set:

```js
var CODE = "bradlasater";   // for https://bradlasater.goatcounter.com
```

It records pageviews, `mailto:` clicks as a `contact-email` event, and
cross-origin clicks as `outbound-<host>` — the two conversions that actually
matter here.

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

**Email.** Inbound mail for `brad@bradlasater.com` is hosted on Zoho Mail —
that address is the primary mailbox there, and the domain is verified. MX
points at Zoho (`10 mx.zoho.com`, `20 mx2.zoho.com`, `50 mx3.zoho.com`), not
Porkbun forwarding. SPF is
`v=spf1 include:zohomail.com include:_spf.porkbun.com ~all`; DKIM
(`zmail._domainkey`) is published.

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
  exceptions are JSON-LD, which uses American spelling for search reasons, and
  proper nouns such as the "Stochastic Multi-Objective Optimization" coursework
  title, which is spelled as the institution spells it.
- The homepage no longer carries the third-person "Who is Brad Lasater?" block
  that used to sit above the contact section; it repeated the introduction and
  the experience list without adding signal. The third-person summary that an
  answer engine needs still exists in the JSON-LD `Person` description and in
  `llms.txt`, which is where a retrieval fetcher looks first anyway.
- The nav is hand-maintained in seven HTML files *and* in the `nav()` function
  of `scripts/build_site.py`. Changing it means editing both, or generated log
  pages will drift from the static ones. Handbook pages are the exception: they
  come from another repository and keep their own sidebar, so they carry a link
  back to the site rather than the site nav.
- The header stacks below `56rem`. That breakpoint is a measurement, not a
  round number: brand plus seven items fit at 880px and wrap at 850px, so it
  sits just above the measured threshold. A wrapped bar strands the GitHub rule
  on its own line and reads as broken, so re-measure in a browser whenever a
  nav item is added or renamed.
- The GitHub link closes the nav in its own `.site-nav__ext` item. It leaves the
  site, so it never takes `aria-current` and is separated by a rule rather than
  reading as one more page. It is in the header because the homepage bio is long
  enough to push a hero button row under the fold on a laptop.
- `aria-current="page"` marks the page you are on; `aria-current="true"` marks
  an ancestor section (used on `vol/methodology.html`, whose nav highlights
  `/vol/` but navigates away).
- Research-log entries are hand-authored fragments in `content/log/`; see
  `content/log/TEMPLATE.html.example`. Each follows the same four-part shape:
  **Expected · Observed · Diagnosis · Changed as a result.**
- Statistical conventions for the track record are documented at the top of
  `assets/js/track-record.js` — read them before changing any formula.

Outstanding work is tracked in [`ROADMAP.md`](ROADMAP.md).

# bradlasater.com

Personal site for Brad Lasater, published at <https://bradlasater.com>. Static
HTML and CSS with two small vanilla-JS files, served by GitHub Pages from the
`main` branch at the repository root.

Its purpose is narrow: it is a recruiting instrument aimed at quantitative
finance roles, built around an end-to-end systematic volatility research and
execution platform — Phase 1 trades defined-risk SPY and SPX/SPXW structures
at roughly 5–45 days to expiry, with VIX options captured for the term
structure — and, more importantly, the research process behind it.

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
| `vol/build-status.html` | The engineering record: pipeline, contracts, evidence, next acceptance test |
| `vol/methodology.html` | The evaluation protocol, written before results exist |
| `vol/track-record.html` | The live out-of-sample trading record (see below) |
| `log/index.html` | Research log index |
| `handbook/` | System handbook, synced from `data_ingest_infra` (see below) |
| `docs/` | Local HTML mirrors of notes, audits, and the roadmap. Unpublished. |
| `notes/` | Working notes and peer research. Unpublished. |
| `404.html` | Custom 404 (`noindex`) |
| `assets/css/site.css` | The entire design system — dark-only, OKLCH tokens |
| `assets/js/track-record.js` | Computes and renders every track-record statistic |
| `assets/css/handbook-chrome.css` | Site-owned interaction layer loaded last on every handbook page |
| `assets/js/analytics.js` | GoatCounter loader (see setup below) |
| `data/components.json` | Implementation status of every system stage. See below |
| `data/evidence/*.json` | Published diagnostic reports, one per file. See below |
| `data/track-record.json` | The append-only track record. See `data/SCHEMA.md` |
| `scripts/append_observation.py` | Appends one day to the record |
| `scripts/validate_track_record.py` | Structural + append-only validation |
| `scripts/build_site.py` | Generates log entry pages, status surfaces, and derived metadata |
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

## The component manifest (`data/components.json`)

**One file decides what the site says is built.** `data/components.json` holds
one entry per stage of the volatility system, and `scripts/build_site.py`
renders it into the homepage status strip and the architecture grid on `/vol/`,
between `BUILD:STATUS-STRIP` and `BUILD:ARCHITECTURE` markers. Nothing between
those markers is hand-edited; the build overwrites it.

This exists because of a specific failure. In September 2026 the public pages
were edited to claim a raw SVI surface fit running over the archive. No such
code was ever written — `pricing/__init__.py` in the system repository opens
"Not a surface", and `handbook/not-built.html` said plainly that there was no
smile fit and no interpolator. The handbook was right and was not updated,
because it lives in another repository; the public pages were wrong and were.
Both surfaces now render from one manifest, so a status is changed in one place
or not at all.

Each component carries four states — `operational`,
`implemented_unvalidated`, `in_progress`, `planned` — and, separately,
`current_behaviour` and `design_intent`. **Both text fields are required.** A
badge on its own cannot distinguish a stage that runs from a stage that is
merely specified, and that ambiguity is exactly what produced the SVI claim.
`blocked_by` is optional and reserved for what an external constraint prevents
(the missing option NBBO entitlement, mostly) rather than what is simply
unwritten — a reader judging the work needs to tell those apart.

`next_acceptance` is a test, not a task: what would have to be demonstrated for
the stage to advance. `evidence` may name an artifact before it exists; links
to site-local pages that are not yet on disk are dropped at render time rather
than shipped as 404s.

The loader validates hard and fails the build on a bad manifest — unknown
state, missing or empty text field, misspelt key, duplicate `id` or `order`,
a `validated_on` that is malformed, impossible, or in the future. A typo must
not silently render as an absent field.

---

## Published diagnostics (`data/evidence/`)

One JSON file per published report, rendered to `/vol/evidence/<slug>.html` and
listed on the build-status page. The filename is the URL.

**These are the ingest box's own outputs, copied in verbatim under `report`.**
`coverage_audit` writes `_meta/coverage.json` and `drift_check` writes
`_meta/drift_check.json` on the box; publishing one here is a deliberate act of
copying it in, not an automatic export. Nothing is invented: a component with no
report shows its next acceptance test instead of a number, the same rule
`/vol/track-record.html` already follows.

Every file needs a provenance envelope, and the build refuses without it:

| Field | Why it is required |
|---|---|
| `data_timestamp` | A diagnostic without a date is not checkable |
| `input_type` | With no NBBO entitlement every analytic here comes from traded prices; a reader who assumed a quote midpoint would draw the wrong conclusion from an identical-looking number |
| `code_version` | A `Crack-the-Sky` commit SHA, so the number can be traced to the code that produced it |
| `known_limitations` | A non-empty list of what the report does **not** establish |

`component` must name a stage in `data/components.json`, so a report cannot be
orphaned from the thing it is evidence for.

The `report` object is rendered generically rather than by a per-report
template, because these payloads are the box's own dataclasses and will gain
fields without asking this renderer first — a template that knew only today's
fields would silently drop tomorrow's, which on a page whose purpose is
checkability is the one failure that matters.

Adding or withdrawing a report converges in a single build: the sitemap, the
component table's evidence links, and the generated page all derive from the
source list rather than from what happens to be on disk mid-pass. Withdrawing a
report deletes its page.

### Not yet done

The term-structure diagnostic needs a chart showing residuals, rejected
observations and failure cases. `assets/js/track-record.js` already contains a
dependency-free SVG chart engine that should be extracted to a shared
`assets/js/chart.js` and used by both. That extraction is deliberately **not**
done yet: it is a pure refactor of working, carefully-commented code that has no
automated test, and doing it before there is a second consumer to validate
against risks breaking the one page that currently depends on it. Extract it
when the term-structure report exists.

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

**DMARC is published, monitor-only** (live 2026-09-04):

```
_dmarc.bradlasater.com  TXT  "v=DMARC1; p=none; rua=mailto:brad@bradlasater.com"
```

Receivers now have a published policy for SPF/DKIM alignment failures, and
send aggregate reports to that address. `p=none` changes no delivery
behaviour — it buys visibility before enforcement, so a legitimate mail
stream that fails alignment shows up in a report rather than in a bounce.
Tighten to `p=quarantine` once a few weeks of reports come back clean.

**One remaining gap:** the domain is not GitHub domain-verified (takeover
protection); adding the `_github-pages-challenge-bradlasater` TXT record
would close that.

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
- **The nav and footer are generated, not hand-maintained.** `NAV_ITEMS`,
  `SECTION_ITEMS` and `site_footer()` in `scripts/build_site.py` are the only
  definitions; `build_site.py` injects them into every page between
  `BUILD:SITE-NAV`, `BUILD:SECTION-NAV` and `BUILD:SITE-FOOTER` markers, and
  `CHROME_PAGES` maps each page to the nav state it should show. This replaced
  a nav copy-pasted into seven files plus a second copy in `nav()`, and five
  different footers across seven pages. Handbook pages are still the exception:
  they come from another repository and keep their own sidebar, so they carry a
  link back to the site rather than the site nav.
- The primary bar is five items. Build Status, the evaluation protocol, the
  trading record and the handbook live in the `/vol/` **section bar** instead,
  because they are parts of the volatility system rather than peers of it.
- The header stacks below `46rem`. That breakpoint is a measurement, not a
  round number: brand plus the current five items fit at 528px and wrap at
  527px, so it sits just above the measured threshold with room for a font that
  loads late with wider metrics. It was `56rem` when the bar carried seven
  items. A wrapped bar strands the GitHub rule on its own line and reads as
  broken, so re-measure in a browser whenever a nav item is added or renamed.
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

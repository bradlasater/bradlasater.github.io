# notes/

Working notes. Since 2026-09-03 these are **mirrored on the published site**
under `/docs/` — a deliberate reversal of the original "never publish the
candid stuff" stance: the research below argues that showing the work,
gaps included, is the stronger signal. The Markdown here remains the source
of truth; edit it, then re-sync the mirror page under `docs/`.

## Start here

**The actionable list is [`../ROADMAP.md`](../ROADMAP.md)** — the survey worklist
that used to live here has been merged into it, alongside the items derived from
the codebase itself, so there is one prioritised list rather than two competing
ones. The files below are the evidence behind it.

| File | What it is |
|---|---|
| `quant-site-playbook.html` | The readable compiled version. Open in a browser. The survey findings in full, plus the post template, phrasing conventions, and the reference-site tables. |
| `baseline-audit.md` | State of the site as of 2026-08-23, before any of this landed. What was already strong, and what the gaps were. |
| `audit-2026-09-02.md` | The 2026-09-02 full-repo audit: 50 deferred improvements plus the docs-mirror addendum, grouped and prioritised. |

## Raw research

Five parallel web crawls run 2026-08-23. Every URL cited in these reports was
loaded and inspected directly; sites that 404'd, 403'd, or turned out to be
link-in-bio pages are reported as such rather than quietly dropped.

| File | Lane | Sites |
|---|---|---|
| `research/01-prop-hft.md` | Prop / market-making / HFT — Jane Street, HRT, Citadel Securities, Jump, SIG, Optiver, IMC, DRW, Tower, Headlands, Radix, Arrowstreet, Akuna | 20 |
| `research/02-hedge-funds.md` | Multi-strategy and systematic funds — Two Sigma, D. E. Shaw, Millennium, Cubist, Balyasny, Squarepoint, WorldQuant, AQR, PDT, Voleon | 21 |
| `research/03-vol-practitioners.md` | Volatility and derivatives practitioners who publish — Sinclair, Carver, Kinlay, Moontower, Robot Wealth, Allocate Smartly, Quantocracy | 22 |
| `research/04-switchers-and-hiring.md` | Career switchers into quant, **plus the hiring-side evidence** — firm career pages, named practitioners, recruiters | 16 + 20 sources |
| `research/05-discovery-and-build.md` | Breadth discovery via GitHub API / curated lists / arXiv, plus a raw-HTML technical teardown of the strongest sites | 20 |

Roughly 80 distinct personal sites after de-duplication across lanes.

### Known gaps in the research

- `reddit.com` and `quantnet.com` were inaccessible to the crawlers, so **no forum
  opinion is cited anywhere.** The hiring-side lane is weighted toward
  firm-official statements and named practitioners instead, which is the stronger
  evidence base but a narrower one.
- Gordon Ritter's page (`cims.nyu.edu/~ritter/`) returned 403 on every attempt and
  was excluded rather than reported second-hand.
- A few reference sites are dormant (2–3.5 years stale) or dead. Those are
  reported as cautionary findings, not as models — see the dead-domain note in
  `research/05-discovery-and-build.md`.

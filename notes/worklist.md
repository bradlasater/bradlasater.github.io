# Site worklist — from the peer survey

Compiled 2026-08-23 from five parallel web crawls covering ~80 quant practitioners'
personal sites and 20+ hiring-side sources. Full evidence in `research/`; the
readable version is `quant-site-playbook.html` (open it in a browser).

Ordered by signal per unit of effort, judged against one question: **does a quant
hiring manager or a specialist recruiter find this more convincing?**

---

## The frame this list is built on

The hiring-side evidence says a personal site matters less than it feels like it
should. Giuseppe Paleologo — Global Head of QR at Balyasny, ex-HRT, Millennium,
Citadel, self-described screener of "a couple thousand résumés" — published ~15
pages of buy-side quant career advice in December 2025 that mentions personal
websites, blogs, GitHub, and side projects **zero times**. Jane Street's
interviewing page and FAQ, HRT's interviewing post, and the Two Sigma, D. E. Shaw,
SIG, and Optiver careers pages all return the same zero-mention result. The most
project-favourable source found still concedes projects are viewed as "nothing
more than a 'show of interest'." A recruiting-side source gives the honest
calibration: GitHub gets checked "especially when deciding between similar
candidates."

So the site is **not** lead generation. It is a *defensibility instrument*: the
thing that converts a warm reader from "plausible" to "worth an hour", and the
thing that makes a claim survive twenty minutes of probing in an interview. Its
highest-leverage content is not the best strategy found — it is documented
evidence of knowing how easily one could have fooled oneself, and what was done
about it.

That is the one thing a career switcher can offer that a strong résumé cannot,
and it is what the evaluation protocol already commits to.

Meanwhile the switcher door is genuinely open, firm-official: Jane Street's
"Problem-solving mindset: required. Finance background: optional."; Two Sigma's
"more than half of Two Sigma's employees come from outside the finance industry"
alongside a posted qualification reading "Performed an in-depth research project,
examining real-world data." D. E. Shaw's posted NYC quantitative analyst base is
$275k (UG/MS) / $300k (PhD), so the $250k target is conservative.

---

## A. Corrections to what is already shipped

Small, fast, and each one is currently costing something.

- [ ] **Remove the `TODO(brad)` comment from `index.html`.** It is visible in
      view-source and reads as a public note-to-self admitting the "roughly 60%"
      Ticketmaster claim is unqualified. Then resolve the underlying issue: name
      the error metric and the baseline, or cut the number. An unqualified
      percentage is the first thing a quant interviewer pushes on.
- [ ] **Set the GoatCounter `CODE` in `assets/js/analytics.js`.** It is empty, so
      nothing is being measured and there is no way to know whether any of this
      works.
- [ ] **Fix the GitHub profile.** No bio, no location, no website field, no
      profile README, missing repo descriptions, and two near-duplicate repos
      (`data_ingest_infra` and `data_ingestion_infra`). The site says "documented
      in the open" and links "Source" to a bare profile. Add bio,
      `location: New York, NY`, `blog: bradlasater.com`, a README linking the
      system and the log, descriptions everywhere, and delete the duplicate.
      *Why this specifically:* the highest-yield way the crawlers found this
      entire cohort was the GitHub Users API filtered by bio text and
      `location:"New York"` — a query a technical recruiter genuinely runs.
- [ ] **Auto-renew and registrar-lock `bradlasater.com`, and never retire the
      `bradlasater.github.io` fallback.** Two reference sites in the survey have
      already been lost this way: `frouah.com` (the standard free Heston
      reference) and `kthohr.com` (an NYU PhD's site) both lapsed and now serve
      online-casino spam under their owners' names. A lapsed domain does not go
      quiet — it gets bought *because* it has inbound links.

---

## B. Tier 1 — evidence content

This is where the entire gap is. The site currently promises process artifacts
and delivers zero: the research log has no entries, the track record has no
observations, and there is no chart, no equation, and no code anywhere on it.
Every claim is prospective.

- [ ] **Promote post-mortems to a named top-level nav item.** Ranked the #1
      signal independently by two lanes, and *nobody* in the prop/HFT lane has
      one. Mark Best's line is the register: "Almost all of what I have looked at
      has been a dead end… most research ends up in the bin." Nobody fabricating
      results writes that sentence.
- [ ] **Add a literal `## What this shows and does not show` heading to the post
      template**, with every bullet beginning "It does not show that…". Jonathan
      Kinlay runs it as a fixed section in every article, alongside a second
      fixed section named "Failure modes I actually saw". Highest trust-per-word
      content available.
- [ ] **Ship a replication as the first post.** A named paper, cited, with the
      delta reported honestly — Dean Markwick's model: "the results are not as
      conclusive as the original paper." It proves competence with zero risk of
      an unfalsifiable claim, and it ships *before* the system has results of its
      own. Candidates: Bakshi–Kapadia–Madan on the variance risk premium, or
      Carr–Madan variance-swap replication against real option chains.
- [ ] **Write up the infrastructure.** Structured logging, daily reconciliation,
      silent-failure alerting, the append-only track-record validator. It proves
      engineering seriousness, is fully verifiable by a reader, and carries zero
      alpha and zero claim risk. Four separate people in the prop/HFT lane lean
      on exactly this. It is publishable *now*, before any results exist.
- [ ] **Add a standing "this analysis may contain errors" disclaimer.** The most
      transferable single artifact in the survey, three clauses long (Kipp
      Rogers): who I am · this does not represent any employer's views · these
      are the products of analysis which may have errors · this is not investment
      advice. Pair it with a per-post invitation to point out what looks wrong,
      and add Carver's companion line — explicitly not regulated, not selling
      courses or signals.
- [ ] **Surface the running trial count as a live number.** The protocol already
      promises automatic logging of every configuration evaluated. A counter that
      only goes up is unfakeable, and nobody else in the survey has one. Without
      a trial count, a Sharpe is uninterpretable — and "out-of-sample" used as a
      magic word is itself a red flag (López de Prado: "It does not matter if the
      backtest is a walk-forward out-of-sample").
- [ ] **State data provenance everywhere.** Vendor, instruments, exact date
      range, how it was obtained, what had to be paid for or proxied, and what is
      wrong with it. The `data_ingest_infra` repo already says Polygon — put that
      on the site.
- [ ] **Publish a result where a named baseline wins.** HAR-RV, GARCH,
      implied-as-forecast, and naive short carry are already named in the
      protocol. Kinlay benchmarks his CNN against plain interpolation and reports
      that the gap is small and may not survive real data. That is the clearest
      tell separating real research from a backtest.
- [ ] **Extract one installable artifact.** An arbitrage-free SVI/SSVI fitter, or
      a deflated-Sharpe / PBO-CSCV implementation. Third-party adoption is
      unfakeable and IP-free — the best eleven words in the survey are Ties de
      Kok's "Officially integrated into Stata as of Stata 17."

---

## C. Positioning and structure

- [ ] **Move the market thesis above the biography on the homepage.** "Options
      are a market in forecasts. The trade is the forecast error." is already the
      right shape and is currently buried on `/vol/`. Artur Sepp — Risk
      Magazine's Quant of the Year 2024 — leads with "volatility regimes migrate
      across asset classes, and models that feel robust fail at the worst moment.
      I build frameworks designed to survive regime change." With no fund name to
      lead with, a falsifiable thesis is the only substitute, and the better
      asset because it is checkable.
- [ ] **Name the system, give it a repo and a version.** "The volatility system"
      cannot be cited, starred, or referenced by anyone else. Everyone credible in
      the survey has named artifacts — Sepp's ROSAA, López de Prado's purged CV
      and deflated Sharpe, Markwick's `HawkesProcesses.jl`.
- [ ] **Cut the capability tag clouds** (three groups, 26 tags). This is the
      flat-breadth pattern that destroys depth signal — the counterexample in the
      survey indexes eighteen research domains and is genuinely accomplished, yet
      a hiring manager scanning it cannot state what he does. Skills walls are
      also a named red flag: "interviewers will pick the most obscure item on
      your list."
- [ ] **Add `Code & Data` and `Post-mortems` as their own nav destinations.** The
      best information architecture found is Ties de Kok's — About / Research /
      Code & Data / Talks & Classes / Blog Posts / CV. One nav item per *kind of
      evidence*, so a reader jumps straight to the type they trust.
- [ ] **Put the finding, not the topic, in every log listing.** Assume 45 seconds
      and no clicks. Abdelmessih puts a one-line finding under each post title;
      Chinco's publication entries each carry a plain-language findings sentence.
- [ ] **State the IP boundary explicitly:** the vol system is built on personal
      time with purchased retail data and contains nothing from any employer.
      Signalling that you know where the line is *is itself* the signal that you
      can be trusted near proprietary information.
- [ ] **Tighten the bio to Sinclair's four-sentence shape:** years → what
      instruments → current seat → credentials and artifacts. No adjectives.
- [ ] **Group by theme once the log passes ~10 entries.** A chronological feed
      decays; a themed index compounds.

---

## D. Research-post craft

Apply when building the log entry template in `content/log/`.

- [ ] Byline and date on every entry. **Non-negotiable** — the Hull Tactical
      blog, where Euan Sinclair writes, is active and expert and carries no
      author attribution on any post. Unattributed research accrues to nobody.
- [ ] Numbered, captioned figures referenced in the prose — bold `Figure N.`
      label, hairline rules above and below, source line beneath.
- [ ] Booktabs tables: horizontal rules only. Vertical rules and zebra striping
      read as spreadsheet export, not analysis.
- [ ] Pre-rendered KaTeX at build time in `build_site.py`; ship `katex.min.css`
      only, self-hosted, one version, zero runtime math JS.
- [ ] Real author-year citations with anchor IDs. Cite specific results, not
      names — one correct reference to Bailey & López de Prado (2014) on the
      deflated Sharpe ratio beats "Sinclair and López de Prado" as influences.
- [ ] Code linked at an exact commit. Ranked ordering from the survey: linked
      repo > inline snippet > nothing > screenshot of code.
- [ ] Costs as specific numbers — bid/ask, exchange fees, delta-hedge slippage —
      quantified rather than waved at.
- [ ] Uncertainty on every headline number: `± SE`, CIs, medians and quartiles.

**Cadence warning:** three otherwise-credible reference sites in the survey are
2–3.5 years stale, which reads worse than having no research section at all. If
a cadence cannot be sustained, present a fixed set of finished pieces with no
dates implying a schedule.

---

## E. Track record

Rob Carver's twelve-year public series is the reference implementation: lead with
the worst number, state the accounting basis, decompose the P&L, benchmark
against named third-party indices *with correlations*, report costs as a
first-class result, show the full path, and admit discretionary errors by name.

Four things **even Carver does not do** — genuine differentiation, and all four
are already within reach given the append-only CI:

- [ ] **Live-vs-backtest overlay** — backtest curve, hard vertical line at
      go-live, realized path after it, gap quantified and attributed.
- [ ] **Confidence interval on the realized Sharpe** — `SE(SR) ≈ √((1+SR²/2)/N)`.
      On eighteen months it will be humiliatingly wide. Publishing it anyway is
      the single most credible thing that could go on that page.
- [ ] **Frozen, pre-registered definition** — "parameters were frozen on `<date>`;
      config hash `<hash>`; nothing below has been re-fit", verifiable against git
      history.
- [ ] **A change log** — every intervention, override, and parameter change,
      dated, with the reason. Silence about changes reads as changes concealed.

Frame the record around **out-of-sample discipline and divergence explanation,
not returns.** Not one person in the prop/HFT lane publishes an equity curve with
a headline Sharpe; in that population it reads as either a compliance violation
or an overfit. The only performance-shaped artifact anyone published was a
paper-vs-live reconciliation where the divergence was explained mechanistically
("the forecast takes about 200 ms to calculate on a new bar, thus in paper and
live the orders are sent later than in sim").

---

## F. Mechanics

- [x] `robots.txt` — shipped, with explicit AI-crawler allows.
- [x] `llms.txt` — shipped.
- [x] `feed.xml` + `sitemap.xml` generation — implemented in `build_site.py`;
      needs a build run and a commit.
- [x] JSON-LD `@graph` with a stable `Person` `@id` — shipped, and better
      structured data than 15 of the 20 sites teared down.
- [x] Per-entry log URLs — implemented; retrieval engines return passages, so an
      entry sharing a URL with twenty others cannot be cited on its own.
- [ ] **Add `/cv.pdf` alongside the HTML CV.** Recruiters forward PDFs and ATSs
      ingest PDFs; hiring managers read HTML. Ship both.
- [ ] **Self-host Inter / Newsreader / JetBrains Mono as woff2.** Google Fonts is
      a render-blocking third-party request.
- [ ] **Rewrite the meta description in the third person, naming the city and the
      specialty.** Gundersen's is the model: "Gregory Gundersen is a quantitative
      researcher in New York." Search engines surface it verbatim, so it is the
      one sentence a recruiter is most likely to read before deciding to click.
- [ ] **Submit the feed to Quantocracy** once there are 2–3 real entries. Still
      the best live aggregator in this niche, and the cheapest real distribution
      available — it puts the log in the same daily roundup as Carver and Kinlay.

**Stack verdict: stay put. Do not migrate.** Hand-written HTML on GitHub Pages
with a custom domain sits at or above the median of the entire survey and ahead
of nearly all of it on structured data. No Vercel, Astro, or Next.js appears
anywhere in the quant cohort; Jekyll dominates and Quarto is the one validated
notebook path (worth considering later for `/research/` alone if `.ipynb`
publishing is wanted — never site-wide).

---

## G. Decided against — do not relitigate

Each was checked across the whole sample. Recorded here so the decision does not
get re-opened on taste.

| Decision | Evidence |
|---|---|
| **Reconsider the dark-only design** | Across ~80 sites, essentially one ships a real dark toggle, and not one site in the hedge-fund lane implements dark mode at all. Every serious research site is light-only with a near-grayscale palette. The current dark-only system is the outlier. |
| **No JS charting library** | Exactly one site out of twenty uses interactive charts; it cost ten scripts and thirteen stylesheets on a landing page. Hand-rolled inline SVG is the better middle path and already beats both Plotly bloat and static PNGs. |
| **No framework migration** | None appear in the cohort. Migration would be pure motion. |
| **No hosted search** | The site is far too small; nobody at this scale has it. |
| **No further visual polish** | Three top-tier people's sites are not mobile-responsive at all, and one deliberately loads `non-responsive.css`. Peter Jäckel — author of "Let's Be Rational" — publishes hand-written HTML with IE6 workarounds. López de Prado's own homepage is a 357-byte `<frameset>` served from IIS. Visible design effort exceeding research effort is itself a negative signal. |

---

## Anti-patterns to check any new page against

1. A headline return or Sharpe with no trial count.
2. "Out-of-sample" used as a magic word, without pre-registration date, sample
   size, and error bars.
3. Implausible numbers.
4. Results with no cost, slippage, or capacity model.
5. No risk section — fatal for anything short-vol-adjacent.
6. "AI trading bot" framing, or model complexity presented as the achievement.
7. Skills walls and technology laundry lists.
8. Anything that cannot be defended for twenty minutes.
9. Vague accomplishment language.
10. Overclaiming the identity — "engineer building a volatility research program"
    is defensible; "quantitative researcher", on a site with no desk experience,
    invites a comparison that is lost.

**Delete on sight:** proven · consistently · robust (unqualified) · proprietary ·
cutting-edge · passionate about · significant returns · battle-tested ·
alpha-generating · any Sharpe stated without a period, a cost assumption, and an
interval.

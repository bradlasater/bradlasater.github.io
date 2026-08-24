# Roadmap

Outstanding work on bradlasater.com, ordered by signal per unit of effort against
one question: **does a quant hiring manager or a specialist recruiter find this
more convincing?**

Two evidence bases feed this list. Items marked *(survey)* come from a crawl of
~80 quant practitioners' personal sites and 20+ hiring-side sources — full
evidence in [`notes/research/`](notes/research/), readable version in
`notes/quant-site-playbook.html`. Items marked *(repo)* come from the codebase
itself: a `TODO`, an unconfigured value, an empty data file, or a promise the
site already makes in public.

---

## The frame

The hiring-side evidence says a personal site matters less than it feels like it
should. Giuseppe Paleologo — Global Head of QR at Balyasny, ex-HRT, Millennium,
Citadel, self-described screener of "a couple thousand résumés" — published ~15
pages of buy-side quant career advice in December 2025 mentioning personal
websites, blogs, GitHub, and side projects **zero times**. Jane Street's
interviewing page, HRT's interviewing post, and the Two Sigma, D. E. Shaw, SIG,
and Optiver careers pages all return the same zero-mention result. The most
project-favourable source still concedes projects are "nothing more than a 'show
of interest'." The honest recruiting-side calibration: GitHub gets checked
"especially when deciding between similar candidates."

So the site is **not** lead generation. It is a *defensibility instrument* — the
thing that converts a warm reader from "plausible" to "worth an hour", and that
makes a claim survive twenty minutes of probing. Its highest-leverage content is
not the best strategy found; it is documented evidence of knowing how easily one
could have fooled oneself, and what was done about it.

That is the one thing a career switcher can offer that a strong résumé cannot,
and it is what the evaluation protocol already commits to.

The switcher door is open, firm-official: Jane Street's "Problem-solving mindset:
required. Finance background: optional."; Two Sigma's "more than half of Two
Sigma's employees come from outside the finance industry", alongside a posted
qualification reading "Performed an in-depth research project, examining
real-world data." D. E. Shaw's posted NYC quantitative analyst base is $275k
(UG/MS) / $300k (PhD), so the $250k target is conservative.

---

## A. Now — cheap, and each currently costing something

- [ ] **Set the GoatCounter `CODE`** in `assets/js/analytics.js:18`. It is an
      empty string, so the script returns before injecting anything: zero
      pageviews, zero events, no way to know whether any of this works. *(repo)*
- [ ] **Resolve the "roughly 60%" claim.** The two `TODO(brad)` comments are
      deleted (they were shipping to view-source), but the number is still
      unqualified: it reads "forecast error ... against the incumbent baseline"
      with no metric named. Name the error metric (MAPE / WAPE / RMSE) in
      `index.html`, `cv.html`, and the CV opening paragraph, or cut the number.
      An unqualified percentage is the first thing a quant interviewer pushes
      on. *(repo + survey)*
- [ ] **Fix the GitHub profile.** Currently `bio: null`, `location: null`,
      `blog: ""`, `name: "bradlasater"`, no profile README, no repo descriptions,
      and two near-duplicate repos (`data_ingest_infra`, `data_ingestion_infra`).
      Set the real name, `location: New York, NY`, `blog: bradlasater.com`, a bio,
      a profile README linking the system and the log, descriptions everywhere,
      and delete the duplicate. *Why this specifically:* the highest-yield way the
      crawlers found this entire cohort was the GitHub Users API filtered by bio
      text and `location:"New York"` — a query technical recruiters genuinely
      run. *(survey)*
- [ ] **Point the "Source" buttons at `algo_vol_base`, not the bare profile.**
      Four buttons labelled *Source* / *GitHub* land on a profile page. The system
      repo exists. If it stays private, relabel the buttons rather than implying
      code a visitor cannot reach. *(repo)*
- [ ] **Add a DMARC record.** `_dmarc.bradlasater.com` does not exist. Mail *is*
      deliverable — verified by SMTP probe, with SPF and DKIM both present — so
      this is deliverability hardening, not an outage. But it makes outbound mail
      to Gmail and Outlook more likely to be filtered, and those are the
      recruiters. Start monitor-only:
      `v=DMARC1; p=none; rua=mailto:brad@bradlasater.com`. *(repo)*
- [ ] **Auto-renew and registrar-lock `bradlasater.com`; never retire the
      `bradlasater.github.io` fallback.** Two reference sites in the survey were
      lost exactly this way: `frouah.com` (the standard free Heston reference) and
      `kthohr.com` (an NYU PhD's site) both lapsed and now serve online-casino
      spam under their owners' names. A lapsed domain does not go quiet — it gets
      bought *because* it has inbound links. *(survey)*
- [ ] **Start the track record.** `data/track-record.json` has zero observations,
      so the page reads "Tracking has not started". Its value is a pure function
      of elapsed time, so the first append is worth more than any further
      polishing — and it exercises the charts, statistics and verdict banner
      against real data for the first time. *(repo)*

---

## B. Tier 1 — evidence content

This is where the entire gap is. The site promises process artifacts and
currently delivers none: the research log has no entries, the track record has no
observations, and there is no chart, equation, or code anywhere on it. Every
claim is prospective.

- [ ] **Promote post-mortems to a named top-level nav item.** Ranked the #1 signal
      independently by two research lanes, and *nobody* in the prop/HFT lane has
      one. Mark Best's line is the register: "Almost all of what I have looked at
      has been a dead end… most research ends up in the bin." Nobody fabricating
      results writes that sentence.
- [ ] **Add a literal `## What this shows and does not show` heading to the entry
      template**, every bullet beginning "It does not show that…". Jonathan Kinlay
      runs it as a fixed section in every article, alongside a second fixed
      section named "Failure modes I actually saw". Highest trust-per-word content
      available.
- [ ] **Ship a replication as the first post.** A named paper, cited, delta
      reported honestly — Dean Markwick's model: "the results are not as
      conclusive as the original paper." Proves competence with zero risk of an
      unfalsifiable claim, and ships *before* the system has results of its own.
      Candidates: Bakshi–Kapadia–Madan on the variance risk premium, or
      Carr–Madan variance-swap replication against real option chains.
- [ ] **Write up the infrastructure.** Structured logging, daily reconciliation,
      silent-failure alerting, the append-only track-record validator and the
      three bypasses it now closes. Proves engineering seriousness, is fully
      verifiable by a reader, carries zero alpha and zero claim risk, and is
      publishable *now*, before any results exist. Four separate people in the
      prop/HFT lane lean on exactly this.
- [ ] **Add a standing "this analysis may contain errors" disclaimer.** The most
      transferable single artifact in the survey, three clauses (Kipp Rogers): who
      I am · this does not represent any employer's views · these are products of
      analysis which may contain errors · this is not investment advice. Pair with
      a per-post invitation to point out what looks wrong, and Carver's companion
      line — explicitly not regulated, not selling courses or signals.
- [ ] **Surface the running trial count as a live number.** The protocol already
      promises automatic logging of every configuration evaluated. A counter that
      only goes up is unfakeable, and nobody else in the survey has one. Without a
      trial count a Sharpe is uninterpretable — and "out-of-sample" as a magic
      word is itself a red flag (López de Prado: "It does not matter if the
      backtest is a walk-forward out-of-sample").
- [ ] **State data provenance everywhere.** Vendor, instruments, exact date range,
      how obtained, what was paid for or proxied, and what is wrong with it. The
      `data_ingest_infra` repo already says Polygon — put that on the site.
- [ ] **Publish a result where a named baseline wins.** HAR-RV, GARCH,
      implied-as-forecast and naive short carry are already named in the protocol.
      Kinlay benchmarks his CNN against plain interpolation and reports the gap is
      small and may not survive real data. Clearest tell separating real research
      from a backtest.
- [ ] **Extract one installable artifact** — an arbitrage-free SVI/SSVI fitter, or
      a deflated-Sharpe / PBO-CSCV implementation. Third-party adoption is
      unfakeable and IP-free. Best eleven words in the survey: Ties de Kok's
      "Officially integrated into Stata as of Stata 17."
- [ ] **Trade-level logs.** `vol/methodology.html` promises "trade-level logs
      behind any live track record, so the reported statistics can be recomputed
      independently." The current schema stores daily aggregates only and cannot
      express this. Extend the data contract or soften the promise — do not leave
      it unbacked. *(repo)*

---

## C. Positioning and structure

- [ ] **Move the market thesis above the biography on the homepage.** "Options are
      a market in forecasts. The trade is the forecast error." is the right shape
      and is currently buried on `/vol/`. Artur Sepp — Risk Magazine's Quant of
      the Year 2024 — leads with "volatility regimes migrate across asset classes,
      and models that feel robust fail at the worst moment. I build frameworks
      designed to survive regime change." With no fund name to lead with, a
      falsifiable thesis is the only substitute, and the better asset because it
      is checkable.
- [ ] **Name the system; give it a repo and a version.** "The volatility system"
      cannot be cited, starred, or referenced. Everyone credible in the survey has
      named artifacts — Sepp's ROSAA, López de Prado's purged CV and deflated
      Sharpe, Markwick's `HawkesProcesses.jl`.
- [ ] **Cut the capability tag clouds** (three groups, 26 tags). This is the
      flat-breadth pattern that destroys depth signal. Skills walls are a named red
      flag: "interviewers will pick the most obscure item on your list."
      *Still outstanding after the 2026-08-24 repositioning pass.*
- [ ] **Add `Code & Data` and `Post-mortems` as nav destinations.** Best
      information architecture found is Ties de Kok's — About / Research / Code &
      Data / Talks & Classes / Blog Posts / CV. One nav item per *kind of
      evidence*, so a reader jumps to the type they trust.
- [ ] **Put the finding, not the topic, in every log listing.** Assume 45 seconds
      and no clicks. Abdelmessih puts a one-line finding under each post title.
- [ ] **State the IP boundary explicitly:** the vol system is built on personal
      time with purchased retail data and contains nothing from any employer.
      Signalling that you know where the line is *is itself* the signal that you
      can be trusted near proprietary information.
- [ ] **Tighten the bio to Sinclair's four-sentence shape:** years → instruments →
      current seat → credentials and artifacts. No adjectives.
- [ ] **Group the log by theme once it passes ~10 entries.** A chronological feed
      decays; a themed index compounds.

---

## D. Research-post craft

Apply when building the entry template in `content/log/`.

- [ ] Byline and date on every entry. **Non-negotiable** — the Hull Tactical blog,
      where Euan Sinclair writes, is active and expert and carries no author
      attribution on any post. Unattributed research accrues to nobody.
- [ ] Numbered, captioned figures referenced in prose — bold `Figure N.` label,
      hairline rules above and below, source line beneath.
- [ ] Booktabs tables: horizontal rules only. Vertical rules and zebra striping
      read as spreadsheet export, not analysis.
- [ ] Pre-rendered KaTeX at build time in `build_site.py`; ship `katex.min.css`
      only, self-hosted, one version, zero runtime math JS.
- [ ] Real author-year citations with anchor IDs. Cite specific results, not
      names — one correct reference to Bailey & López de Prado (2014) on the
      deflated Sharpe ratio beats "Sinclair and López de Prado" as influences.
- [ ] Code linked at an exact commit. Ranked: linked repo > inline snippet >
      nothing > screenshot of code.
- [ ] Costs as specific numbers — bid/ask, exchange fees, delta-hedge slippage.
- [ ] Uncertainty on every headline number: `± SE`, CIs, medians and quartiles.

**Cadence warning:** three otherwise-credible reference sites in the survey are
2–3.5 years stale, which reads worse than having no research section at all. If a
cadence cannot be sustained, present a fixed set of finished pieces with no dates
implying a schedule.

---

## E. Track record

Rob Carver's twelve-year public series is the reference implementation: lead with
the worst number, state the accounting basis, decompose the P&L, benchmark against
named third-party indices *with correlations*, report costs as a first-class
result, show the full path, and admit discretionary errors by name.

Four things **even Carver does not do** — genuine differentiation, all within
reach given the append-only CI:

- [ ] **Live-vs-backtest overlay** — backtest curve, hard vertical line at
      go-live, realized path after it, gap quantified and attributed.
- [ ] **Confidence interval on the realized Sharpe** — `SE(SR) ≈ √((1+SR²/2)/N)`.
      On eighteen months it will be humiliatingly wide. Publishing it anyway is the
      single most credible thing that could go on that page. (The page already
      reports MinTRL, which is the same instinct.)
- [ ] **Frozen, pre-registered definition** — "parameters were frozen on `<date>`;
      config hash `<hash>`; nothing below has been re-fit", verifiable against git
      history.
- [ ] **A change log** — every intervention, override and parameter change, dated,
      with the reason. Silence about changes reads as changes concealed.

Frame the record around **out-of-sample discipline and divergence explanation, not
returns.** Not one person in the prop/HFT lane publishes an equity curve with a
headline Sharpe; in that population it reads as either a compliance violation or
an overfit. The only performance-shaped artifact anyone published was a
paper-vs-live reconciliation where divergence was explained mechanistically ("the
forecast takes about 200 ms to calculate on a new bar, thus in paper and live the
orders are sent later than in sim").

---

## F. Mechanics and distribution

Shipped:

- [x] `robots.txt` with explicit AI-crawler allows, and `llms.txt`.
- [x] `feed.xml` + `sitemap.xml` generated by `build_site.py`, built and committed.
- [x] JSON-LD `@graph` with a stable `Person` `@id` — better structured data than
      15 of the 20 sites torn down.
- [x] Per-entry log URLs — retrieval engines return passages, so an entry sharing
      a URL with twenty others cannot be cited on its own.

Outstanding:

- [ ] **Add `/cv.pdf` alongside the HTML CV.** Recruiters forward PDFs and ATSs
      ingest PDFs; hiring managers read HTML. Ship both. (The print stylesheet now
      produces a correct printed CV, so this is close to free.)
- [ ] **Self-host Inter / Newsreader / JetBrains Mono as woff2.** Google Fonts is
      a render-blocking third-party request.
- [x] **Rewrite the meta description in the third person, naming city and
      specialty.** Done: the homepage description now opens "Brad Lasater is an
      applied scientist and machine-learning engineer in New York…", following
      Gundersen's model. `cv.html` and the Open Graph tags were brought into
      line at the same time.
- [ ] **Submit the feed to Quantocracy** once there are 2–3 real entries. Best live
      aggregator in this niche and the cheapest real distribution available — it
      puts the log in the same daily roundup as Carver and Kinlay.

**Stack verdict: stay put. Do not migrate.** Hand-written HTML on GitHub Pages
with a custom domain sits at or above the median of the entire survey and ahead of
nearly all of it on structured data. No Vercel, Astro, or Next.js appears anywhere
in the quant cohort; Jekyll dominates and Quarto is the one validated notebook path
(worth considering later for `/research/` alone if `.ipynb` publishing is wanted —
never site-wide).

---

## G. Code health

Low stakes, none visitor-facing, all *(repo)*.

- [ ] **Add a `.gitignore`.** None exists; only a global ignore rule keeps
      `.claude/settings.local.json` and scratch directories out of commits.
- [ ] **`ensure_ascii=False`** in `append_observation.py` — `json.dumps` re-escapes
      the em-dash in `strategy` to `—` on first write, producing a confusing
      diff on the very first observation commit.
- [ ] **Dead CSS:** `.btn__icon`, `.card--link`, `.stack-4`, `.stack-6`,
      `.measure`, the `.num`/`time` selector, and the `--c-surface-hover` custom
      property are unreferenced by any HTML or JS.
- [ ] **`[id] { scroll-margin-top: 6rem }`** applies to every element with an id,
      including each `<span>` stat readout — 28 ids on the track-record page
      against 1 used as a link target. Harmless now; will silently alter any future
      `scrollIntoView()`.
- [ ] **Breakpoint overlap:** `min-width: 44rem` and `max-width: 44rem` both match
      at exactly 704px. Benign today (disjoint properties), latent trap.
- [ ] **Repeated inline styles** — `style="font-size: var(--step-3); margin-top:
      var(--sp-3);"` verbatim on four pages. The only thing that would force a
      `style-src 'unsafe-inline'` relaxation if a CSP is added.
- [ ] **Footer drift** — five distinct footers across seven pages; `404.html`, the
      page most needing wayfinding, has the fewest links. Now that `build_site.py`
      exists, this wants a single partial. (Nav was consolidated this way already;
      note it lives in *two* places — the static HTML and `build_site.py:210` — so
      a nav change is still a two-place edit.)
- [ ] **Section landmark naming** — `index.html` and `vol/index.html` label nearly
      every section with `aria-labelledby`; `vol/methodology.html`,
      `vol/track-record.html` and `log/index.html` label none.

---

## H. Open decisions

Genuinely undecided, and not to be resolved on taste alone.

**Dark-only design.** The survey is blunt: across ~80 sites essentially one ships
a real dark toggle, not one site in the hedge-fund lane implements dark mode at
all, and every serious research site is light-only with a near-grayscale palette
— making the current dark-only system the outlier. Against that: dark was an
explicit design instruction, the palette is fully tokenised, and the contrast
measurements clear AA throughout (body 16.9:1, muted 6.7:1). This is a real
tension between measured peer convention and stated preference, and it is Brad's
call. A light-mode variant would mean redefining the token block under
`prefers-color-scheme`, not a rewrite.

---

## I. Decided against — do not relitigate

| Decision | Evidence |
|---|---|
| **No JS charting library** | Exactly one site out of twenty uses interactive charts; it cost ten scripts and thirteen stylesheets on a landing page. Hand-rolled inline SVG beats both Plotly bloat and static PNGs. |
| **No framework migration** | None appear in the cohort. Migration would be pure motion. |
| **No hosted search** | The site is far too small; nobody at this scale has it. |
| **No further visual polish** | Three top-tier people's sites are not mobile-responsive at all, and one deliberately loads `non-responsive.css`. Peter Jäckel — author of "Let's Be Rational" — publishes hand-written HTML with IE6 workarounds. López de Prado's own homepage is a 357-byte `<frameset>` served from IIS. Visible design effort exceeding research effort is itself a negative signal. |
| **No OKLCH fallbacks** | Baseline support is Chrome 111+, Safari 15.4+, Firefox 113+, all from 2023. Acceptable for this audience. |
| **No SHA-pinning of GitHub Actions** | Overhead for a personal site. Revisit if anyone else gains write access — note the append-only guarantee ultimately depends on branch protection, since the workflow runs the validator from the commit under test. |

---

## Anti-patterns — check any new page against these

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
10. Overclaiming the identity. **Amended 2026-08-24:** the homepage descriptor
    now reads "Applied Scientist · Quantitative Research · Systematic
    Volatility", adopting *Quantitative Research* as the term recruiters
    actually search on. This was a deliberate override of the original rule,
    which held that "quantitative researcher" on a site with no desk experience
    invites a comparison that is lost. The rule still binds everywhere else: the
    site does not claim desk experience, a trading seat, or institutional P&L,
    and `jobTitle` in JSON-LD remains "Applied Scientist".

**Delete on sight:** proven · consistently · robust (unqualified) · proprietary ·
cutting-edge · passionate about · significant returns · battle-tested ·
alpha-generating · any Sharpe stated without a period, a cost assumption, and an
interval.

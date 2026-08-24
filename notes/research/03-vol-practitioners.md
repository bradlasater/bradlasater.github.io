# Research 03 — Volatility / Derivatives Practitioners Who Publish Publicly

**Date of research:** 2026-08-23
**Scope:** Personal sites, blogs, and research-publishing setups of volatility/options/derivatives practitioners and serious quant researchers who publish work publicly. Focus: *how research is presented*, not org charts.
**Verification rule applied:** every URL below was loaded with WebFetch unless explicitly flagged as `[NOT FETCHED]`. Sites that blocked the fetcher are flagged with the reason.

---

## 0. Verification ledger (read this first)

### Verified by direct fetch (20)

| # | URL | Person / org | Last-dated content seen | Status |
|---|-----|--------------|------------------------|--------|
| 1 | https://qoppac.blogspot.com/ | Rob Carver | 2026-07-03 | **Active**, high cadence |
| 2 | https://www.systematicmoney.org/ | Rob Carver (books/pro site) | undated | Active brochure site |
| 3 | https://jonathankinlay.com/ | Jonathan Kinlay | 2026-08-16 | **Active** |
| 4 | https://www.quantresearch.org/ (+ `/Intro.htm`, `/LeftFrame.htm`, `/Software.htm`) | Marcos López de Prado | code items to 2015; site content current-ish | Active but technically archaic |
| 5 | https://quantocracy.com/ | Aggregator (Mike @ Quantocracy) | 2026-08-23 | **Active daily** |
| 6 | https://robotwealth.com/blog/ (+ `/about/`, `/author/es/`, 4 posts) | Kris Longmore, Euan Sinclair | 2026 series ongoing; Sinclair last 2025-10-10 | **Active** |
| 7 | https://robotwealth.com/author/es/ | **Euan Sinclair** | 2025-10-10 | Active-ish |
| 8 | https://www.hulltactical.com/blog/ (+ 2 posts) | Hull Tactical (Sinclair is PM there) | 2026-08-05 | **Active**, but **no bylines** |
| 9 | https://blog.moontower.ai/ (+ tag pages, 2 posts) | Kris Abdelmessih | 2026-08-16 | **Active** |
| 10 | https://moontower.substack.com/ (+ `/about`) | Kris Abdelmessih | 2025+ | Active |
| 11 | https://dm13450.github.io/ (+ `/about/`, `/blog/`, post) | Dean Markwick | 2026-08-23 | **Active** — best `github.io` model |
| 12 | https://epchan.blogspot.com/ | Ernie Chan | 2025-11-27 | Slowing (~4 posts/yr) |
| 13 | https://falkenblog.blogspot.com/ | Eric Falkenstein | 2024-06-13 | **Dormant ~2 yrs** |
| 14 | https://www.thinknewfound.com/ + https://blog.thinknewfound.com/ (+ post) | Newfound Research (Corey Hoffstein) | 2023-08-28 | **Dormant ~3 yrs** |
| 15 | https://volvibes.substack.com/ (+ `/archive`, post) | Harel Jacobson | 2026-08-23 | **Active daily/weekly**, mostly paywalled |
| 16 | https://reasonabledeviations.com/ | Robert Andrew Martin | 2023-02-05 | **Dormant ~3.5 yrs** |
| 17 | https://malchevskiy.pro/ | Sergey Malchevskiy | undated | Active page, **no research** |
| 18 | https://www.allocatesmartly.com/ (+ `/faqs/`, post) | Allocate Smartly | ongoing | **Active** — best live-tracking model |
| 19 | https://www.qvradvisors.com/ (+ `/media` → 404) | Benn Eifert / QVR | undated | Active firm, **zero public research** |
| 20 | https://www.quantbeckman.com/p/with-code-backtesting | "Quant Beckman" (pseudonymous) | 2026-05-24 | Active |
| 21 | https://www.risk.net/author/euan-sinclair | Euan Sinclair (publications) | 2022-05-12 | Archive |
| 22 | https://concretumgroup.substack.com/ | Concretum Research | ongoing | Active, thin front page |

### Attempted and blocked / dead — reported honestly

| URL | Result | Note |
|-----|--------|------|
| https://moontowermeta.com/ | **HTTP 403** (bot protection) | This is Kris Abdelmessih's *original* blog. Its content has largely migrated to `blog.moontower.ai` (Ghost). Confirmed alive via search index but not fetchable by me. |
| https://cssanalytics.wordpress.com/ | **HTTP 403** | David Varadi's CSSA. Search index shows last post **2026-07-27, "The Inflation Compass Model"** — so it *is* active, but I could not load it. `[NOT FETCHED]` |
| https://alphaarchitect.com/blog/ and post URLs | **HTTP 403** | Structure confirmed only via search snippets. `[NOT FETCHED]` |
| https://euansinclair.com/ | **DNS does not resolve** | **Euan Sinclair has no personal website.** See §1. |
| https://deanmarkwick.com/ | **DNS failed from my fetcher** | Canonical domain in his feed; `dm13450.github.io` serves the same content and works. |
| https://mfe.baruch.cuny.edu/jgatheral/ | **TLS cert error** | Jim Gatheral's Baruch page. `[NOT FETCHED]` |
| https://physikinvest.com/ | **HTTP 403** | Retail-leaning vol/GEX blog. `[NOT FETCHED]` |
| https://notion.moontower.com/ | **DNS does not resolve** | Referenced in third-party writeups; not live. |
| https://moontowerquant.com/about-me | **Connection refused** | Referenced from the Substack About page; not reachable. |
| https://www.qvradvisors.com/media | **HTTP 404** | Media page referenced by search but gone. |

---

## 1. Euan Sinclair — the specific finding Brad needs

**There is no `euansinclair.com`.** DNS does not resolve. He has never run a personal site.

His actual public surface, in order of how a hiring manager would encounter it:

**a) Robot Wealth author page — https://robotwealth.com/author/es/ [VERIFIED]**
He is a listed contributor on Kris Longmore's Robot Wealth. Posts on that page:
- "Why You Can't Tell if Your Strategy 'Stopped Working' (Statistically Speaking)" — 2025-10-10
- "Finding Edges" — 2025-08-31
- "To Trend or Not To Trend? (Wrong question)"
- plus AMA and "Volatility Book Club" series entries.

Robot Wealth's `/about/` page describes him under the heading **"Options & Volatility"** as *"one of the most respected options traders and authors in the world."* Note the structure: the site owner vouches for the specialist; the specialist does not self-praise.

**b) Hull Tactical blog — https://www.hulltactical.com/blog/ [VERIFIED]**
He announced (June 2024, via X) he'd be blogging regularly at hulltactical.com/blog. The blog is active — most recent post 2026-08-05. Post titles seen:
- "The Market Is Efficient (Eventually)" — 2026-08-05
- "Buying The Dip" — 2026-07-28
- "Attention Is Not Efficiency" — 2026-07-15
- **"0DTE Options: Tiny Edge, Huge Distribution"** — 2026-07-08
- "When Good Advice Goes Bad" — 2026-06-24

**Critical anti-pattern observed:** *the Hull Tactical blog has no author bylines.* I fetched two posts directly and neither attributes an author. This is a real loss of credibility signal — the writing is clearly expert, but nothing connects it to a named person with a track record. **Brad must not replicate this.** Every research post should carry a name and a date.

**c) Risk.net author page — https://www.risk.net/author/euan-sinclair [VERIFIED]**
Two peer-reviewed *Journal of Investment Strategies* pieces:
- "The risk-reversal premium" — 2022-05-12
- "Reflections on recent volatility" — 2018-04-10

**His verbatim authority statement (this is the model for Brad's bio — copy the shape, not the content):**

> "Euan Sinclair is an option trader with over 25 years of professional trading experience. He has traded options on indexes, stocks, commodities and interest rate products. He currently trades equity options at Bluefin Capital Management. He holds a PhD in theoretical physics from the University of Bristol and has written three books: *Volatility Trading*, *Option Trading* and *Positional Option Trading*, all published by Wiley."

Four sentences. Years of experience → *what instruments* → current seat → credential + artifacts. No adjectives. No "passionate about." No "proven track record."

### 1.1 Deep read: Sinclair's "Why You Can't Tell if Your Strategy 'Stopped Working'" [VERIFIED]

URL: https://robotwealth.com/why-you-cant-tell-if-your-strategy-stopped-working-statistically-speaking/ (2025-10-10, ~1,850 words)

This is the single most transferable post I found for Brad's purposes, because it is **a rigor demonstration disguised as a practical question.**

Structure:
1. Hook — "Traders love the illusion of precision"
2. Simulation setup — hypothetical strategy at 10%/yr, 20% vol ("roughly the S&P's long-term profile")
3. The core problem — statistical inability to detect regime change
4. Results table — p-values from two tests
5. The noise paradox — why *dead* strategies still show strong recent months
6. 3,000-run Monte Carlo — quantifies false-positive rate
7. Critique of the non-parametric alternative (Kolmogorov–Smirnov)
8. Philosophical reframe — from binary "is it dead?" to Bayesian updating
9. "Practical Interpretation" — Type I / Type II errors
10. Close — probabilistic over binary

Numbers he actually shows (note how everything is derived in the open):
- Sample sizes: `n₁ ≈ 1260 vs. n₂ ≈ 21`
- Daily noise: `20% / √252 ≈ 1.26% daily`
- Daily drift: `0.10 / 252 ≈ 0.04% per day`
- Daily Sharpe: `0.04 / 1.26 ≈ 0.03, an astronomically low signal-to-noise ratio`
- Welch t-test p = 0.12; K–S test p = 0.37; t-stat ≈ −1.6
- "In 16% of runs, it beat more than 80% of the prior months. In 7.5% of runs, it beat more than 90%. So, one in every thirteen 'dead' months looks like a top-decile success."

Verbatim hedges worth stealing:
- *"That's the problem: volatility dominates everything"*
- *"The test confidently says 'nothing to see here.' It's technically correct"*
- *"The conclusion isn't that tests are bad—it's that the problem is mis-specified"*
- *"The answer is always probabilistic, never definitive"*

**No code, no charts, no LaTeX.** Math is inline arithmetic with `≈`. The rigor comes from *making the reader do the signal-to-noise calculation with him*, not from typography.

### 1.2 "Finding Edges" (2025-08-31) [VERIFIED]

His stated epistemology, useful as a quotable standard:
- Edge = profitability **+** tolerable risk **+** *tradeability*. He dismisses many academic anomalies because they ignore access/regulatory reality.
- *"There is too much stuff to test until you have an idea from somewhere else."* — i.e. theory-first, not data-mining-first.
- *"If it doesn't clearly point to money, no amount of tweaking is likely to produce a robust trading idea."* — premature abandonment beats over-fitting.

---

## 2. Site-by-site analysis

### 2.1 Rob Carver — https://qoppac.blogspot.com/ ("Investment Idiocy" / "This Blog is Systematic") [VERIFIED]

**Person & authority.** From `/p/about-me.html`, verbatim self-description: *"an ex Hedge fund manager and derivatives trader, economist and statistics/finance geek."* Career: Barclays Capital (trader) → CEPR (research manager) → **AHL, seven years**, building global macro systems and running fixed income → now independent systematic futures trader and author. BA Economics (Manchester), MSc Economics (Birkbeck). Visiting lecturer, Queen Mary UoL. Research advisor, Stylus Capital. Five books.

A nice touch: the About page *disambiguates him from other Rob Carvers* (a 15th-century Scottish composer, a travel writer, several academics). Small, human, and it signals "I expect people to google me."

**Companion pro site:** https://www.systematicmoney.org/ — nav is `Home / Which book to buy / About Rob / Talks, Media, Consultancy / Contact / Blog`, plus a book-title secondary menu. Includes an explicit, blunt disclaimer that he is **"not regulated or authorised to provide investment advice"** by FCA/SEC, and an all-caps **"ROBERT DOES NOT OFFER TRADING COURSES"** — a deliberate anti-grift signal.

**Site type & IA.** Blogger (Blogspot), default-ish template. Sidebar: Home, Systematic Investment, Systematic Trading, code repository links, books, media, resources, archive back to 2013, popular posts, ~54-label tag cloud. Deliberately ugly. It works *because* the content is dense.

**Research post structure.** Not a rigid template but a stable habit:
> Recap of prior findings in the series → "Prior Art" (enumerate the methodological options) → Methods → Testing (multiple scenarios) → Discussion & Conclusion → what's next.

Example post analyzed: "Jumping back in the pool(ing)..." (2026-07-03, ~3,500 words). Sections: Introduction & Recap → Prior Art (6 approaches, 2 pooling strategies) → Methods → Testing (five in-sample/out-of-sample period combinations: 5/10/20/40-yr IS against 1-yr and 5-yr OOS) → Discussion & Conclusion.

**Charts.** Frequently **none**. Results are plain monospaced text tables:
```
unpooled                 0.046     0.0
all pooled               0.425     0.0
asset class pooled       0.557     NaN
```
When charts appear (e.g. "R squared and Sharpe Ratio", 2025-11), they are **raw matplotlib defaults** — log-x, linear-y, title indicating forecast horizon, frequently no axis labels or legend. He does not style. The signal is "I ran this and I'm showing you the output," not "I made you a deck."

**Code.** Almost never inline. Linked instead: *"There is code [here](link); you'll need psystemtrade to run it though."* His entire production system (`pysystemtrade`) is open-source on GitHub. That is the strongest possible code signal — the reader can go read the actual system, not a toy snippet.

**Math.** Plain text, no LaTeX. E.g. `SR for N days holding period = 16 × √(R² / N)`.

**Uncertainty.** This is his core differentiator:
- p-values on every method comparison (with `NaN` marking the reference/winner)
- **Multiple IS/OOS period combinations** rather than a single split
- Reports **median and 25th-percentile Sharpe**, not just mean — distributional thinking
- Monte Carlo / random resampling ("many, many runs of random resampling")
- Explicit shrinkage parameters stated in-line ("SR shrinkage 0.5, correlation 0.75")
- In "The crossword puzzle of fitting" (2026-06) he ran thousands of random 5×5 instrument/rule combinations and reported the full breakdown: meets neither criteria 3.8%, meets both 0.81%, rule-grouping only 0.11%, **instrument-grouping only 95.3%** — i.e. he *built a null* and reported the whole distribution.
- Also states the design choice that protects against implicit fitting: **testing opposite trading rules** so a "good" result can't be an artifact of sign selection.

**Negative results / self-criticism.** Constant and casual:
- *"Strictly speaking we should remove overlapping periods as that will inflate our R squared, but as long as we consistently don't remove overlapping periods then our results will be fine"*
- *"With real data we can lose money. So we remove all the negative SR before plotting"*
- *"There is some weird deep correlation pattern that the simple analysis by asset class and trading rule doesn't pick up. I don't buy that."*
- *"(yes, bad move in retrospect, and another failure of discretionary trading on my part)"*
- *"Personally I'm taking the absence of any contradictory evidence as evidence that I should continue to do what I've done before"* — i.e. he explicitly labels a null result as a null result.

**Live track record — the gold standard.** Annual series, one post per year, twelve years running:
- "Annual performance update — year 12" (2026-04): mark-to-market **+21.9%**, net after fees/commissions/slippage **+23.7%**, Sharpe **0.80** vs SG CTA 0.52–0.54, correlations **0.68 to SG CTA, 0.56 to AHL**. Reports slippage explicitly: *"Without my execution algo, if I had just traded at the market, I would have paid 1.34% in slippage; my simple algo earned 78bp and cut my slippage bill by around 40%."* He also notes *his Sharpe would be lower if a risk-free rate were deducted.*
- "Annual performance update returneth — year 11" (2025-04): leads the TLDR with **"it's my worst ever"** / **"my worst ever in futures."** Futures **−16.3%**, decomposed into **−14.5%** pure futures, **−0.64%** cash-like ETFs, **−2.7%** FX. Contextualized against benchmarks that also fell: SG CTA ~−18%, AHL −18.2%.

What he shows: non-compounded equity curve (monthly and annual), a year-by-year table across all 11–12 years marking best/worst, Sharpe comparisons, per-market P&L breakdown, per-trading-rule attribution.

What he does **not** do (worth noting as a gap Brad can improve on): he does not overlay live-vs-backtest, and he does not put confidence intervals on his own realized Sharpe. He benchmarks and decomposes rather than significance-tests himself.

**Voice.** Conversational, self-deprecating, British. Metaphors ("like the dad whose kid at sports day is winning everything"). ~2,500–4,000 words. Numbered/ALL-CAPS section headings. Leads bad-news posts with a TLDR.

**Distribution.** Blogger RSS, syndicated to Quantocracy (appeared in the 2026-06-06 daily roundup), X presence, GitHub, books via Harriman House. No newsletter capture, no paywall, no ads.

---

### 2.2 Jonathan Kinlay — https://jonathankinlay.com/ ("Quantitative Research and Trading") [VERIFIED] — **the strongest single template**

**Person & authority.** From `/about/`: *"Head of Quantitative Trading at Systematic Strategies, LLC, a systematic hedge fund that deploys high frequency trading strategies using news-based algorithms."* Founder/GP of Caissa Capital; founded Proteom Capital (stat arb); *"Global Head of Model Review at the US investment bank Bear Stearns."* PhD in economics; faculty at NYU Stern, Carnegie Mellon, Reading.

**Track-record claim, stated the right way:** *"Caissa, which managed $400M in assets, was ranked by FIMAT as the top performing fund in its class in 2004."* — Note: AUM stated, ranking attributed to a **named third party**, and **dated**. Not "consistently outperformed."

(Minor anti-pattern: the bio also mentions a 1978 World Student Olympiad chess gold and family relations to a Fleet Street editor and a British actress. Charming, but it dilutes. Brad should keep the credential block tighter.)

**Nav.** Minimal: `Home / Systematic Strategies (submenu) / About`. Reverse-chronological posts. Recent:
- 2026-08-16 "Your Research Agent Is an Undisclosed Factor Exposure — And So Is Everyone Else's"
- 2026-05-17 "Agentic Workflows for Alpha Research"
- 2026-05-10 "Reinforcement Learning for Optimal Execution"
- **2026-05-04 "Deep Learning for Volatility Surface Repair"**

**The post template (this is the thing to copy).** "Deep Learning for Volatility Surface Repair" section order:
1. Opening context / problem motivation (unlabeled)
2. **Setup** — grid definition, training surfaces, test surfaces, baselines
3. **Model** — architecture, with code
4. **Loss** — loss function, with code
5. **Training** — procedure, with code
6. **The 2 × 2 result** — headline table + interpretation
7. **Diagnostics** — secondary metric table
8. **Downstream SVI projection** — does the improvement survive to a *downstream* task?
9. **"What this experiment shows and does not show"** ← the crown jewel
10. **"Where to take this next"**
11. **Code and references** — full reproducible script

The "Agentic Workflows" post uses the same skeleton with different labels: *"What alpha research actually consists of" / "The naive loop and why it fails" / "The architecture: separated roles, instrumented handoffs" / "The objective function, written down" / "The tooling, concretely" / "Validating the Critic" / "What it changed: 12 weeks on FX carry" / "Failure modes I actually saw" / "What this means in practice"*.

Note the two recurring slots: **a named-failure-modes section** and **a scoped-claims section**. Both appear in every post.

**Charts.** A single well-chosen diagnostic figure per post. In the vol-surface post: a 2×3 grid of heatmaps — clean vol / sparse observations / CNN repair / interpolation baseline / model uncertainty / error — across maturity × log-moneyness. Static. No caption, no figure numbering (a weakness Brad can improve on).

**Code.** Extensive and inline. PyTorch `RepairCNN` class (~15 lines), `repair_loss` function (~12 lines with weighted MSE + calendar penalty + smoothness penalty), parameter ranges in `U()` pseudo-code notation, then a **~800-line self-contained reproducible script at the end**, headed:
> `"""Deep Learning for Volatility Surface Repair. Self-contained, CPU-friendly PyTorch script...`

"CPU-friendly" is a deliberate reproducibility signal.

**Math.** Domain-conventional notation inline, not heavy LaTeX display blocks: total variance `w(k, T) = σ²(k, T)·T`; calendar constraint as cumulative max along T; butterfly diagnostic `g(k) ≥ 0` citing **Gatheral–Roper**; SSVI parameterization (θ₀, θ_slope, θ_curve, ρ, η, γ). He names the arbitrage conditions by their canonical authors — that's a domain-fluency tell a vol desk reads instantly.

**Uncertainty — this is best-in-class.**
- Train/val/test discipline stated numerically: **1,600 training surfaces (SSVI, tight parameter range) / 200 validation (held out for checkpoint selection) / 200 test per cell in a 2×2 design (800 total) / independent random seeds across all sets.**
- Every headline metric as **mean ± standard error** (e.g. `0.0184 ± 0.0010`), with the formula stated: `std(ddof=1) / √N`.
- **Two out-of-distribution test families**, one structurally unseen: shifted SSVI (widened params) and **SABR-style events (never seen in training)**.
- Diagnostics beyond RMSE: calendar violation rate (raw and post-projection), butterfly arbitrage violation rate, **uncertainty coverage at nominal 80% and 95% vs empirical**, error–uncertainty correlation, stale-quote detection AUC, and downstream SVI fit quality.
- On the multiple-testing side, the 2026-08 post cites **Bailey & López de Prado's deflated Sharpe ratio**, **Harvey, Liu & Zhu** on multiple-testing corrections, **White's Reality Check**, and **McLean & Pontiff (2016)** on post-publication decay ("32%... attributable to publication-informed trading").
- Reports confidence intervals on correlations: random expressions **+0.15 [−0.02, +0.37]**, LLM runs **+0.62 [+0.54, +0.69]**, published canon **+0.82 [+0.67, +0.91]**.

**Negative results / discarded findings.** He *reports a metric he threw away*:
> "I mention it because this is precisely the failure mode that agentic research pipelines are good at manufacturing at scale — a plausible number, in the expected direction, that dissolves against a null nobody bothered to run."

**Hedging phrasing — the highest-value quotes in this whole document.** From the vol-surface post's "What this experiment shows and does not show":
- *"It does not show that this kind of CNN-based repair is useful on real data."*
- *"The synthetic surfaces have no calibration drift, no quote-time-of-day noise, no microstructure asymmetries…"*
- *"Whether the small relative gap between CNN and interpolation on the adversarial cell survives a real-data test is an open question."*
- *"It does not show that a CNN is the right architecture for this task."*
- *"It does not, on its own, justify a production system."*
- *"The heteroscedastic head undercovers"* (naming his own model's failure mode)
- *"This says the model's residual is not, on its own, a strong stale-quote detector"*
- *"The convergence is slow and the validation curve is still improving slightly at epoch 60"*

From the 2026-08 post:
- *"This is a small one, and it does not come out where I expected."*
- *"I would not defend it further than 'worth running properly.'"*
- *"The ordering of the three baselines as the result and the levels as approximate."*
- *"I would not swear to it"*
- *"should be read as an order of magnitude, not a point estimate"*

**Voice.** Academic-technical but first-person-plural and readable. ~4,500–5,000 words excluding code.

**Distribution.** Listed on Quantocracy's blogroll. Personal domain, WordPress. No newsletter capture visible.

---

### 2.3 Dean Markwick — https://dm13450.github.io/ [VERIFIED] — **the best `github.io` model, and closest structural analogue to Brad's site**

**Person & authority.** `/about/`: *"I am a quant researcher focused on execution at both the high (parent) and low (order routing) level."* Previously quant at BestX (TCA across FX, rates, equities). **PhD Statistical Science, UCL** — thesis *"Bayesian Nonparametric Hawkes Processes with Applications"*; MRes CS Manchester; MPhys Theoretical Physics Manchester. Maintains open-source: `dirichletprocess`, `HawkesProcesses.jl`, market-data libraries. Runs a crypto liquidity dashboard. Guest posts for QuestDB. Conference speaker.

**Nav.** `About Me / Blog / Research / Teaching / Physics`. Social: GitHub, LinkedIn, Twitter, **RSS**. Jekyll on GitHub Pages (canonical domain `deanmarkwick.com`, though that DNS failed from my fetcher; the `.github.io` host serves identically).

**Cadence and range.** 100+ posts, Sept 2014 → 2026-08-23. Recent:
- 2026-08-23 Big Ticks and Small Ticks in Equity Microstructure
- 2026-07-15 A Statistical FX Factor Model
- 2026-04-19 A Fundamental FX Factor Model
- 2026-03-10 Making Sense of the DXY
- 2025-07-23 Easy Neural Nets and Finance – Part 1
- 2025-03-14 Fitting Price Impact Models
- 2024-06-06 Solving the Almgren-Chriss Model
- **2024-02-08 Cross Asset Skew – A Trading Strategy**
- 2023-07-15 Stat Arb – An Easy Walkthrough

(He also posts football/soccer stats and physics. Mixed-topic is fine for him because the quant posts are technically unambiguous; **Brad, with a single hiring goal, should not mix.**)

**Deep read: "Cross Asset Skew – A Trading Strategy" (~3,500 words ex-code).**

Section order:
1. **What is Skew?** — definition + formula + visual intuition
2. **Skew as a Trading Strategy** — rationale, cross-sectional construction
3. **The ETF Trading Universe** — exact asset list and data source
4. **Building the Backtest** — methodology, weighting, forward-fill logic
5. **Alpha, Beta or Something Else?** — regression vs market
6. **A Deeper Dive With More Equity Factors** — multi-factor regression
7. **Conclusion**
8. **Related Reading**

- **Replicates a named academic paper** and says so: Nick Baltas, *Cross-Asset Skew* (ResearchGate link). *"After reading the original paper… I decided to try and replicate the results."* Also credits the podcast where he heard it (Flirting with Models S7E3).
- **Data sources named exactly:** AlpacaMarkets free API (daily bars, 10-yr history limit), full ETF universe enumerated (25 equity, 15 fixed income, 7 commodity, 7 FX, 5 other), factor proxies MTUM/VTV/VUG/VIG, plus a BlackRock reference doc.
- **Code inline throughout**, Julia 1.9, complete and runnable: package imports listed, custom `parse_date()`, `clean()`, `load()`, `ffill()` defined in the post. Packages named: AlpacaMarkets, Dates, CSV, DataFrames, DataFramesMeta, RollingFunctions, Plots, StatsBase, Distributions, GLM.
- **Charts:** Plots.jl, static PNG, 900 DPI, consistent sizing (800×200 for time series), minimal titles ("Skew demo", "Returns", "Global Portfolio"). Not beautiful — but consistent and clearly generated by the code shown.
- **Math:** real LaTeX via MathJax, `\[ ... \]` display delimiters. Skewness formula and the regression model `Skew Return = α + β · Market Return` rendered as display math.
- **Statistics reported:** p-values in regression tables (`0.0544`, `<1e-27`), R² per asset class (`0.0003` to `0.08`), 10% vol targeting applied at portfolio combination.
- **Honest gaps flagged, not hidden:** no out-of-sample split (full-period backtest); transaction costs deferred with *"assuming we can trade at the previous closing price but that is a problem to solve for another day."*

**Hedging phrases, verbatim:**
- *"Although the results are not as conclusive as the original paper, they are on a shorter timescale"*
- *"We have neglected the trading costs and potential capacity"*
- *"this is probably safe to ignore until you hit the super asset manager size"*
- *"this is a promising sign that there is perhaps something more to be done"*

**Distribution.** *"Enjoy these types of posts? Then sign up for my newsletter."* Byline with GitHub/LinkedIn/Twitter/RSS. Internal cross-links to related posts. **No affiliate links, no sponsorships.**

---

### 2.4 Kris Abdelmessih — https://blog.moontower.ai/ and https://moontower.substack.com/ [VERIFIED]

**Person & authority.** 21 years in options: **traded in the pits at SIG**, ran his own market-making team, ran the commodities book for a volatility manager. (The original blog **moontowermeta.com returned 403** to my fetcher — content now lives on `blog.moontower.ai`, a Ghost install; `moontowerquant.com/about-me` refused connection.) The Substack `/about` is deliberately non-credentialed; authority is established through **third-party testimonials** ("one of the best thinkers I've encountered") and, more importantly, through *demonstrated fluency* in the posts.

**Two-property architecture — worth noting as a pattern:**
- `blog.moontower.ai` (Ghost) — the **research/product** property. Nav: `Home (moontower.ai) / How Markets Work / Options & Volatility / Risk & Edge / Options Theory`. Tag-based IA, not chronological.
- `moontower.substack.com` — the **personality/newsletter** property. Subtitle: *"math, education, parenting, games, business, and occasionally hair bands🎸"*.

This split is smart: the wandering-personal-essay audience and the vol-desk audience get different front doors. **Brad's equivalent: keep the trading-system research on the main site; if he wants a personal voice, put it somewhere else.**

**Options & Volatility tag — post titles (this is a menu of what a vol audience actually reads):**
- A Devilish Question for Option Sellers: Which VRP is Higher?
- A Cleaner Way to Compute Seasonal Vol
- Does Revenue Seasonality Translate to Vol Seasonality?
- How High Implied Vol Works for and Against You
- How a High Implied Vol Can be Cheap
- Delta-Hedged Risk Reversals
- The Bias of Hedging on Implied Delta
- Approximating Gamma in Your Head
- Options Policework
- Hedging is for Gardeners
- Collar Shopping

**Deep read: "A Devilish Question for Option Sellers: Which VRP is Higher?" (2026-06-22, ~2,800 words, byline + date present).**

Sections: opening premise on VRP → definitional distinction (**volatility vs variance**) → "The Gamma-Theta Tug of War" → "Theta-weighting position size" → "How Rich Does The Low-Vol Name Need To Be?" → concrete worked example in HYG → **mathematical appendix**.

- **Charts:** four static embedded images. (1) 30-day IV vs trailing RV in HYG, line chart; (2) VRP ratio scatter with RV percentiling; (3) variance-edge comparison table across the vol spectrum; (4) spread-equivalence table. Light background, standard financial palette, **no source attribution in the chart metadata** — a weakness.
- **Math:** rendered as **screenshots of hand-worked algebra**, not LaTeX. Appendix shows the derivation steps visually. E.g. `IV_low = 10 × √(1 + 1100 / (10 × 50))`. Informal but it reads as *someone actually working the problem*.
- **Structural device worth stealing:** an italicized **"Aside"** block where he discloses his own trading history in the instrument being analyzed — explicitly flagging potential bias while keeping analytical authority.

**Hedging, verbatim:**
- *"It is entirely possible that my trading profits made up for…"*
- *"This is hard to translate into risk-adjusted, opportunity-cost-aware amounts"*
- *"There's enough evidence to not disagree"*
- *"It's hard to bang on the VRP desk with fervor"*
- *"Spreads are a more solid footing, but…"*

Note how *"There's enough evidence to not disagree"* is a double-negative hedge — it concedes the claim is weak while still being usable. That's a distinctly practitioner register.

**Second post read: "stock-bond correlation" (2026-08-16, ~1,200 words, "3 min read").** Sections: "Confidence Intervals on Correlation" / "The Problem" / "The Recipe" / "Broadly Educational Bits". One static figure (Fisher transformation). Math in plain-text: `z = arctanh(r) = ½ · ln[(1 + r) / (1 − r)]`. Reports **30-day correlation +0.43, 1-year +0.28, CI [+0.02, +0.72]** — i.e. he leads with the point estimate and immediately shows how wide the interval is. That's the whole point of the post.

**This is a template Brad should note: "here is a number everyone quotes; here is its confidence interval; the interval is embarrassingly wide."** It's cheap to produce, it's undeniably correct, and it demonstrates exactly the not-fooling-yourself instinct a vol desk wants.

---

### 2.5 Robot Wealth — https://robotwealth.com/ [VERIFIED]

**Positioning.** *"Research lab and shared infrastructure for independent quants"* — "technical people who treat their trading as a serious business and run it themselves, in a few hours a week."

**Nav.** `Home / About / Blog / Free Case Study / Bootcamp / RW Pro / Login`. Blog categories: Quant trading, Think like a trader, Trading strategies. There is an **"Index of Strategies"** page — a curated map into the archive, which is a strong IA idea for a site with years of posts.

**Founder credentials, verbatim from `/about/`:** *"I started as an engineer, the kind that builds things in the physical world."* Then an equity partnership at a prop firm; now runs a portfolio of systematic strategies from home. **No performance claims at all.** The closest: *"Today I trade a portfolio of strategies that needs only part-time attention."* Instead: *"Any single trade is close to a coin flip. The process is what matters over hundreds of trades."*

**This is a notable and copyable choice: a commercial site that sells education and deliberately makes zero return claims.**

**Post style evolution.**
- Older posts (e.g. "Exploring Mean Reversion and Cointegration Part 2") are **code-forward in R**, with inline snippets (`m <- lm(AUDUSD.Close ~ NZDUSD.Close, data = closes)`), text-rendered equations (`Δy(t) = λy(t−1) + βt + μ + α₁Δy(t−1) + … + αₖΔy(t−k) + εₜ`), and `plot.zoo()` charts with basic titles ("AUDUSD and NZDUSD Closing Prices", "AU-NU OLS residuals"). Self-deprecating chart note: *"Go easy on my design abilities…"*
  Hedging: *"we unfortunately can't reject the null hypothesis"*; *"unlikely that we can form a stationary portfolio"*; *"admittedly does not look overly stationary."*
- 2026 posts (the "Triangulated Stat Arb" 6-part series) are **narrative-first, code-free**, ~2,200 words, with charts *promised in text but not rendered* on the pages I fetched. Math is inline text (`z_AB = α_A – α_B`).
  Hedging: *"none of these factors is necessarily 'better'"*; *"the juice may not be worth the squeeze"*; *"you'll be wrong plenty, but you should be right more than you're wrong"*; *"I reckon"*; *"mileage may vary"*; *"not foolproof"*; *"we can't really tell from what I've shown you here."*

**Confessional post-mortem: "Much Ado About Variance" (Kris Longmore, 2026-01-11, ~2,200 words).** He admits abandoning a turn-of-month bond strategy during a drawdown and then watching it recover. Four charts: strategy performance over time; rolling 12-month Sharpe from the mid-90s; 2023–24 deterioration; 2025 recovery. The lesson is the statistical one — **at Sharpe ≈ 1, two-year drawdowns are expected**, so the "it stopped working" inference was unjustified. He also notes his vol-selling book *"realised some of that famous negative skew during the April tariff tantrum, but was still profitable."*

**This pairs directly with Sinclair's post on the same site.** Together they form a house position: *you cannot statistically detect strategy death on realistic sample sizes, and acting as if you can is itself the error.* That's a very sellable intellectual stance.

**Note on failure narratives:** "The Metamorphosis" (2026, Part 4 of the stat-arb series) is *not* a post-mortem despite the framing — it's a problem→solution piece about pairs-trading's structural limits (*"there are inherent limitations"*; betas are *"not stable, and they're prone to measurement error"*; *"It's difficult to model this stuff well in a way that's of practical benefit"*; *"you lose some simplicity"*). Worth distinguishing: **criticizing a method is not the same as publishing your own failure.** Real post-mortems are rarer than the genre implies.

---

### 2.6 Marcos López de Prado — https://www.quantresearch.org/ [VERIFIED]

**Technically the worst-built site in this document, and it does not matter at all** — which is itself the finding.

**Implementation.** Deprecated HTML **`<frameset>`** (LeftFrame.htm + Intro.htm), with a `<noframes>` fallback reading *"This page uses frames, but your browser doesn't support them."* No responsive design, no dark mode, no RSS, no newsletter.

**Nav (verbatim, in order):** `INTRO / BIO / INNOVATIONS / PUBLICATIONS / SEMINARS / VIDEOS / PATENTS / MACHINE LEARNING / PRESS / EVENTS / SOFTWARE / CO-AUTHORS / WHY GEOMETRY?` Plus an "Other Sites" block: ADIA Lab, State Honors, True Positive Tech, Cornell. Header: *"Professor Marcos López de Prado (RAI, OMC)."*

**Authority is 100% external validation, stacked:** three decades managing *"large pools of funds for some of the most demanding institutional investors"*; international member of Spain's Royal Academy of Engineering; Buy-Side Quant of the Year; Quant of 2019; Spain's Order of Merit; Frank Fabozzi editorials; *Advances in Financial Machine Learning*.

**Disclaimer, verbatim:** *"statements made in this communication are strictly those of the author"* and do not represent affiliated entities.

**The `/Software.htm` page is the transferable idea.** A dated, itemized code archive, each entry tied to a specific paper, under GNU-GPL for non-commercial academic use:
- Backtest Overfitting Simulator (LBL, 2014) — *"This online tool overfits a seasonal investment strategy within the parameter ranges specified by the user."*
- `HRP.py` / `HRP_MC.py` (2015) — hierarchical risk parity + Monte Carlo vs CLA
- **`DSR.py` (2014) — Deflated Sharpe Ratio, closed-form**
- KCA files 1–4 (2014) — Kinetic Component Analysis
- `OTR.py` (2014) — optimal trading rules for OU processes
- SFD 1–2 (2014) — Stochastic Flow Diagrams
- **CSCV 1–3 (2013) — Probability of Backtest Overfitting via Monte Carlo and EVT**
- DD 1–4 with data (2013) — drawdown quantile functions
- `CLA.py` / `CLA_Main.py` / `CLA_Data.csv` (2013) — *"A Python class containing the Critical-Line Algorithm for quadratic optimization subject to inequality constraints"*
- ERC / MMSC / Clustering (2012); PSR (2012); OEH (2012); EF3M (2012)

**Lesson for Brad.** Design investment does not buy credibility with this audience; *artifacts* do. A "Code" page listing named, dated implementations tied to specific write-ups is worth more than any amount of CSS. And **`DSR.py` + the CSCV/PBO files are literally the reference implementations of the hygiene Brad says he's practicing — he should cite them by name and show he's applied them.**

---

### 2.7 Harel Jacobson — https://volvibes.substack.com/ and https://volquant.medium.com/ [VERIFIED / partially]

The only person in this list whose *entire* public output is options/vol.

**Person.** Global/FX volatility trader. Medium bio (via search index; `/about` returned 403): writes about options and volatility, *"Python addict, Bloomberg junkie, and amateur boxer."* Guest on Corey Hoffstein's *Flirting with Models* (S5E10, "Trading FX Volatility"). Best-known long-form: *"(Almost) Everything You Wanted To Know About FX Volatility Smile"* series and *"Think Like a Market Maker — Understanding Implied Volatility."*

**Publication.** *"Options, Volatility & Trading"* — *"0-DTE option structures, historical option strategy performance dashboards for US Indices, market performance around events / data releases & general market commentary through the lens of volatility."* 4,000+ subscribers.

**Cadence (from `/archive`, verified) — extremely high, event-driven:**
- SPX ATM Option Structure Dashboards — 2026-08-23
- August 2026 Update | Option Strategy Returns & Sharpe + Intraweek Breakdown — 2026-08-23
- Monthly OpEx: August 2026 — SPX & SPX Index Options Historical Performance — 2026-08-20
- VIX Futures Monthly Expiration: SPX Index & Index Options Performance — 2026-08-18
- Market Overview — 2026-08-16
- CPI — SPX Index & Options — 2026-08-11
- NFP Overview — 2026-08-07
- End-of-month SPX Straddle Trade: July 2026 Update — 2026-07-31

**Anti-patterns observed (important, because this is the closest topical neighbor to Brad).** I fetched the SPX ATM dashboard post. Free preview:
- **No methodology disclosure**: no backtest period, no data source, no construction rules, no cost assumptions
- **No source labels on charts**
- Performance and Sharpe figures referenced in adjacent posts with **no caveats attached in the visible portion**
- The visible content functions as a **promotional teaser**; the substance is paywalled

**Conclusion for Brad:** high-frequency dashboard content builds a *subscriber* audience, not a *hiring-manager* audience. A vol PM skimming this cannot tell whether the numbers are trustworthy. Cadence is not credibility. Jacobson's *long-form educational* pieces (the FX smile series) are the credible half of his output; the dashboards are the commercial half.

---

### 2.8 Allocate Smartly — https://www.allocatesmartly.com/ [VERIFIED] — **the model for live/out-of-sample presentation**

Not a personal site, but it solves exactly Brad's hardest problem: *how do you present tracked performance so a skeptic believes you?*

**Premise.** Independently re-implements published tactical asset allocation strategies, backtests them under **one uniform assumption set**, then tracks them forward in near-real-time. Members combine them into model portfolios.

**Verbatim backtest assumption disclosure (from `/faqs/`) — copy this pattern exactly:**
- *"All strategies trade at the market close (4 pm ET)"*
- *"Transaction fees plus slippage total 0.10% per trade (0.20% round-trip)"*
- *"Both dividends and gains are reinvested"*
- *"Return on cash… is assumed to equal the 3-month US Treasury rate"*
- *"We do not account for taxes… but we do model the historical tax efficiency"*
- On extending history with simulated pre-ETF data: *"This is inappropriate for hyperactive strategies that rely on small price changes to generate return, because this simulated data is not sufficiently accurate."*
- Deliberate conservatism, stated: *"we assume that we did not know about a dividend until 2-days after the ex-dividend date"*
- On execution-timing sensitivity: *"The strategies… are designed to capture broad market trends, and have been robust to reasonable delays in execution. Trades could have been delayed by up to a full day with a negligible impact."*

Notice the shape: **every assumption is a specific number or a specific rule, and each limitation is stated as a condition under which the method fails**, not as a generic "past performance" boilerplate.

**Their flagship methodological post — "Beware Strategies That Fall Down on Good Data" [VERIFIED].** They replicate a Dow Award-winning utilities-sector strategy and show it earns **13.4% annualized on Fama-French academic data** but **essentially matches the market when tested with real tradeable ETFs over 30 years**. Four charts of the *same* strategy under progressively more realistic data:
1. French data only (green) — 13.4%, looks great
2. French signals + tradeable ETFs (blue) — disappointing
3. ETF-based signals *and* trades (orange) — flat vs market
4. Extended with SPTRUTIL index — confirms no edge over 30 years

Caveats, verbatim:
- *"Unlike other tests on this site, transaction costs have been excluded, because we don't want to confuse the point"* (explaining a deviation from house standard)
- *"Is it possible that a weak edge existed in our 30-year test, but it was hidden by imperfections in SPTRUTIL, et al.? Absolutely."* (steelmanning the opposite conclusion)
- Closing exhortation: be *"more cynical about backtested results"*; insist on *"quality data and realistic backtest assumptions"*

**This is the highest-leverage post format in the whole document for Brad: take a published/celebrated result, re-run it under honest assumptions, and show the gap.** It demonstrates skill, skepticism, data handling, and independence in one artifact — and it cannot be accused of self-promotion because the headline result is negative.

---

### 2.9 The dormant and the thin (reported because dormancy is a finding)

**Newfound Research — https://www.thinknewfound.com/ + https://blog.thinknewfound.com/ [VERIFIED, DORMANT].**
Last post **2023-08-28** ("15 Ideas, Frameworks, and Lessons from 15 Years"). Prior: "Is Managed Futures Value-able?" (2023-06-19), "Index Funds Reimagined?" (2023-05-19), "Portfolio Tilts versus Overlays" (2023-04-12), "What Is Managed Futures?" (2023-02-02).

Despite dormancy, **their figure conventions are the best institutional model I found**:
- Sequential **Figure 1–11** numbering
- Bolded descriptive caption **above** each chart
- A standardized **source line under every figure**: *"Source: Kenneth French Data Library, BarclayHedge. Calculations by Newfound Research."*
- Regression tables with significance stars (`*`, `**`, `***`)
- **Block bootstrap: 100,000 ten-year samples** for Information Ratios and MAR ratios
- Conditional/regime analysis (performance during value drawdowns ≥10%)
- Tracking-error sensitivity across allocation ranges
- Appendix A: Index Definitions

**Their standard performance disclaimer, verbatim — the single most reusable sentence block in this file:**
> *"Performance is backtested and hypothetical. Performance is gross of all costs (including, but not limited to, advisor fees, manager fees, taxes, and transaction costs) unless explicitly stated otherwise. Performance assumes the reinvestment of all dividends. Past performance is not indicative of future results."*

Note: **no** Summary/TLDR bullet box at the top of their posts — headings do the work (`Diversifying Value` → `But How Much?` → `What About Other Factors?` → `Conclusion` → `Appendix A`).

Firm-level nav: `About Us / ETFs / Model Portfolios / Podcast / Research (subsections) / Contact Us`, with named research *themes* as landing pages (Liquidity Cascades, Return Stacking, Rebalance Timing Luck) rather than only a chronological feed. **That "named research themes" IA is worth copying** — it turns a blog archive into a body of work.

**Ernie Chan — https://epchan.blogspot.com/ [VERIFIED].** Chairman, QTS Capital Management. Sidebar: books (*Generative AI in Trading and Asset Management*, *Machine Trading*), workshops, @echanQT, subscribe, archives back to **2006**. Recent: "Deep Latent Variable Models" (2025-11-27), "Features Selection in the Age of Generative AI" (2025-10-27), "Deep Reinforcement Learning for Portfolio Optimization" (2025-06-18). Slowed to ~4 posts/year. Posts blend concept + application, link out to Substack for depth and to code examples. **Note the pattern: blog → book → workshop → fund.** That's the standard practitioner monetization ladder; Brad wants the credibility half without the commercial half.

**Eric Falkenstein — https://falkenblog.blogspot.com/ [VERIFIED, DORMANT].** Author of *The Missing Risk Premium* and *Finding Alpha*; prior risk/derivatives work. Last post **2024-06-13** ("A Better Stablecoin on a Perp DEX"). Posts use explicit mechanism specification: leverage/margin/funding-rate formulas, account-balance tables across scenarios, liquidation flow diagrams, historical DeFi exploit case studies. **Strength worth stealing: he explains a market mechanism precisely enough that you could implement it.** That's a different credibility axis from backtesting — it says "I understand how the plumbing actually works."

**Reasonable Deviations — https://reasonabledeviations.com/ [VERIFIED, DORMANT].** Robert Andrew Martin (author of PyPortfolioOpt). Nav: `Home / Post Archive / Projects / Revision Notes / Book Reviews / About`. Last post **2023-02-05**. Quant content (DCF convexity, option-implied probability distributions, Kelly criterion, Monte Carlo) is genuinely good, but it's interleaved with note-taking/productivity/book-review posts. **This is the clearest illustration of the dilution risk: a strong quant archive buried under lifestyle content, on a site that's been dead for 3.5 years.**

**Sergey Malchevskiy — https://malchevskiy.pro/ [VERIFIED] — pure anti-pattern.** Self-description: *"Entrepreneurial Background & AI/ML Product Leader | Algorithmic Trading | MIPT Alumnus."* MIPT applied math/physics master's, President's Scholarship, founded AI Works Lab. Single-page: intro, "random facts" achievement bullets, contact + LinkedIn + CV. **No dated content, no research posts, no code, no charts.** His actual technical work (HMM market-regime modeling, Renko noise reduction, pairs trading with crypto, event-based rebalancing) lives on **Medium**, disconnected from the site. Result: the site is a résumé restatement with a pile of unfalsifiable adjectives, and the evidence is somewhere else. **This is precisely the failure mode Brad's site must avoid.**

**Benn Eifert / QVR Advisors — https://www.qvradvisors.com/ [VERIFIED] — instructive negative case.** Eifert has a PhD (Economics, UC Berkeley), ran quant research and derivatives trading for Wells Fargo's prop desk, co-founded Mariner Coria, and was named to EQDerivatives' *"Top 25 Leaders In Systematic And Volatility Investing"* — selected partly for *"quality of practitioner research published."* And yet **the firm site publishes nothing.** No research, no letters, no dated content, no nav to speak of. Credibility mechanisms are: SEC registration status, *"average 25 years working together,"* and a leadership-experience paragraph. The `/media` page is a **404**. His actual distribution is X/Twitter and podcasts.
**Takeaway:** at his level, the network already knows him; publishing is optional. **Brad is not at that level, so publishing is mandatory** — the site has to do the work that Eifert's reputation does for him.

**Quant Beckman — https://www.quantbeckman.com/ [VERIFIED].** Pseudonymous Substack. Post title format is literally **`[WITH CODE] Backtesting`** — the tag is a promise. Fixed template: cautionary narrative intro → numbered concept sections → technical deep-dive with math → **executable Python blocks** → matplotlib/seaborn outputs → progressively harder validation → paywall cut. Ships a complete `Backtester` class plus `run_monkey_test()` and **`deflated_sharpe_ratio()`**. Demonstrates a strategy at **0.39 daily Sharpe deflating to negative after accounting for 100 trials**.
Verbatim hedges: *"This is not peripheral concern but central flaw"*; *"A strategy that survives this gauntlet is one in which we can have a **moderate degree** of evidence-based confidence"*; *"Passing this test is a **necessary, but not sufficient** condition."*
**"Necessary but not sufficient" is the single most useful phrase in this document.**

**Quantocracy — https://quantocracy.com/ [VERIFIED, ACTIVE DAILY].** *"A curated mashup of quantitative trading links."* Most recent item at fetch time: **2026-08-23, ~1 hour old.** ~120+ source blogs in the blogroll, with per-source click stats (a reported 117 sites cleared 500 clickthroughs in a year). Distribution surfaces: RSS, Twitter/X, Facebook, Threads, Bluesky, StockTwits, plus periodic "Recent Quant Links from Quantocracy as of MM/DD/YYYY" roundup posts.

Blogroll names confirmed on the pages I loaded: Alpha Architect, Quantpedia, **Robot Wealth**, Allocate Smartly, **Flirting with Models** (Newfound), **Jonathan Kinlay**, Morgue Labs, **Investment Idiocy (qoppac)**, Concretum Group, Capital Spectator, Macrosynergy, Beyond Passive, Aligrithm, Quanter Lab, TradeQuantiX, Jan Heger/yizon.

**Actionable:** getting listed on Quantocracy is the cheapest real distribution in this niche, and being adjacent to Carver/Kinlay/Robot Wealth in a daily roundup is itself a credibility signal. Requires a working **RSS feed** — which means Brad's site needs one.

**CSSA (David Varadi) — `[NOT FETCHED, 403]`.** Search index confirms last post **2026-07-27 "The Inflation Compass Model"**, bylined *David Varadi, MBA, CFA*. Prior: "The Growth and Inflation Sector Timing Model" (2025-03-20), "Iterative PSD Shrinkage (IPS)" (2025-01-21). Active, but I could not load it and am not characterizing its internals.

**Alpha Architect — `[NOT FETCHED, 403]`.** Their "Academic Research Insight" series is known for a rigid fixed template (paper title / authors / publication / research questions / academic insights / why it matters / most important chart from the paper), but **I could not load any post to verify the exact headings**, so I am not quoting them.

---

## 3. Synthesis (a): The anatomy of a credible research post — reusable template

Distilled primarily from **Kinlay** (structure + scoped claims), **Carver** (uncertainty + nulls), **Markwick** (reproducibility + data disclosure), **Sinclair** (signal-to-noise realism), and **Newfound** (figure conventions).

```markdown
# <Specific, falsifiable title — a question or a claim, not a topic>
<Author byline> · <Date> · <Estimated read time> · <Tags>

## The question
One paragraph. State the *decision* this affects, not just the curiosity.
"If X is true, I would do Y differently." Name the prior you held going in.

## Data
- Source, named exactly, with vendor/API and access tier
  (e.g. "OptionMetrics IvyDB, 2012-01-03 to 2026-06-30"; "Alpaca free tier, daily bars")
- Universe: enumerated, with inclusion rules
- Sample period, N observations, and what is *excluded* and why
- Known defects: survivorship, stale quotes, corporate actions, vendor revisions
- Point-in-time discipline: what was knowable when

## Method
- The construction, stated tightly enough to reimplement
- Every free parameter listed with its chosen value AND how it was chosen
- **"Number of variants tested before this one: N"**  ← say this out loud
- Baselines: at least one naive and one strong. Name them.
- Costs: bid/ask, commission, slippage, borrow, financing — as explicit numbers
  ("0.10% per trade / 0.20% round-trip") or an explicit statement that they are excluded and why

## Results
- Headline number with an uncertainty attached: `mean ± standard error`, or a CI
  ("Sharpe 0.61, 95% CI [0.12, 1.09]" beats "Sharpe 0.61" every time)
- Table over prose for anything with more than 3 numbers
- One or two figures maximum. Each with:
  title · axis labels with units · a caption above stating the takeaway ·
  a source line below ("Source: … Calculations by <name>.")
- Distributional view, not just central tendency: median + 25th pct, or the histogram

## Robustness
- Out-of-sample: state the split date and that it was chosen *before* fitting
- Walk-forward / multiple IS-OOS windows (Carver runs five combinations)
- Out-of-distribution: a test family structurally unlike the training data
- Bootstrap or block bootstrap for path-dependent statistics
- Multiple-testing adjustment: **Deflated Sharpe Ratio** (Bailey & López de Prado)
  and/or **PBO via CSCV**; cite Harvey-Liu-Zhu; state the trial count used
- Parameter sensitivity: does it survive a ±30% perturbation of every knob?
- The sign test: does the *opposite* rule lose money? If both make money, you fit noise.

## What this shows and does not show      ← NON-NEGOTIABLE SECTION
Bullet list. Every bullet begins "It does not show that…".
Name the specific real-world frictions your setup omitted.
Name the alternative explanation you could not rule out.
State the one experiment that would falsify your conclusion.

## What I'd do next
Ranked. Cheapest decisive test first.

## Code & references
- Link to the exact commit / notebook / script that produced every figure
- Note the runtime and hardware ("self-contained, CPU-friendly, ~8 min")
- Numbered academic references, real citations
```

**Length target:** 1,800–4,500 words. Below ~1,500 it reads as a take; above ~5,000 nobody finishes.

**Two structural slots that appear in essentially every credible post and almost never in a retail one:**
1. **"What this does not show"** — a named, explicit scope-limitation section.
2. **"Failure modes I actually saw"** — the things that broke while you were doing it.

---

## 4. Synthesis (b): the 15 strongest recurring characteristics

Ranked by how much signal each sends to a vol/derivatives hiring manager, relative to how cheap it is to implement.

1. **An explicit "what this does not show" section.** Kinlay does it in every post; Allocate Smartly steelmans against itself. Nothing else so cheaply proves you are not selling something. **Highest ROI item in this document.**
2. **Uncertainty attached to every headline number.** `mean ± standard error`, CIs on correlations and Sharpes, medians and quartiles alongside means. Kinlay reports `0.0184 ± 0.0010` and states the SE formula. Abdelmessih's entire stock-bond post exists to show a correlation's CI is `[+0.02, +0.72]`.
3. **The trial count, disclosed.** "I tested N variants" plus a Deflated Sharpe or PBO adjustment. Almost nobody does this — which is exactly why doing it stands out. The reference implementations (`DSR.py`, CSCV) are sitting on López de Prado's Software page.
4. **Realistic-costs discipline, stated as numbers.** Allocate Smartly's `0.10% per trade / 0.20% round-trip` and 4pm-close execution. Carver reports his *actual* slippage bill and what his execution algo saved (78bp, ~40%). For an options system this means bid/ask, exchange fees, and delta-hedge slippage — quantified, not waved at.
5. **Named data sources with defects acknowledged.** Markwick names the exact API and its 10-year limit; Allocate Smartly explains precisely when simulated pre-ETF data is invalid. Vague provenance reads as either sloppiness or concealment.
6. **Reproducible code tied to the specific result.** Kinlay's ~800-line self-contained "CPU-friendly" script; Markwick's complete inline Julia; Carver's whole open-source `pysystemtrade`. **Linked repos beat inline snippets; inline snippets beat none; screenshots of code are worse than none.**
7. **Published negative results and nulls.** Carver: *"I'm taking the absence of any contradictory evidence as evidence…"* Kinlay discards a metric that gave him the answer he wanted because it had no null. Allocate Smartly's entire "Beware Strategies That Fall Down on Good Data" is a demolition.
8. **A strong, named baseline that the fancy method has to beat.** Kinlay's CNN is benchmarked against plain interpolation — and he reports that the gap is *small* and may not survive real data.
9. **Downstream evaluation.** Does the improvement survive to the task you actually care about? Kinlay checks whether repaired surfaces produce better SVI fits, not just lower RMSE. For Brad: does a better vol forecast produce better *P&L after hedging costs*, not just lower MSE.
10. **Sample-size and power realism.** Sinclair's post is entirely this: `n₁ ≈ 1260 vs n₂ ≈ 21`, daily Sharpe ≈ 0.03, therefore you cannot detect what you think you're detecting. Longmore's independent version: at Sharpe ≈ 1, multi-year drawdowns are expected. **Demonstrating you understand this is a stronger hire signal than any backtest.**
11. **Credentials stated as facts, in four sentences or fewer.** Sinclair's Risk.net bio is the template: years → instruments → seat → credential + artifacts. Kinlay attributes his ranking to a named third party (FIMAT) and dates it (2004). No adjectives.
12. **Consistent figure conventions.** Newfound: sequential Figure N, bold caption above, standardized source line below, "Calculations by <name>." Cheap, and it makes an amateur site read as a research shop.
13. **A named body of work, not just a feed.** Newfound's themed research landing pages (Liquidity Cascades, Rebalance Timing Luck); Robot Wealth's "Index of Strategies"; Moontower's topic tags. A chronological blog decays; a themed index compounds.
14. **Replication of a named paper, with the delta reported.** Markwick replicates Baltas's *Cross-Asset Skew*, cites it, and says plainly *"the results are not as conclusive as the original paper."* Replication is the safest possible first post: it proves competence with zero risk of an unfalsifiable claim.
15. **Working RSS + Quantocracy listing.** The one distribution move that puts you in the same daily roundup as Carver and Kinlay. Requires only a feed.

**Runners-up worth noting:** a bias-disclosure aside when you have a position in the thing you're analyzing (Abdelmessih's italic "Aside"); explicit disclaimers that you are not regulated and do not sell advice (Carver's all-caps *"ROBERT DOES NOT OFFER TRADING COURSES"*); and stating conservatism you deliberately built in (Allocate Smartly's 2-day dividend-knowledge lag).

---

## 5. Synthesis (c): phrasing and caveating conventions worth copying

### Scope limitation (Kinlay — use this exact construction)
- "It does not show that ___ is useful on real data."
- "It does not show that ___ is the right architecture for this task."
- "It does not, on its own, justify a production system."
- "Whether ___ survives a real-data test is an open question."
- "The synthetic surfaces have no calibration drift, no quote-time-of-day noise, no microstructure asymmetries."

### Calibrated confidence in a result
- "I would not defend it further than 'worth running properly.'"
- "should be read as an order of magnitude, not a point estimate"
- "Treat the *ordering* as the result and the *levels* as approximate."
- "I would not swear to it."
- "This is a small one, and it does not come out where I expected."
- "necessary, but not sufficient" (Quant Beckman)
- "a moderate degree of evidence-based confidence" (Quant Beckman)

### Conceding weak evidence while still using it (Abdelmessih)
- "There's enough evidence to not disagree."
- "It's hard to bang on the ___ desk with fervor."
- "It is entirely possible that ___."
- "This is hard to translate into risk-adjusted, opportunity-cost-aware terms."

### Naming your own model's failure mode (Kinlay)
- "The heteroscedastic head undercovers."
- "The convergence is slow and the validation curve is still improving slightly at epoch 60."
- "This says the model's residual is not, on its own, a strong ___ detector."

### Reporting a null honestly (Carver)
- "I'm taking the absence of any contradictory evidence as evidence that I should continue to do what I've done before."
- "we unfortunately can't reject the null hypothesis" (Robot Wealth)
- "admittedly does not look overly stationary" (Robot Wealth)

### Flagging a deliberately deferred problem (Markwick)
- "We have neglected the trading costs and potential capacity."
- "…but that is a problem to solve for another day."
- "this is a promising sign that there is perhaps something more to be done"

### Steelmanning against yourself (Allocate Smartly)
- "Is it possible that a weak edge existed in our 30-year test, but it was hidden by imperfections in the data? Absolutely."

### Explaining a deviation from your own standard
- "Unlike other tests on this site, transaction costs have been excluded, because we don't want to confuse the point."

### On the impossibility of certain inferences (Sinclair)
- "The test confidently says 'nothing to see here.' It's technically correct."
- "The conclusion isn't that tests are bad — it's that the problem is mis-specified."
- "The answer is always probabilistic, never definitive."

### Boilerplate disclaimer (Newfound — copy verbatim, adapted)
> "Performance is backtested and hypothetical. Performance is gross of all costs (including, but not limited to, advisor fees, manager fees, taxes, and transaction costs) unless explicitly stated otherwise. Performance assumes the reinvestment of all dividends. Past performance is not indicative of future results."

### Non-solicitation / not-regulated (Carver)
> "Not regulated or authorised to provide investment advice." + an explicit statement that you do not sell courses or signals.

### Words to delete on sight
"proven," "consistently," "robust" (unqualified), "proprietary," "cutting-edge," "passionate about," "significant returns," "battle-tested," "alpha-generating," any Sharpe stated without a period, a cost assumption, and an interval.

---

## 6. Synthesis (d): how a live track record is credibly presented — and how it is presented badly

### The credible version (Carver's twelve-year series is the reference implementation)

**1. Lead with the worst number, not the best.**
Year 11 TLDR opens with **"it's my worst ever"** / **"my worst ever in futures."** A track record that only surfaces in good years is not a track record.

**2. State the exact accounting basis.**
Mark-to-market **vs** net-of-everything, side by side: *+21.9% mark-to-market, +23.7% net of fees, commissions and slippage.* Say which one the headline is. Say the currency. Say the period boundaries (his run on the UK tax year, April 6 – April 5, and he says so).

**3. Decompose the P&L.**
Year 11: **−16.3% total** = **−14.5%** futures + **−0.64%** cash-like ETFs + **−2.7%** FX. Then by market (Equities −6.0%, Agriculture +3.2%, …) and by trading rule. Decomposition is the strongest anti-cherry-picking signal available, because it exposes every component including the losers.

**4. Benchmark against named third-party indices, vol-adjusted.**
SG CTA Index and AHL, with **correlations** (0.68 and 0.56) — which simultaneously proves he isn't just levered beta and situates his result in the peer distribution. In the bad year: his −16.3% against SG CTA ~−18% and AHL −18.2%. In the good year he says plainly *"I was actually the worse of the three for this year at least."*

**5. Report costs as a first-class result.**
*"Without my execution algo, if I had just traded at the market, I would have paid 1.34% in slippage; my simple algo earned 78bp and cut my slippage bill by around 40%."* Nothing else so quickly establishes that live results are real.

**6. Deduct the risk-free rate, or say you didn't.**
Carver explicitly notes his Sharpes *"would be lower if a risk-free rate were deducted."*

**7. Show the full path, not a summary stat.**
Non-compounded equity curve (monthly and annual), plus a year-by-year table across all twelve years marking best and worst.

**8. Admit discretionary errors by name.**
*"(yes, bad move in retrospect, and another failure of discretionary trading on my part)."*

### What Brad should add that even Carver doesn't do

These are genuine gaps in the best example available, and closing them is differentiation:

- **An explicit live-vs-backtest overlay.** Carver never charts realized against the backtest that motivated the system. For someone building from scratch with an explicitly documented research process, this is *the* chart: backtest equity curve, a hard vertical line at the go-live date, realized path after it, and the honest gap quantified.
- **A confidence interval on his own realized Sharpe.** With N months of live data, `SE(SR) ≈ √((1 + SR²/2)/N)` — publish the interval. On 18 months of data it will be humiliatingly wide, and publishing it anyway is the single most credible thing on the page.
- **A pre-registered, frozen definition.** "This strategy's parameters were frozen on <date>; the config hash is <hash>; nothing below has been re-fit." Verifiable via git history. This is the strongest available answer to "how do I know you didn't tweak it?"
- **A no-changes log.** Every intervention, override, or parameter change, dated, with the reason. Silence about changes reads as changes concealed.

### How it is presented badly (observed in this research)

- **Dashboards without methodology.** Vol Vibes publishes "Option Strategy Returns & Sharpe" monthly with no visible backtest period, data source, construction rules, or cost assumptions — and the substance behind a paywall. A vol PM cannot evaluate it, so they discount it entirely.
- **No byline.** The Hull Tactical blog is well-written and has no author attribution on any post I loaded. Unattributed research accrues to nobody.
- **Cumulative-return-only presentation.** A big up-and-to-the-right number with no vol, no drawdown, no Sharpe, no benchmark, no costs.
- **Headline Sharpe with no interval and no trial count.** The instant tell for backtest overfitting — Quant Beckman's demo shows a 0.39 daily Sharpe deflating *below zero* once 100 trials are accounted for.
- **Gross-of-costs framed as live.** Any results section that doesn't state its cost assumption is assumed to have none.
- **Restarted or re-based track records.** Presenting a fresh start date without disclosing what came before.
- **Credential inflation in place of evidence** (malchevskiy.pro): a résumé restatement with adjectives and no dated, falsifiable artifact anywhere on the site.
- **Mixed-topic dilution** (reasonabledeviations.com): real quant work interleaved with productivity and book-review posts, so nothing reads as a body of work.
- **Dormancy.** Newfound (last post Aug 2023), Falkenblog (Jun 2024), Reasonable Deviations (Feb 2023). A visibly stale research section is worse than no research section — it reads as an abandoned project. **If Brad ships a research feed, he must sustain it; if he can't sustain cadence, he should present a fixed set of finished pieces with no dates implying a schedule.**

---

## 7. Concrete recommendations for bradlasater.github.io

1. **Every research post gets a byline and a date.** Non-negotiable. (Anti-Hull-Tactical.)
2. **Adopt the Kinlay skeleton verbatim** — including a literal `## What this shows and does not show` section in every post. It's the single highest-signal, lowest-cost move available.
3. **Add a `/code` page in the López de Prado style**: named, dated implementations, each linked to the write-up it produced. Include his `DSR.py`-equivalent and a PBO/CSCV run applied to Brad's *own* strategy, and say the trial count.
4. **Publish RSS and submit to Quantocracy.** Cheapest real distribution in this niche.
5. **Write one Allocate-Smartly-style demolition post**: take a widely cited vol result (short-vol VRP harvesting, 0DTE premium selling, VIX term-structure roll) and re-run it under honest costs and OOS discipline. Negative or heavily-qualified result. Impossible to read as self-promotion, and it demonstrates every skill at once.
6. **Write one Sinclair-style power post** using Brad's own live sample: "here is how long I would need to run before I could statistically distinguish my system from zero." Publish the number even if it's five years.
7. **Adopt Newfound's figure conventions** — Figure N, bold caption above, source line below with "Calculations by Brad Lasater."
8. **Restructure the live track record section** around: worst number first → accounting basis → decomposition → third-party benchmark with correlation → costs as a result → live-vs-backtest overlay with the go-live line → CI on realized Sharpe → frozen-config hash → change log.
9. **Ship the Newfound disclaimer block** under any backtested chart, and Carver's not-regulated/not-selling-anything statement in the footer.
10. **Do not mix topics.** One audience, one body of work.
11. **Name the research themes** (à la Newfound's Liquidity Cascades / Rebalance Timing Luck) so the archive reads as a program rather than a feed.
12. **Model the bio on Sinclair's four sentences.** Years → what you actually worked on → current seat → credentials + artifacts. Zero adjectives.

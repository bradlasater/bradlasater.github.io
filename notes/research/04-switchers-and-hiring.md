# Research 04 — Career-Switcher Exemplars & Hiring-Side Signals

Research date: 2026-08-23. Every URL below was fetched and read before citing. Sources are
labeled by evidence tier:

- **[A] Firm-official** — published by the hiring firm itself.
- **[B] Named practitioner** — an identifiable person with a verifiable industry role.
- **[C] Commercial / anonymous** — content-marketing sites, anonymous newsletters, recruiter
  marketing pages. Directionally useful, weakest evidence.

**Access failures (stated honestly):** `reddit.com` is blocked to this crawler entirely
(r/quant, r/quantfinance, r/algotrading could not be read). `quantnet.com` returns HTTP 403
to automated fetches — the QuantNet threads that appeared in search results (including
"Top 3 Resume Mistakes I See MFEs Make" and the buy-side QR AMA) could **not** be verified
and are therefore **not cited anywhere below**. Wilmott and NuclearPhynance yielded nothing
loadable. So this report is deliberately light on anonymous forum opinion and heavy on
firm-official and named-practitioner sources — which is the right weighting anyway.

---

# HALF 1 — CAREER-SWITCHER EXEMPLARS

## Tier 1: Strong analogues for Brad (technical field → quant, public site)

### 1. Ray — https://oneraynyday.github.io/about/
- **Prior field → current role:** UCLA computer science → **"Algorithm Engineer" at Hudson
  River Trading, New York.** Prior internships: Airbnb, Citadel Securities, Bloomberg; one
  year on Airbnb's ML infrastructure team.
- **Site structure:** Minimal Jekyll blog. Nav = Home / About / GitHub / Categories. No
  project gallery, no resume page, no "hire me" framing.
- **First-screenful positioning (exact):** *"Hi, my name is Ray and this is my blog for math
  and CS related topics. I believe that you don't really know what you're talking about
  unless you can present the information in a digestible and intuitive way."*
- **What's showcased:** Expository math/CS posts, not projects. He notes the blog gained
  traction on Reddit and Hacker News and has been translated into multiple languages.
- **Self-description of intent (exact):** he blogs *"because I'm too lazy to take on some
  huge project and just want to chill and learn some fun stuff."*
- **Why the transition reads as credible:** He does **not** try to prove he can trade. He
  proves he can *explain hard technical material clearly*, and lets HRT on the resume carry
  the finance credibility. **The site is a thinking-quality artifact, not a track record.**
  This is the single most important structural lesson in this whole report.

### 2. Kris Longmore — https://robotwealth.com/about-robot-wealth/
- **Prior field → current role (his words):** *"I started as an engineer, the kind that
  builds things in the physical world."* Now: *"I trade a portfolio of systematic strategies
  for my own account, and I share the strategies, the research, the tools and the thinking
  with the hundreds of independent quants in RW Pro."* In between: proprietary trader, hedge
  fund quant, freelance researcher, **equity partner at a proprietary trading firm.**
- **First-screenful positioning (exact):** *"Robot Wealth is the research lab and shared
  infrastructure for independent quants: technically minded traders who research and run
  systematic strategies on their own terms."*
- **The credibility bridge — he leads with his own failures (exact):** *"Trading began as a
  side interest. What followed was years of every beginner mistake in the book: chart
  patterns, then increasingly elaborate backtests. Eventually I was throwing machine learning
  at market data and calling it research."*
- **The pivot (exact):** a professional trader asked him *"What's your edge?"* — *"I had no
  answer. That question rebuilt my approach from the ground up."*
- **Why it works:** The confession *is* the credential. By narrating precisely how he
  over-fit and over-engineered, he demonstrates he now knows the difference — which is the
  exact thing a quant hiring manager is trying to determine. He does not present headline
  return numbers on the about page at all.
- **Caveat for Brad:** Longmore's business is education/community, so his framing is tuned
  to sell subscriptions, not to get hired. Borrow the failure-narrative structure, not the
  commercial tone.

### 3. Ernie Chan — https://epchan.com/
- **Prior field → current role:** BSc Physics (Toronto), **PhD theoretical physics (Cornell)**
  → ML researcher at IBM T.J. Watson Research Center (Human Language Technologies) →
  Morgan Stanley AI group in Manhattan → Credit Suisse → founded QTS Capital Management
  (2011) → Founder/Chief Scientist, PredictNow.ai.
- **Site structure:** Corporate-consultancy layout, not a blog-first personal site. Nav =
  Home / Financial Machine Learning / Workshops / Books / About / Contact. Hero: "E.P. Chan
  & Associates" + portrait + tagline about AI and quantitative analytics. Self-description:
  *"an expert in machine learning and the application of quantitative models for asset
  management."*
- **Notable:** the physics-to-quant story is **absent from the homepage.** The site sells
  present-day authority (books, workshops, media), not the transition narrative.
- **Third-party verification & the key career quote** —
  https://databento.com/blog/quants-worth-following-ernie-chan : *"With a PhD in theoretical
  physics from Cornell University, Ernie's early work as a machine learning researcher at
  IBM's T.J. Watson Research Center's Human Language Technologies division facilitated his
  transition into the quant industry."* And, critically, Chan on where his work comes from:
  **_"Everybody that I have worked with since I became an independent trader is inbound...
  These traders reached out to me because of the books I published."_**
- **Lesson:** public artifacts *do* generate inbound — but the artifact that did it was
  three published Wiley books, not a website. This is a high bar, and honest evidence about
  the effort level required.

### 4. Harel Jacobson — https://volquant.medium.com/ (+ verified interview below)
- **Prior field → current role:** BA in economics → support representative at
  SuperDerivatives → self-taught quant → quant trader → **quantitative portfolio manager
  running a global volatility and systematic strategies book at Oporto Delta.** FX and rates
  vol specialist.
- **His own account of the transition (exact, from
  https://tradingtechnologies.com/blog/2021/02/08/5-questions-with-harel-jacobson-of-oporto-delta/ ):**
  - *"My first interaction with the derivatives market was during the second year of my BA in
    economics. I started working as a support representative at SuperDerivatives"*
  - *"I decided to teach myself quantitative disciplines, mainly math and statistics/
    probability theory, and coding."*
  - *"After gaining confidence in my abilities, and after I built and backtested my first
    trading strategy"* …
  - *"I joined my former boss as a quant trader under his mentorship. After my mentor left
    that firm, I stayed and moved up to portfolio manager."*
- **What he publishes:** vol-specific research under the handle **VolQuant** — including
  post-mortems: *"Epic Failures — Lessons from Volatility Funds blow-ups"* and *"Beware of
  the traps — Quantitative Trading Mistakes."*
- **Two lessons, one supportive and one deflating:**
  1. **Supportive:** his *published corpus is topically identical to Brad's target* — vol
     surfaces, vol modeling, blow-up post-mortems. Writing vol post-mortems is a recognized
     way to establish a vol-trading identity.
  2. **Deflating and important:** the writing came *after* the job. **The job came from a
     mentor/referral relationship**, not from public writing.

### 5. Vivek Palaniappan — https://engineerquant.substack.com/about
- **Prior field → current role (exact):** *"studied Engineering but now work as a trader at
  a hedge fund"*.
- **Positioning (exact):** *"I use this substack to explore interesting topics in Machine
  Learning, Mathematics, Physics and occasionally Neuroscience."*
- **Structure:** newsletter, essay-first. The engineer→trader fact is a single clause in a
  one-paragraph bio; the *content* is technical exposition.
- **Lesson:** same pattern as Ray. The switch is stated flatly and briefly, then never argued
  for again — the writing is the argument.

### 6. Jakub — https://quantjourney.substack.com/about
- **Prior field → current role:** **"a physicist-turned-quantitative trader"** with 20+ years
  across hedge funds, prop firms, and technology companies.
- **Positioning (exact):** *"With over 20 years of experience across hedge funds, proprietary
  trading firms, and leading technology companies, I've dedicated my career to mastering
  systematic trading and building the robust infrastructure it demands."*
- **Bridge language (exact):** bridging *"scientific rigor with practical trading expertise."*
- **The concrete proof artifact:** a *"hedge-fund-caliber system"* comprising **"over 80,000
  lines of meticulously tested code."**
- **Lesson for Brad:** *"meticulously tested"* is doing real work in that sentence. The claim
  is about **engineering discipline**, which is verifiable and unfalsifiable-in-a-bad-way,
  rather than about returns, which invite scrutiny. Note also that "physicist-turned-
  quantitative trader" is a four-word bridge that does the entire positioning job.

## Tier 2: Structural exemplars (useful shape, weaker bridge)

### 7. Letian Wang — https://letianzj.github.io/
- Headline: *"Letian Wang Blog on Quant Trading and Portfolio Management."* Tagline:
  *"a place dedicated to quantitative trading and systematic investing."*
- Structure: Home / Archives / Sitemap, with content hierarchically categorized into
  Systematic Investment, Quantitative Trading, Machine Learning, Time Series, Order Flow.
- Showcases two named open-source assets: **`quanttrader`** (positioned as *"a pure
  python-based event-driven backtest and live trading package for quant traders"*, on
  GitHub + PyPI) and the **QuantResearch** repo.
- Results/code: narrative-first on the blog, with Jupyter notebooks and video demos, linking
  out to Medium and GitHub for full implementations.
- **Lesson:** a *named, installable library* is a much harder credential than a folder of
  notebooks. The taxonomy (order flow / time series / systematic investment) also signals
  market-domain literacy before you read a single post.

### 8. Mark Best — https://markrbest.github.io/
- ~20 years programming (Java, R, Matlab, Python, C++, Rust); previously **Deutsche Bank
  algorithmic trading**; fixed-income + HFT background; now an independent quant trader in
  crypto.
- Tagline: *"Quantitative Trading – Trading ideas and discussions."* Nav = Links / About /
  Archive, reverse-chronological.
- Content is operational and unglamorous — OMS hazards, Rust logging optimization, message
  arrival rates and latency, data handling — mixed with theory (fractional differencing,
  MCMC), Bitcoin microstructure, vol analysis, mean reversion. Presents code snippets and
  statistical tables.
- **Lesson:** posts about *the boring failure modes of running a system* (order management
  dangers, logging, latency under message-rate spikes) read as operator experience. Almost
  nobody fakes these, so they are high-signal.

### 9. Jonathan Shore — https://tr8dr.github.io/about/
- **About text (exact, complete):** *"These are my musings about strategies, statistics,
  computer science, numerical techniques, etc. I am a quant / developer, living in the New
  York area."*
- Background: parallel algorithms / applied math → Lehman Brothers research group in the
  1990s (neural nets, VR, parallel processing, NLP for trading and risk) → complex
  derivatives → algo trading from the mid-2000s. NYC-based.
- Nav = Data / Links / About.
- **Lesson:** the entire self-description is two sentences and one of them is a location. A
  reader who wants credentials goes to LinkedIn; the site is for the work. This is the
  opposite of the "portfolio site" instinct and it is what senior practitioners actually do.

### 10. Jonathan Kinlay — https://jonathankinlay.com/
- Tagline: *"The latest theories, models and investment strategies in quantitative research
  and trading."* Nav = Home / Systematic Strategies / About.
- Research depth is genuinely high: full Python implementations, detailed experimental
  protocols with validation suites, quantified results **with confidence intervals**, and
  **explicit limitation sections acknowledging confounds.** Recent topics: LLM agents in
  alpha research and crowding risk, agentic research workflows, RL for trade execution,
  deep learning for vol-surface interpolation.
- Reports negative results and failure modes; quantifies catch rates; caveats claims like a
  "2× lift" with the confounds attached rather than selling it.
- **Lesson — this is the closest model for how Brad should present results.** Confidence
  intervals + a limitations section + published negative results is the single most
  quant-legible way to say "I am not fooling myself."

### 11. Anthony Makarewicz — https://anthonymakarewicz.github.io/volatility-trading/
  and https://github.com/anthonymakarewicz/volatility-trading
- **The closest topical analogue to Brad's system that exists in public.** README opening
  (exact): *"This project develops and evaluates daily options-volatility strategies on index
  and single-stock underlyings."*
- Scope: ORATS ETL data pipeline (API/FTP download, extraction, chain building, QC);
  `src/volatility_trading/` with backtesting, options modeling, signal generation, strategies;
  `notebooks/` research; `examples/` executable scripts; YAML config templates; `docs/` with
  API scope and data contracts.
- **Backtest realism:** bid/ask spreads, slippage, configurable per-leg commissions, position
  sizing tied to risk budgets, Reg-T margin constraints, delta hedging with dynamic rebalance
  policies, and transaction-cost attribution split across option and hedge legs.
- **Two strategies:** VRP harvesting (realized vs. implied) and skew mispricing.
- **Out-of-sample:** RV forecasting reported at *"about 30% OOS R²"* versus naive baselines.
- Published as reproducible HTML notebook reports on GitHub Pages.
- **What's excellent:** the cost model, the Reg-T margin constraint, and the per-leg cost
  attribution are exactly the details that separate a real vol backtest from a toy one.
  Reporting **OOS R² against a naive baseline** rather than a headline Sharpe is exactly
  right.
- **What's broken — and this is the lesson:** the GitHub Pages site's entire first screenful
  is the heading **"Notebook Reports"** followed by six bare links (`greeks.html`,
  `iv_surface_modelling.html`, `rv_forecasting.html`, `vrp_harvesting.html`, `qc_eda.html`,
  `skew_trading.html`). No author name, no bio, no framing, no summary of findings, no
  navigation. **The research is strong and the site converts none of it.** A recruiter
  landing there learns nothing and leaves. Brad should read this as: *the research artifact
  and the persuasion artifact are two different deliverables, and doing only the first is
  the default failure mode for technically strong people.*

### 12. Ricki Heicklen — https://rickiheicklen.com/
- Former Jane Street quantitative trader; now runs the Arbor trading bootcamp; writes at
  bayesshammai.substack.com.
- Minimal centered layout, photo, a few paragraphs. Positioning (exact): *"My background is
  in quantitative trading, and I spend a lot of time thinking about markets, incentives, and
  human dynamics."* She describes being in an "explore" stage, *"splitting my time between
  NYC and the Bay Area as I rotate through different jobs and projects."*
- **Notably, Jane Street is not named on the page.** The credibility is carried by the
  *quality of the trading-education work* she links to.
- **Lesson:** once the work is good enough, the employer logo becomes optional. Brad is not
  there yet and should name Nift / Ticketmaster / Lockheed / Boeing — but the direction of
  travel is toward letting artifacts carry the weight.

## Tier 3: Instructive negative examples

### 13. Dev Kewlani — https://dev-kewlani.github.io/
- Positions as "Quantitative Researcher & Trader." Quant Summer Associate at JPMorgan; prior
  NX Block Trades, BlackRock, Futures First. Single-page portfolio: About / Experience /
  Projects / Skills / Contact, with LinkedIn / GitHub / resume links.
- Four featured projects with headline metrics:
  - AlphaPortfolio — deep RL with transformers, **"1.7 Sharpe Ratio"**
  - Pure Momentum — crypto arbitrage, **"250%+ annual returns (pre-costs)"**, hourly rebalance
  - Options backtesting framework — **"10x speed improvement over existing solutions"**
  - Loss Given Default model — XGBoost on mortgage data, **"65% accuracy"**
- **Why this is the anti-pattern:** metrics are asserted without validation methodology, code
  samples, walk-forward or cross-validation procedure, live verification, or trial counts.
  "250%+ annual returns (pre-costs)" on an hourly-rebalanced crypto strategy is a number that
  *invites* a hostile question, and "pre-costs" on an hourly strategy is close to an
  admission that the strategy does not survive costs. To the audience Brad is targeting,
  this reads as *not knowing what would make the claim credible* — which is worse than
  claiming nothing.
- **Direct instruction for Brad:** every performance number on his site must arrive with
  (a) sample period, (b) in-sample vs. out-of-sample split, (c) cost and slippage
  assumptions, (d) the number of variants tried before this one, and (e) capacity/risk
  limits. A number without those five is a liability, not an asset.

### 14. Chakradhar Rangi — https://crangi.github.io/
- Physics PhD candidate (LSU, computational physics / condensed matter), BS-MS from IISER
  Bhopal, internships at Los Alamos and JNCASR, peer reviewer for Physical Review B/A/Research
  and Chaos. Hugo site on GitHub Pages: Home / Posts / Projects / Publications / Contact / Notes.
- Among six projects: an **MBS convexity** quant-finance framework and a **"Quant Finance
  Bootcamp"** set of mini-projects in portfolio theory and risk management, alongside DMFT
  and domain-adaptation work.
- **Where it fails for a quant audience:** the finance projects are presented in **academic-CV
  format** — title, thumbnail, one-line description, GitHub link. No backtesting results, no
  out-of-sample validation, no risk discussion, no performance comparison. The physics work
  has real citations (`Phys. Rev. B 112, 245137`); the finance work has nothing equivalent.
- **Lesson:** an academic portfolio template actively hurts a quant pitch. It signals
  "I did some finance coursework," not "I can do research a desk would trust." Brad, coming
  from industry rather than academia, should avoid the publications-and-projects-grid layout
  entirely.

### 15. Shashank Hegde — https://hegde95.github.io/
- Self-description: *"Researcher, Roboticist, PhD Candidate, Musician."* AI PhD researcher at
  USC's Robotics Embedded Systems Lab (deep RL, ML, robotics). Employment history includes
  **Fidelity Investments**, developing ML for trade order selection and execution, and work
  with fixed-income research teams.
- Site is a full academic portfolio: About / Experiences / Publications (topic-filtered) /
  Projects / Skills / Education / Accomplishments & Service. Projects span autonomous vehicle
  navigation, quadruped hurdling, prosthetic voice control, multi-agent RL, MFCC/spectrogram
  work. Metrics reported are ML-native (compression ratios, "1/45th of inference-time FLOPS").
- **Marginal as an analogue, but one useful data point:** he has genuine execution-side
  finance experience (ML for trade order selection) and it is **buried in a reverse-chron
  experience list** among robotics work. The finance-relevant item is the one a quant reader
  wants and it is not surfaced. Brad's Nift/Ticketmaster/Lockheed work has the same risk:
  the market-relevant parts (state estimation under noise, real-time optimization, latency,
  sensor fusion) must be pulled to the top and translated, or they will be read as
  "unrelated ML resume."

---

# HALF 2 — HIRING-SIDE SIGNALS

## [A] Firm-official statements

### Jane Street — https://www.janestreet.com/join-jane-street/interviewing/
The single most explicit firm-official statement on career switchers found anywhere:

- Quantitative Trading section, verbatim: **"Problem-solving mindset: required. Finance
  background: optional."** and *"We're looking for strong quantitative minds and collaborative
  team players to work in Quantitative Trading. **We won't test you on knowledge of finance or
  economics.** Instead, we'll try to get a sense of what it's like to work with you to solve
  a problem."*
- Quantitative Research section: *"Part trader, part engineer, all encompassing — The work our
  researchers do overlaps both trading and software engineering, so the interview process is
  a mix of the two."*
- FAQ, verbatim: **"Do I need a background in finance? Nope! But those with previous finance
  experience are of course welcome to apply."**
- FAQ, verbatim: **"Do I need a cover letter? Nope!"** — *"If there's something you think we
  should know about that doesn't fit nicely onto your resume/CV, feel free to include it in
  the text box at the bottom of our application."*
- Recruiter Kristen (NY office), verbatim: *"There are no real requirements to apply to any of
  our campus positions. We're always just looking for interesting resumes from intellectually
  curious students. You don't need to know OCaml. **You don't need experience within finance.
  We'll teach you everything you need to know.**"*
- On reapplying: *"Plenty of people who currently work at Jane Street didn't make it through
  our interview process their first time around."*
- Also: *"We consider applicants for every open role, not just the one you apply for"* and
  *"We believe that asking great questions is more important than knowing all the answers."*
- **Critical negative finding:** across the entire interviewing page and a ~25-question FAQ,
  Jane Street mentions **personal websites, blogs, GitHub, and side projects exactly zero
  times.** The artifacts they name are: the resume, the free-text box, and the interview.

### Two Sigma — job posting, Quantitative Researcher Intern (NYC)
https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-Quantitative-Researcher-Intern-2027-Summer/13945

Verbatim: **"You don't need a background in finance. It's nice to have, but more than half of
Two Sigma's employees come from outside the finance industry. If you've got the quantitative
skills, we can teach you the financial aspects of the job."**

Listed qualifications, verbatim, include:
- *"Are pursuing a degree in a technical or quantitative disciplines, like statistics,
  mathematics, physics, electrical engineering, or computer science"*
- *"Demonstrate intermediate skills in at least one programming language (like C, C++, Java,
  or Python)"*
- **"Performed an in-depth research project, examining real-world data"**
- *"Are an independent thinker who can creatively approach data analysis and communicate
  complex ideas clearly"*

**This is the most directly exploitable line in the entire report.** A firm-official
qualification bullet asks for *an in-depth research project on real-world data.* Brad's vol
system is literally that. The site's job is to make that mapping instant and undeniable.

### Two Sigma — "From STEM to Finance: Employees Share Their Stories"
https://www.twosigma.com/articles/from-stem-to-finance-employees-share-their-stories/

Two Sigma's own switcher-framing examples:
- **Mike**, Head of AI Core, from a long career at Google (speech recognition / AI):
  *"When I came here, we said, hey, let's do a similar thing in finance, because I think
  finance is ripe for this kind of change."*
- **Rob**, Security Architect, from the intelligence community: *"When I came here, I quickly
  realized that the basic problem set is very similar, in that it's about protecting very
  sensitive and valuable information."*
- **Katie**, Product Manager, from mechanical engineering.
- **Jiasen**, Quantitative Researcher (Macro Techniques): *"Financial sciences is simply
  applying the scientific approach to everything we do that's related to finance."*
- **Ris**, MD Engineering (CS background): *"The tools that we're building are similar to what
  you'd see at other large-scale tech companies."*

**The rhetorical pattern the firm itself endorses is isomorphism: "the underlying problem is
the same, only the domain changed."** Rob's intelligence-community line is almost exactly the
sentence Brad should be able to write about Lockheed/Boeing state estimation vs. filtering a
noisy price/vol signal.

### D. E. Shaw — Quantitative Analyst, NYC
https://www.deshaw.com/careers/quantitative-analyst-2636
- Verbatim: *"Successful candidates will have impressive records of academic achievement and
  be the top students in their respective math, statistics, physics, engineering, computer
  science, and other technical and quantitative programs."*
- Finance experience is not listed as a requirement.
- **Stated base salary: "$275,000" for undergraduate/master's and "$300,000" for PhDs (or
  comparable professional experience).**
- **Calibration for Brad:** his ~$250k base target is *below* the published entry-level QA
  base at D. E. Shaw in NYC. That target is realistic — arguably conservative — for a QR/QD
  role. It also means he is competing in a pool where the firm's default assumption is
  "top student in a technical program," so his differentiator has to be *demonstrated applied
  research*, not credentials.

### Susquehanna (SIG) — https://sig.com/careers/quant/
Verbatim: **"The ability to develop a new idea or approach to a problem is far more valued
than having a preexisting knowledge of finance."**

Also: *"Susquehanna provides ample resources to aide with learning about finance, including a
3-month long class in finance, a mentorship program, and a starter project designed to help
cut one's teeth in finance."*

**Note the implication:** if a firm budgets three months to teach finance, then *finance
knowledge is not the scarce input they are screening for.* Original problem-framing is. This
argues against Brad's site being primarily a demonstration that he has learned options theory,
and for it being a demonstration that he asks good questions and designs good experiments.

### Optiver — https://www.optiver.com/join-us/students/internships/research/
What they evaluate, per the firm: *"Comfort with uncertainty and risk"*, *"Production
mindset"*, *"Ability to iterate quickly"*, *"Clear communication across disciplines"*,
*"Curiosity and ownership."* They seek people *"comfortable reasoning about noisy data,
imperfect signals, and risk"* and who *"don't wait to be told what to do next"* but
*"explore, ask questions, and take initiative."* The program *"begins with comprehensive
training, where you'll learn trading fundamentals"* — again, finance taught in-house.

**"Comfortable reasoning about noisy data, imperfect signals, and risk" is a literal
description of state estimation work.** This is the phrase Brad's Lockheed/Boeing experience
should be translated into.

### Hudson River Trading — "Answers to Questions I Often Get: Engineering and Interviewing at HRT"
https://www.hudsonrivertrading.com/hrtbeat/engineering-and-interviewing-at-hrt/ (Joe Smith)
- **"We rate our engineers as much on communication as we do on technical ability."**
- **"We want engineers with strong fundamentals but stay away from obscura and 'tricks'."**
- **"Most people do not fail the interview because they lack some specialized piece of
  knowledge."** The stated most common failure is *shallow* understanding of fundamentals —
  candidates should grasp *why* a tool was invented, not just how to use it.
- *"We expect engineers and engineering managers to make individual contributions on a
  quarterly basis."* Same technical tests are administered regardless of seniority.
- **No mention of portfolios, side projects, GitHub, or personal sites.**

### Hudson River Trading — "In Trading, Machine Learning Benchmarks Don't Track What You Care About"
https://www.hudsonrivertrading.com/hrtbeat/trading-machine-learning/ (Iain Dunning)
This is the most useful firm-official statement of *research taste* found, and it maps
directly onto how Brad should present results:
- *"an incremental 0.1% improvement in the accuracy of a neural network's ability to
  distinguish dog breeds might not translate to predicting the price of a stock."*
- HRT evaluates papers on **"simplicity, reproducibility, and generality."**
- **"we still have the issue of statistical power... it is easy to lie to ourselves while
  resolving small differences in our low signal-to-noise domain."**
- *"weak improvements will not generalize 'out of sample' to other instances in the space of
  deep learning problems."*
- *"subtle differences in the exact evaluation protocol can completely invert results"*
  (citing Agarwal et al. on deep RL evaluation standards).
- They run *"standardized ways we run 'backtests' internally for our changes."*

**Takeaway:** "simplicity, reproducibility, and generality" is a hiring firm handing Brad the
three axes to organize his research write-ups on. And "it is easy to lie to ourselves" is HRT
independently articulating the Feynman/López de Prado thesis that Brad's site is already
oriented around.

## [B] Named practitioners

### Giuseppe "Gappy" Paleologo — "2025 Buy-Side Quant Job Advice"
https://byfire.substack.com/p/2025-buy-side-quant-job-advice (Dec 29, 2025)

**Authority: this is the single highest-authority source in the report.** Paleologo is Global
Head of Quantitative Research at Balyasny Asset Management and a member of its Investment
Committee; previously Head of Risk Management at Hudson River Trading, Head of Enterprise Risk
at Millennium, and Director of Equities Quantitative Research at Citadel. PhD Stanford
(Management Science & OR); adjunct professor at NYU; author of *Advanced Portfolio Management*
and *The Elements of Quantitative Investing*. (Confirmed via
https://icme.stanford.edu/events/tech-talk-featuring-stanford-alum-gappy-paleologo-global-head-quantitative-research-balyasny
and https://www.rebellionresearch.com/2024-quant-of-the-year-dr-giuseppe-paleologo-balyasnys-incoming-head-of-quant-research-future-of-generative-ai-in-hedge-funds .)

**Market size — the outside view (verbatim):**
- *"I would guess that the total number of investment professionals in this space is around
  15,000. So maybe 7,000 quants, and a demand of roughly 700 quants per year. That includes
  everyone—from alpha research, to portfolio construction, to data analysis, to execution, to
  risk management."*
- *"job openings depend on firm growth and employee turnover; a reasonable ballpark is 5–10%
  per year."*
- *"I have personally screened maybe a couple thousand résumés, some of which were
  masterpieces of surrealist literature."*
- On the 0.2% offer rate: *"True, but also false, because they count every single submitted
  résumé... If you are a piano player in a brothel, know that your chances are unfairly
  slim—but rest assured that your résumé was still counted in the denominator."*
- He explicitly names career switchers as a major supply source: *"Sell-side employees on the
  verge of a nervous breakdown and trying to switch sides. I have no idea of the exact number,
  but it's clearly large, since about half (~20,000) of my current LinkedIn contacts fall into
  this category."*

**His actual "before the interview" checklist (verbatim, complete):**
1. *"Follow target firms on social media: LinkedIn and X, and perhaps a few Reddit channels
   (r/quant, r/algotrading), Discord servers, or similar forums. Follow their job postings and
   apply in a timely manner..."*
2. **"Research your prospective employer the way you would research a company you invest in.
   Be prepared, and know specifically what they do and what they are good at."**
3. *"Show up at on-campus recruiting events... Attendance gives you brownie points. Bring a
   résumé... ask informed questions about the company."*
4. *"Participate in a few extracurricular activities, such as a local investment club."*
5. *"Subscribe to Matt Levine's 'Money Stuff' newsletter."*
6. *"Read a few entertaining books for fun and profit"* (Derman, Bernstein, Brown,
   Niederhoffer, Zuckerman, Thorp, Taleb, Soros).

**On what to study (verbatim):** *"Applied probabilistic modeling and statistics are very
important skills to have. Physics is still a good major to hire from, because it is a
model-based discipline rather than a technique-based one, and you will be exposed to many
models."* Reading list: Wasserman *All of Statistics*, Ross *Applied Probability Models*,
Boyd & Vandenberghe *Convex Optimization*, Trefethen & Bau *Numerical Linear Algebra*, Strang
*Linear Algebra and Learning from Data*, Pólya *How to Solve It*. And: **"Note that I do not
recommend any finance books. You will learn that on the job."**

**On what makes a great analyst (verbatim), from 50–100 successful traders/PMs he polled:**
- *"**Curiosity.** People who read articles and scientific papers on their own, maybe during
  weekends, for the sheer pleasure of finding things out."*
- *"**Creativity.** ... looking at the same thing everyone else looks at, noticing something
  different, and proposing an original course of action. Most ideas do not survive scrutiny,
  but a few are brilliant."*
- *"**Humility.** When something does not work, admit it early and openly, examine why, and
  move on. In practice, humility (as described to me) is both a willingness to take
  responsibility and an openness to experience."*
- *"**Integrity.** Following both the letter and the spirit of the rules."*
- And, tellingly: *"not a single person mentioned 'capability,' 'mental throughput,' or
  'puzzle-solving' as a defining quality—yet we select in part on the ability to solve
  puzzles. Go figure."*

**He recommends Feynman's "Cargo Cult Science" as required reading, quoting it (verbatim):**
*"In summary, the idea is to try to give all of the information to help others to judge the
value of your contribution; not just the information that leads to judgment in one particular
direction or another […] The first principle is that you must not fool yourself--and you are
the easiest person to fool."*

**On compensation (verbatim):** *"At the top end, an alpha researcher will receive a
$450–500K package, inclusive of sign-on, salary, and guaranteed bonus. Software engineers,
execution research, risk, and data roles typically fall somewhere between $250K and $400K."*

**THE CRITICAL NEGATIVE FINDING.** This is roughly 15 pages of career advice from someone who
has screened thousands of quant résumés and now runs quant research at a major multi-manager.
It contains **zero mentions of personal websites, personal blogs, GitHub profiles, portfolio
sites, or side projects** as a hiring channel or evaluation input. Not dismissed — *absent
from the model entirely.* The channels he names are: job postings applied to promptly,
recruiting events, referrals/mentors, and the résumé.

### Marcos López de Prado — "The 10 Reasons Most Machine Learning Funds Fail"
https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf (Jan 2018; GARP whitepaper)

Directly relevant because Brad's system is explicitly MLdP-influenced — which means a hiring
manager who knows this literature will hold him to it.

**Pitfall #2, "Research Through Backtesting" (verbatim):**
> *"One of the most pervasive mistakes in financial research is to take some data, run it
> through an ML algorithm, backtest the predictions, and repeat the sequence until a
> nice-looking backtest shows up. Academic journals are filled with such pseudo-discoveries,
> and even large hedge funds constantly fall into this trap. **It does not matter if the
> backtest is a walk-forward out-of-sample. The fact that we are repeating a test over and
> over on the same data will likely lead to a false discovery.** This methodological error is
> so notorious among statisticians that they consider it scientific fraud, and the American
> Statistical Association warns against it in its ethical guidelines... **It typically takes
> about 20 such iterations to discover a (false) investment strategy subject to the standard
> significance level (false positive rate) of 5%.**"*

And: **"Remember, feature importance is a research tool, and backtesting is not."**

**Pitfall #10, "Backtest Overfitting" (verbatim):** *"WF's high variance leads to false
discoveries, because researchers will select the backtest with the maximum estimated Sharpe
ratio, even if the true Sharpe ratio is zero. **That is the reason why it is imperative to
control for the number of trials (I) in the context of WF backtesting. Without this
information, it is not possible to determine the Family-Wise Error Rate (FWER), False
Discovery Rate (FDR), Probability of Backtest Overfitting (PBO) or similar.**"*

The full Exhibit 1 taxonomy (pitfall → solution), verbatim:
| # | Category | Pitfall | Solution |
|---|---|---|---|
| 1 | Epistemological | The Sisyphus paradigm | The meta-strategy paradigm |
| 2 | Epistemological | Research through backtesting | Feature importance analysis |
| 3 | Data processing | Chronological sampling | The volume clock |
| 4 | Data processing | Integer differentiation | Fractional differentiation |
| 5 | Classification | Fixed-time horizon labeling | The triple-barrier method |
| 6 | Classification | Learning side and size simultaneously | Meta-labeling |
| 7 | Classification | Weighting of non-IID samples | Uniqueness weighting; sequential bootstrapping |
| 8 | Evaluation | Cross-validation leakage | Purging and embargoing |
| 9 | Evaluation | Walk-forward (historical) backtesting | Combinatorial purged cross-validation |
| 10 | Evaluation | Backtest overfitting | Backtesting on synthetic data; the deflated Sharpe ratio |

Also (verbatim): *"When misused, ML algorithms will confuse statistical flukes with patterns.
This fact, combined with the low signal-to-noise ratio that characterizes finance, all but
ensures that careless users will produce false discoveries at an ever-greater speed."*

**Operational implication for Brad's site:** since he cites López de Prado, a knowledgeable
reader will check whether he actually applies the evaluation half of the taxonomy (#8, #9,
#10). Publishing an out-of-sample track record **without disclosing the number of trials** is,
by this source's own standard, insufficient. Disclosing trial count, purging/embargoing, and
a deflated Sharpe ratio would put him in a very small minority of public sites and is
strongly differentiating with this exact audience.

### Ernie Chan — on where opportunities come from
https://databento.com/blog/quants-worth-following-ernie-chan
> **"Everybody that I have worked with since I became an independent trader is inbound...
> These traders reached out to me because of the books I published."**

Verified-practitioner evidence that public artifacts generate inbound — with the honest
caveat that the artifact was three Wiley books over a decade, not a website.

### Dirk Bester — via eFinancialCareers
https://www.efinancialcareers.com/news/2018/05/quant-hedge-fund-interviews
Bester (PhD, Bayesian algorithmic design; author of the open-source *Quantitative Primer*,
https://github.com/dwcoder/QuantitativePrimer ; interviewed at ~7 quant hedge funds):
- **"Hedge funds (and banks who interview well) will ask you specific questions about stuff on
  your CV. If you mention spatial statistics, they will ask you questions about model
  comparison and Gaussian processes."**
- *"When I was interviewing four years ago, some hedge funds made me sit an exam before
  they'd interview me."* Funds now *"ask applicants to do a pair-programming exercise before
  they'll even speak to you,"* with questions *"mostly focus on algorithms from graph theory."*
- *"Hedge funds are moving away from vanilla brainteasers"* toward *"questions that allow you
  to establish the breath and depth of a candidate's knowledge."*

**Implication:** everything on Brad's site is interview surface area. If the site says
"Kalman filter," "combinatorial purged cross-validation," or "variance risk premium," he will
be examined on it. Anything he cannot defend in depth should come off the site.

### Recruiters (named)
https://www.efinancialcareers.com/news/2016/02/quant-hedge-funds-are-ramping-up-their-hiring-heres-what-they-look-for-in-candidates
- **Ben Hodzic**, Managing Consultant, Quantitative Analytics/Research/Trading Americas,
  **Selby Jennings**: *"At a more junior level, the ability to code in Python and Java has
  increasingly been an attractive credential [for quant hedge funds]."*
- **Crosby Baker**, Managing Consultant, **Korn Ferry Futurestep**: *"Quant funds in particular
  are looking for the smart, analytical people right out of undergrad – such as math or econ
  majors from MIT or Wharton."* … *"There's a lot of data analytics in tech-oriented roles at
  hedge funds, and if you have an interest in investing, that will give you a leg up.
  However, that's not as important as the programming skills that they're looking for."*

### H.W. Anderson (quant executive search since 2014)
https://www.hw-anderson.com/quant-headhunter
They look for candidates who can *"combine fundamental analytics with quantitative expertise
and coding skills to enhance trading insights"* or who have **"created and are able to create
their own systematic trading strategies."** They *"track top tier Quantitative talent from
their first year in 'industry' and maintain good relations with many leading PhD programmes."*
No mention of personal projects or websites.

**Mixed signal:** "created and are able to create their own systematic trading strategies" is
the most directly Brad-favourable recruiter language found. But the sourcing model described
is tracking people already *in* industry and PhD-program relationships — i.e., a channel Brad
is not in.

### Durlston Partners (quant recruiter) — "Engineer to Quant? Challenge Accepted"
https://durlstonpartners.com/engineer-to-quant-challenge-accepted/
- *"The primary obstacle facing SWEs when applying for QR roles at top hedge funds lies in the
  stiff competition they will face."*
- Interviews cover *"Probability (very important), Mathematics (linear algebra calculus
  etc..), Computer Science (leet code medium to hardcore style problems is required for the
  top tier systematic hedge funds and prop trading firms)"*.
- Notes SWEs are disadvantaged because *"the depth and breadth of theoretical knowledge
  required for quantitative research are different and more advanced"* than a CS education.
- Recommends demonstrating skills through *"open-source quant projects or participating in
  competitions like Kaggle"*, plus a master's, starting as a quant developer, or internal
  transfer.

### QuantStart — "Engineering To Quant Finance: How To Make The Transition"
https://www.quantstart.com/articles/engineering-to-quant-finance-how-to-make-the-transition/
- *"80-90% of a quant's day is spent coding, whether they are developer or researcher"*
- *"a strong knowledge of statistics is an absolutely essential skill for a quantitative
  researcher"*
- **"It will be a challenge to target a mid-level quantitative trading research role without
  either prior quant finance research experience or examples of other rigourous research"**
- *"practice as much software development as possible by writing your own large-scale projects
  or by contributing to open source software"*
- Names *"your current network"* and *"dedicated quantitative finance recruiters"* as the job
  search routes — **not** blogs or portfolios.

**That bolded line is the strategic core of Brad's whole situation.** It concedes that a
career switcher *can* substitute *"examples of other rigourous research"* for prior quant
finance experience — which is precisely the gap his vol system + post-mortems are meant to
fill. The word doing the work is **"rigourous."**

## [C] Commercial / anonymous sources

### "QM" / quantymacro — "A Non-Guide on Building Personal Projects For HF Quant Roles (Part I)"
https://quantymacro.substack.com/p/personal-projects-guide (Mar 25, 2024)

Anonymous, but with a specific verifiable-ish claim: *"I completed my undergraduate last year,
& received multiple offers from PMs in Citadel/MLP/Bluecrest/Rokos/Brevan to join their pod
w/o going through the typical grad rotations."*

**The single most calibrating quote in this report (verbatim):**
> *"most of the interview articles/guides out there talk about brainteasers, leetcode, options
> questions etc, but almost none of them talk about how to build/present personal projects in
> hedge fund interviews. And **most people (including interviewers, practitioners that are way
> more experienced than me), view personal projects as nothing more than a "show of interest".
> Which is something I disagree with** (surprise surprise). I think if done right personal
> projects can push you much further."*

He is candid about noise: *"luck and randomness play a huge role. Recruitment is an incredibly
noisy environment, so trying to create good generalizations is almost impossible."* And he
scopes it: *"I only have experience with junior/grad role, I suspect for senior roles it's
obviously different."*

He also defers to Paleologo: *"@__paleologo (a real quant) did write a real quant job advice.
So you have to be crazy to read an article by an anon with a dinosaur profile pic but not read
the one by a legit quant... there are glaring differences between what practitioners with
years of experience emphasize on, vs what me a naive junior emphasizes on."*

**Read this carefully.** Even the most pro-personal-project source available concedes that the
industry default view — including among interviewers — is that personal projects are merely a
"show of interest." His contrary claim is explicitly a minority opinion. Part II with the
actual project examples was promised but is not published at the URL.

### Quantt — "Quant Resume: How to Write One That Gets Interviews in 2026"
https://www.quantt.co.uk/resources/quant-resume-guide (commercial guide, no named author)
- **"A GitHub link with substantial projects is one of the strongest signals you can send."**
- **"Projects are proof of genuine interest and initiative — two things that are hard to fake."**
- *"'Developed quantitative models' tells a recruiter nothing. Which models? What data? What
  was the result? Specificity is what separates a strong CV from a weak one."*
- *"Numbers are the currency of quant finance. A resume without quantified results reads as
  though you either didn't achieve anything measurable."*
- On listing skills: *"If you write 'C++, Java, Scala, Rust, Julia, MATLAB, R, Python' but can
  only competently code in two of those languages, you've created a trap for yourself...
  Interviewers will pick the most obscure item on your list."*
- Named red-flag examples of *unbelievable* numbers: a **Sharpe ratio of 12** *"without saying
  it came from a short and carefully chosen backtest"*; **95%+ accuracy predicting stock
  prices** *"with no time horizon or out-of-sample proof"*; a **$5M P&L gain** *"from a paper
  trading sim with no transaction costs or slippage"*.
- Strong-bullet example given: *"Implemented Monte Carlo pricer for European and Asian options
  in C++, using variance reduction techniques (antithetic variates, control variates) to
  reduce pricing error by 60% vs naive simulation"*.
- *"One excellent project beats five unfinished ones - aim for depth, reproducibility, and
  clean communication."*

### Quantt — "How to Break Into Quant Finance"
https://www.quantt.co.uk/resources/landing-your-first-role-breaking-into-quant-finance
On whether GitHub/projects matter, verbatim: **"Recruiters and hiring managers do check this,
especially when deciding between similar candidates."**

**This is the most honest single-sentence calibration found.** Projects are a **tiebreaker
between comparable candidates**, not a mechanism that creates candidacy.

Also: *"If you have a strong quantitative background, targeted preparation takes 3-6 months
(interview prep, building projects, applications). Career changers from non-quantitative
fields should allow 1-2 years."*

### Street of Walls — Quantitative Recruiting
https://www.streetofwalls.com/finance-training-courses/quantitative-hedge-fund-training/quant-recruiting/
- *"many firms may not actively recruit for such candidates by visiting college campuses"* —
  candidates must *"scout out your own role, rather than relying on a job board or on-campus
  recruiting."*
- *"once a job is posted, a firm can receive hundreds of resumes for a single position"* —
  direct outreach to hiring managers is critical to standing out.
- Advises a cover letter that details *"your quantitative skills and past history by
  referencing prior work projects or college assignments"* and shows *"that quantitative
  finance interests you, and give solid reasons why."* (Note this directly contradicts Jane
  Street's official "Do I need a cover letter? Nope!")

### OpenQuant — Quantitative Finance Portfolio Projects
https://openquant.co/blog/quantitative-finance-portfolio-projects
No named author or stated authority. Claim: *"side projects are one of the best ways to
highlight these attributes. Not only do candidates who have completed side projects tend to
pass more resume screens"* — asserted without data. Treat as marketing.

### "The Hiring Funnel at Top Quant Firms" — youngandcalculated (anonymous newsletter)
https://youngandcalculated.substack.com/p/the-hiring-funnel-at-top-quant-firms
- *"Getting a quant role at a firm like Jane Street, SIG, Optiver, Two Sigma, or D.E. Shaw is
  a multi-stage elimination process."*
- Names as a mistake: **"Missing a GitHub. Firms are actively reviewing GitHub profiles now,
  particularly for any role touching implementation."**
- Also flags *"Listing every programming language you have touched"* and *"Generic bullet
  points with no numbers."*
- Anonymous and partly paywalled; lowest weight.

---

# SYNTHESIS

## (a) The credibility-bridge playbook

Ordered. Each step is justified by a source above.

**Step 0 — Accept what the site is for.** No source in this report describes a personal
website as a hiring channel. Paleologo — who screens résumés for a living at a firm on Brad's
target list — does not mention personal sites once in 15 pages. Jane Street's full FAQ does not
mention them. HRT's interviewing post does not mention them. The honest model is:
**the résumé and the referral get the interview; the site is what converts a warm reader —
a recruiter mid-screen, a hiring manager after a referral, a PM before a call — from "plausible"
to "worth an hour."** Design for the warm reader, not for discovery.

**Step 1 — Put the isomorphism in the first sentence, not the third paragraph.** Two Sigma's
own switcher stories are all structurally *"the basic problem set is very similar"* (Rob,
intelligence community) and *"let's do a similar thing in finance"* (Mike, Google). Jakub's
entire positioning is four words: *"a physicist-turned-quantitative trader."* Brad needs one
sentence that names the old domain, the new domain, and the shared problem — e.g. state
estimation from noisy, non-stationary sensor data → signal extraction from noisy,
non-stationary market data. Optiver's own criterion is literally *"comfortable reasoning about
noisy data, imperfect signals, and risk."* Use their vocabulary.

**Step 2 — Lead with the research artifact framed as research, not as a product.** Two Sigma's
posted qualification is *"Performed an in-depth research project, examining real-world data."*
QuantStart concedes the switcher path requires *"examples of other rigourous research."* So the
vol system should be presented as **a research program with findings**, not as "my trading bot"
or "my platform." Title it as a question answered, not a system built.

**Step 3 — Organize every write-up on HRT's three stated axes: simplicity, reproducibility,
generality.** These are the words a hiring firm published as its own evaluation criteria for
research. Reproducibility means runnable notebooks and pinned data provenance (Makarewicz's
`docs/` with data contracts is the model). Generality means: does it hold on other underlyings,
other regimes, other years. Simplicity means: prefer the two-parameter model that works to the
neural net that works slightly better.

**Step 4 — Make the evaluation protocol the headline, and the returns a footnote.** This is
the strongest available differentiator, because almost no public site does it. Publish, for
every result: sample period; in-sample/out-of-sample split; **number of variants tried
(López de Prado: "it is imperative to control for the number of trials")**; purging and
embargoing; cost, slippage, and margin assumptions; capacity limits. Report **OOS R² against a
naive baseline** the way Makarewicz does ("about 30% OOS R²"), and a **deflated Sharpe ratio**
rather than a raw one. Kinlay's site is the presentational model: confidence intervals, explicit
limitation sections, published negative results.

**Step 5 — Publish the failures, prominently and first-person.** Longmore's about page leads
with *"years of every beginner mistake in the book... throwing machine learning at market data
and calling it research."* Jacobson publishes vol blow-up post-mortems. Paleologo's polled
managers named **humility** — *"when something does not work, admit it early and openly,
examine why, and move on"* — as a top-four trait, and he prescribes Feynman: *"you must not
fool yourself--and you are the easiest person to fool."* HRT independently says *"it is easy to
lie to ourselves."* A documented killed strategy, with the reason it died, is worth more to
this audience than a working one, because it is the only cheap way to prove Brad won't sell his
future employer a false discovery.

**Step 6 — Ship one hard, named, installable artifact.** Letian Wang has `quanttrader` on PyPI;
Bester has the *Quantitative Primer*; Chan has books. A named library or a genuinely reusable
dataset/tool is a harder credential than a notebook collection, and it is checkable. Quantt:
*"One excellent project beats five unfinished ones."*

**Step 7 — Demonstrate market-domain literacy, not options-textbook literacy.** SIG budgets a
three-month in-house finance class and says *"the ability to develop a new idea or approach to
a problem is far more valued than having a preexisting knowledge of finance."* Paleologo:
*"I do not recommend any finance books. You will learn that on the job."* So do **not** build a
site that proves Brad has learned Black-Scholes. Build one that proves he can frame a good
question about the vol surface and design an experiment that could falsify his own answer.
Microstructure/frictions realism (Makarewicz's per-leg costs, Reg-T margin, delta-hedge
rebalance policy) is the credible form of "I know how markets actually work."

**Step 8 — Keep the site's surface area exactly equal to what he can defend.** Bester:
*"Hedge funds... will ask you specific questions about stuff on your CV. If you mention spatial
statistics, they will ask you questions about model comparison and Gaussian processes."* HRT:
the common failure is *shallow* fundamentals, and candidates should know *why* a tool exists.
Every technique named on the site is a scheduled interview question. Prune accordingly.

**Step 9 — Write to be understood.** HRT: *"We rate our engineers as much on communication as
we do on technical ability."* Two Sigma's qualification: *"communicate complex ideas clearly."*
Ray's entire premise: *"you don't really know what you're talking about unless you can present
the information in a digestible and intuitive way"* — and that blog belongs to someone who
went from UCLA CS to HRT in New York. Expository clarity is itself a screened-for trait.

**Step 10 — Spend most of the effort off-site.** Chan's opportunities are *"inbound... because
of the books I published"* — a decade of artifacts. Jacobson got his seat through a mentor.
Paleologo's list is postings, events, mentors, and preparation. H.W. Anderson tracks people
already in industry. The site should be the thing Brad points at; the pointing is a separate,
larger job.

## (b) Ranked: what hiring-side evidence says actually matters

1. **Demonstrable coding ability.** QuantStart: *"80-90% of a quant's day is spent coding."*
   Two Sigma requires an actual language proficiency. Hodzic (Selby Jennings): Python/Java are
   the junior-level credential. Baker (Korn Ferry): programming skills matter more than
   investing interest. Durlston: LeetCode-medium-to-hard is required at top firms.
2. **Applied probability and statistics depth.** Paleologo: *"Applied probabilistic modeling
   and statistics are very important skills to have."* QuantStart: *"absolutely essential."*
   Durlston: *"Probability (very important)."*
3. **An in-depth research project on real-world data.** A literal Two Sigma qualification
   bullet. QuantStart's stated substitute for missing quant-finance experience.
4. **Evaluation discipline / not fooling yourself.** HRT: *"simplicity, reproducibility, and
   generality"*, *"easy to lie to ourselves."* Paleologo prescribes Feynman's Cargo Cult
   Science. López de Prado's entire evaluation taxonomy (#8–#10).
5. **Original problem-framing over domain knowledge.** SIG, verbatim: *"The ability to develop
   a new idea or approach to a problem is far more valued than having a preexisting knowledge
   of finance."* Paleologo's "creativity."
6. **Communication.** HRT rates it equal to technical ability; Two Sigma names it; Optiver names
   *"clear communication across disciplines."*
7. **Curiosity and humility as observable behaviors.** Paleologo's top-four traits from 50–100
   managers; Optiver's *"curiosity and ownership."*
8. **The résumé itself, specific and quantified.** The one artifact every source names.
   Paleologo screened *"a couple thousand résumés."* Jane Street: no cover letter needed —
   the résumé plus a free-text box is the channel.
9. **Referrals, mentors, and warm channels.** Jacobson got his seat via a former boss/mentor.
   Paleologo: get *"one or two mentors."* Street of Walls: *"scout out your own role"* and
   contact hiring managers directly. H.W. Anderson sources by tracking people in industry.
10. **A substantive GitHub — as a tiebreaker.** Quantt: *"Recruiters and hiring managers do
    check this, **especially when deciding between similar candidates**."* H.W. Anderson values
    people who *"created... their own systematic trading strategies."* But note QM's honest
    framing that the industry default is "show of interest."
11. **A personal website, specifically.** Lowest rank, and the evidence is mostly *absence*:
    zero mentions across Paleologo, Jane Street's FAQ, HRT, Two Sigma, D. E. Shaw, SIG, and
    Optiver. Its realistic function is conversion of already-interested readers.

## (c) Red-flag list — things on a personal site that actively hurt a quant candidate

1. **A headline return or Sharpe number with no trial count.** López de Prado: *"it is
   imperative to control for the number of trials"*; *"It typically takes about 20 such
   iterations to discover a (false) investment strategy"* at 5% significance. A backtest Sharpe
   with no disclosed search process is read as evidence of *not knowing this*, which is
   disqualifying in a way that having no number is not.
2. **"Out-of-sample" used as a magic word.** López de Prado, verbatim: **"It does not matter if
   the backtest is a walk-forward out-of-sample. The fact that we are repeating a test over and
   over on the same data will likely lead to a false discovery."** Brad's live OOS track record
   is genuinely valuable — but only if presented with the trial count, the pre-registration date,
   and the sample size, and with explicit acknowledgment that a short live sample has enormous
   error bars.
3. **Implausible numbers.** Quantt's named examples: a Sharpe of 12; 95%+ directional accuracy;
   a P&L figure from a paper-trading sim with no costs or slippage. Dev Kewlani's live site
   carries *"250%+ annual returns (pre-costs)"* on an hourly-rebalanced crypto strategy — a
   concrete example of the failure mode.
4. **Results with no cost, slippage, or capacity model.** The presence of per-leg commissions,
   bid/ask, margin constraints, and hedge-cost attribution (as in Makarewicz's repo) is what
   separates a real vol backtest from a toy. Their absence is immediately visible to a vol
   person.
5. **No risk section at all.** Optiver screens for *"comfort with uncertainty and risk"*;
   Paleologo's own career is in risk. A vol strategy presented without drawdown behavior, tail
   exposure, gap risk, and what would make it stop working reads as naive about short-vol
   payoffs specifically.
6. **"AI trading bot" / buzzword ML framing.** HRT: *"an incremental 0.1% improvement in the
   accuracy of a neural network's ability to distinguish dog breeds might not translate to
   predicting the price of a stock."* López de Prado: *"ML algorithms will confuse statistical
   flukes with patterns."* Longmore's own confession: *"throwing machine learning at market data
   and calling it research."* Model complexity presented as the achievement is a negative signal.
7. **Skills walls / technology laundry lists.** Quantt: *"If you write 'C++, Java, Scala, Rust,
   Julia, MATLAB, R, Python' but can only competently code in two of those languages, you've
   created a trap for yourself... Interviewers will pick the most obscure item on your list."*
   Same applies to a badge grid of libraries.
8. **Anything he cannot defend for 20 minutes.** Bester: *"they will ask you specific questions
   about stuff on your CV."* HRT: shallow fundamentals is the top failure mode. Name-dropping
   "combinatorial purged cross-validation" without having implemented and understood it is
   worse than not mentioning it.
9. **Vague accomplishment language.** Quantt: *"'Developed quantitative models' tells a
   recruiter nothing. Which models? What data? What was the result?"*
10. **Academic-portfolio layout.** The publications/projects grid (crangi.github.io) signals
    coursework, not desk-ready research. Brad is an industry practitioner and should not adopt
    a PhD-applicant template.
11. **A bare artifact dump with no framing.** Makarewicz's landing page — "Notebook Reports" and
    six file links — wastes genuinely strong research. Also its inverse: a beautiful landing
    page with nothing behind it.
12. **Burying the transferable work.** Hegde's ML-for-trade-order-selection experience at
    Fidelity sits inside a reverse-chron list dominated by robotics. Brad's state-estimation and
    real-time optimization work must be surfaced and translated into market vocabulary, or it
    reads as generic ML résumé filler — which the pinned project memory correctly identifies as
    lower-value for this audience.
13. **Overclaiming the identity.** Calling himself a "quant" before holding the role invites the
    comparison he'd lose. "Engineer building a volatility research program" is defensible;
    "quantitative researcher" on a site with no desk experience is not.
14. **Anything unfalsifiable.** Feynman via Paleologo: *"give all of the information to help
    others to judge the value of your contribution; not just the information that leads to
    judgment in one particular direction."* Results presented so that no reader could ever
    disconfirm them are read as evasion by people whose job is disconfirming things.

## (d) Blunt assessment: how much does a personal site move the needle?

**Less than Brad hopes. Materially less.** The evidence:

**Against:**
- **Giuseppe Paleologo** — Global Head of QR at Balyasny, ex-HRT/Millennium/Citadel, self-
  reported screener of *"a couple thousand résumés"* — wrote ~15 pages of buy-side quant career
  advice in December 2025 and mentioned personal websites, blogs, GitHub, and side projects
  **zero times.** His enumerated pre-interview actions are: follow firms and apply promptly,
  research the employer, attend recruiting events with a résumé, join clubs, read Matt Levine,
  read eight books. Nothing about building or publishing anything.
- **Jane Street's** interviewing page and ~25-question FAQ mention them zero times, and
  explicitly say a **cover letter is unnecessary** — the résumé plus a free-text box is the
  entire pre-interview channel.
- **HRT's** own interviewing post: zero mentions.
- **Two Sigma, D. E. Shaw, SIG, Optiver** job/careers pages: zero mentions.
- **QuantStart** names *"your current network"* and *"dedicated quantitative finance
  recruiters"* as the routes.
- **Even the most pro-project source available (QM/quantymacro)** concedes: *"most people
  (including interviewers, practitioners that are way more experienced than me), view personal
  projects as nothing more than a 'show of interest'."* His disagreement is explicitly a
  minority position, and explicitly scoped to junior/grad roles.
- **Quantt's** honest framing: projects get checked *"especially when deciding between similar
  candidates"* — i.e., a tiebreaker.
- **Harel Jacobson**, the closest topical analogue in the whole report, got his quant trader
  seat *"under [his former boss's] mentorship."* The vol writing came afterward.

**For:**
- **Ernie Chan**: *"Everybody that I have worked with since I became an independent trader is
  inbound... These traders reached out to me because of the books I published."* Public
  artifacts demonstrably generate inbound — at book scale, over years.
- **H.W. Anderson**, an actual quant search firm, explicitly seeks people who have *"created and
  are able to create their own systematic trading strategies"* — the most Brad-favourable
  recruiter language found.
- **Two Sigma's own posted qualification** asks for *"an in-depth research project, examining
  real-world data."* Something must evidence that, and a well-built site is the natural vehicle.
- **QuantStart** concedes a switcher can substitute *"examples of other rigourous research"* for
  quant-finance experience. The site is where that evidence lives.
- **Ray** went UCLA CS → HRT Algorithm Engineer in New York with a public blog that is purely
  expository — and it reached Reddit and Hacker News. Not proof of causation, but the closest
  positive case, and the mechanism is *demonstrated clarity of thought*, not a track record.
- Firms are unanimous that **finance background is not required** (Jane Street: *"Finance
  background: optional"*; Two Sigma: *"more than half... come from outside the finance
  industry"*; SIG: originality *"far more valued than having a preexisting knowledge of
  finance"*). **The switcher door is genuinely open.** The bottleneck is not "does he have
  finance experience" — it is getting a résumé read at all, given Paleologo's ~700 quant hires
  per year against a supply that includes ~20,000 sell-side people trying to switch.

**Ranked expected value of Brad's channels:**
1. **Referral / warm introduction** into a specific team. Every source points here; Jacobson's
   actual path; Paleologo's mentor advice; H.W. Anderson's sourcing model.
2. **A résumé that is specific, quantified, and legible as quant-adjacent**, applied promptly
   to posted roles. The one artifact universally named.
3. **Specialist recruiter relationships** (Selby Jennings, Durlston, H.W. Anderson, Oxford
   Knight) — they are named as a route by QuantStart and are actively sourcing.
4. **Interview readiness** — probability, stats, LeetCode-hard, and the ability to defend
   everything he has ever written down.
5. **The site + GitHub** — conversion and tiebreaking. Real, but downstream of 1–4.
6. **Public writing at scale over time** (the Chan mechanism) — highest ceiling, longest
   horizon, least reliable on a job-search timeline.

**The reframe that follows.** The site should stop being conceived as a lead-generation
instrument and start being conceived as **a defensibility instrument**: the thing that makes a
warm reader confident enough to spend an hour, and the thing that makes Brad unshakeable when
someone probes his claims in an interview. Its highest-leverage content is not the best
strategy he has found — it is the documented evidence that he knows how easily he could have
fooled himself, and what he did about it. That is the one thing a career switcher can
credibly offer that a strong résumé cannot, and — per Paleologo's polled managers, per HRT's
own blog, per Feynman via both — it is exactly what the buyers say they are looking for.

---

## Appendix — every URL fetched and verified for this report

**Career-switcher / practitioner sites**
- https://oneraynyday.github.io/about/
- https://robotwealth.com/about-robot-wealth/
- https://epchan.com/
- https://engineerquant.substack.com/about
- https://quantjourney.substack.com/about
- https://tradingtechnologies.com/blog/2021/02/08/5-questions-with-harel-jacobson-of-oporto-delta/
- https://letianzj.github.io/
- https://markrbest.github.io/
- https://tr8dr.github.io/about/
- https://jonathankinlay.com/
- https://anthonymakarewicz.github.io/volatility-trading/
- https://github.com/anthonymakarewicz/volatility-trading
- https://rickiheicklen.com/
- https://dev-kewlani.github.io/
- https://crangi.github.io/
- https://hegde95.github.io/
- https://databento.com/blog/quants-worth-following-ernie-chan

**Firm-official**
- https://www.janestreet.com/join-jane-street/
- https://www.janestreet.com/join-jane-street/interviewing/
- https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-Quantitative-Researcher-Intern-2027-Summer/13945
- https://www.twosigma.com/articles/from-stem-to-finance-employees-share-their-stories/
- https://www.twosigma.com/careers/quantitative-research-data-science/
- https://www.deshaw.com/careers/quantitative-analyst-2636
- https://sig.com/careers/quant/
- https://www.optiver.com/join-us/students/internships/research/
- https://www.hudsonrivertrading.com/hrtbeat/engineering-and-interviewing-at-hrt/
- https://www.hudsonrivertrading.com/hrtbeat/trading-machine-learning/

**Named practitioners / research**
- https://byfire.substack.com/p/2025-buy-side-quant-job-advice (Paleologo)
- https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf (López de Prado)
- https://icme.stanford.edu/events/tech-talk-featuring-stanford-alum-gappy-paleologo-global-head-quantitative-research-balyasny
- https://www.rebellionresearch.com/2024-quant-of-the-year-dr-giuseppe-paleologo-balyasnys-incoming-head-of-quant-research-future-of-generative-ai-in-hedge-funds
- https://www.efinancialcareers.com/news/2018/05/quant-hedge-fund-interviews (Bester)
- https://www.efinancialcareers.com/news/2016/02/quant-hedge-funds-are-ramping-up-their-hiring-heres-what-they-look-for-in-candidates (Hodzic, Baker)
- https://github.com/dwcoder/QuantitativePrimer

**Recruiters**
- https://www.hw-anderson.com/quant-headhunter
- https://durlstonpartners.com/engineer-to-quant-challenge-accepted/
- https://www.streetofwalls.com/finance-training-courses/quantitative-hedge-fund-training/quant-recruiting/
- https://www.quantstart.com/articles/engineering-to-quant-finance-how-to-make-the-transition/

**Commercial / anonymous**
- https://quantymacro.substack.com/p/personal-projects-guide
- https://www.quantt.co.uk/resources/quant-resume-guide
- https://www.quantt.co.uk/resources/landing-your-first-role-breaking-into-quant-finance
- https://openquant.co/blog/quantitative-finance-portfolio-projects
- https://youngandcalculated.substack.com/p/the-hiring-funnel-at-top-quant-firms
- https://moontower.substack.com/p/a-talk-i-gave-at-a-quant-bootcamp (paywalled; not cited for substance)
- https://news.ycombinator.com/item?id=17235210 (via HN Algolia API; low signal, not cited for substance)

**Could not access:** all of reddit.com (crawler-blocked); quantnet.com (HTTP 403).

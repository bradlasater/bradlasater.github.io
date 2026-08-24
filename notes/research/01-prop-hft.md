# Research 01 — Personal Sites of Prop / Market-Making / HFT People

**Lane:** personal websites of people who currently or recently work at proprietary trading,
market-making, or HFT firms (Jane Street, HRT, Citadel Securities, Jump, SIG, IMC, DRW, Tower,
Radix, Headlands, Akuna, Belvedere, Arrowstreet, Optiver, XTX, Virtu, …).

**Method.** Generic web search was near-useless in this lane (it returns firm career pages and
interview-prep SEO spam, not people). What worked was mining the **GitHub Users API by bio text** —
`gh api search/users -f q='"Headlands Technologies" in:bio'` etc. — across ~40 firm names and role
keywords, keeping only accounts with a populated `blog` field, then loading every candidate URL.
Sites were loaded with WebFetch and, where WebFetch was blocked (403) or the fetcher's summary was
thin, with `curl` + HTML-to-text so I could read raw markup for the technical-implementation
questions. Every URL below was successfully loaded. Anything that 404'd, was a link-in-bio, or was
just a LinkedIn redirect was discarded or moved to the "not real sites" section.

**Headline caveat that shapes everything else in this document:** in this lane, the people with the
most impressive employers have the *least* content, and the people with the most content are
deliberately vague about their employer. That inversion is the central finding, and it is directly
actionable for Brad.

---

# PART 1 — VERIFIED SITES

## 1. Ming Fong — https://evilpegasus.github.io/
*(`mingyfong.github.io` is a redirect stub that forwards here; the canonical page is evilpegasus)*

1. **Exact self-description:** "I am a Quantitative Researcher at Headlands Technologies in Chicago
   where I work on high frequency trading strategies."
2. **Site type:** One-page card / mini-résumé. Roughly 250 words total.
3. **IA:** No nav bar. Name → headshot → one paragraph of bio → icon row (LinkedIn, GitHub, Kaggle,
   Google Scholar). Everything above the fold; there is no second screen.
4. **First 100 words:** The role sentence above, then Berkeley Physics + CS 2024, then the Nachman
   Group / LBNL work on transfer learning for particle-physics simulation and GNNs for pion
   reconstruction in ATLAS at CERN, then prior internships.
5. **Content types:** None on-site. All evidence is outbound links.
6. **Evidence format:** Delegated entirely. Google Scholar carries the physics papers, Kaggle
   carries competition standing, GitHub carries code. The page itself asserts nothing quantitative.
7. **Rigor signals:** Only the named research group and named collaborators. No methodology, no data,
   no caveats — because there is no claim to caveat.
8. **Voice/length:** Third-person-ish, flat, factual, ~250 words. Zero adjectives.
9. **Tech:** Hand-rolled static HTML, single `assets/main.css`, FontAwesome kit, Google `gtag`.
   No generator meta tag. No math rendering, no charts. 5.9 KB, loads in ~0.2 s.
10. **Recruiting affordances:** No email, no résumé PDF, no "open to work". LinkedIn icon only.
11. **Notably absent:** Everything. No projects, no writing, no results, no CV.
12. **Anti-patterns:** Arguably none — it is honest about being a stub. But it is also close to
    content-free; it works *only* because "Headlands / HFT strategies" plus a Scholar profile is
    already the whole signal.

**Lesson for Brad:** this is what a real HFT researcher's site looks like when the firm badge does
the talking. Brad does *not* have that badge, so he cannot copy this shape — he has to be at the
opposite end (content-heavy) precisely because he lacks the credential shortcut.

---

## 2. Nick Georgakopoulos — https://nickg-math.github.io/
1. **Exact self-description:** "I am currently a Quantitative Researcher at Radix Trading." Followed
   by Ph.D. in mathematics, University of Chicago, March 2022, advisor J. P. May.
2. **Site type:** Academic-style single page.
3. **IA:** No nav. Sections in order: **About** → **Math Papers and Code (2017–2022)** → a picture
   from his research. There is a light/dark toggle (`switch.js`, `slider.css`).
4. **First 100 words:** Role sentence, PhD, advisor, then straight into the paper list.
5. **Content types:** 5 mathematics papers (equivariant topology / algebraic structures) and 2 C++
   libraries on GitHub. No blog, no résumé PDF, no talks.
6. **Evidence format:** Papers + working code. Nothing about trading at all.
7. **Rigor signals:** Peer-reviewed publications with named advisor and institution.
8. **Voice:** Terse, academic, ~200 words of prose.
9. **Tech:** Hand-rolled HTML with three small stylesheets (`colors.css`, `layout.css`,
   `slider.css`) + `switch.js` for the theme toggle. MathJax loaded from the long-dead
   `cdn.mathjax.org` endpoint (stale). 3.3 KB.
10. **Affordances:** No email, no CV, no contact section at all.
11. **Absent:** Any contact method; anything post-2022.
12. **Anti-pattern:** Dead MathJax CDN.

**The move worth stealing:** the section is titled **"Math Papers and Code (2017–2022)"**. That
explicit closed date range is a compliance-safe fence — it silently says *everything on this page
predates my trading job, so none of it is my employer's*. Several people in this lane do a version
of this; he does it most cleanly.

---

## 3. Panagiotis "Panos" Kostopanagiotis — https://infinity4471.github.io/
1. **Exact self-description:** "Quantitative Researcher at Susquehanna International Group based in
   Dublin, Ireland where I work in the Sports Trading and Analytics desk." Previously "quantitative
   developer at IMC Trading" working on "ultra-low latency infrastructure for options market making
   in C++" across European Index Options and Crypto Options desks; before that Bloomberg LP.
2. **Site type:** Hybrid — landing bio + linked blog + projects/publications.
3. **IA:** Nav = **Home / The Turing Complete Blog / Algoholics / Projects-Publications**. Landing
   page is a single bio block, reverse-chronological career, then education (NTUA Integrated
   Master's, thesis on approximability of multistage min-sum set cover under D. Fotakis).
4. **First 100 words:** Current SIG role and desk, then IMC (naming the *technology*: ultra-low
   latency C++ for options market making) and the desks, then Bloomberg, then the thesis.
5. **Content types:** Blog, competitive-programming community ("Algoholics"), projects/publications
   page, CV PDF, plus outbound GitHub / LinkedIn / DBLP / Google Scholar.
6. **Evidence format:** Publication record (DBLP + Scholar), CV, competitive-programming lineage.
7. **Rigor signals:** Named advisor, named venues, DBLP.
8. **Voice:** Compact professional prose.
9. **Tech:** Jekyll with the **Lanyon/Poole** theme (`poole.css`, `lanyon.css`, `syntax.css`),
   MathJax 2.7 from cdnjs, FontAwesome 4.7. 6.3 KB.
10. **Affordances:** CV PDF is directly linked. No email in the clear.
11. **Absent:** No photo, no metrics, no trading content whatsoever despite two market-making jobs.
12. **Anti-patterns:** Dated theme (Lanyon + FA4 reads 2016); no dark mode.

**Note the disclosure boundary:** he names the *desks* and the *technology stack* but nothing about
strategy or performance. "Ultra-low latency infrastructure for options market making in C++,
European Index Options and Crypto Options desks" is a lot of specificity that costs the employer
nothing. That's a good template for describing employer work legally.

---

## 4. Ties de Kok — https://www.tiesdekok.com
1. **Exact self-description:** the header block is literally three stacked lines — **"Ties de Kok /
   Quant Researcher / Arrowstreet Capital."** The About page states the site is a *read-only archive,
   last updated October 2023*, from when he was an Assistant Professor at the University of
   Washington Foster School of Business.
2. **Site type:** Multi-page academic portfolio.
3. **IA:** Nav = **About me / Research / Code & Data / Talks & Classes / Blog Posts / CV** (CV is a
   direct `Vitae.pdf` link). This nav is the single cleanest information architecture I found in the
   lane and is the one I'd most recommend Brad study.
4. **First 100 words:** Name, role, firm; then the archive disclaimer; then research interests
   (machine learning, NLP, generative AI/LLMs, social media, XBRL) framed as "combining computer
   science with accounting research."
5. **Content types:** Peer-reviewed papers **with full abstracts inline**, 9 open-source projects,
   talks & classes, blog articles hosted elsewhere (Medium, EAA ARC) but *indexed on his own site*,
   CV PDF.
6. **Evidence format — the best in the set.** Research page renders each paper as: title → journal
   and year → `(paper)` `(ssrn)` links → co-author list → **the full abstract expanded on the page**.
   A reader can assess the work without leaving. Code & Data page renders each project as: name →
   one-sentence description of what it does → GitHub link. E.g. "IPyStata — Python package to
   combine Python and Stata in a jupyter notebook. **Officially integrated into Stata as of Stata 17.**"
   That last clause is a third-party validation datum doing enormous work in eleven words.
7. **Rigor signals:** Named journals (*The Accounting Review*, *Review of Accounting Studies*), named
   co-authors, SSRN preprints, abstracts that state their own measurement limitations.
8. **Voice:** Academic-neutral; abstracts are long-form, everything else is one-line.
9. **Tech:** Footer says **"Generated using a Python script 🐍 and simple.css."** Literally one
   3.3 KB page, one stylesheet (`/static/simple.css`), Google Analytics. No JS framework, no math
   rendering, no dark mode. Fastest site in the sample (0.16 s).
10. **Affordances:** Email `tdekok@uw.edu` in the clear, LinkedIn, GitHub, Twitter, CV PDF.
11. **Absent:** Nothing about Arrowstreet, at all, beyond the two-word header. No finance content.
    No photo.
12. **Anti-patterns:** The stale email (still `@uw.edu`) and the "read-only archive" banner make the
    site read as abandoned — the firm line at the top is the only current thing on it.

**Lesson:** the firm name is a *header attribute*, not a content section. Everything demonstrable is
pre-employment academic work and open source. He never tries to make Arrowstreet the story.

---

## 5. Leo Adberg — https://leo.adberg.com
1. **Exact self-description:** "I'm an algorithm engineer at Hudson River Trading working on HAIL
   (HRT AI Labs)." Previously Apple (Vision Pro), B.S. EECS Berkeley.
2. **Site type:** One-page portfolio.
3. **IA:** Nav = **Home / Experience / Portfolio / Contact**, all anchors on one page. Name +
   one-paragraph bio above the fold, then experience timeline, then a project grid, then contact.
4. **First 100 words:** The HRT line, the Apple line, the degree, then "interests span low-level
   software engineering alongside computer vision and machine learning."
5. **Content types:** Project grid (10 projects: textshader, Realtime Raytracer, Speed Challenge,
   RAWB, DCSO, SIL, Ricochet, CalCentral.me, Jumbo Jobs, FRC Robotics), résumé PDF, GitHub.
6. **Evidence format:** **Live demos.** Several projects are runnable in-browser (shader/raytracer
   work). This is the strongest "show don't tell" mechanism in the set — it is unfakeable and
   requires zero disclosure.
7. **Rigor signals:** None in the statistical sense — it's an engineering portfolio, not a research
   one.
8. **Voice:** First-person, friendly, short.
9. **Tech:** Hand-rolled, all CSS inlined (zero external stylesheets), `gtag`, and it does respect
   `prefers-color-scheme`. 11.8 KB.
10. **Affordances:** `leo@adberg.com` in the clear + résumé PDF.
11. **Absent:** No writing at all. No mention of what HAIL does.
12. **Anti-patterns:** Everything demonstrated is graphics/systems work with no relationship to
    trading. A trading hiring manager learns nothing about his trading ability from it — which is
    presumably the point, and also the limitation.

---

## 6. Sean Vernon — https://seanvernon.me (301 → https://www.ocf.berkeley.edu/~seanvernon/)
1. **Exact self-description:** "Quantitative Trader at Akuna Capital." Berkeley BA Computer Science
   2020.
2. **Site type:** One-page text résumé, ~150 words.
3. **IA:** Name, one bio paragraph, four links: `resume.pdf`, LinkedIn, GitHub, Medium.
4. **First 100 words:** The Akuna line, the degree, then extracurriculars (Berkeley Model UN
   Director of Technology, Open Computing Facility ops, CS peer advisor, co-founded a Math for ML
   course).
5. **Content types:** Résumé PDF only; blog is outsourced to Medium.
6. **Evidence format:** Credentials and roles. Nothing shown.
7. **Rigor signals:** None.
8. **Voice:** Plain, ~150 words.
9. **Tech:** Raw HTML on a university shell account (`ocf.berkeley.edu/~seanvernon`). No CSS
   framework. Custom domain 301s to it.
10. **Affordances:** Résumé PDF prominent.
11. **Absent:** Everything. His GitHub bio even reads "Email me for access to private repositories."
12. **Anti-pattern:** Hosting a professional identity on a student org's shell server, and gating
    the code behind a manual email request. A recruiter will not email you for repo access.

---

## 7. Mike DeCrescenzo — https://mikedecr.computer
1. **Exact self-description:** "I am a quantitative researcher / software developer at an
   **algorithmic trading firm**." — the firm is deliberately unnamed on the site. (GitHub bio adds
   "Quantitative researcher in low-latency trading. Former political scientist.")
2. **Site type:** Minimal technical blog.
3. **IA:** Title `mikedecr . computer`, one-line bio, **Recent posts**, **Archive**. Nav is just
   GitHub / Bluesky / Archive plus a dark/light toggle.
4. **First 100 words:** The unnamed-firm sentence, the former-political-scientist pivot, and a note
   that the blog is about statistics and programming.
5. **Content types:** Blog posts only. Titles: *Hy translations of Python translations of R
   functions*; *Using dark magic to create local scopes in Python*; *Map in terms of Reduce*;
   *Sugar-free: Python dictionaries*; *Just enough Conda advice*.
6. **Evidence format:** Craft posts. He demonstrates depth of language/tooling knowledge — nothing
   about markets.
7. **Rigor signals:** Functional-programming rigor rather than statistical rigor.
8. **Voice:** Wry, first-person, medium-length technical posts.
9. **Tech:** Static, hashed stylesheet (`style.css?h=24a8d9df…`), **both KaTeX 0.11 (with
   auto-render) and MathJax 3** loaded, `prefers-color-scheme` plus an explicit toggle. 4.9 KB.
10. **Affordances:** No email, no résumé. GitHub and Bluesky only.
11. **Absent:** Any finance content, any employer name, any CV.
12. **Anti-patterns:** For a job search this is under-instrumented — no contact path at all.

**The key pattern:** *"an algorithmic trading firm."* Naming the category and not the firm is a
recognised, respected move in this lane. It signals you understand the compliance norm.

---

## 8. Colin Swaney — https://cswaney.github.io
1. **Exact self-description (from `/info.html`):** "Quantitative researcher living and working in the
   Greater New York area." PhD in Finance, University of Iowa. **No employer named anywhere.**
   Self-describes as focused on "building intelligent systems" and blogging about machine learning
   "in spare time."
2. **Site type:** Research/teaching blog with a thin info page.
3. **IA:** Nav = **Blog / Info**. Landing page is the post feed in reverse chronological order.
4. **First 100 words:** The feed itself — the site leads with the work, not the bio.
5. **Content types:** Long-form technical posts, categorised by URL path into `/research/` and
   `/programming/`. Titles: *Variational Autoencoders*; *Gaussian Processes*; *Hidden Markov
   Models*; *Receiver Operating Characteristic (ROC) Curves*; *Policies and Optimality*;
   *Introduction to Deep Reinforcement Learning*; *The Linked List Cycle Problem*. Plus a linked
   résumé and GitHub.
6. **Evidence format — "mini-lecture."** I read the *Gaussian Processes* post in full: ~1,200 words,
   rendered LaTeX throughout (kernel definitions, the RBF example, the posterior), one figure
   ("Sampling for the log Gaussian Cox process"), two worked examples (time-series regression with
   noise; log Gaussian Cox processes for inhomogeneous Poisson modelling), and a real bibliography
   (Neal 2003 on slice sampling; Murray et al. 2010 on elliptical slice sampling).
7. **Rigor signals:** He explicitly flags what he is *not* deriving — the posterior is presented as
   "a well-known result for linear Gaussian systems" that is "easy to look up." That one sentence
   does a lot: it shows he knows the difference between what he derived and what he cited.
   Citations are to primary sources, not blog posts.
8. **Voice:** Pedagogical, first-person-plural, ~1,000–1,500 words per post. Not chatty.
9. **Tech:** Jekyll (`/research/YYYY/MM/DD/…` permalinks), **UIkit** CSS framework
   (`uikit.min.css` + `uikit-icons.min.js`), `base16.css` for syntax highlighting, jQuery 1.11,
   Google Fonts (Fjalla One + Lora + Indie Flower), **and both KaTeX 0.10 and MathJax 3** loaded on
   every page. 15.6 KB — the heaviest of the minimal sites. `polyfill.io` is referenced, which is
   now a defunct/hijacked domain — a live liability.
10. **Affordances:** Résumé linked from the info page; Twitter and GitHub; no email in the clear.
11. **Absent:** No employer. No finance content despite a Finance PhD. No dates on the info page.
12. **Anti-patterns:** Site has gone quiet since 2022; `polyfill.io` reference; jQuery 1.11.

**This is the closest structural analogue to what Brad is proposing** — a NYC quant researcher whose
credibility rests entirely on written technical exposition rather than on a named employer. Note
what he did *not* do: no strategy posts, no backtests, no returns. He proved statistical competence
on neutral ground.

---

## 9. Sunny Balasubramanian — https://sunnybala.com
1. **Exact self-description:** "Current quantitative researcher in the crypto & equities space.
   Formerly at Citadel, AQR, Columbia SEAS '16."
2. **Site type:** Project gallery.
3. **IA:** One heading — **Projects** — and a grid. Bio is two lines above it. LinkedIn + GitHub.
4. **First 100 words:** The role/history line, then an invitation to get in touch about prior work.
5. **Content types:** ~16 projects, each a short write-up with media: *PairType*, *BaristArt*,
   *Random Walks Around Manhattan*, *Charging Airpods with iPhone*, *AI Speech Synthesis for
   Dubbing*, *E-Ink Train Display*, *Lego Wireless Charger*, *Spherical Cucumber*, *Etch-a-Sketch
   Robot*, *Elevator Awkwardness Minimizer*, *Senate Insider Trading Investigation*, *VR Conducting
   Game*, *Fake YouTube Video Detection*, *Landmark*, *AlgoBlues*, *CUDiningView*.
6. **Evidence format:** Playful, self-evidently-real artefacts — hardware, WebGL, scrapers,
   simulations. *Senate Insider Trading Investigation* and *Random Walks Around Manhattan* are the
   only quantitatively-flavoured ones.
7. **Rigor signals:** Low. This is a curiosity/creativity signal, not a rigour signal.
8. **Voice:** Light, funny, short blurbs.
9. **Tech:** **Jekyll 3.10** with a GitHub Pages default-ish theme (`/assets/css/style.css?v=<sha>`),
   `html5shiv`, `scale.fix.js`, `gtag`. 11.4 KB.
10. **Affordances:** `sunny.m.bala@gmail.com` in the clear.
11. **Absent:** No résumé, no writing, no employer name for the current role.
12. **Anti-patterns:** For a $250k quant search this would read as unserious on its own — but as a
    *second* page next to a rigorous research section, "here is proof I am relentlessly curious" is
    a real asset. Note he names Citadel and AQR only in the past tense and refuses to name the
    current employer.

---

## 10. Kipp Rogers — https://mechanicalmarkets.wordpress.com
1. **Exact self-description (About This Blog, verbatim):** *"Kipp Rogers began studying market data
   in his free time, later founding Anamnesis LLC, a company specializing in algorithmic trading.
   The contents of this blog are purely his opinions, do not represent the views of Anamnesis LLC,
   are the products of analysis which may have errors, and do not constitute any sort of trading or
   investment advice."*
2. **Site type:** Long-form market-microstructure research blog.
3. **IA:** Nav = **Home / About This Blog / Contact**. Feed of posts. Sidebar lists ~30 posts by
   title — the archive *is* the credential.
4. **First 100 words:** Straight into the current post. No bio on the landing page at all.
5. **Content types:** Essays only, 2015–2023.
6. **Evidence format — quantitative essay with public data.** I read *Price Impact in Efficient
   Markets* in full: **~7,100 words**, numbered footnotes, embedded figures, and a two-part
   structure signposted in the intro ("In part I, we'll start with the simplest principles… In part
   II, we'll replace the fair pricing condition with…"). It derives price-impact predictions from
   integral equations built out of stated market principles, and grounds the square-root impact law
   in the published empirical literature across European and U.S. equities, futures, and bitcoin —
   every one of those a *public* citation. Other posts: *Sarao Spoofing Allegations and Queue
   Position*, *A Close Look at the Treasury Flash Rally Report*, *Who Executes Retail Trades? A Look
   at Market Share and Payment for Order Flow*, *Can We Tell Who Trades on Which Dark Pools?*,
   *Blind Analysis, Inefficient Markets, and UK Polling Accuracy*.
7. **Rigor signals — the strongest in the sample.**
   - A standing disclaimer that his analysis "may have errors."
   - An open invitation on every post: "Please feel free to discuss anything that looks wrong in the
     comments section or over email with me."
   - Analysis built exclusively on **public** data (SEC filings, exchange rule filings, regulatory
     reports, academic papers) — so there is no IP question at all.
   - A whole post on **blind analysis** as a methodology for avoiding self-deception. That is the
     López de Prado instinct expressed as a blog post rather than a claim.
8. **Voice:** Careful, hedged, long. 3,000–7,000 words is normal. He writes "I try to predict…",
   "some of the criticism is justified", "I have my doubts."
9. **Tech:** WordPress.com hosted, stock theme. No math rendering — equations are images. No dark
   mode. Blocks generic user-agents (WebFetch got 403; loads fine with a browser UA).
10. **Affordances:** Contact page. No résumé, no photo, no "hire me."
11. **Absent:** No CV, no code, no employer beyond his own LLC.
12. **Anti-patterns:** `wordpress.com` subdomain rather than a custom domain; dormant since 2023.

**Most transferable single artefact in this entire report:** that About paragraph. Three clauses —
who I am, this is not my employer's view, this analysis may contain errors — is the exact
disclosure/humility register that a quant hiring manager reads as professional maturity.

---

## 11. Mark Best — https://markrbest.github.io ("Quantitative Trading — Trading ideas and discussions")
1. **Exact self-description (About, verbatim excerpts):** "I started my career in investment banking
   in 2005 in London at Deutsche Bank… I worked at Citi for a few years in the electronic trading
   group for the Euro government bond desk… After deciding that I wanted to learn more about
   high-frequency trading I hit a roadblock… I spent the next eight years working for startups which
   were more willing to take people with less algo trading experience… At these firms, I managed to
   work with some talented people who taught me most of what I know about **HFT system
   architectures, HPC and a lot about market-making strategies**." **He never names his current
   employer.**
2. **Site type:** Long-running research/engineering blog. 30+ posts, 2020–2025.
3. **IA:** Nav = **Links / About / Archive**. Landing page is a post feed with generous excerpts.
   The **Archive** page is grouped **by tag**, not by date — Moving Average, FIR Filters, HMM,
   Distribution Forecasting, Swing Trading, MCMC, Books, Algo Trading, Crypto, Microstructure,
   Bitcoin, Volatility, Sklearn, Market Making, Strategy Testing, **Deprado**, Options, Betting
   Markets, Deep Learning, Market Data, HFT, Programming, Rust, Latency. Yes — there is a tag
   literally named **"Deprado."**
4. **First 100 words of About:** the career narrative above.
5. **Content types:** Blog posts, a *Book Reviews and Reading List* page, a *Links* blogroll.
6. **Evidence format — this is the model Brad should study hardest.** Two categories running side by
   side:
   - **Research posts on public/crypto data**, so nothing proprietary leaks: *Paper vs Live Slippage
     Analysis* (parts 1–4), *Alpha Decay*, *Fractional Differencing*, *Informational Disadvantage of
     Market Makers*, *Volatility and Time of Day*, *Bitcoin Microstructure*, *Bitcoin Elasticity and
     Volatility*, *GANs and Synthetic Market Data*, *Classifying Returns*, *MCMC for Return
     Distributions*, *The Problem with Moving Averages*, *Savitzky-Golay Swing Points*.
   - **Infrastructure posts**, which are verifiable and carry zero alpha risk: *Fast Logging for HFT
     in Rust*, *Even Faster Logging in Rust!*, *Message Arrival Rates and Latency*, *Hidden Dangers
     of Writing an OMS*, *Building Candlesticks in Rust*, *Dealing with Data*.
7. **Rigor signals — the best "not fooling yourself" material I found.**
   - The *Paper vs Live Slippage Analysis* series (~1,500 words each) puts **simulation vs paper vs
     live** side by side in one table (buy/sell counts, quantities, average prices, computed
     slippage) plus an equity curve and a deployment diagram. Measured slippage 0.000557%.
     Crucially he then explains the *mechanisms* of divergence: "The forecast takes about 200 ms to
     calculate on a new bar thus in paper and live the orders are sent later than in sim," and notes
     crypto exchanges lack sequence IDs, creating cross-feed inconsistencies.
   - He states his own scope limit rather than overselling: **"I should note my aim is not to get a
     perfect simulator as this task takes a lot of effort and I would like to focus on strategy
     optimisation as much as possible."**
   - *Alpha Decay* (~1,500 words) has a returns boxplot across holding horizons, the profit-factor
     formula, and pandas/seaborn code — and ends on open problems he has not solved: with RL
     execution "each fill might be associated with a chain of different actions"; on collapsing an
     alpha-decay chart to a number, **"it is not clear to me how this could be converted to a single
     measure"**; and simply **"more to follow…"**.
   - And the governing statement of intent, from the About page: **"Almost all of what I have looked
     at has been a dead end and arguably a waste of time… My plan for the blog is to discuss
     research as I progress and to present it as a learning experience. Partly this is to not
     divulge too much proprietary information but also to highlight the reality that most research
     ends up in the bin. Research is exactly that, and anyone that has done a lot of it knows both
     the euphoria of finding a new idea and the sadness of giving up on something with significant
     time investment."**
8. **Voice:** First-person, plain, ~1,200–1,800 words, occasional casual aside (a PS5 analogy in the
   slippage post). Never triumphal.
9. **Tech:** Jekyll on GitHub Pages, MathJax, inline SVG, no generator meta. Serviceable but plain;
   no dark mode.
10. **Affordances:** No résumé, no email in the clear, no "open to work."
11. **Absent:** No CV, no employer name, no photo, no headline performance figures.
12. **Anti-patterns:** Publishing cadence collapsed (5+ posts in Dec 2020, ~1/year since). Some
    social share buttons at the top read a bit dated.

**Why this matters most for Brad:** Mark Best has *exactly Brad's constraint* — real trading work he
cannot publish — and solved it by (a) doing all public research on crypto/public data, (b) writing
about infrastructure where correctness is checkable, (c) declaring up front that most research
fails, and (d) publishing paper-vs-live reconciliation instead of a headline Sharpe. That is a
ready-made blueprint.

---

## 12. Kris Abdelmessih — https://moontowermeta.com and https://blog.moontower.ai
1. **Exact self-description (from post text, verbatim):** "Back in my SIG days, every trader had a
   cell on their spreadsheet showing the SPUs… premium or discount to the 'cash'." And: "As a
   market-maker on the floor, I was not involved in index arbitrage this directly (although most of
   my clerking experience was much closer to these strategies)." The site's About link goes to a
   Notion page ("welcome traveler"). External sources describe him as ex-SIG options market maker →
   Parallax relative-value commodities vol → co-founder of moontower.ai; **I am reporting only what
   the site itself says**, which is the SIG floor-market-maker framing above.
2. **Site type:** Two properties. `moontowermeta.com` is a 7-year, 1,100+ post personal
   blog/newsletter archive; `blog.moontower.ai` is the product-adjacent options/vol blog.
3. **IA (moontowermeta):** Nav = **Home / My Writing (The Money Angle, Money Math, Newsletter
   Thoughts, Gaming, Education, Productivity, Investing) / Wikis (The Moontower Money Wiki, The
   Moontower Quant Codex) / Notes (Books, Essays, Podcasts) / Curated Sources (Blogs and Online
   Writers, Book Recs and Tools, The Investing Pro's Library, so you're interested in trading,
   Digital Learning, Productivity Apps, Investing Resources, For Investing Beginners) /
   Newsletter / About**. Category counts are shown: Newsletter Thoughts 1,130 · The Money Angle 441
   · Money Math 209 · Archive 315 · Education 68.
   **IA (blog.moontower.ai):** four evergreen buckets — **How Markets Work / Options & Volatility /
   Risk & Edge / Options Theory** — each post with a one-line subtitle underneath the title.
4. **First 100 words:** The landing page opens directly into a post, not a bio.
5. **Content types:** Essays, "wikis" (the **Moontower Volatility Wiki** and **Quant Codex** are
   structured evergreen reference material, not chronological posts), a free put-call-parity
   teaching game, interactive tooling (an "Attribution Visualizer" supporting multi-leg
   delta-hedged trades), curated reading lists, podcasts.
6. **Evidence format — pedagogy plus worked numerics.** I read *futures premium cell* in full: it
   walks the SPX cash/EFP/futures-fair-value relationship with an explicit worked example (SPX 7,800,
   RFR 3.5%, div yield 1.5%, t = 1 → 7800·e^((3.5%−1.5%)·1) ≈ 7957.57, EFP = 157.57, and then "if
   the future was trading 7977.57… 20 points or about 25 bps rich"), then explains beta-weighting
   the premium to reprice a single stock's fair value, then explains why index arbs get uneven fills.
   Every claim is anchored to floor experience and to arithmetic you can check.
7. **Rigor signals:** Worked numbers, mechanism-first explanations, explicit scoping of what he did
   and did not personally do on the floor, and post titles that are counterintuitive claims he then
   has to defend (*How a high implied vol can be cheap*; *If you make money every day you're not
   maximizing*; *Bet sizing is not intuitive*; *Hedging is for gardeners*; *How to get arbed with
   perfect information (again)*). There is even a post titled *the sound of inevitability* subtitled
   **"Post-mortem on Leopold's SALP"** — post-mortems are a first-class content type here.
8. **Voice:** Conversational, lowercase titles, generous, dense with domain vocabulary (SPUs, EFP,
   NBBO, delta-hedged risk reversals). Posts range 800–3,000 words.
9. **Tech:** WordPress with AMP for WP + Google Site Kit on moontowermeta (heavy: 423 KB landing
   page). blog.moontower.ai is a Ghost-style membership blog with sign-in/sign-up.
10. **Affordances:** Newsletter signup everywhere; the blog exists partly to sell moontower.ai.
11. **Absent:** No résumé, no CV, no photo-forward "about me" on the main page — the About is
    offloaded to Notion.
12. **Anti-patterns:** For a *job search*, this shape is wrong — it is a media property, not a
    portfolio. Discoverability of "who is this person and what should I hire him for" is poor. Also
    a 423 KB landing page and a 404ing `/about/` path.

**Directly relevant to Brad's Sinclair-modelled system:** the site proves a market can exist for
options/vol writing by a former market maker, and its evergreen-wiki-plus-chronological-posts split
is a good structural idea. But it is a *following-building* architecture, not a *hiring* one.

---

## 13. Florian Wechsung — https://florianwechsung.github.io
1. **Exact self-description:** the news line reads **"I have left NYU and joined Citadel GQS as a
   quantitative researcher."** The body still describes him as a postdoc at NYU Courant working with
   Georg Stadler on large-scale nonlinear optimisation under uncertainty applied to nuclear fusion
   reactor design; DPhil Oxford under Patrick Farrell on shape optimisation and fast solvers for
   incompressible Navier-Stokes.
2. **Site type:** Academic homepage.
3. **IA:** Nav = **Home / Publications / Teaching**. Sections: name → Research interests → Education
   → Awards.
4. **First 100 words:** Research interests, then the postdoc, then the doctorate and advisor.
5. **Content types:** Publications page, teaching page, open-source software (SIMSOPT, Fireshape,
   PyROL, Firedrake), awards, Google Scholar.
6. **Evidence format:** Papers plus *named, real, used* open-source scientific-computing packages.
   The optimisation/PDE-solver work is unusually close to what a systematic researcher does.
7. **Rigor signals:** Thesis prize and research-competition awards, named advisors, named packages.
8. **Voice:** Academic, sparse.
9. **Tech:** **Hugo 0.100.2** (generator meta present), Bootstrap 3.3.7, FontAwesome 4.7,
   highlight.js 9.12 with Python grammar, jQuery 3.4.1, MathJax 2.7.5. 7.8 KB.
10. **Affordances:** `wechsung@nyu.edu` in the clear, GitHub, Google Scholar.
11. **Absent:** Nothing about Citadel beyond the one-line news item. No finance content.
12. **Anti-patterns:** The body copy still reads present-tense-academic while the news line says he
    left — a stale-transition smell. Old Bootstrap/jQuery/FA versions.

**The pattern:** the transition from academia into a prop firm is announced as a *one-line news
item* and the site is otherwise unchanged. Nobody in this lane rebuilds their site around the firm.

---

## 14. Tim Tsz-Kit Lau — https://timlautk.github.io
1. **Exact self-description:** "I am currently an **AI Researcher at DRW**, based in Palo Alto,
   California." Header block reads "Tim Tsz-Kit LAU / AI Researcher / DRW / Palo Alto, California."
   Previously postdoc at Penn (Weijie Su, Qi Long) and postdoc principal researcher in Econometrics
   and Statistics at Chicago Booth.
2. **Site type:** Academic homepage.
3. **IA:** Nav = **Home / Bio / Research / Publications / Teaching**, with **CV**, **Google
   Scholar**, **GitHub** and email surfaced immediately under the header.
4. **First 100 words:** Role/firm/location, email, CV/Scholar/GitHub links, then the postdoc
   lineage with named supervisors and departments.
5. **Content types:** Bio, research statement, publications, teaching, CV PDF.
6. **Evidence format:** Publication record + named collaborators + institutions.
7. **Rigor signals:** Named advisors and departments; Scholar profile.
8. **Voice:** Formal academic.
9. **Tech:** Simple static academic template, no generator meta.
10. **Affordances:** `timlautk [AT] gmail.com` obfuscated but present; CV PDF linked.
11. **Absent:** Any DRW content; any trading content.
12. **Anti-patterns:** None serious. Very conventional.

---

## 15. Annie Bryan — https://anniebryan.github.io
1. **Exact self-description:** "I'm a quantitative developer for Arrowstreet Capital in Boston, MA.
   In May 2022, I graduated from MIT, where I double-majored in Computer Science and Mathematical
   Economics and played on the volleyball team."
2. **Site type:** One-page portfolio.
3. **IA:** Nav = **About / Projects / Skills / Contact**. Bio → Résumé button → project cards.
4. **First 100 words:** Role/firm/city, MIT degrees, volleyball, crochet and her dog.
5. **Content types:** Résumé PDF, project cards with tech-stack tags and Code/Demo/Paper links.
6. **Evidence format:** Each project card lists the stack and gives working links: *Wordle Solver*
   (Python, Code), *Interface for Machine Learning Interpretability* (React, NLPaug, TensorFlow,
   sklearn — Demo + About), *Survey of Cryptographic Developments* (Paper).
7. **Rigor signals:** Low; these are coursework-scale projects.
8. **Voice:** Warm, first-person, brief.
9. **Tech:** Static HTML, no generator.
10. **Affordances:** Résumé button prominent; contact section.
11. **Absent:** No writing, no finance content.
12. **Anti-patterns:** Personal-life details (volleyball, crochet, dog) in the first 40 words. Fine
    for a 2022 grad; wrong register for a $250k senior hire.

---

## 16. A. Tuan Nguyen — https://atuannguyen.com
1. **Exact self-description:** "Researcher, Jane Street." Previously "Research Scientist at Meta,
   working on large multi-modal language model for the search problems." PhD in ML, Oxford (Philip
   Torr, Yarin Gal, Gunes Baydin), on distribution shift; MSc at KAIST.
2. **Site type:** Academic homepage (al-folio).
3. **IA:** Nav = **About / Blog / Publications / Teaching / Collaborators**. Sections: name → **News**
   → **Selected Publications**.
4. **First 100 words:** Jane Street role framed as "quantitative finance and machine learning," then
   Meta, then the Oxford PhD with all three advisors named.
5. **Content types:** 6 selected papers (ECCV incl. an oral, CVPR, NeurIPS, ICLR, AAAI), blog,
   teaching, CV PDF, collaborators page.
6. **Evidence format:** Top-tier venue publications, Google Scholar.
7. **Rigor signals:** Named venues, named advisors, oral-presentation distinction.
8. **Voice:** Academic.
9. **Tech:** **Jekyll with the al-folio theme** (stated in the footer). al-folio ships MathJax,
   dark mode, and a publications-from-BibTeX pipeline.
10. **Affordances:** `a.tuan.nguyen at outlook.com`, Scholar, GitHub, LinkedIn, Twitter, CV PDF.
11. **Absent:** Zero Jane Street content. The **distribution shift** thesis topic is arguably the
    most trading-relevant thing on the page and he never connects it to finance.
12. **Anti-patterns:** None. This is the standard "strong ML researcher who happens to be at a prop
    firm" page.

---

## 17. David Álvarez Rosa — https://david.alvarezrosa.com
1. **Exact self-description on the site:** "David Álvarez Rosa — **Mathematician · Engineer ·
   Dublin**" and "I'm a mathematician and engineer based in sunny Dublin, passionate about
   low-latency, high-performance systems." **The site does not name an employer.** (His GitHub bio,
   separately, reads "Software Engineer @ Susquehanna | Algorithmic Trading | Low-Latency Systems |
   High-Performance Computing" — I am flagging that as the *GitHub bio*, not a site claim.)
2. **Site type:** Technical blog + personal site.
3. **IA:** One-paragraph bio → **Recent Posts** feed with dated excerpts.
4. **First 100 words:** "Hi! This is my personal site, where I share notes on software and
   self-hosting. You'll learn how things work under the hood, and how to make them run fast, very
   fast." Then the mathematician/engineer line, free-software advocacy, Emacs, and GitHub/GitLab/
   LinkedIn links.
5. **Content types:** Posts, tagged by topic (`performance`, etc.). One post is a milestone note —
   *One Hundred Thousand Reads* — which frames the site as "a public notebook that almost no one
   read. The plan hasn't changed: one post a [week/month]."
6. **Evidence format — reproducible benchmarking.** *Tuning a Server for Benchmarking* (~1,300
   words) opens with the thesis "a measurement is only useful if it is repeatable: a 2% improvement
   is invisible under 5% of noise," then shows the actual C++ google-benchmark harness inline
   (`PauseTiming`/`ResumeTiming`, `DoNotOptimize`, `alignas(64)`), the exact compiler flags
   (`-O3 -march=native -mtune=native -flto -ffast-math`), the exact command
   (`--benchmark_repetitions=10 --benchmark_min_time=200x`), and the raw output
   (`BM_Sum_mean 99575 ns`, `BM_Sum_stddev 2704 ns`, `BM_Sum_cv 2.72%`), then tunes the machine step
   by step, **re-measuring after every change**.
7. **Rigor signals — best-in-class for the "not fooling yourself" axis in an engineering register.**
   He uses **coefficient of variation** as the headline metric rather than the mean. He uses
   **sidenotes** (numbered margin notes, Tufte-style) for caveats, e.g. distinguishing "tuning for
   benchmarking" (repeatability, even at the cost of peak speed) from "tuning for performance."
   Every number is reproducible by the reader.
8. **Voice:** Precise, instructional, first-person-plural, ~1,300 words per post.
9. **Tech:** **Fully self-contained** — zero external CSS or JS files (everything inlined),
   `prefers-color-scheme` dark mode, KaTeX, HTML `<table>`s and `<pre>` blocks rather than images.
   38 KB for a full article page. Sidenote layout. This is the best-engineered site in the sample.
10. **Affordances:** GitHub, GitLab, LinkedIn. No email, no CV.
11. **Absent:** Employer, résumé, contact email.
12. **Anti-patterns:** None technical. The only gap is that a recruiter has no way to contact him.

---

## 18. Tr8dr — https://tr8dr.github.io ("Musings on Algorithms, Models, and the Markets")
1. **Exact self-description:** "These are my musings about strategies, statistics, computer science,
   numerical techniques, etc. **I am a quant / developer, living in the New York area.**" Career
   narrative: joined a Lehman Brothers research group in the 90s doing "Neural Nets, VR, Parallel
   Processing, and NLP – applied to trading and risk management"; New York, Japan, London; built
   "the first electronic marketplace for bonds in Japan in the late 90s"; moved to algo trading in
   the mid-2000s. **Pseudonymous — no real name, no current employer.**
2. **Site type:** Long-running strategy-research blog.
3. **IA:** Nav = **Data / Links / About**, plus a post feed. A dedicated **Data** page is unusual and
   good — it signals data provenance as a first-class concern.
4. **First 100 words:** Straight into the current post.
5. **Content types:** Posts on MEV/DEFI arbitrage path optimisation, crypto stat-arb, adaptive
   state-based mean reversion.
6. **Evidence format:** Algorithmic write-ups with graphs and problem framing (e.g. optimal size and
   path of arbitrage through ~700K ERC20 tokens and a few hundred thousand AMM pools; brute-force vs
   graph approaches). MathJax present.
7. **Rigor signals:** Explicit scoping of problem size and of which approaches only work for small
   graphs. Named strategy families rather than claimed returns.
8. **Voice:** First-person, technical, medium length.
9. **Tech:** Jekyll on GitHub Pages, MathJax, inline SVG.
10. **Affordances:** None — no email, no name, no CV.
11. **Absent:** Identity.
12. **Anti-patterns / caveat:** **Pseudonymous.** Included because it is a real, verified,
    NY-quant-authored technical site with a useful *Data* section, but it is the counter-example for
    Brad: an anonymous blog builds an audience, not a job offer. Listed last among the strong sites
    for that reason.

---

## 19. Jordan Kaye — https://jordankaye.dev ("Organizing Chaos")
1. **Exact self-description on the site:** none. The site tagline is "Thoughts on technical
   leadership and software engineering." (GitHub bio, separately: "Head of Technology at Belvedere
   Trading." The *site* never says this.)
2. **Site type:** Technical-leadership blog.
3. **IA:** Nav = **Archive / Tags / About / Lexicon / Follow**.
4. **Posts:** *Refinement in Rust: optimization, arithmetic, and stateful predicates*; *Refined:
   simple refinement types for Rust*; *Technical debt and conscious decision making*; *Spending time
   wisely*; *Letting go*; *Overcorrection*; *A Rust + WASM development environment with Nix*;
   *Enabling constraints*; *A few fast solutions for Advent of Code 2023*; *Minimize global process*.
5. **Content types:** Posts, a released open-source Rust library (`refined`), podcast appearances.
6. **Evidence format:** Shipping a real library and writing the design rationale for it; performance
   claims on Advent of Code solutions (sub-1 ms).
7. **Rigor signals:** Design-tradeoff essays; the library is public and inspectable.
8. **Voice:** Reflective engineering-management prose interleaved with hard Rust posts.
9. **Tech:** Static (Hugo/Jekyll-shaped archive + tag structure).
10. **Affordances:** GitHub, LinkedIn. No email, no CV.
11. **Absent:** Employer, finance content of any kind.
12. **Anti-patterns:** A "Lexicon" nav item is idiosyncratic; last post Feb 2025.

**Pattern confirmation:** a *Head of Technology at a market-making firm* runs a public blog and never
once mentions the firm or the market. The alternating leadership/deep-technical rhythm is a useful
model.

---

## 20. Saksham Sharma — https://sakshamsharma.com
1. **Exact self-description on the site:** the tagline under his name is a single word — **"Quant."**
   (GitHub bio, separately: "Director, Quant Research Technology. @tower-research.")
2. **Site type:** Personal technical blog, 46 posts.
3. **IA:** Nav = **Home / About / GitHub / LinkedIn / Résumé / RSS**; landing page shows
   **Categories**, **Tags**, **Recents**.
4. **Content types:** C++/Haskell/Linux tutorials, career narratives (Google internship, Max Planck),
   project documentation, cryptography and algorithms posts, sysadmin guides, and poetry.
5. **Evidence format:** Deep technical posts on distributed systems, functional programming,
   infrastructure.
6. **Rigor signals:** Moderate — it is craft writing, not empirical research.
7. **Voice:** Personal, varied.
8. **Tech:** **Hakyll** (Haskell static site generator) with an RSS feed — the generator choice is
   itself a competence signal to the right reader.
9. **Affordances:** Résumé in the nav; GitHub and LinkedIn.
10. **Absent:** Employer on the site; any finance content.
11. **Anti-patterns:** Poetry sits in the same feed as the technical posts, diluting the signal.

---

# PART 2 — INSTRUCTIVE NEGATIVES

These loaded successfully but are either not real personal sites, or are counter-examples worth
knowing.

- **https://dev-kewlani.github.io/** — Dev Kewlani, "Quantitative Summer Associate at JPMorgan Chase
  & Co." **Not a prop firm; a student.** Included as the canonical anti-pattern gallery: skill
  percentage bars ("Python 95%, Risk Modeling 95%, Time Series Analysis 95%"), a hero counter row
  ("4.0 GPA, 2+ years experience, 4+ major projects"), and unsourced performance claims
  ("1.7 Sharpe Ratio", "45% cumulative profit", "250%+ returns", "65% accuracy") with no data
  window, no universe, no cost assumptions, no out-of-sample split. Tagline: "Building Quantitative
  systems that find signal in the noise." A quant hiring manager will discount everything on the
  page the moment they hit an unqualified Sharpe.

- **https://www.shreejitverma.com** — Shreejit Verma, "Quantitative Developer, Quantitative
  Researcher, and Quantitative Trading Engineer based in New York. I build ultra-low latency C++
  market-making systems." Next.js + Tailwind, well built technically. But: three job titles stacked
  in one sentence; nav sections named **"Technical Arsenal," "Impact," "Intelligence," "GitHub
  Impact"**; unsourced deltas ("20% Sharpe ratio improvement", "29% execution efficiency gain"); a
  Calendly link. The listed employers are BNP Paribas / Versor / Bank of America / LogiNext, i.e.
  bank and asset-manager roles, while the positioning claims HFT market-making. **That gap between
  claimed positioning and verifiable history is precisely what this audience is trained to spot.**
  This is the single most important site in the report to *not* imitate — and it is the one closest
  in ambition to what Brad might be tempted to build.

- **https://hwz0428.github.io/** — GitHub bio says "Quantitative researcher at Citadel Securities,"
  but the live site is still a **6th-year photonics PhD page** at UC San Diego. Stale-site failure
  mode: the bio and the site disagree, and the site wins because it's what a recruiter loads.

- **https://zihuiwu.github.io/** — GitHub bio says "QR @ Jump Trading"; the site is still a Caltech
  CMS PhD-student page (Jekyll + AcademicPages, fork of Minimal Mistakes) with computational-imaging
  publications and no mention of Jump. Same failure mode.

- **https://kevvyang.com** — Kevin Yang (GitHub bio: "Quant Trader @ Belvedere Trading · ex SIG").
  The page renders only the word **"Loading…"** — a client-side SPA shell with no server-rendered
  content. Nothing is readable without executing JS. A recruiter's link preview, a text-mode
  fetch, and most crawlers see an empty page. Hard lesson: **never ship a JS-only shell for a
  hiring-facing site.**

- **https://www.jakob-aungiers.com** — Jakob Aungiers, "I work as a quantitative researcher and
  trader for proprietary trading firms," founder of Altum Intelligence. The *nav* is ABOUT /
  ARTICLES / CONTACT, but the **section headings** are: Who Am I? → Companies I've Invested In →
  Conferences & Events → **Skydiving** → **Surfing** → **Flying** → Contact. The competence signals
  the page actually foregrounds are 2,500+ skydives, a world record, an FAA instrument rating, and
  an ISA surf-instructor certification. For a lifestyle brand this works; for a quant hire it buries
  the one relevant claim under three hobby sections.

- **http://www.vitorian.com** — Henrique Bucher, "Chief Executive Officer" of Vitorian LLC,
  previously "Global Head of Ultra Low Latency Trading Technology at JP Morgan (2011–2020)" and
  "Financial Engineer at Citadel Investment Group." **This is a company/consultancy site, not a
  personal site** — it has services, testimonials, a team page, a Calendly, a street address and two
  phone numbers. Noted because the *content strategy* is relevant: a Substack ("Low Latency Trading
  Insights," 4,000+ subscribers) is the credibility engine and the corporate site is the conversion
  layer.

- **https://www.zeelmpatel.com** — Zeel M. Patel, "I am a computer scientist, investor, and
  advisor," NYC; states he is "currently serving a non-compete with Citadel Securities." Real site,
  clean four-section IA (Personal / Background & Work / Interests & Projects / Contact), email in the
  clear. Included mainly for the disclosure register: stating a non-compete openly is a maturity
  signal, but the site has no demonstrable work product.

- **https://jmerle.dev/** — Jasper van Merle, "Software Engineer @ IMC Trading" (GitHub bio). The
  site itself is a name plus three links (GitHub, LinkedIn, `jaspervmerle@gmail.com`) and states no
  role. Effectively a link page.

- **https://bowenyu.me** — renders "Please enable JavaScript to view this page." Same failure mode
  as kevvyang.com.

- **https://mirayadav.com** (Radix quant dev) — DNS does not resolve. **https://guazi.dev** — TLS
  error 525. **https://jlscheerer.me** (Radix quantitative technologist) — loads but returns
  essentially only a name. **https://icosahedral-dice.github.io** — a GitHub profile-README template
  ("Just another econ undergraduate from Peking University") with auto-generated repo cards, not a
  real site. All discarded.

---

# PART 3 — SYNTHESIS

## 3.1 The structural fact that governs this lane

**The employer badge and the content volume are inversely correlated.** Ming Fong (Headlands, HFT
strategies) publishes ~250 words total. Nick Georgakopoulos (Radix) publishes five *pre-2022* math
papers and nothing since. Leo Adberg (HRT) publishes graphics demos and nothing about trading.
Meanwhile Mark Best, Kipp Rogers, Colin Swaney, and Mike DeCrescenzo publish tens of thousands of
words and **none of them names a current employer**.

The reason is compliance, not modesty. Once you can write "Quantitative Researcher at Jane Street"
you have already transmitted the entire signal and every additional word is legal risk. Once you
cannot write that, prose is the only channel you have.

**Brad is structurally in the second group.** He has no prop-firm badge, so the badge-minimal
architecture (sites 1, 2, 5, 6, 15, 16) is unavailable to him — copying it would produce a page that
says nothing. He should build in the register of sites 11 (Mark Best), 10 (Kipp Rogers), 8 (Colin
Swaney), and 17 (David Álvarez Rosa): the sites whose authority comes from demonstrated reasoning.

## 3.2 The 14 recurring characteristics, ranked by how much I think they move a quant hiring manager

1. **A visible record of research that failed, framed as normal.** Rarest and highest-value. Mark
   Best: "Almost all of what I have looked at has been a dead end… most research ends up in the
   bin." A hiring manager reads this as someone who has actually done research. Nobody who is
   fabricating results writes this sentence. Brad's planned post-mortems are exactly this asset —
   they should be a *named, navigable content type*, not buried.

2. **Paper-vs-live (or in-sample-vs-out-of-sample) reconciliation, with the divergence *explained
   mechanistically*.** Mark Best's four-part slippage series is the only instance I found of anyone
   in this lane publishing a simulation-vs-paper-vs-live table — and the value is not the 0.000557%
   number, it is "the forecast takes about 200 ms to calculate on a new bar thus in paper and live
   the orders are sent later than in sim" and "crypto exchanges lack sequence IDs." Naming the
   mechanism of your own slippage is the strongest possible evidence that you have run a real system.

3. **An explicit, standing disclaimer / errors-may-exist statement.** Kipp Rogers' About paragraph is
   the template: who I am, this is not my employer's view, "the products of analysis **which may
   have errors**," this is not investment advice — plus a per-post "please discuss anything that
   looks wrong in the comments or over email." This costs nothing and buys enormous credibility with
   an audience whose job is scrutinising claims.

4. **Public / crypto / synthetic data as the research substrate.** The universal solution to the IP
   problem. Mark Best does all published research on BYBIT crypto data; Kipp Rogers works entirely
   from SEC filings, exchange rule filings, regulatory reports and the academic literature; Tr8dr
   uses on-chain data and keeps a dedicated **Data** page. Brad should state his data provenance
   explicitly and prominently — vendor, universe, date range, and what he had to pay for or proxy.

5. **Stating the boundary of what you are *not* claiming.** Three separate instances:
   Mark Best — "my aim is not to get a perfect simulator"; Colin Swaney — the posterior is "a
   well-known result… easy to look up" (i.e. *I did not derive this*); David Álvarez Rosa — "tuning
   for benchmarking is not the same as tuning for performance." Each is one sentence and each
   converts a potential criticism into evidence of self-awareness.

6. **A repeatability/noise metric reported alongside the headline number.** David Álvarez Rosa leads
   with **coefficient of variation**, not the mean, and re-measures after every single change. The
   trading analogue is obvious and underused: report the dispersion, the number of independent
   trials, and the sensitivity — not just the point estimate.

7. **Open-source code that someone else uses.** Ties de Kok's eleven-word killer: IPyStata is
   "Officially integrated into Stata as of Stata 17." Also Nick Georgakopoulos's C++ libraries,
   Florian Wechsung's SIMSOPT/Fireshape/Firedrake contributions, Jordan Kaye's `refined` Rust crate,
   Mark Best's Rust HFT logger. Third-party adoption is unfakeable and IP-free.

8. **Infrastructure writing as a safe competence proxy.** Latency, logging, OMS design, message
   arrival rates, benchmark methodology, candlestick construction. Mark Best, David Álvarez Rosa,
   Jordan Kaye and Panagiotis Kostopanagiotis all lean on this. It proves engineering seriousness,
   is fully verifiable by the reader, and contains zero alpha. For Brad this maps directly onto his
   logging and documentation work — that is not a boring side-detail, it is publishable proof.

9. **A clean, boring, five-to-six-item nav that separates *kinds* of evidence.** Ties de Kok's
   **About me / Research / Code & Data / Talks & Classes / Blog Posts / CV** is the best IA in the
   sample and would transfer to Brad almost unchanged (→ About / Research / Code & Data / Writing /
   Track Record / CV). The pattern that repeats: a hiring manager wants to jump straight to the
   *type* of evidence they trust, and each nav item should be one type.

10. **Abstracts / one-line summaries rendered inline, so nothing requires a click to evaluate.**
    Ties de Kok expands full abstracts on the research page; Kris Abdelmessih puts a one-line
    subtitle under every post title ("Futures lead the cash"; "an example of a market-maker decision
    to not hedge"); Mark Best's feed shows 60–80 word excerpts. Assume the reader gives you 45
    seconds and never clicks.

11. **Correct, rendered mathematics.** MathJax or KaTeX is present on essentially every serious site
    in this lane (Colin Swaney, Mike DeCrescenzo, Nick Georgakopoulos, Panagiotis Kostopanagiotis,
    Florian Wechsung, Mark Best, Tr8dr, David Álvarez Rosa). Its **absence** on a quant site is a
    negative signal; its presence with stale/broken CDNs (Nick Georgakopoulos points at the dead
    `cdn.mathjax.org`) is worse than not having it.

12. **Real citations to primary sources.** Colin Swaney cites Neal 2003 and Murray et al. 2010; Kipp
    Rogers cites the empirical impact literature across equities, futures and bitcoin. Citing papers
    rather than blog posts is a cheap, strong signal of where you learned things. For Brad this maps
    onto Sinclair and López de Prado directly — but cite the specific results, not just the names.

13. **A closed date range or explicit scope fence around pre-employment work.** Nick Georgakopoulos's
    "Math Papers and Code **(2017–2022)**"; Sunny Balasubramanian's "**Formerly** at Citadel, AQR";
    Zeel Patel's stated non-compete. Signalling that you know where the line is *is itself* the
    signal that you can be trusted near proprietary information.

14. **Speed, self-containment, and server-rendered HTML.** The best sites are 3–16 KB and load in
    under 0.3 s (Ties de Kok 3.3 KB / 0.16 s; Ming Fong 5.9 KB / 0.20 s). David Álvarez Rosa inlines
    *all* CSS and JS, uses real `<table>` and `<pre>` elements rather than screenshots, and supports
    `prefers-color-scheme`. Two sites in the sample (kevvyang.com, bowenyu.me) render literally
    nothing without JavaScript — an unforced, total failure.

## 3.3 Patterns specific to prop/HFT people — how they prove ability without disclosing IP

This is the part most directly useful to Brad, because it is a *solved problem* in this population.
Seven distinct mechanisms, in rough order of usefulness to him:

1. **Move the research onto a public market.** Crypto is the standard choice — it is liquid, the
   data is free or cheap, the microstructure is genuinely interesting, and nothing you publish about
   it belongs to your employer. Mark Best runs his entire public research programme on BYBIT/Bitcoin
   data while working in HFT. Brad's vol system is on equity options; the transferable version is to
   run the *methodology* posts on a dataset whose provenance he can state completely.

2. **Publish the method, withhold the parameters.** Every rigorous post in this lane shows the
   estimator, the code, the diagnostic and the failure mode — and never the fitted values, the
   universe weights, or the live sizing. *Alpha Decay* shows the boxplot and the profit-factor
   formula and the pandas code, and no signal.

3. **Publish infrastructure instead of alpha.** Logging, OMS pitfalls, benchmark repeatability,
   message-rate/latency analysis. Fully checkable, obviously hard, zero disclosure risk.

4. **Publish *negative* results and open problems.** "It is not clear to me how this could be
   converted to a single measure." "More to follow…" Open problems are safe to publish precisely
   because they aren't edge, and they demonstrate taste in problem selection better than solutions
   do.

5. **Anonymise the employer to a category.** "An algorithmic trading firm" (Mike DeCrescenzo). "I am
   a quant / developer, living in the New York area" (Tr8dr). "Startups… taught me most of what I
   know about HFT system architectures, HPC and market-making strategies" (Mark Best). This is a
   recognised professional register; readers in the industry decode it instantly and read it as
   compliance-literate rather than evasive.

6. **Describe employer work by *desk and stack*, never by *strategy or P&L*.** Panagiotis
   Kostopanagiotis: "ultra-low latency infrastructure for options market making in C++, spanning
   European Index Options and Crypto Options desks." That sentence is highly informative to a
   hiring manager and discloses nothing. It is the exact template for how Brad should describe Nift,
   Ticketmaster, Lockheed and Boeing work.

7. **Fence off pre-employment work with dates.** "(2017–2022)". "Formerly at Citadel, AQR."

**And the single most important negative finding: not one person in this lane publishes an equity
curve with a headline Sharpe ratio.** The only performance-shaped artefact anyone published was Mark
Best's *slippage* table — an execution-quality reconciliation, not a returns claim. In this
population, a big Sharpe number on a personal site reads as either (a) a compliance violation, or
(b) an overfit. Brad's live out-of-sample track record is a genuine differentiator, but the framing
that will land with this audience is **"here is my out-of-sample discipline, here is the paper-vs-live
divergence and why it happened, here is what I got wrong"** — not "here is my Sharpe."

## 3.4 Anti-patterns catalogue (things I saw that would actively hurt)

- Skill percentage bars / proficiency meters ("Python 95%").
- Unsourced performance figures: a Sharpe, a return, or a "% improvement" without universe, date
  range, cost model, and out-of-sample split.
- Title stacking ("Quantitative Developer, Quantitative Researcher, and Quantitative Trading
  Engineer").
- Sections named "Technical Arsenal," "Impact," "Intelligence," "GitHub Impact."
- Positioning that outruns the verifiable CV (claiming HFT market-making with a bank/asset-manager
  history).
- Calendly on a personal quant page — reads as consulting-sales, not candidacy.
- Stale sites where the landing page still describes a role you left years ago (two Citadel/Jump
  researchers are still presenting themselves as PhD students).
- JS-only shells that render "Loading…" to anything that doesn't execute JavaScript.
- Hobby sections (skydiving/surfing/volleyball/crochet) positioned above or level with the technical
  evidence.
- Dead or hijacked third-party dependencies: `cdn.mathjax.org`, `polyfill.io`, jQuery 1.11,
  Bootstrap 3 / FontAwesome 4.
- Code gated behind "email me for access to private repositories."
- No contact path at all (four of the most technically impressive sites here have no email — good
  for them, wrong for a job search).
- `*.wordpress.com` / `*.github.io` default domains for a $250k-role-facing site, when a custom
  domain costs $12.

## 3.5 Concrete transfers for bradlasater.github.io

- **Adopt a Ties de Kok–shaped nav:** About / Research / Code & Data / Writing / Track Record / CV.
  Each item is one *kind* of evidence.
- **Make "post-mortems" or "failed experiments" a named, linked content type in the nav or on the
  research index.** Nobody else in this lane has one. It is the highest-differentiation, lowest-cost
  thing on this list, and it is already what Brad is producing.
- **Write a Kipp-Rogers-style standing disclaimer** on the About page: what this is, whose views it
  isn't, that the analysis may contain errors, that corrections are welcome by email.
- **Reframe the live track record around reconciliation, not returns**: sim vs paper vs live, with
  the divergences explained mechanistically (latency, fill assumptions, borrow, vol-surface staleness).
- **Add a Data page** (Tr8dr has one; almost nobody does): every source, vendor, date range, known
  gaps, and what had to be proxied.
- **Describe prior employers by problem and stack, not by achievement percentage** — the
  Kostopanagiotis template.
- **Ship server-rendered HTML, inline the CSS, support `prefers-color-scheme`, use KaTeX, keep the
  landing page under ~20 KB, use real tables and `<pre>` blocks instead of screenshots.** David
  Álvarez Rosa's site is the technical reference implementation.
- **Put an email address in the clear and a CV PDF in the nav.** Brad is job-searching; the people
  above mostly are not, which is why they can afford to omit both.

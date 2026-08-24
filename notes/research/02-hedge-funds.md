# Research 02 — Personal Websites of Quant Researchers / PMs at Multi-Strategy & Systematic Funds

**Lane:** personal websites of people who currently or recently work as quantitative researchers,
portfolio managers, or quant developers at multi-strategy / systematic hedge funds and quant asset
managers (Two Sigma, D. E. Shaw, Millennium, Point72/Cubist, Balyasny, Squarepoint, Schonfeld,
WorldQuant, AQR, PDT, Voleon, Man, Qube, Marshall Wace, CFM, Acadian, BlackRock Systematic, GS/MS/JPM
quant strats).

**Method:** WebSearch to generate candidates → WebFetch / curl to actually load every reported URL →
HTML source inspection for generator tags, CSS/JS assets, viewport meta, math rendering.
Every site below was successfully loaded by me. Role/employer text is quoted **exactly as the site
states it**; where a site states no employer, that is recorded explicitly.

**Client context:** Brad Lasater, targeting NYC quant roles ~$250k base; background in applied ML,
optimization, state estimation (Nift, Ticketmaster, Lockheed Martin, Boeing); building an end-to-end
volatility trading system modeled on Euan Sinclair and Marcos López de Prado, with heavy docs,
logging, and written post-mortems.

---

## PART 1 — VERIFIED SITES (deep analysis)

---

### 1. Qiwen Cui — https://qwcui.github.io/

**Exact self-description:** "I am a quantitative researcher at Two Sigma. I did my Ph.D. in the Paul
G. Allen School of Computer Science & Engineering at the University of Washington, where I was very
fortunate to be advised by Professor Simon Shaolei Du."
Page label: "Quantitative Researcher at Two Sigma."

**Site type:** Pure academic homepage. Three pages, no blog, no projects.

**Information architecture:** Nav = Home | Publications | CV. Above the fold: name, one-line role
label, photo, "About me" paragraph, email, Google Scholar link. Section order on home: About me →
Selected Publications (grouped by research theme).

**Positioning line:** Employer first, PhD second, advisor third. The claim is "I am a credentialed
ML theory researcher who now works at Two Sigma" — not "here is what I can do for you."

**Content types:** Peer-reviewed papers + arXiv preprints, CV PDF, Google Scholar. No blog, no code,
no talks, no teaching, no projects.

**Evidence presentation:** Publications grouped under *topic* headings rather than by year —
"Offline Multi-agent Reinforcement Learning", "Online Multi-agent Reinforcement Learning", "Learning
in Congestion Games", "Reinforcement Learning for AI System". Each entry: linked title → author list
with asterisks for equal contribution → venue (NeurIPS/ICML-class) or arXiv ID. That is it. No
abstracts, no figures, no metrics, no narrative.

**Rigor signals:** Entirely delegated to peer review. Venue names are the proof. No data sources, no
out-of-sample discussion, no caveats — because nothing on the site is a performance claim.

**Voice / length:** Three sentences of prose total on the whole homepage. Zero adjectives.

**Technical implementation:** `<meta name="generator" content="jemdoc">` — jemdoc, a ~2007-era
academic static site generator. Single `jemdoc.css`, table-based layout (`table#tlayout`), Georgia
serif body, white background. **No `<meta name="viewport">` tag at all — the site is not mobile
responsive.** No dark mode. No math rendering.

**Contact/recruiting:** Obfuscated email (`qwcui1107 [at] gmail (dot) com`), Google Scholar, CV PDF.
No "hire me," no LinkedIn CTA.

**Notable absences:** No finance content whatsoever. Nothing about markets, Two Sigma work, alpha,
or trading. The industry job is a one-line credential; the intellectual identity is RL theory.

**Anti-patterns:** None that would hurt him — but note this site works *only because* the
publication list is at top venues. Copy this format without top-tier papers and the page is empty.

---

### 2. Jonathan Lacotte — https://jonathanlctt.github.io/

**Exact self-description:** "I am a Quantitative Researcher at Tower Research Capital (Latour team)
in New York, where I design and apply machine learning methods to build predictive signals (alphas)
for global financial markets."

**Site type:** Minimal three-page portfolio (Home / Research / Code).

**Information architecture:** Nav = Home | Research | Code. Above the fold: the positioning
sentence, then an "Education" section (Stanford PhD, advisor link to Mert Pilanci).

**Positioning line:** The single strongest sentence in this whole survey for Brad's purposes,
because it names *the firm, the desk, the method, and the output*: "design and apply machine
learning methods to build predictive signals (alphas) for global financial markets." It converts a
generic ML background into a market-facing job description in one line.

**Content types:** Research page (papers), Code (GitHub link). No blog, no CV PDF surfaced on home,
no talks, no teaching.

**Evidence presentation:** Publication list on a separate page; GitHub for code. Very thin.

**Rigor signals:** None on the homepage — no numbers, no charts, no methodology. The Stanford PhD +
named advisor + firm name is the entire credibility stack.

**Voice / length:** Two paragraphs. Telegraphic.

**Technical implementation:** Hand-rolled Bootstrap 3 with jQuery 1.11 from Google CDN. Loads
`css/bootstrap.min.css`, then **`css/non-responsive.css`** — i.e., he deliberately disabled
Bootstrap's responsive grid. Desktop-only by design. No math rendering, no dark mode.

**Contact/recruiting:** GitHub link, advisor link. No email visible on home.

**Notable absences:** No trading results, no writing, no explanation of what "alphas" means to a
non-quant, no CV on the landing page.

**Anti-patterns:** Nearly zero content — this is a business card. It works because "Tower Research /
Latour" + "Stanford PhD under Pilanci" is already the whole message. Brad cannot borrow this form
because he does not yet have the firm name to do the work.

---

### 3. William Chen — https://www.wzchen.com/

**Exact self-description:** "I was previously a Quantitative Researcher at Two Sigma. Prior to that,
I was a Data Science Manager at Quora. Back in college, I studied statistics."
**No current employer is stated anywhere on the site.**

**Site type:** Hybrid personal-brand / educational-artifacts site. Not a research site.

**Information architecture:** Nav = Free Data Science Books | Probability Cheatsheet | Escape Room
Tips | Media | Contact Me | Home. Home sections: name → "Some Things I've Worked On" → talks →
Escape Room Tips → "How to Build a Compelling Data Science Portfolio and Resume" → Probability
Cheatsheet → Free Data Science Books.

**Positioning line:** Past tense, deliberately. He is positioned as an *educator and
artifact-producer*, not as an employee.

**Content types:** YouTube talks, downloadable PDFs (the Probability Cheatsheet, which has been
downloaded enormously), curated book lists, blog posts, media appearances.

**Evidence presentation:** Distribution and reuse, not publications. The proof is "hundreds of
thousands of people use my cheatsheet" — artifacts that traveled. This is a *reputational* proof
format rather than a *technical* one.

**Rigor signals:** Essentially none — and it does not matter for his purpose, but it would matter a
lot for Brad's.

**Voice / length:** Friendly, second-person, short.

**Technical implementation:** Squarespace (`assets.squarespace.com`, `site-bundle.js`), Typekit
fonts, Google Analytics. Responsive, modern, visually polished — by far the most *designed* site in
this survey, and the least technically credible one.

**Contact/recruiting:** LinkedIn + a Contact page.

**Notable absences:** No papers, no code, no math, no market content, no CV.

**Anti-patterns for a quant hiring manager:** Escape-room content sits in the primary nav directly
adjacent to the Two Sigma credential. The site says "content creator," not "researcher." Instructive
as an inverse example: **polish and personality without technical substance reads as a career
change, not a quant.**

---

### 4. Bryan T. Kelly — https://www.bryankellyacademic.org/

**Exact self-description:** "Bryan Kelly is Frederick Frank '54 and Mary C. Tanner Professor of
Finance at the Yale School of Management and Head of Machine Learning at AQR Capital Management. He
is also a Research Fellow at the National Bureau of Economic Research and Co-director of Yale's
Swenson Asset Management Institute."

**Site type:** Academic homepage with a practitioner-facing data-distribution layer bolted on.

**Information architecture:** Nav = Home | CV | Publications | Working Papers | My Google Scholar |
Data | Contact | More. Sections on home: About Me → **Data** → Publications → Published Articles →
Working Papers → Contact. Note that **Data comes before Publications** — the most reused artifact is
promoted above the credential list.

**Positioning line:** Dual identity stated in one sentence: chaired professor *and* Head of ML at
AQR. This is the canonical "academic legitimacy + fund legitimacy" construction.

**Content types:** ~47 numbered published articles, working papers, CV PDF, GitHub code repos,
downloadable factor/characteristics datasets with PDF documentation, Google Scholar.

**Evidence presentation:** Publications numbered 47 → 1 (descending), title in caps, journal + year,
co-authors in parentheses, SSRN or DOI link. Plus a **Data** section that ships actual usable
research inputs (factor data, firm characteristics) with documentation. That data section is the
single most practitioner-relevant thing on the site: it lets a stranger *use* his research rather
than merely read it.

**Rigor signals:** Top-5 finance journals do the heavy lifting. Reproducibility signaled via public
data + code repos. No performance claims to caveat.

**Voice / length:** Third person, institutional, formal.

**Technical implementation:** `<meta name="generator" content="Wix.com Website Builder"/>` — Wix,
with React/Thunderbolt bundles and Sentry. **A Wix site.** No math rendering. Responsive.

**Contact/recruiting:** Full institutional address, office phone, university email — the academic
convention of maximal contactability.

**Notable absences:** No blog, no essays, no opinion, no trading discussion, no AQR-specific
content. The AQR affiliation is asserted but never elaborated.

**Anti-patterns:** Wix is aesthetically undistinguished, and nobody cares. This is the clearest
evidence in the survey that **for this audience, site technology carries approximately zero signal.**

---

### 5. Lasse Heje Pedersen — https://www.lhpedersen.com/

**Exact self-description:** "I am a financial economist who loves to solve real-world problems using
models and data. A Stanford PhD, I am a professor at Copenhagen Business School, director of the
BIGFI center, and a principal at AQR."

**Site type:** Academic homepage + book platform.

**Information architecture:** Nav = Home | Research | Data | Vita | Books | Teaching | More.
Home sections: Bio → News → Research Summary → Translations → Disclosure Statement → Archive →
Contact.

**Positioning line:** Leads with *disposition* rather than title — "loves to solve real-world
problems using models and data" — then stacks credentials. This is the only site in the survey whose
first clause is about how the person works rather than where they work. Worth noting for Brad: it is
the one opening that a non-PhD could plausibly imitate without sounding thin.

**Content types:** Papers (SSRN links), books (*Efficiently Inefficient*, *Market Liquidity*), data
downloads, Vita PDF, teaching materials, media/podcasts, translations.

**Evidence presentation:** SSRN abstract-ID links, italicized titles, dates. Plus a **Data** section
and a **Disclosure Statement** — the latter is a compliance-flavored artifact almost never seen on
engineer portfolios, and it reads as extremely industry-native.

**Rigor signals:** Journal venue + public data. The explicit Disclosure Statement (declaring the AQR
relationship) is itself a rigor signal: it says "I know my affiliations could bias what I publish and
I am telling you up front."

**Voice / length:** First person, warm, economical.

**Technical implementation:** **Google Sites.** Lato throughout, responsive viewport. Zero custom
engineering.

**Contact/recruiting:** Full postal address, two institutional emails.

**Notable absences:** No code repos, no blog, no negative results.

**Anti-patterns:** None material.

---

### 6. Artur Sepp — https://artursepp.com/ (and /research/)

**Exact self-description:** "I am Global Head of Quantitative Analytics at LGT Private Banking,
Zurich, leading a quant team of 10+ across portfolio construction, factor analytics, systematic
macro, and applied GenAI." Later in the same block: "20+ years across the sell-side and buy-side —
equity, credit and rates derivatives, a systematic CTA, crypto/DeFi, now private banking";
"Risk Magazine Quant of the Year 2024"; "Co-author of the log-normal beta stochastic volatility
model; ~1,200 citations"; "PhD in Mathematical Statistics, University of Tartu"; "Associate Editor,
Journal of Computational Finance."

**Site type:** Research blog + publication archive. **This is the single closest model for Brad's
site in the whole survey** — a practitioner who is not a professor, whose entire credibility rests on
volatility research he published himself.

**Information architecture:** Nav = Blog | Research | About. Home page *is* the About page:
positioning paragraph → external profile links (LinkedIn, SSRN, Google Scholar, GitHub, Twitter) →
email → reverse-chronological list of ~20 post titles with dates.

**Positioning line — worth studying closely.** It does four things in one paragraph:
1. Names the role and the team size (scope of responsibility).
2. Names the *specific framework he built* — "ROSAA (Robust Optimization of Strategic and Active
   Asset Allocation) … published in the Journal of Portfolio Management (2026)" — a named artifact
   with a citation.
3. States a **thesis about markets**, not about himself: *"volatility regimes migrate across asset
   classes, and models that feel robust fail at the worst moment. I build frameworks designed to
   survive regime change."* This is the most important sentence in the survey. It is a market view,
   it is falsifiable, and it explains what all his work is *for*.
4. Quantifies open-source reach: "open-source Python libraries for quantitative finance — portfolio
   optimization, stochastic volatility, factor models — downloaded 300,000+ times."

He also includes one human detail (Brazilian Jiu-Jitsu purple belt) tied back to the work
("patience, adaptability, and problem-solving under pressure").

**Content types:** ~30 research papers, blog posts announcing each paper, presentation slide decks
(QuantMinds etc.), podcast appearances, YouTube seminar recordings, open-source Python packages.

**Evidence presentation — the standout mechanic:** the Research page lists every paper with the
journal reference **and a dropdown that reveals a copy-pasteable BibTeX entry**. Example format:

```
Robust Optimization of Strategic and Tactical Asset Allocation for Multi-Asset Portfolios
(with Ivan Ossa and Mika Kastenholz), Journal of Portfolio Management, 2026, 52 (4), 86-120
  @article{seppossakastenholz2026, ... doi={10.3905/jpm.2025.1.806} }
```

Working papers are labeled "Working Paper" or "Under revision at the Journal of Portfolio
Management" — he does not inflate submission status. Papers carry DOIs, SSRN preprint links, and
publisher links.

**Rigor signals:** peer-reviewed venues (Quantitative Finance, Review of Derivatives Research,
IJTAF, Risk Magazine, JPM); named co-authors including Alex Lipton and Natalie Packham; explicit
"Preprint:" annotations distinguishing preprint from published version; open-source implementations
that let anyone reproduce the models; download counts as adoption evidence.

**Voice / length:** Blog posts are short announcements (a few hundred words) that hand off to the
paper. The heavy content lives in PDFs. **The blog is a distribution layer, not the product.**

**Technical implementation:** WordPress.com (`wp-content/themes/personal`, Jetpack, wpcomsh), PT
Sans via Google Fonts API, **MathJax loaded** for equations. Email-subscribe widget ("Join 348 other
subscribers"). Standard WP responsive theme. No dark mode.

**Contact/recruiting:** `artursepp@gmail.com` in plain text on the front page, plus LinkedIn, SSRN,
Scholar, GitHub, Twitter.

**Notable absences:** No CV PDF. No live track record. No negative results published as such.

**Anti-patterns:** A generic WordPress theme and a slightly cluttered sidebar with duplicated
"Recent Posts" widgets. Immaterial next to the content.

---

### 7. Jonathan Kinlay — https://jonathankinlay.com/ (About: /about/)

**Exact self-description:** "Dr Jonathan Kinlay is the Head of Quantitative Trading at Systematic
Strategies, LLC, a systematic hedge fund that deploys high frequency trading strategies using
news-based algorithms."

**Site type:** Long-running practitioner research blog. Site title: "QUANTITATIVE RESEARCH AND
TRADING". Tagline: "The latest theories, models and investment strategies in quantitative research
and trading."

**Information architecture:** Nav = Home (with a "Systematic Strategies" sub-item) | About. The fund
is one click from every page. Homepage is a reverse-chronological feed with featured image +
100–150-word excerpt per post.

**Recent posts (verified on the live homepage):**
- 2026-08-16 "Your Research Agent Is an Undisclosed Factor Exposure — And So Is Everyone Else's"
- 2026-05-17 "Agentic Workflows for Alpha Research"
- 2026-05-10 "Reinforcement Learning for Optimal Execution"
- 2026-05-04 "Deep Learning for Volatility Surface Repair"
- 2026-03 "State Space Models for Market Microstructure: Can Mamba Replace Transformers in
  High-Frequency Finance?", "Transformer Models for Alpha Generation: A Practical Guide",
  "Reinforcement Learning for Portfolio Optimization: From Theory to Implementation",
  "From Hype to Reality: Building a Hybrid Transformer-MVO Pipeline"
- 2026-02 "GARCH Volatility Clustering Across Asset Classes", "Time Series Foundation Models for
  Financial Markets: Kronos and the Rise of Pre-Trained Market Models"

**Deep read of one post — "Deep Learning for Volatility Surface Repair" (2026-05-04).** This is the
most directly transferable artifact I found for Brad, so I read it in full:

- **~8,500 words**, single-page, self-contained.
- **Full Python/PyTorch implementation inlined (~700 lines)** — a complete runnable script, not
  fragments.
- **Equations in LaTeX**: SSVI parameterization, loss functions, the Gatheral–Roper `g(k)`
  no-arbitrage diagnostic.
- **One 2×3 diagnostic figure**: clean vol / observed quotes / CNN repair / interpolation baseline /
  uncertainty estimates / absolute error.
- **Data provenance stated honestly**: *synthetic only*. 1,600 training SSVI surfaces, test sets from
  "Shifted SSVI" and "SABR-event" families, ~18bp quote noise, structured missingness. No real
  market data, and he says so.
- **Negative results published prominently.** The CNN **loses** to a plain interpolation baseline by
  40% on in-distribution smooth data and is 1.4–2.7× worse on out-of-distribution SABR smiles.
  Butterfly-arbitrage violations remain in 5–11% of points after projection. The uncertainty head is
  badly miscalibrated (28–69% empirical coverage against an 80% nominal target). Stale-quote
  detection AUC is only 0.55–0.66.
- **Explicit limitation paragraph, verbatim:** *"It does not show that this kind of CNN-based repair
  is useful on real data. The synthetic surfaces have no calibration drift, no quote-time-of-day
  noise, no microstructure asymmetries, no realistic smile dynamics, no hard-to-fit weeklies or
  single-name idiosyncrasies."*
- **Closing verdict, verbatim:** *"It does not, on its own, justify a production system."*
- Methodological choices are justified rather than hidden: *"Sixty epochs is therefore a deliberate
  choice rather than a generous one."*
- **Opening two sentences, verbatim:** *"A volatility surface marker is rarely a clean rectangle of
  quotes. Strikes go unobserved during illiquid hours, wings get crossed and then erased, broker
  stripes drop out across an entire maturity, and weeklies arrive at the desk with random missingness
  on top of base quote noise."*

**Evidence presentation:** the *experiment write-up* is the unit of proof. Each post is a complete
research note: motivation → model → code → baseline comparison → diagnostics → what failed → what it
does not license you to conclude.

**Rigor signals:** the strongest in the entire survey. Named baseline comparisons, admitted losses to
the baseline, arbitrage-violation counts, calibration coverage numbers, synthetic-data disclosure,
scope-limiting conclusions.

**Voice / length:** first person, desk-native vocabulary ("broker stripes," "weeklies," "the wing"),
technical but readable, self-critical without false modesty. 3,000–8,500 words per post.

**Technical implementation:** WordPress. MathJax for equations, syntax-highlighted Python blocks.
Featured images per post. Responsive.

**Contact/recruiting:** the "Systematic Strategies" nav item is the fund; the About page carries no
email. Weak on contactability — the one clear gap.

**Notable absences:** no CV, no email address, no live track record, no category/tag taxonomy for
navigating 15+ years of archive.

**Anti-patterns:** thin About page (single paragraph, no photo, no contact); reliance on stock
featured images.

---

### 8. Charles-Albert Lehalle — https://lehalle.net/ → https://www.cmap.polytechnique.fr/~charles-albert.lehalle/

**Exact self-description:** "Professor, CMAP, Ecole Polytechnique, Institut Polytechnique de Paris
(IPP)." Opening line: "Welcome to my web page(s). I started as a Professor at the Center for Applied
Maths at Ecole Polytechnique the 1st of Sept 2024." (Previously Global Head of Quantitative Research
& Development at ADIA, and before that CFM.)

**Site type:** Academic homepage with a projects layer and a blog. Custom vanity domain (lehalle.net)
301-redirecting to the institutional URL — a nice pattern: stable personal brand, institutional
hosting.

**Information architecture:** Nav = Teaching | Publications | Projects | Blog | CV. Home sections:
Welcome → "If you look for recent news" → Blog → Projects → Publications and Talks.

**Positioning line:** Purely institutional and current-state. Notably, the buy-side history (ADIA,
CFM) is *not* the headline — it sits in the CV. The academic title leads.

**Content types:** 80+ papers and book chapters, books, blog posts, teaching materials, named
projects, CV PDF, talks.

**Evidence presentation:** publications are presented **with images/figures pulled from the papers**,
each linking to an individual publication page. That is unusual and effective — a reader scrolling
the list sees the *shape of the results* (order book plots, impact curves) before reading a word.
Projects get their own cards.

**Rigor signals:** venue quality, long citation record, teaching materials that expose the derivations.

**Voice / length:** warm-professorial, first person.

**Technical implementation:** **"Made with Quarto ∙ based on Silvia Canelon's style"** — Quarto, the
most technically credible generator in the survey (it is the tool quants actually use for reproducible
reports: executable code + LaTeX + HTML/PDF from one source). Responsive, clean typography.

**Contact/recruiting:** full office address, room number, obfuscated institutional email.

**Notable absences:** relatively little on the ADIA/CFM years; no code repositories foregrounded.

**Anti-patterns:** none material.

---

### 9. Peter Cotton — https://home.microprediction.org/

**Exact self-description:** **The site states no role or employer on the homepage.** (Externally
verifiable as Chief Data Scientist at Intech; formerly JPMorgan, founder of Benchmark Solutions.
The site itself does not say so.)

**Site type:** Topic-indexed research archive. Effectively a personal "collected works" index.

**Information architecture — the most unusual in the survey.** The nav is not About/Blog/Contact; it
is **a taxonomy of research domains**: GitHub · Google Scholar · Software · Bio · Virtual Peter (GPT)
· Book Length · Numerical statistics (Probit, logit, …) · Time series · Portfolio construction &
covariance · Market making & trading · Contests, Rankings · Global optimization · Market mechanisms &
scoring rules · Economics · Conformal prediction · Fixed income & stochastic volatility ·
Epidemiology · Sports analytics · Mathematical analysis · Selected Essays · Software · Selected
Talks · Videos · Interviews · Patents.

**Positioning line:** There is none. The page opens on his *most recent result*: "A >100x performance
upgrade when n>1000 for factor additive random-utility discrete-choice models (including multinomial
factor probit), in this paper." He leads with a quantified technical result rather than an identity
statement.

**Content types:** SSRN/arXiv/journal papers, Python and JavaScript packages, an MIT Press book,
PhD thesis, Medium essays, talk slides, YouTube videos, interviews, **patents**.

**Evidence presentation:** *breadth-as-depth by category*. Each topic heading is followed by papers
and shipped software in that topic. The proof is that in a dozen distinct technical domains he has
both a paper and a package.

**Rigor signals:** open-source packages backing the papers; a live "probability exchange" that scores
predictions publicly (the strongest possible out-of-sample discipline — public, timestamped,
adversarial).

**Voice / length:** terse, result-forward.

**Contact/recruiting:** GitHub, Google Scholar, Medium, repos subdomain. No email.

**Notable absences:** no employer, no CV, no narrative, no design.

**Anti-patterns:** the topic list is enormous and undifferentiated — a hiring manager cannot tell
what he is *best* at. This is the survey's clearest illustration of the breadth-vs-depth failure
mode: 18 topic headings dilute rather than compound. Also, the missing employer statement means a
recruiter must go to LinkedIn to learn anything about his employability.

---

### 10. Sangmin Simon Oh — https://sangmino.github.io/

**Exact self-description:** "Assistant Professor of Finance, Columbia Business School." Bio names
prior stints at **AQR Capital Management** and **Forefront Capital Management**, plus the Wharton
M&T program and the Chicago Booth Joint Program in Financial Economics.
Research statement: "My research is broadly within economics and finance, focusing on asset pricing,
investments, and insurance. My work focuses on how market structures and societal shifts shape the
pricing and allocation of risk across financial markets, with a focus on investor behavior and often
leveraging ML/AI tools."

**Site type:** Academic homepage extended with public-goods infrastructure. The most *generous*
site in the survey.

**Information architecture:** Nav = Home | CV | Research | Teaching | Discussions | Notebook |
Public Goods | Resources | AI. Note four non-standard sections:
- **Discussions** — his conference discussant slides (a genuinely differentiated artifact type)
- **Notebook** — informal research notes
- **Public Goods** — resources built for the field, not for himself
- **AI** — a dedicated page on AI tooling
He also links two live web apps he built (`practice-dry-run.vercel.app`, `turtl.finance`), a Notion
page, a Substack, and three podcast shows.

**Positioning line:** research-question-first. The first sentence is about *what he studies*, not
about his title — the title sits underneath.

**Content types:** papers, CV, teaching, discussant slides, blog/notebook, Substack, podcasts,
deployed web apps, curated resource lists, a job-market-candidate list page (`/jmc`) built as a
service to the field.

**Evidence presentation:** conventional academic paper list, but the *differentiator* is the public
goods — the JMC list, the resource pages, the apps. He proves competence partly by **building things
other researchers use**.

**Rigor signals:** journal placements; discussions demonstrate he can critique others' identification
strategies, which is a distinct and hard-to-fake competence signal.

**Voice / length:** professional, service-oriented, minimal self-promotion.

**Technical implementation:** Jekyll on GitHub Pages. **No `<meta name="viewport">` detected — not
mobile-optimized.** No math rendering on the landing page.

**Contact/recruiting:** institutional email, Twitter, Google Scholar, LinkedIn.

**Notable absences:** no code repos foregrounded; no data downloads.

**Anti-patterns:** the nav is 9 items wide and several are idiosyncratic ("AI", "Public Goods") —
a visitor cannot tell which two matter most.

---

### 11. Alexander Chinco — https://www.alexchinco.com/ (Notebook: /notebook/)

**Exact self-description:** **The homepage states no employer or title.** The name and a CV link are
the only identity markers. (Externally he is a finance professor at Baruch/CUNY; the site does not
say so.)

**Site type:** Research blog + publication list hybrid. Site is literally titled "Research Notebook."

**Information architecture:** Nav = Publications | Working Papers | Curriculum Vitae | Notebook |
Courses. The **Notebook is a first-class nav item, not a footnote**.

**Positioning line:** none — the site opens straight into Publications. Identity is entirely
implicit.

**Content types:** peer-reviewed papers, working papers, CV PDF, long-form research notes, course
materials, online appendices / visualizations.

**Evidence presentation — the most instructive detail in the survey:** each publication entry is
title (linked to PDF) → journal + year + volume/issue → co-authors (linked to *their* sites) →
**and a short plain-language paragraph explaining what the paper found**. That summary paragraph is
what converts a publication list from a credential dump into something a reader can actually use.

**The Notebook** is the model for what Brad's research-log section should look like. Verified recent
entries:
- "Excessively Volatile? Or Inexplicably Precise?" (Aug 11, 2026)
- "Deriving the Gordon Model" (Jul 26, 2026)
- "Trailing PEs Imply Low Elasticities" (Jul 22, 2026)
- "Inelastic Markets ~ Flat SML" (Jul 21, 2026)
- "Gordon Prime" (Jun 23, 2026)

Posts run **1,000–3,000+ words**, are dense with LaTeX-rendered derivations and numerical examples,
and have **titles that state a finding or pose a sharp question** rather than naming a topic. Note
the cadence: five posts across two months, several building on each other — a visible *research
program* rather than scattered one-offs.

**Rigor signals:** derivations shown in full; numerical worked examples; posts that revise or extend
earlier posts.

**Voice / length:** first person, thinking-out-loud, unpolished-on-purpose, mathematically explicit.

**Technical implementation:** WordPress with the **eleven40 Pro** child theme on the **Genesis
Framework**. Responsive viewport present. System font stack.

**Contact/recruiting:** none on the homepage. A real gap.

**Notable absences:** no employer, no contact, no photo, no bio.

**Anti-patterns:** a visitor cannot tell who he is or how to reach him. For an established academic
with a Google-able name this is survivable; for a job seeker it would be fatal.

---

### 12. Dean Markwick — https://dm13450.github.io/ (About: /about/)

**Exact self-description:** "I am a quant researcher focused on execution at both the high (parent)
and low (order routing) level. I also dabble in market-making and alpha signals when there is a spare
5 minutes at work." **No current employer is named** (previously at BestX; PhD in Statistical Science
from UCL, thesis "Bayesian Nonparametric Hawkes Processes with Applications").

Site tagline: "Personal website for Dean Markwick. If you like stats, sports and rambling, you've
come to the right place."

**Site type:** Long-running technical research blog (100+ posts, 2014–2026) with an academic layer.

**Information architecture:** Nav = About Me | Blog | Research | Teaching | Physics. About page
sections: About Me → Talks → Articles → Outside the Day Job → Recent Post.

**Positioning line:** narrow and specific — *execution*, parent-order and order-routing level. He
names a sub-specialty rather than claiming "quantitative finance." Then he immediately shows range
("market-making and alpha signals") without over-claiming it ("dabble … spare 5 minutes").

**Content types:** blog posts, open-source packages (`HawkesProcesses.jl`, `dirichletprocess`,
`AlphaVantage.jl`, `CoinbasePro.jl`, `AlpacaMarkets.jl`), PhD thesis, published articles, YouTube
talks, a live dashboard (`cryptoliquiditymetrics.com`), teaching.

**Evidence presentation:** **one deep technical thread, executed publicly for a decade.** Hawkes
processes are his signature: the thesis, the Julia package, and a long series of posts applying them
to microstructure noise, FX, terror attacks, and football goals. A reader instantly knows what he
*owns*.

**Deep read of one post — "Big Ticks and Small Ticks in Equity Microstructure" (Aug 23, 2026):**
- **~2,200 words** — notably shorter than Kinlay's; a good target length for a regular cadence.
- **Python code inline** (Polars), with function definitions and processing examples.
- **Two charts** (normalized depth-of-book size; trading-cost curves) and LaTeX for the
  basis-point spread formula.
- **Data source named precisely**: LOBSTER (NASDAQ order-book reconstruction), five tech stocks
  (GOOG, AMZN, MSFT, AAPL, INTC), a single day: **June 21, 2012**. He also says *how he got it* — it
  came bundled with the book *Trades, Quotes and Prices*.
- **Caveats stated plainly**: it is a "whistle-stop tour" of basics, not comprehensive; the 2012 data
  predates the 2024 SEC Reg NMS tick-size amendments; **AAPL is called out as an exception to the
  pattern he describes**; and he flags that his day job is FX, not equities.
- **Opening two sentences, verbatim:** *"I bought Trades, Quotes and Prices a few years ago and it
  came with access to some free data to help you understand the concepts. That data was from LOBSTER
  and it has the limit order book (LOB) of five tech stocks for a single day in 2012."*
- **Closing, verbatim:** *"Finally, I managed to write all that without a single big tick energy
  joke."* Followed by a "Related Reading" section linking his own prior posts.
- **Mid-post CTA:** "Enjoy these types of posts? Then sign up for my newsletter."

**Rigor signals:** named data vendor and exact date range; explicit acknowledgment of regime change
(tick-size rules); named counterexamples in his own data; cross-links that let a reader trace the
research lineage.

**Voice / length:** conversational, humorous, unpretentious, but the math is never hand-waved.
~2,000–2,500 words, roughly monthly.

**Technical implementation:** `<meta name="generator" content="Jekyll v3.10.0" />` — Jekyll on GitHub
Pages, responsive viewport present. Clean, plain, fast.

**Contact/recruiting:** obfuscated email (`dean[dot]markwick[at]talk21[dot]com`), GitHub, LinkedIn,
Twitter, RSS, newsletter signup.

**Notable absences:** no current employer named; no CV PDF; no dark mode.

**Anti-patterns:** sports-analytics and "Physics" content mixed into the same feed as microstructure
research dilutes the professional signal somewhat — though the sheer volume of quant content
overwhelms it. Brad should note the trade-off rather than copy it.

---

### 13. Chad Gray — https://alphascientist.com/ (About: /pages/about.html)

**Exact self-description:** "I'm Chad, aka The Alpha Scientist. I've created this blog to explore the
intersection of my two professional passions: locating 'alpha' in market inefficiencies and applying
data science methods." Describes himself as a **"full-time quantitative trader"**; MS in EE/CS from
MIT; CFA (2009); prior career building analytics products in Silicon Valley. **No firm named.**

**Site type:** Practitioner research blog with a consulting page.

**Information architecture:** Nav = Atom | RSS | About | Consulting. Sidebar: Recent Posts, Tags,
Social, Latest Tweets, **Blogroll**.

**Positioning line:** the *career-transition* framing — Silicon Valley analytics → quant trading —
which is structurally the closest to Brad's story of anyone in the survey. He handles it by naming
both halves as "professional passions" and letting the blog content prove the second half.

**Content types:** long-form Python/Jupyter tutorial posts, tag taxonomy, email list, consulting
offer.

**Evidence presentation:** teaching-by-doing. Posts walk through feature engineering, model
validation, and evaluation on real market data with runnable code. He proves competence by showing
the *workflow*, which is exactly the thing a hiring manager wants to inspect.

**Rigor signals:** heavy emphasis on avoiding lookahead bias and on proper validation splits in his
tutorial series.

**Technical implementation:** **Pelican** (Python static site generator) — an apt choice for a
Python-centric blog. Responsive viewport present.

**Contact/recruiting:** LinkedIn (`chadgraycfa`), Twitter (`@data2alpha`), email subscription,
explicit **Consulting** page. Best commercial-intent affordances in the survey.

**Notable absences:** no employer, no CV, no papers, no live track record.

**Anti-patterns:** "full-time quantitative trader" with no firm and no verifiable results is a claim
a fund hiring manager will discount. A Twitter-feed widget in the sidebar dates the design.

---

### 14. "The Refutation" (pseudonymous) — https://therefutation.com/ (+ /about/, /graveyard/)

**Exact self-description:** no name given. Bio verbatim: "mathematics head teacher with bachelor's
degrees in mathematics and chemistry (BSc Mathematics, BSc Chemistry), who has spent over a decade
trading and investing his own money, including more than two years living and teaching overseas,
among them a stint in Beijing."

**Site type:** Thesis-driven research blog with a paid tier. **Include this one not as a
credibility model but as the single best example of falsification-as-positioning.**

**Headline verbatim:** "Honest Crypto Quant Research That Tries to Kill Every Edge"

**First paragraph verbatim:** *"Most edges are statistical mirages. Ours are statistical outliers. We
take your favourite trading strategy, try everything we can to kill it: fee-realistic,
look-ahead-free, intra-candle honest, tested across multiple market regimes, and we publish the
results."*

**Information architecture:** Nav = The method | **Graveyard** | **Survivors** | About | Premium |
Sign in. The IA *is* the epistemology: a page for things that died and a page for things that lived.

**Evidence presentation — the Graveyard.** Failed strategies get "autopsies" with headline numbers:
- Supertrend: 1,239 trades, "lost 92.9% while buy and hold gained 940%"
- 50/100 MA Ribbon: "Every configuration lost money" across 55 variants over five years
- MACD: "Every signal failed; the filter was driving" across 320 tuned variants
- RSI overbought/oversold: tested "across four assets and six timeframes. There's no edge"
- Golden Cross: "It doesn't survive"

Framing verbatim: *"plain-English autopsies of the strategies everyone repeats — and the failure
modes that fool everyone else."* And: *"The graveyard of everything that failed is the work it took
to find each survivor."*

**Rigor signals:** a named validation protocol — parameter sweep → proprietary backtest chamber →
**leave-one-regime-out** cross-validation, described verbatim as *"Hold out a whole market era…then
test it on the part it was never shown. Survive the unseen regime, or it was just memorising the
past."* Variant counts are disclosed (55, 320) — an implicit multiple-testing accounting.

**Negative-claim discipline:** an explicit list of what the site is *not*: *"This is not a signals
service, a Discord 'pump' room, a course promising financial freedom, or personal advice."* Plus a
disclaimer: "Educational and data-journalism content only. Not financial product advice."

**Technical implementation:** **Ghost** CMS, CSS custom properties for typography
(`--serif/--display/--mono/--sans`), responsive.

**Contact/recruiting:** paid newsletter ($29.90/mo, $299/yr), sign-in. Commercial, not
career-oriented.

**Anti-patterns for a fund audience:** anonymity, crypto-only scope, a paywall, "head teacher" as the
professional credential, and the marketing cadence of the copy. **The structure is worth stealing;
the register is not.**

---

### 15. Emanuel Derman — https://emanuelderman.com/ (About: /about/)

**Exact self-description:** "EMANUEL DERMAN is Professor of Practice Emeritus at Columbia University,
where he directed their program in financial engineering from 2003 – 2023."

**Site type:** Author/thinker site. The quant career (Goldman Sachs MD, Black-Derman-Toy,
Derman-Kani local volatility) is *history*, and the site is organized around books and writing.

**Information architecture:** Nav = About Me | blog | Books | photos | press | quotes | writing |
Finance | Publications | Paintings | contact. Eleven items, including paintings and photos.

**Positioning line:** titles → then **three books with their accolades**. Books are the proof unit.

**Content types:** books, blog, essays, technical publications, press, quotes, photographs,
paintings.

**Evidence presentation:** authored books and named models. Also relevant to Brad: Derman is the
co-author of the *Financial Modelers' Manifesto*, the canonical statement of model humility — a
useful citation if Brad writes a "how I think about models" page.

**Technical implementation:** WordPress 6.7, `wp-content/themes/founder`, Bootstrap, responsive.

**Contact/recruiting:** contact page, no email inline.

**Anti-patterns:** the nav mixes paintings and photos with Publications and Finance. Acceptable for a
70-something eminence; disastrous for a job seeker.

---

### 16. Campbell R. Harvey — https://people.duke.edu/~charvey/ (research list: /research.htm)

**Role:** Duke Fuqua finance professor; leads strategic research for Research Affiliates. **The
frameset homepage itself contains no role statement in its HTML** — the identity lives in frame files.

**Site type:** Archival academic homepage. Frameset-based (Netscape 2.0-era `<frameset>` layout,
40px header / 280px sidebar / content).

**Evidence presentation — worth studying for scale discipline.** The research page is organized:
Dissertation → **Peer-Reviewed Publications (P1–P179+, ~176 entries, reverse chronological
1988→2026)** → Books and Monographs (B1–B3) → **New Work (W174–W180)**. Every entry carries a stable
ID (P118, W180), journal/volume/pages, DOI, a Duke-hosted PDF, a Google Scholar citation link, SSRN
link, NBER designation where applicable, and **awards printed inline** (e.g. "Graham and Dodd Award,
2007"). Lead-article designations are marked.

Supplementary data is offered on specific papers ("Supplementary tables available", "Updated
not-seasonally adjusted consumption data available") but there is **no systematic
code/data-availability statement** — reproducibility is ad hoc.

**Why he matters for Brad specifically:** Harvey is the author of the multiple-testing critique of
factor research ("…and the Cross-Section of Expected Returns", "Backtesting", "A Backtesting Protocol
in the Era of Machine Learning"). If Brad's site claims backtest-overfitting hygiene, Harvey and
López de Prado are the two names that make the claim legible to a fund.

**Anti-patterns:** framesets in 2026; no responsive layout; visually indistinguishable from 1998.
**And it is one of the most-visited quant research pages on the internet.** Strongest possible
evidence that design is not the binding constraint for this audience.

---

### 17. Marcos M. López de Prado — https://www.quantresearch.org/ (content at /Intro.htm)

**Exact self-description:** **the intro frame states no current role or employer.** A separate "Vita"
page is linked.

**Site type:** Book-companion / method-evangelism site. Frameset-based (`LeftFrame.htm` + `Intro.htm`)
with a `<noframes>` fallback reading "This page uses frames, but your browser doesn't support them."

**First paragraph verbatim:** *"Machine learning (ML) is changing virtually every aspect of our
lives. Today ML algorithms accomplish tasks that until recently only expert humans could perform. As
it relates to finance, this is the most exciting time to adopt a disruptive technology that will
transform how everyone invests for generations. This website explains scientifically sound ML tools
that have worked for me over the course of three decades, helping me to manage large pools of funds
for some of the most demanding institutional investors."*

**Section headings:** WELCOME! → ON THE SOCIAL IMPACT OF QUANTS → CONTACT → DISCLAIMER.

**Evidence presentation:** the *methods themselves* are the proof — purged/embargoed cross-validation,
the deflated Sharpe ratio, probability of backtest overfitting, meta-labeling — plus the book
(*Advances in Financial Machine Learning*) and JPM editorials.

**Positioning note relevant to Brad:** he asserts industry experience in prose ("three decades …
large pools of funds for some of the most demanding institutional investors") **without naming a
single employer or a single number.** The credibility is carried entirely by the named, adopted
methods.

**Contact:** `mldp(at)QuantResearch(dot)org`, Twitter `@lopezdeprado`. A prominent DISCLAIMER section.

**Anti-patterns:** frames; no employer; marketing-toned opening paragraph. Again: does not matter,
because the methods are the brand.

---

### 18. Weichen Wang — https://weichwang.github.io/weichenw/

**Exact self-description:** "I joined HKU in 2021 as an Assistant Professor in the area of Innovation
and Information Management of HKU Business School. I am also one of the members of the Business
Analytics Group." Bio names a post-PhD stint as **quantitative researcher at Two Sigma Investments**
and a Princeton visiting lectureship.

**Site type:** Academic homepage. Nav = Home | Research | Teaching | Group.
Sections: Biography → Research Interests → Publications and Preprints → Working Papers → Teaching →
BLAST Lab.

**Evidence presentation:** standard citation format (authors, year, bracketed linked title, italic
journal, volume/pages). Statistics venues (Annals of Statistics-class) plus finance applications.

**Technical:** hand-rolled HTML, responsive viewport present, `font-family: 'Brush Script'` used
decoratively — the one genuinely bad typographic choice in the survey.

**Relevance:** an example of the **industry-stint-as-line-item** pattern — the Two Sigma role is one
clause in a biography whose center of gravity is academic.

---

### 19. Jialei Wang — https://jialeiw.github.io/

**Exact self-description:** "I received my PhD at Department of Computer Science, University of
Chicago, my advisors are Nathan Srebro and Mladen Kolar." **No current role or employer stated
anywhere.** Email still an expired university address (`jialei [@] cs.uchicago [DOT] edu`).

**Site type:** stale academic homepage. Nav = Home | Publication | Activities. Footer: "Page
generated 2019-10-21, by jemdoc."

**Why included:** it is the **failure case**. A Two Sigma quantitative researcher whose site has not
been touched since 2019, states no employer, and routes contact to a dead academic address. For a
person not looking for work, harmless. For anyone signaling availability, it actively subtracts —
it reads as abandoned. **Staleness is the most common and most costly defect in this genre.**

---

### 20. Kris Abdelmessih — https://blog.moontower.ai/ (author page: /author/kris/)

**Role:** the author page carries **no bio text**. (Externally: co-founder of moontower.ai; 12 years
as an options market maker at SIG and then Parallax, running relative-value commodity vol.)

**Site type:** Ghost-powered options/volatility blog attached to a product.

**Information architecture — the most useful thing here:** the nav is **conceptual, not
chronological**: Home | **How Markets Work** | **Options & Volatility** | **Risk & Edge** |
**Options Theory**. Posts are organized by *idea*, so a reader can enter at their level.

**Verified post titles:** "Futures premium cell", "Stock-bond correlation", "Collar shopping",
"The sound of inevitability", "Workflows", "Introducing Collar Workflows", "Introducing Defensive
Workflows", "Introducing Income Workflows", "Hedging is for gardeners", "Become an option
mixologist", "How I Teach Middle Schoolers To Build Stock Portfolios", "Investing orbits",
"Delta-hedged risk reversals", "AI Traders", "Hurst", "Stacking carry: an inflation hedge you get
paid to own".

**Relevance to Brad:** the closest content match to a volatility-trading focus, and proof that
**topic-clustered navigation beats a reverse-chronological feed** once you have more than ~15 posts.

**Anti-patterns:** no bio on the author page; sign-in walls; product-marketing posts interleaved with
research.

---

### 21. "Vertox" — https://www.vertoxquant.com/ (About: /about)

**Role:** pseudonymous ("Vertox", with a collaborator "malik"). **No name, role, or employer stated.**

**Positioning verbatim:** "Applied quantitative research on trading, risk, and systematic strategy
design"; writes about "quantitative trading the way it's actually practiced: Robust models and
portfolios, combining signals and strategies, understanding the assumptions behind your models."

**Site type:** Substack. Topics: portfolio construction, market making, risk management, research
methodology.

**Relevance:** demonstrates that *"understanding the assumptions behind your models"* is a
positioning line that resonates in this community. But it is anonymous and platform-hosted —
structurally unable to serve a job search.

---

## PART 2 — SITES CHECKED AND REJECTED

| Candidate | Reason rejected |
|---|---|
| `cims.nyu.edu/~ritter/` (Gordon Ritter, CIO Ritter Alpha, ex-GSA Capital NY, Risk Buy-Side Quant of the Year 2019) | **Dead.** Returns HTTP 403 on every variant tried (`https`, `http`, `www`, `math.nyu.edu`, `/index.html`). Indexed by Google but not currently servable. Not reported as a verified site. |
| Various LinkedIn profiles (Jialei Wang, Chengye Yang, Nan Meng, Krutarth Satoskar, Peizhe Shi, etc.) | LinkedIn-only, per instructions. |
| Nick Baltas (GS Managing Director, Head of R&D STS) | No personal website exists — only LinkedIn, Google Scholar, ResearchGate. |
| Giuseppe "Gappy" Paleologo (Global Head of Quant Research, Balyasny) | **No personal website.** Notable finding in itself: one of the most publicly visible quants in NYC multi-strat operates entirely through books, X/Twitter, and podcasts. |
| Andrew Ang (Head of BlackRock Systematic factor group) | No personal website found. |
| Igor Halperin (Fidelity, ex-JPM ED Quant Research) | No personal website found. |
| Ben Wellington (Two Sigma quantitative analyst, "I Quant NY") | Tumblr blog; civic-data content, no quant-finance research. Not analyzed in depth. |
| Zura Kakushadze (Quantigic) | Corporate site, not a personal homepage. |
| Euan Sinclair | No personal website; presence is books + QuantInsti faculty page. Relevant because Brad models on him — there is **no site to imitate**, which means Brad's site can occupy that space. |

---

## PART 3 — SYNTHESIS

### 3A. The 14 recurring characteristics of the strongest sites, ranked by likely impact on a quant hiring manager

**1. A named, falsifiable thesis about markets — not a description of the person.**
The strongest opening in the survey is Artur Sepp's: *"volatility regimes migrate across asset
classes, and models that feel robust fail at the worst moment. I build frameworks designed to survive
regime change."* That is a claim about the world that could be wrong, and everything else on the site
is evidence for it. Compare the weak openings: "I am a quantitative researcher at X" tells a reader
only who employs you. Brad has no fund name to lead with, so **a thesis is the only available
substitute — and it is the better asset anyway.**

**2. Published negative results, stated in numbers, with the conclusion refused.**
Kinlay's vol-surface post is the exemplar: the CNN loses to interpolation by 40%, arbitrage
violations persist in 5–11% of points, the uncertainty head is miscalibrated at 28–69% coverage
against 80% nominal — and the post ends *"It does not, on its own, justify a production system."*
The Refutation builds an entire site section (the Graveyard) out of this. Nothing else on a personal
site buys as much trust with this audience per word. A hiring manager reading a page of wins asks
"what did he hide"; a page that opens with a loss is answering that question before it is asked.

**3. Exact data provenance: vendor, instruments, date range, and how it was obtained.**
Markwick: "LOBSTER … five tech stocks (GOOG, AMZN, MSFT, AAPL, INTC) … a single day in 2012 … it came
with the book *Trades, Quotes and Prices*." Kinlay: "synthetic only — 1,600 SSVI surfaces, ~18bp
quote noise," said up front. Vague data is the fastest way to be dismissed; a named vendor and a date
range is the cheapest way not to be.

**4. Depth in one named sub-specialty, visible at a glance.**
Markwick = Hawkes processes and execution (thesis → Julia package → decade of posts). Sepp =
log-normal stochastic volatility (papers → the model bears his name → open-source implementation).
Chinco = a multi-post series compounding on the Gordon model. Contrast Peter Cotton's 18 topic
headings — enormously accomplished, but a reader cannot say what he is *best* at. **The unit of
credibility is a thread, not a portfolio.** For Brad this is decisive: one volatility system,
documented obsessively, beats a grid of unrelated ML projects.

**5. A defensible baseline you compare against, and sometimes lose to.**
Kinlay benchmarks his CNN against plain interpolation and reports losing. This is the single clearest
tell that separates someone who has done real research from someone who has run a backtest. Any
result presented without a named baseline is unreadable to a quant.

**6. Explicit accounting of how many things you tried.**
The Refutation reports 55 MA-ribbon configurations and 320 tuned MACD variants. This is
multiple-testing hygiene expressed in plain English. Given Brad's López de Prado framing, stating
trial counts and applying a deflated Sharpe is the natural way to make the hygiene claim *operational*
rather than decorative — Campbell Harvey and López de Prado are the two names that make it legible.

**7. Named artifacts with citations or adoption counts.**
Sepp: "ROSAA … published in the Journal of Portfolio Management (2026)"; "downloaded 300,000+ times";
"~1,200 citations." Kelly ships factor datasets. Cotton ships packages in a dozen domains. **A thing
with a name that other people use** is worth more than any adjective. Brad's system needs a name, a
repo, and a number attached to it.

**8. Scope-limiting sentences that pre-empt the obvious objection.**
Kinlay: *"The synthetic surfaces have no calibration drift, no quote-time-of-day noise, no
microstructure asymmetries…"* Markwick flags that his 2012 data predates the 2024 Reg NMS tick-size
amendments, and that AAPL contradicts his own pattern. Naming your own strongest counterargument
first is the highest-leverage rhetorical move available on a quant site — it converts an interview
ambush into a demonstration of judgment.

**9. Runnable code that reproduces the figures.**
Kinlay inlines ~700 lines of PyTorch. Markwick inlines Polars. Markwick, Cotton, and Sepp ship
installable packages. Code is the only proof that survives skepticism without a trusted employer
name behind it.

**10. Real math, rendered properly.**
MathJax on Sepp and Kinlay; LaTeX derivations throughout Chinco's Notebook. Equations are not
decoration here — they establish that the author can specify a model precisely. A quant site with no
equations reads as a data-science site.

**11. Publication/artifact entries that include a one-line plain-language finding.**
Chinco's format — title, venue, co-authors, **then a short paragraph on what the paper found** — is
the best evidence-presentation mechanic in the survey. Sepp's copy-pasteable BibTeX is the same
instinct applied to reuse. A bare list makes the reader work; a list with findings makes the reader
keep reading.

**12. Topic-clustered navigation once the archive exceeds ~15 items.**
Moontower's *How Markets Work / Options & Volatility / Risk & Edge / Options Theory* lets a reader
enter at their level. Cui groups publications by research theme rather than by year. Kinlay's flat
reverse-chronological feed — with 15 years of posts and no tag taxonomy — is his site's biggest
navigational weakness.

**13. A visible research cadence.**
Chinco: five substantial posts across two months, several building on each other. Markwick: 100+
posts over 12 years. Sepp: dated papers spanning 2018–2026. Dates on posts are a liveness signal;
Jialei Wang's 2019 timestamp is the counterexample that shows what staleness costs.

**14. Frictionless contact and an unambiguous current status.**
Sepp puts a plain-text email on the front page next to LinkedIn/SSRN/Scholar/GitHub. Kelly and
Pedersen give full addresses. Against this: **Chinco has no contact and no employer, Kinlay has no
email, Cotton has no employer, Markwick names no employer, Kris Abdelmessih's author page has no
bio.** These are all people who do not need to be found. Brad is the opposite case, and should treat
contactability as a first-class requirement rather than a footer afterthought.

**Ranked "not actually important" list, on the evidence:** site technology, visual design, dark mode,
and mobile responsiveness. See 3C.

---

### 3B. Academic homepage convention vs. engineer portfolio convention — which reads as more credible to a fund

**The academic convention** (Cui, Kelly, Pedersen, Wang, Oh, Chinco, Harvey, Lehalle):
- IA: About → Research/Publications → Teaching → CV → Contact
- Positioning: institutional title + PhD lineage (advisor, department)
- Evidence: a dated, citable list; venue names do the work
- Voice: third person or restrained first person; no adjectives
- Contact: institutional email, sometimes a postal address and phone
- Design: deliberately plain, often ancient (Wix, Google Sites, jemdoc, framesets)

**The engineer portfolio convention** (largely *absent* from this lane, but visible in Chen's site):
- IA: Hero statement → Projects grid → Skills → Experience → Contact
- Positioning: a value proposition aimed at an employer
- Evidence: project cards, tech-stack badges, screenshots, GitHub stars
- Voice: marketing register, second person
- Design: heavily invested, responsive, animated

**Verdict: the academic convention wins decisively with this audience, and the gap is not close.**
Three reasons, all supported by what I actually found:

1. **The unit of evidence differs.** Academic sites present *dated, attributable, checkable claims*.
   Portfolio sites present *assertions with screenshots*. A quant hiring manager's job is checking
   numbers; a format that invites checking reads as confident, and a format that resists it reads as
   evasive.
2. **The register differs.** Every strong site in this lane understates. Sepp, whose accomplishments
   would justify considerable noise, writes "20+ years" and "~1,200 citations" — bounded, verifiable
   quantities. Nothing in this lane says "passionate," "cutting-edge," or "innovative." A
   marketing register in a quant context is read as compensation for absent substance.
3. **Ostentatious design actively costs credibility here.** Harvey's frameset and Cui's
   non-responsive jemdoc page belong to people at the top of the field. The one visually polished
   site in the survey (Chen's Squarespace) is also the one with the least technical substance and the
   most career-ambiguous positioning. **Design effort visibly exceeding research effort is itself a
   negative signal.**

**But the pure academic convention has a specific failure mode Brad must avoid.** It works because
peer review has already certified the claims. Brad has no journal placements. If he copies Cui's
form — a nav bar, a photo, and a list — he gets an empty page. So:

**The correct target is the Sepp/Kinlay/Markwick hybrid: academic *rigor conventions* wrapped around
practitioner *artifacts*.** Concretely:
- Academic from the academic side: dated entries, precise data provenance, equations, citations to
  the literature (Sinclair, López de Prado, Harvey, Gatheral), an understated voice, a CV,
  contactability, and a disclosure statement.
- Practitioner from the practitioner side: the artifacts are **research notes, post-mortems, code,
  and a live out-of-sample track record** rather than journal articles — with each note structured
  the way a paper is (motivation → method → data → baseline → result → limitations → what this does
  not license).

This is also exactly where Brad's existing material fits: his documentation, logging, and written
post-mortems *are* the artifact class this genre rewards, and almost nobody in the survey has a live
out-of-sample record — which is a real differentiator, provided it is presented with the caveats
these sites model.

---

### 3C. How these people signal depth rather than breadth

Six observed mechanisms, in rough order of usefulness to Brad:

1. **One technique carried across many applications.** Markwick's Hawkes processes appear in his
   thesis, his Julia package, and posts on microstructure noise, FX, terror attacks, and football.
   The *method* is the identity; the applications demonstrate range without diluting it.
2. **A named model or framework you own.** Sepp's log-normal beta stochastic volatility model and
   ROSAA. López de Prado's purged CV / deflated Sharpe / meta-labeling. Once a method has your name
   attached, breadth elsewhere becomes free.
3. **Deliberate narrowing in the positioning line.** Markwick: *"focused on execution at both the
   high (parent) and low (order routing) level"* — a sub-sub-specialty. Lacotte: *"predictive signals
   (alphas) for global financial markets."* Neither says "quantitative finance."
4. **Explicitly demoting side interests.** Markwick's "I also dabble in market-making and alpha
   signals when there is a spare 5 minutes at work" claims range while marking it as secondary —
   honest and structurally protective of the core claim.
5. **Grouping by theme, never by year.** Cui's publications are grouped under four research themes;
   a reader sees four coherent programs instead of eleven scattered papers.
6. **Compounding post sequences.** Chinco's Gordon-model series, where each post builds on the last,
   makes a research *program* visible. Isolated posts read as hobbies; sequences read as work.

**The counterexample makes the point:** Peter Cotton's site indexes eighteen research domains,
each with papers and shipped software, and is genuinely more accomplished than most sites here — but
a hiring manager scanning it cannot state what he does. Breadth presented flat destroys the signal
that depth creates.

---

### 3D. Technical implementation summary (all inspected in HTML source)

| Site | Generator / platform | Math | Responsive | Notes |
|---|---|---|---|---|
| qwcui.github.io | **jemdoc** (2007-era) | none | **No viewport tag** | Table layout, Georgia serif |
| jonathanlctt.github.io | Bootstrap 3 + jQuery 1.11 | none | **`non-responsive.css`** | Deliberately desktop-only |
| wzchen.com | **Squarespace** + Typekit | none | Yes | Most designed, least technical |
| bryankellyacademic.org | **Wix** (React/Thunderbolt) | none | Yes | Chaired professor on Wix |
| lhpedersen.com | **Google Sites** | none | Yes | Lato |
| artursepp.com | **WordPress.com**, theme `personal`, Jetpack | **MathJax** | Yes | PT Sans |
| jonathankinlay.com | **WordPress** | **MathJax** | Yes | Syntax-highlighted Python |
| lehalle (polytechnique) | **Quarto** | yes | Yes | Best-in-class technically |
| sangmino.github.io | **Jekyll** / GitHub Pages | none on home | **No viewport tag** | 9-item nav |
| alexchinco.com | **WordPress** + Genesis / eleven40 Pro | **LaTeX** | Yes | System font stack |
| dm13450.github.io | **Jekyll v3.10.0** / GitHub Pages | yes | Yes | Clean, fast |
| alphascientist.com | **Pelican** (Python SSG) | yes | Yes | Fits the Python audience |
| therefutation.com | **Ghost** | n/a | Yes | CSS custom properties |
| emanuelderman.com | **WordPress 6.7**, theme `founder` | n/a | Yes | Bootstrap |
| people.duke.edu/~charvey | **HTML framesets** | none | **No** | Netscape-2.0-era |
| quantresearch.org | **HTML framesets** | none | **No** | `<noframes>` fallback |
| weichwang.github.io | hand-rolled HTML | none | Yes | `font-family: 'Brush Script'` |
| blog.moontower.ai | **Ghost** | n/a | Yes | Topic-clustered nav |

**Not one site in the survey implements dark mode.** Not one uses a JS framework for the site itself.
The two most technically sophisticated builds — Lehalle's Quarto and Gray's Pelican — belong to
people whose *work* is in those ecosystems, which makes the tool choice itself a small competence
signal. That is the only place where technology carries any information at all.

---

### 3E. Anti-patterns catalogue (things observed that would cost Brad)

1. **Staleness.** Jialei Wang's site: last generated 2019, no employer, dead university email. Reads
   as abandoned.
2. **No stated current role.** Chinco, Cotton, Markwick, Abdelmessih, Vertox, López de Prado's intro
   page. Fine for the already-famous; disqualifying for a candidate.
3. **No contact method.** Chinco has none; Kinlay has none on his About page.
4. **Unearned first-person claims.** "Full-time quantitative trader" with no firm and no verifiable
   record (Gray) is the exact claim a fund will probe hardest.
5. **Non-work content in the primary nav.** Chen's escape rooms; Derman's paintings; Markwick's
   sports posts in the main feed.
6. **Anonymity + paywall.** The Refutation — structurally incompatible with a job search.
7. **Design investment visibly exceeding research investment.** Chen's Squarespace site.
8. **Flat reverse-chronological archives with no taxonomy.** Kinlay, 15 years deep, no tags.
9. **Undifferentiated breadth.** Cotton's 18 topic headings.
10. **Wide idiosyncratic navs.** Oh (9 items), Derman (11 items) — the reader cannot tell what matters.
11. **Marketing-register prose.** Even López de Prado's "most exciting time to adopt a disruptive
    technology" opening reads as promotional; he survives it on the strength of the methods.
12. **Publication lists with no findings attached** — a wall of titles the reader must decode.

---

### 3F. Direct implications for bradlasater.github.io

The specific moves this survey supports, in priority order:

1. **Replace any "I am an ML engineer who..." opening with a market thesis** in the Sepp mold — one
   or two sentences about how volatility behaves and what kind of system survives it, followed by the
   claim that his system is built to that spec.
2. **Give the volatility system a proper name**, a repo, and a version — turn it into a citable
   artifact rather than a project description.
3. **Publish at least one post-mortem where the result was negative**, with numbers, a named
   baseline, and an explicit "this does not license the conclusion that…" paragraph. This is the
   highest-trust-per-word content available to him, and his existing written post-mortems are already
   the raw material.
4. **State data provenance everywhere**: vendor, instruments, exact date ranges, and how the data was
   obtained and cleaned.
5. **Report trial counts and apply a deflated Sharpe / PBO** to any headline number, citing Harvey
   and López de Prado. Make the hygiene operational, not decorative.
6. **Keep the live out-of-sample track record but wrap it in this genre's caveat conventions** —
   sample length, regime coverage, capacity, costs, what would falsify it. Almost nobody in the
   survey has a live record; presented with these caveats it is a genuine differentiator, and
   presented without them it looks like every other backtest.
7. **Structure the site the academic way** — dated research notes, a CV, precise citations,
   understated voice, plain-text email above the fold — while keeping the *artifacts* practitioner:
   code, notes, post-mortems, track record.
8. **Group notes by theme once there are more than ~10** (Moontower/Cui pattern), not by date alone.
9. **Do not over-invest in visual design, dark mode, or animation.** On the evidence of Harvey's
   framesets and Kelly's Wix, the marginal return is near zero and the downside — looking like a
   marketer — is real. Spend the effort on math rendering (MathJax/KaTeX), readable code blocks, and
   figure quality instead.
10. **Do not let non-quant content into the primary nav.**

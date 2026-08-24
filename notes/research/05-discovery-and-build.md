# Research 05 — Discovery Sweep + Technical Teardown of Quant Personal Sites

**Scope:** breadth discovery through non-search channels (GitHub API, curated lists, Quantocracy,
aggregators) plus a raw-HTML technical teardown of the strongest sites.
**Method:** every URL was fetched. Discovery used the authenticated GitHub API (`gh api search/users`,
`search/repositories`, then per-user profile fetch to surface the `blog` field), the Quantocracy
blogroll, `awesome-quant` and `awesome-systematic-trading` raw READMEs, and targeted search.
Teardown used `curl` against the **raw HTML + response headers** (not markdown-converted text), so
every stack claim below is grounded in an observed tag, asset path, or HTTP header.
**Date of capture:** 2026-08-23/24.

---

## PART 0 — Accuracy notes and negative findings

Three domains that appear in quant reading lists and citations are **dead or hijacked**. These are
reported as cautionary findings, not as sites to emulate:

| Domain | Was | Now (observed) |
|---|---|---|
| `kthohr.com` | Keith O'Hara, NYU PhD, econometrics; author of the `optim`/`stats` C++ libs | 302s to `idcolympus88.com`, an Indonesian online-gambling site. 700KB, Product JSON-LD. |
| `frouah.com` | Fabrice Douglas Rouah — the standard free reference for Heston model derivations | Serves "Online Casino Real Money: Top Sites Reviewed & Ranked" with FAQPage JSON-LD. |
| `luiscota.com` | Luis Cota, Brooklyn NY, quantitative/systematic trading (GitHub bio still lists it) | Connection fails outright (curl exit, 0 bytes). |
| `symmys.com` | Attilio Meucci's personal/ARPM site | 301s to `arpm.co` — a company site, no longer personal. |

**Implication for Brad:** a custom domain is an asset that *decays*. A lapsed registration on a site
carrying your name does not go quiet — it gets bought precisely because it has inbound links, and it
starts serving casino spam under your name. Auto-renew plus registrar-lock is a career-hygiene item,
not a domain-admin chore. It also argues for keeping the `bradlasater.github.io` GitHub Pages URL
alive as a permanent fallback that cannot be seized.

Also note: `cims.nyu.edu/~ritter/` (Gordon Ritter, Ritter Alpha LP; teaches at Baruch/NYU/Columbia/
UChicago) returns **403 to both curl and WebFetch**. Its existence is confirmed by search results and
by `cims.nyu.edu/~ritter/GordonRitterCV.pdf` appearing in the index, but since I could not load it,
it is excluded from the verified list and from the teardown.

---

## PART 1 — Discovery sweep: verified personal sites

All 19 below were fetched successfully (HTTP 200) and inspected.

### Tier A — closest models for what Brad is building

**1. `https://gregorygundersen.com/blog/` — Gregory Gundersen**
*Quantitative researcher, Tudor Investment Corporation, New York.* Meta description reads literally
"Gregory Gundersen is a quantitative researcher in New York."
This is the single best template in the sample. Nine years of continuous technical writing on
statistics, ML, and quant finance, including "An Intuitive Explanation of Black–Scholes." Every post
is laid out like a journal article: numbered figures with bold `Figure N.` captions bounded by
hairline rules, a real author-year bibliography, booktabs-style tables, and pre-rendered KaTeX. It
looks like something a researcher wrote for other researchers, and there is not one decorative
element anywhere. The archive is grouped by year, which makes a decade of consistency legible at a
glance — exactly the signal Brad wants his research log to send.

**2. `https://artursepp.com/` — Artur Sepp**
*Head of Investment Services Quant Group, LGT (Zurich); Risk Magazine Quant of the Year 2024; PhD
Mathematical Statistics, Tartu.* The closest analogue to Brad's stated ambition: a practitioner who
publishes volatility research and maintains open-source Python libraries (`qis`, `stochvolmodels`,
`optimalportfolios`) alongside the writing. The site cross-links SSRN author page, Google Scholar,
GitHub, LinkedIn, and X from the header — meaning any one of his identities leads a recruiter to all
the others. Technically it is unremarkable WordPress; the credibility is entirely carried by the
research artifacts and the citation trail.

**3. `https://jgatheral.github.io/` — Jim Gatheral**
*Presidential Professor of Mathematics, Baruch College; formerly head of Equity Quantitative
Analytics, Merrill Lynch; author of "The Volatility Surface."* Directly instructive for Brad because
it is **Jekyll on a bare `*.github.io` domain** — the most senior figure in the sample uses the exact
free stack Brad is on, with no custom domain at all. The homepage is 4KB with zero external scripts.
The `/publications/` page is nothing but a list of SSRN and arXiv links. It demonstrates that in this
field, the substance-to-chrome ratio *is* the design.

**4. `https://www.moontowermeta.com/` — Kris Abdelmessih**
*Former options market maker (Susquehanna-lineage floor/vol trading), writes "Party at the
Moontower."* The most respected practitioner-voice vol blog. Heavy use of footnotes for the "here's
the caveat a real trader would raise" asides, which is exactly the register Brad's post-mortems
should hit. Technically the weakest of the Tier A group (420KB, 24 scripts, 24 stylesheets on
WordPress) — proof that in vol-land, audience follows insight and forgives page weight.

### Tier B — NYC practitioners, directly comparable career stage

**5. `https://zachjs.com/` — Zachary J. Snow**
*Software engineer in systematic trading, New York City; CMU SCS 2019.* A 1,970-byte homepage. Name,
one-sentence positioning ("I am Zach, a software engineer working in systematic trading in New York
City"), a `/resume.pdf` link, GitHub, LinkedIn. Notable as the minimum viable credible site, and as
the one deployment in the sample that puts Cloudflare in front of GitHub Pages.

**6. `https://sunnybala.com/` — Sunny Balasubramanian**
*Quantitative researcher, crypto & equities; formerly Citadel, AQR; Columbia SEAS '16.* The meta
description is a full paragraph that names the prior employers outright — deliberate recruiter-SEO,
and the single most copyable move on the site. Jekyll on GitHub Pages with a custom domain, JSON-LD
`WebSite` schema, OG preview image. Projects-first rather than writing-first.

**7. `https://florianwechsung.github.io/` — Florian Wechsung**
*Quantitative Researcher, Citadel GQS, New York; former NYU Courant postdoc.* Hugo on a bare
`*.github.io`. Retains the academic structure — publications list with Google Scholar link, MathJax,
syntax highlighting — after moving from academia to a top-tier fund. A useful model for how a
research identity survives the transition to industry.

**8. `https://cswaney.github.io/` — Colin Swaney**
*Quantitative researcher and developer, greater New York.* Jekyll on GitHub Pages, KaTeX + MathJax,
Rouge highlighting. Content is solid market-microstructure work; the presentation is undermined by
loading three unrelated display typefaces (Fjalla One, Lora, **Indie Flower** — a handwriting font).
Included specifically as a counter-example: one whimsical font choice makes serious content read as
hobbyist.

**9. `https://algoquant.github.io/` — Jerzy Pawlowski**
*Adjunct professor at NYU Tandon; previously portfolio manager and quant analyst.* Exactly the
practitioner-adjunct profile the brief asked for. Jekyll on GitHub Pages using the off-the-shelf
`beautiful-jekyll` / `architect-theme`. Has `sitemap.xml` and `feed.xml`. **Its homepage renders no
`<title>` tag at all** and the theme's Google Font is Architects Daughter (another handwriting face)
— a demonstration that adopting a stock theme unmodified leaves visible defects.

**10. `https://quantguild.com/` — Roman Paolucci**
*New York, NY; runs Quant Guild (quant education); Columbia-affiliated.* The only site in the sample
using **Plotly for genuinely interactive charts** (8 references), plus MathJax. Cloudflare-hosted.
Shows what interactive figures cost: 56KB HTML, 10 scripts, 13 stylesheets for a landing page.

**11. `https://joshuapjacob.com/` — Joshua P. Jacob**
*Research Engineer, New York.* Built on **SvelteKit** — the only JS-framework personal site found in
the quant cohort — yet still only 6.2KB. Included to show a framework build *can* stay light, though
it buys nothing a static generator wouldn't.

### Tier C — canonical practitioner references

**12. `http://www.jaeckel.org/` — Peter Jäckel**
*Author of "Monte Carlo Methods in Finance" and "Let's Be Rational" (the implied-vol inversion
algorithm used across the industry).* Hand-written static HTML with an inline `<style>` block that
still contains IE6 "holly hack" workarounds. No SSG, no external CSS or JS files, no analytics, no
RSS. The entire site is a flat list of ~40 PDFs
(`StochasticVolatilityModels-PastPresentAndFuture.pdf`, `QuantoSkewWithStochasticVolatility.pdf`…).
The source carries `<!-- Time-stamp: "2026-08-18 19:21:25 pj" -->` — updated five days before
capture. The most important calibration point in this whole report: **zero design, total
credibility**, because the artifacts are load-bearing.

**13. `https://www.quantresearch.org/` — Marcos López de Prado**
*One of Brad's two stated influences.* The homepage is a **357-byte HTML `<frameset>`** served from
Microsoft-IIS/10.0 + ASP.NET — a literal 1990s frames layout, on the personal site of the person who
wrote the book on backtest overfitting. Reinforces the same lesson as Jäckel: the audience is buying
the research, not the CSS.

**14. `https://qoppac.blogspot.com/` — Robert Carver**
*Ex-AHL (ran their multi-billion fixed income book); author of "Systematic Trading," "Advanced
Futures Trading Strategies"; visiting lecturer, Queen Mary University of London.* On **Blogger**, at
a `blogspot.com` subdomain, 208KB with 32 images. One of the most-read systematic trading blogs in
the world. Directly relevant to Brad: Carver's reputation rests on publicly trading his own money
with a documented, open-source Python system since April 2014 — the same "show the live track record
and the machinery" play Brad is running.

**15. `https://jonathankinlay.com/` — Jonathan Kinlay**
*Quantitative researcher and trader (Systematic Strategies LLC).* WordPress 7.1, and the heaviest
page in the sample at **580KB with 43 images**. Both KaTeX and MathJax are loaded. Uses Plausible
rather than GA. Notable for linking arXiv preprints and his own GitHub pipelines inline with blog
posts — research artifacts embedded in the writing.

**16. `https://alexchinco.com/` — Alex Chinco**
*Finance academic (formerly Baruch/Zicklin, NYC).* Titled simply **"Research Notebook"** — a framing
Brad should consider, since it sets the expectation of work-in-progress rather than polished
marketing. WordPress, Lora + Oswald, footnotes, and a bare `cv_alexander_chinco.pdf` at the domain
root.

**17. `https://emanuelderman.com/` — Emanuel Derman**
*Professor Emeritus of Financial Engineering, Columbia; formerly head of quantitative strategies,
Goldman Sachs; co-author of the Derman-Kani local volatility model.* WordPress 6.7, 67KB. Writer-
first presentation (books, essays, columns) rather than a paper repository.

**18. `https://www.hardikp.com/` — Hardik Patel**
*ML/quant engineer; listed in `awesome-systematic-trading`'s blogs section.* Jekyll on GitHub Pages
with a custom domain. Has the most complete structured data in the sample: JSON-LD with a nested
`Person` author object plus `sameAs` links. PT Serif + PT Sans. Atom feed.

**19. `https://wilsonfreitas.net/` — Wilson Freitas**
*Quant, São Paulo; **maintainer of `awesome-quant`** (the field's most-used curated list).* The only
**Quarto** site found in the quant cohort (`generator: quarto-1.2.335`), deployed on **Netlify**.
Ships reading-time estimates, code copy-buttons, TOC, footnotes, and MathJax out of the box. This is
the existence proof that Quarto is a legitimate choice for a quant personal site.

### Non-quant build reference (included for stack comparison only)

**20. `https://eugeneyan.com/` — Eugene Yan.** Applied scientist, not a quant. Included because it is
the most-copied "research blog" build in ML: GitHub Pages behind Cloudflare with a custom domain,
hand-maintained `main.min.css`, `darkmode.js` toggle, `monokai.css` for code, `anchor.min.js` for
heading permalinks, and **Algolia search**. Merriweather (serif body) + Raleway (sans headings).

### Channel notes

- **GitHub API was by far the highest-yield channel.** Querying `search/users` with `in:bio`
  qualifiers (`quantitative … location:"New York"`, `volatility trading`, `systematic trading`,
  `market making`, `derivatives pricing`) and then fetching each profile's `blog` field surfaced
  ~20 NYC-area quant practitioners with live personal sites in minutes. This is reproducible and
  worth re-running periodically — it is also, notably, how a recruiter *could* find Brad, which
  argues for making his GitHub profile bio and website field carry the same positioning as the site.
- **`awesome-quant` has no practitioner-blog section** (verified against the raw README: sections run
  Numerical Libraries → … → Related Lists). Its "Commercial & Proprietary Services" section has been
  heavily spammed with low-quality API startups. `awesome-systematic-trading` *does* carry a real
  blogs list (Robot Wealth / Kris Longmore, Blackarbs, Hardik Patel, Quantsportal / Jacques Joubert,
  Tom Starke, Max Dama).
- **Quantocracy remains the best live aggregator**, but its feed has drifted heavily toward Substack
  newsletters (Beyond Passive, Delphic Alpha, Concretum, Paper to Profit, VertoxQuant) and away from
  self-hosted personal blogs.
- **Substack-with-custom-domain** (`vertoxquant.com`) is now a common quant-writer pattern. It is the
  worst technical profile measured: **121 `<script src>` tags** and 18 stylesheets on the index.

---

## PART 2 — Technical teardown

### Master table

| Site | Generator (observed) | Hosting (from headers) | Custom domain | Raw HTML | Scripts | Math | Charts | Dark mode | JSON-LD | Feed |
|---|---|---|---|---|---|---|---|---|---|---|
| gregorygundersen.com | none (hand-rolled; Jekyll-style permalinks) | Apache, self-hosted | yes | 127KB index / 422KB post | 3 | **KaTeX pre-rendered** + MathJax fallback | static PNG | no | no | `/feed.xml` |
| jgatheral.github.io | `Jekyll v3.10.0` | `server: GitHub.com` | **no** | 4.1KB | **0** | none | none | no | `WebSite` | yes |
| artursepp.com | WordPress | Automattic (`a8c-cdn`) | yes | 104KB | 8 | MathJax | static | no | no | yes |
| moontowermeta.com | WordPress + AMP for WP | Automattic | yes | 421KB | 24 | none | static | `data-theme` | `CollectionPage` | yes |
| jonathankinlay.com | `WordPress 7.1` | nginx/1.25.5 | yes | **580KB** | 11 | KaTeX + MathJax | 43 images | no | `CollectionPage` | yes |
| alexchinco.com | WordPress | Apache | yes | 39KB | 10 | none on index | static | no | no | yes |
| emanuelderman.com | `WordPress 6.7` | hcdn/PHP 8.1 | yes | 67KB | 10 | none | static | no | no | yes |
| sunnybala.com | `Jekyll v3.10.0` | `server: GitHub.com` | yes | 11KB | 3 | none | static | no | `WebSite` | no |
| hardikp.com | `Jekyll v3.10.0` | `server: GitHub.com` | yes | 8KB | 2 | none on index | none | no | `WebSite`+`Person` | Atom |
| cswaney.github.io | Jekyll (Rouge) | `server: GitHub.com` | **no** | 15.5KB | 6 | KaTeX + MathJax | none | no | no | no |
| algoquant.github.io | Jekyll (beautiful-jekyll) | `server: GitHub.com` | **no** | 4.6KB | 1 | none | none | no | no | yes + sitemap |
| florianwechsung.github.io | `Hugo 0.100.2` | `server: GitHub.com` | **no** | 7.8KB | 5 | MathJax | none | no | no | `index.xml` |
| zachjs.com | undetermined | GitHub Pages **behind Cloudflare** | yes | **2.0KB** | 1 | none | none | no | no | no |
| eugeneyan.com | undetermined (custom) | GitHub Pages behind Cloudflare | yes | 62KB | 11 | none | static | **toggle** | no | yes |
| wilsonfreitas.net | **`quarto-1.2.335`** | **Netlify** | yes | 41KB | 15 | MathJax | static | Quarto default | no | yes |
| joshuapjacob.com | **SvelteKit** | nginx/1.27.1 | yes | 6.2KB | 1 | none | none | no | no | no |
| quantguild.com | undetermined | Cloudflare | yes | 57KB | 10 | MathJax | **Plotly** | no | no | no |
| jaeckel.org | **none** (hand-written) | Apache/2.4.68 | yes | 70KB | 0 ext | none | none | no | no | no |
| quantresearch.org | **none** (`<frameset>`) | Microsoft-IIS/10.0 | yes | **357 B** | 0 | none | none | no | no | no |
| qoppac.blogspot.com | Blogger | GSE | **no** | 209KB | 2 | none | 32 images | no | no | RSS+Atom |
| vertoxquant.com | Substack | `x-served-by: Substack` | yes | 87KB | **121** | none | none | no | no | yes |

### Deep dive: Gundersen's build (the one to copy)

**Math is pre-rendered at build time.** The Black–Scholes post's raw HTML contains 186 instances each
of `<span class="katex">`, `katex-mathml`, `katex-html`, and
`<annotation encoding="application/x-tex">`. The only `<script src>` on the entire page is Google
Analytics. There is **no math library executing in the browser** — KaTeX ran server-side and only its
stylesheet ships. This is why a 422KB page still feels instant: the bytes are inert pre-computed
markup, not a layout engine. (Minor defect: two KaTeX CSS versions, 0.11.1 and 0.13.3, are both
pulled from jsDelivr.)

**The entire stylesheet is 6,040 bytes.** Verbatim key values:

```css
html   { font-family: -apple-system, Helvetica, arial, sans-serif;
         color: rgba(0, 0, 0, 0.8); line-height: 1.5em; }
.wrap  { max-width: 700px; margin: 0 auto; }
.article { font-size: 15px; line-height: 1.6em; color: rgba(0, 0, 0, 0.8); }
a      { color: rgba(0, 0, 0, 0.8); text-decoration: underline; }
```

Observations that matter:
- **Body text is `rgba(0,0,0,0.8)`, never `#000`.** Headings use the same family as body — one
  typeface for the whole site.
- **Links are black and underlined**, not blue. Hover *reduces* contrast (`0.5`) and removes the
  underline — inverted from the usual convention, and it keeps a citation-dense page from turning
  into a field of blue.
- **700px measure at 15px** ≈ 75–85 characters per line — the academic-paper measure.
- **No dark mode, no `prefers-color-scheme`, no custom webfont, no CSS framework.**

**Figures are numbered and ruled like a journal:**
```css
.article .figure { border-top: 1px solid hsla(0,0%,0%,0.2);
                   border-bottom: 1px solid hsla(0,0%,0%,0.2); padding: 20px 0; }
.article .figure .caption { font-size: 13px; }
.article .figure .caption-label { font-weight: bold; }   /* renders "Figure 1." */
```
Confirmed in the post source: `<div class="figure">` … `<span class="caption-label">Figure 1.`

**Tables use the LaTeX `booktabs` convention** — horizontal rules only, never vertical:
```css
table { border-top: 2px solid black; border-bottom: 1px solid black;
        border-collapse: collapse; font-size: 14px; }
table thead > tr > th { border-bottom: 1px solid black; }
```

**There is a real bibliography.** `#bibliography ol.bibliography`, with author-year anchor IDs
(`id="merton1973theory"`, `id="ito1944stochastic"`, `id="bru2002comments"`,
`id="derman2002boy"`) and correctly formatted references — Merton (1973) *Bell Journal of Economics
and Management Science*, Itô (1944) *Proc. Imperial Academy*, Nielsen (1992) *Understanding N(d1) and
N(d2)*. Six citations on a single blog post.

**The archive is grouped by year**, with the year set in the left margin
(`#blog .year { position: relative; right: 100px; color: rgba(0,0,0,0.5); }`), post dates in bold
uppercase 12px, titles at 18px, and a one-line subtitle under each. There is a tag navigation bar
(`ul#tag-nav`). Footnotes get a 12px block behind a top rule.

### Cross-cutting patterns

**Hosting.** GitHub Pages is the single most common host in the static cohort (8 of 20:
gatheral, algoquant, cswaney, wechsung on bare subdomains; sunnybala, hardikp, zachjs, eugeneyan
with custom domains). Two of those put **Cloudflare in front of GitHub Pages** (`x-github-request-id`
*and* `cf-ray` both present on zachjs.com and eugeneyan.com). Netlify appears once (Quarto). No
Vercel, no Astro, no Next.js anywhere in the quant cohort.

**Custom domains are common but explicitly not required.** A Presidential Professor at Baruch, a
Citadel GQS researcher, and an NYU Tandon adjunct all run bare `*.github.io`. Nobody in this audience
reads a `github.io` URL as amateur — if anything it reads as "engineer who didn't waste time on
branding." Brad already has `bradlasater.com`; keep it, but understand it's a convenience, not a
credibility gate.

**Charts are overwhelmingly static images.** Across ~20 sites, exactly one (quantguild.com) uses an
interactive charting library. Gundersen — writing about Black–Scholes, drift, log-normal densities
and vol surfaces — uses **plain PNGs** with numbered captions. The field's convention is a
matplotlib figure exported to file, captioned, and cited in the text.

**Dark mode is rare.** Only eugeneyan.com ships a real toggle. Every serious research site in the
sample is light-only with a near-grayscale palette.

**Structured data is a real differentiator.** Only 5 of 20 have any JSON-LD, and three of those are
auto-generated by Yoast/Jekyll defaults (`WebSite`/`CollectionPage`, which say nothing about the
person). Only hardikp.com carries a genuine nested `Person` object.

---

## PART 3 — Synthesis

### (a) Recommended stack and feature checklist

Brad's current state, audited: hand-written HTML/CSS on GitHub Pages, custom domain `bradlasater.com`
(confirmed `server: GitHub.com` on the live site), a 25KB design-token stylesheet with
`--font-sans/serif/mono` and a `--measure` variable, hand-rolled SVG charts in
`assets/js/track-record.js`, `Person` JSON-LD already on the homepage, OG + Twitter cards, an HTML CV
at `/cv.html`, and a track-record JSON schema with a CI validation workflow.

**Verdict: stay exactly where he is. Do not migrate.** He is already at or above the median of this
sample on every axis that matters, and ahead of nearly all of it on structured data and on
hand-rolled SVG charts (which beat both Plotly bloat and static PNGs). Migrating to Astro/Next.js
would be pure motion. The gap is not the stack — it's roughly six missing features.

**Keep as-is:** GitHub Pages hosting; custom domain *plus* the `bradlasater.github.io` fallback;
hand-written HTML; hand-rolled inline SVG for charts; `Person` JSON-LD; the CI-validated
`track-record.json`.

**Add, in priority order:**

1. **Pre-rendered KaTeX.** Non-negotiable for a vol site — he will need
   $\sigma_{\text{imp}}$, $d_1$, $d_2$, variance-swap replication integrals. Render at build time
   (`katex.renderToString`) in a small Node/Python build step and commit the output, exactly as
   Gundersen does. Ship `katex.min.css` only, **one version**, self-hosted rather than from a CDN.
   Zero runtime math JS.
2. **`sitemap.xml` and `robots.txt`** — both currently **missing**. This is the cheapest SEO fix
   available and it directly serves the "recruiter Googles his name" scenario.
3. **An RSS/Atom feed for the research log** — currently missing. Quantocracy and the quant community
   run on feeds; a feed is how a post gets picked up and amplified beyond his own network.
4. **Numbered, captioned figures with a `Figure N.` label and hairline rules**, and **booktabs
   tables** (horizontal rules only). These two CSS conventions do more to make a page read as
   research than any other change on this list.
5. **A references section with real citations** on any methodology page — Sinclair, López de Prado,
   Gatheral, Carr–Madan, Bakshi–Kapadia–Madan. Author-year anchors. This is the strongest
   "I read the literature" signal available, and it's free.
6. **Both CV formats.** He has `/cv.html`; add a linked `/cv.pdf`. Recruiters forward PDFs; ATSs
   ingest PDFs; hiring managers read HTML.
7. **Footnotes/sidenotes** for the caveats and "here's what would break this" asides — the register
   Moontower uses and the one that reads as trader-honest rather than salesy.
8. **Visible dates on everything** — published and last-updated. For a live track record this is a
   correctness requirement, not a nicety.

**Explicitly do not add:** a JS charting library (Plotly cost quantguild.com 10 scripts for a landing
page); a dark-mode toggle (essentially nobody serious in this sample has one — spend the effort on
the light palette); Algolia or any hosted search (his site is far too small); a CSS framework; a
SPA framework. And drop the Google Fonts dependency — Inter/Newsreader/JetBrains Mono should be
self-hosted `woff2` to remove a third-party render-blocking request and the privacy footprint.

**If he ever wants notebook publishing:** Quarto is the validated choice (`wilsonfreitas.net`,
maintainer of `awesome-quant`, ships it on Netlify with reading time, copy buttons, TOC, footnotes).
It renders `.ipynb` directly and can output to a subdirectory of the existing Pages site, so it can be
adopted for `/research/` alone without touching the hand-written pages. Do not adopt it site-wide.

### (b) Quality tells — serious researcher vs. bootcamp portfolio

**Reads as a serious researcher:**
- One typeface family, used consistently. Gundersen uses a single system stack for body *and*
  headings across the entire site.
- Text at ~80% black, not pure black; a near-grayscale palette; at most one accent color.
- A fixed measure of 650–750px. Full-bleed body text is the single loudest amateur tell.
- **Numbered figures with captions that are referenced in the prose** ("as Figure 3 shows"). Unnumbered
  decorative screenshots are the opposite signal.
- **Tables with horizontal rules only** (booktabs). Vertical rules and zebra striping read as
  spreadsheet export, not analysis.
- **Real citations with page-anchored references.** Six on a single Gundersen blog post.
- **Dated entries, including a visible last-updated stamp.** Jäckel's hand-written HTML carries a
  timestamp comment from five days before capture.
- **Dense archive listings grouped by year.** A reverse-chronological list going back years is itself
  the credential — it proves sustained output, which is the thing that cannot be faked in a weekend.
- **Negative results published.** Post-mortems and documented failures. In this audience, evidence of
  not fooling yourself outranks headline performance.
- **Explicit methodology pages** separate from results, with assumptions and known limitations stated.
- Links out to the primary artifacts: SSRN, arXiv, Google Scholar, the actual repo. Sepp links all
  five identities from the header.
- Prose in first person about *decisions and tradeoffs*, not third-person marketing copy.

**Reads as a bootcamp portfolio:**
- Hero section with a large photo, a tagline, and a "Let's build something amazing together" CTA.
- A **skills grid with technology logos**, or worse, proficiency bars ("Python ████░ 80%"). Nobody who
  has hired a quant has ever been persuaded by a progress bar.
- Card-grid "Projects" with stock thumbnails and no results, no methodology, no data provenance.
- Animated gradients, scroll-triggered fade-ins, parallax, typewriter effects, particle backgrounds.
- Multiple display typefaces, especially handwriting faces (Indie Flower on cswaney.github.io,
  Architects Daughter on algoquant.github.io both actively damage otherwise credible sites).
- Emoji as section headers.
- **Performance numbers with no sample period, no out-of-sample split, no cost assumptions, no
  capacity discussion, and no drawdown.** A Sharpe with no confidence interval is a red flag to this
  audience specifically — evaluating that claim is literally their job.
- Undated content, or a "latest post" that is 18 months old.
- "Passionate about" anything.
- A testimonials section on a personal site.

**The single sharpest discriminator:** a bootcamp portfolio is organized around *what the author can
do* (skills, tools, project count). A researcher's site is organized around *what the author found*
(results, methods, and the specific ways the result might be wrong). Brad's `/vol/methodology.html`
and `/vol/track-record.html` split is already the right shape — that structure is the asset.

### (c) SEO and discoverability for "Brad Lasater quant"

**Already correct:** canonical URL, `Person` JSON-LD with `jobTitle`, `knowsAbout`, and `sameAs` to
GitHub + LinkedIn; OG tags with a real `og:image`; `theme-color`; a descriptive `<title>` in the
`Name — Role, Specialty` form. This is better structured data than 15 of the 20 sites measured.

**Fix now:**

1. **Ship `sitemap.xml` and `robots.txt`.** Both missing. Static XML is fine; there are only ~7 pages.
   `robots.txt` should reference the sitemap.
2. **Extend `sameAs`.** Currently only GitHub and LinkedIn. Every serious site in the sample points at
   its full identity graph. Add X/Bluesky if he uses them, and — the moment he has anything posted —
   Google Scholar and SSRN author pages. `sameAs` is exactly how search engines merge scattered
   profiles into one entity, which is what makes a Knowledge-Panel-style result for his name possible.
3. **Add `alumniOf`, `worksFor`, and `address`/`homeLocation` (New York, NY) to the `Person` schema.**
   "New York" appearing as structured data, not just prose, is directly on-target for the recruiter
   query he cares about.
4. **Put the positioning sentence in the meta description in the third person, naming the city and the
   specialty.** Gundersen's is the model: *"Gregory Gundersen is a quantitative researcher in New
   York."* Sunny Balasubramanian's names his prior employers outright — for someone at Brad's stage,
   naming Nift / Ticketmaster / Lockheed Martin / Boeing in the description does the same work.
   Search engines frequently surface the meta description verbatim, so this is the one sentence a
   recruiter is most likely to read before deciding whether to click.
5. **Add `BlogPosting` / `ScholarlyArticle` JSON-LD to each research-log entry**, with `datePublished`,
   `dateModified`, `author` (referencing the same `Person` `@id`), and `keywords`. Give the `Person`
   node a stable `@id` (e.g. `https://bradlasater.com/#person`) and reference it from every page so
   the whole site resolves to one entity rather than several.
6. **Make the GitHub profile carry the same positioning.** The GitHub API sweep proves this is a live
   discovery channel — `search/users` with `in:bio` plus `location:"New York"` surfaces exactly this
   cohort. Brad's GitHub `bio`, `location: New York, NY`, and `blog: https://bradlasater.com` fields
   should mirror the site's positioning, and his profile README should link the vol system and the
   research log. That query is one a technically-minded recruiter genuinely runs.
7. **Title pattern for interior pages:** `Specific Topic — Brad Lasater`, with the distinguishing term
   first. Gatheral's title stuffs his full research specialty into the tag; that's aggressive but it
   works, because searches in this field are topic-led ("rough volatility") as often as name-led.
8. **Protect the name asset.** Set `bradlasater.com` to auto-renew with registrar lock, and never
   retire the `bradlasater.github.io` fallback. Two of the reference sites in this very report have
   already been lost to lapsed registration and now serve casino spam under a quant's name.

**Realistic expectation:** "Brad Lasater" is a low-competition query, so the site should rank first
for it quickly once a sitemap exists. The harder and more valuable target is being findable for
*topic* queries — "systematic volatility research log," "variance risk premium out-of-sample" — and
that is won by publishing dated, cited, indexable HTML posts consistently over months. The archive
grouped by year is both the SEO surface and the credibility artifact; they are the same thing.

# Roadmap

Outstanding work on bradlasater.com, ordered by what actually moves the goal:
inbound contact from quantitative-finance recruiters and hiring managers.

Everything here is evidence-based — each item traces to a `TODO` in the source,
an unconfigured value, an empty data file, or a promise the site already makes
in public.

---

## Blocking, and cheap

**Set the GoatCounter site code.** `assets/js/analytics.js` line 18 is
`var CODE = ""`, so the script returns immediately: zero pageviews and zero
events are being recorded. The recruiter funnel is entirely unmeasured. One
line. See the README's analytics section.

**Add a DMARC record.** `_dmarc.bradlasater.com` does not exist. Mail *is*
deliverable — this is a deliverability-hardening gap, not an outage — but it
makes outbound mail to Gmail and Outlook more likely to be filtered, and those
are the recruiters. Start with `p=none` and a `rua` address.

**Name the metric behind the "roughly 60%" claim.** Two `TODO(brad)` comments,
`index.html` and `cv.html`, both above *"Cut live-event sales forecast error by
roughly 60% against the incumbent baseline."* Which error metric — MAPE, WAPE,
RMSE — and against which baseline? This is the first thing a quant interviewer
will push on, and "I'd have to check" is a bad first answer. The comments ship
to the browser and are visible in view-source.

**Start the track record.** `data/track-record.json` has zero observations, so
`/vol/track-record.html` shows "Tracking has not started". The page's value is a
pure function of elapsed time, so the first append is worth more than any
further polishing. It also exercises the charts, statistics and verdict banner
against real data for the first time.

---

## Content debt — promises the site already makes

Each of these is published copy that nothing currently backs. None are broken
links; all are missing content.

**First research-log entry.** `/log/` is empty while `vol/index.html` §04 calls
post-mortems *"the most useful pages on this site."* Delete the `.pending` block
once the first entry ships.

**A post-mortem.** `index.html` commits to *"written post-mortems whenever the
system loses money or a hypothesis dies."*

**Trade-level logs.** `vol/methodology.html` promises *"trade-level logs behind
any live track record, so the reported statistics can be recomputed
independently."* The current schema stores daily aggregates only (`nav`,
`gross_pnl`, `costs`, `positions`, `mode`) and cannot express this. Either
extend the data contract or soften the promise — do not leave it unbacked.

**Decide where "Source" points.** Four buttons labelled *Source* / *GitHub* all
link to the GitHub profile, not to a trading-system repository. A visitor
clicking "Source" on `/vol/` lands on a profile page. If the system repo stays
private, relabel the buttons.

---

## Robustness and polish

**`.claude/settings.local.json` and scratch directories are untracked but
unignored.** There is no `.gitignore`; only a global ignore rule is keeping that
file out of commits. Add one.

**`ensure_ascii=False`** in `append_observation.py` — `json.dumps` currently
re-escapes the em-dash in the `strategy` field to `—` on first write,
producing a confusing diff on the very first observation commit.

**Dead CSS.** `.btn__icon`, `.card--link`, `.stack-4`, `.stack-6`, `.measure`,
the `.num`/`time` selector, and the `--c-surface-hover` custom property are
unreferenced by any HTML or JS.

**`[id] { scroll-margin-top: 6rem }`** applies to every element with an id,
including each `<span>` stat readout — 28 ids on the track-record page against
1 actually used as a link target. Harmless now; it will silently alter any
future `scrollIntoView()`.

**Breakpoint boundary overlap.** `min-width: 44rem` and `max-width: 44rem` both
match at exactly 704px. Currently benign — the blocks set disjoint properties —
but a latent trap.

**Repeated inline styles.** `style="font-size: var(--step-3); margin-top:
var(--sp-3);"` appears verbatim on four pages. Worth a class, and it is the only
thing that would force a `style-src 'unsafe-inline'` relaxation if a CSP is ever
added.

**Footer drift.** Five distinct footers across seven pages; `404.html` — the
page most in need of wayfinding — has the fewest links. Now that
`scripts/build_site.py` exists, this wants a single partial.

**Section landmark naming.** `index.html` and `vol/index.html` label nearly
every section with `aria-labelledby`; `vol/methodology.html`,
`vol/track-record.html` and `log/index.html` label none, so a screen-reader user
gets a rich landmark map on two pages and bare regions on three.

---

## Deliberately not doing

**Light mode.** The design commits to dark and paints every surface explicitly.

**OKLCH fallbacks.** Baseline support is Chrome 111+, Safari 15.4+, Firefox
113+, all from 2023. Acceptable for this audience.

**Pinning GitHub Actions to SHAs.** Reasonable for a shared repo; overhead for a
personal site. Revisit if anyone else gains write access — note that the
append-only guarantee ultimately depends on branch protection, since the
workflow runs the validator from the commit under test.

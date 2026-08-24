# Baseline audit — bradlasater.com (as of 2026-08-23, branch improve_v1)

## Inventory
- `index.html` — hero + positioning, "in development" vol system feature, 4 roles, capability tags, patents/education, contact
- `vol/index.html` — premise, 8 architecture cards, results pointer, post-mortems pointer, influences (Sinclair, MLdP)
- `vol/methodology.html` — pre-committed evaluation protocol (universe, PIT, purged CV, baselines, cost model, stats table, kill criteria)
- `vol/track-record.html` — live OOS record, browser-computed stats, append-only integrity argument
- `log/index.html` — research log, **zero entries**, template in HTML comment
- `cv.html` — full CV
- `data/track-record.json` — **zero observations**, inception null
- `scripts/validate_track_record.py` + GH Action — append-only CI enforcement
- `assets/css/site.css` — 25KB hand-rolled design system, OKLCH tokens, dark-only
- `assets/js/track-record.js` — 20KB browser-side stats/charts
- `assets/js/analytics.js` — GoatCounter, **CODE is empty → analytics not running**

## Already strong (do not regress)
1. Pre-committed evaluation protocol published before results exist — rare, high-signal.
2. Append-only track record enforced by CI, with git history as timestamp trail.
3. MinTRL / deflated Sharpe / PSR presented next to raw Sharpe; withholding stats under 20 obs.
4. Honest empty states ("Tracking has not started") instead of fake sample data.
5. Kill criteria committed in advance, including "P&L from unintended exposure retires the strategy."
6. Positioning line is specific and non-generic: "Estimating what uncertainty is worth, then trading the difference."
7. Career-bridge framing is explicit (particle filters ≈ filtering latent vol from discrete quotes).
8. Design system is restrained, technical, accessible (skip links, aria, colorblind-safe semantic colors).
9. JSON-LD Person schema, OG tags, canonical URLs, custom domain.

## Gaps found in this audit (pre-research)
- **Empty of evidence.** Log: 0 entries. Track record: 0 observations. The site promises process artifacts and currently delivers zero. Every claim is prospective.
- **No charts, no math, no code anywhere on the site.** Nothing to read that demonstrates ability.
- **GitHub is a liability right now.** 4 public repos, no profile README, no bio, no linked website, no repo descriptions on 3 of 4, and two near-duplicate repos (`data_ingest_infra` AND `data_ingestion_infra`). Site says "documented in the open" and links "Source" to a bare profile.
- **Shipped TODO in `index.html`** (visible in view-source): `TODO(brad): name the exact error metric here — MAPE, WAPE, RMSE?` next to the "roughly 60%" Ticketmaster claim. The TODO is correct about the risk; the fix hasn't landed.
- **"roughly 60%"** unqualified against unnamed baseline/metric — exactly the claim this audience probes.
- Analytics configured but inert (empty CODE) — no idea who is visiting.
- No RSS/feed, no sitemap.xml, no robots.txt.
- No resume PDF (HTML CV only) — recruiters forward PDFs.
- No photo, no location statement beyond "New York" in contact copy (he is remote/not-NYC — relocation intent is not stated).
- Dark-only; prints exist in CSS but no light mode.
- Log entry template lives in an HTML comment — no build step, so each entry is hand-authored HTML.

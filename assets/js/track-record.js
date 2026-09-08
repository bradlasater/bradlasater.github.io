/* ==========================================================================
   Live out-of-sample track record.

   Reads data/track-record.json and derives every statistic in the browser —
   nothing is precomputed and pasted in, so the page cannot disagree with the
   append-only data file behind it.

   The headline statistic is deliberately NOT the Sharpe ratio. It is the
   Minimum Track Record Length: how long this record would have to run before
   its Sharpe could be distinguished from zero. A short record says so.

   CONVENTIONS a reader needs in order to check these numbers:
     - Sharpe is excess of a 0% risk-free rate, i.e. mean/stdev of returns.
     - Sample standard deviation (ddof = 1).
     - Skewness and kurtosis are the biased sample moments g1 and b2
       (population sd in the denominator), matching scipy.stats.skew(bias=True)
       and scipy.stats.kurtosis(fisher=False, bias=True). Kurtosis is raw, so a
       normal distribution gives 3. NOTE pandas' .skew()/.kurt() default to the
       bias-corrected G1/G2 and will differ slightly.
     - PSR and MinTRL use the PER-PERIOD Sharpe, never the annualised one, and
       a benchmark Sharpe of zero, one-sided at 95%.

   Reference: Bailey & Lopez de Prado (2012), "The Sharpe Ratio Efficient
   Frontier", eq. 7 (PSR) and eq. 12 (MinTRL).

   INFERENTIAL vs DESCRIPTIVE. Cumulative return, drawdown and costs are facts
   about what happened and are always shown. Sharpe, PSR, MinTRL, skewness and
   kurtosis are inferences about an unknown distribution; below MIN_RETURNS
   they are not merely imprecise but actively misleading (a two-day sample can
   produce an annualised Sharpe in the thousands), so they are withheld. This
   asymmetry is the whole point of the page.

   RECORD KINDS ARE NEVER JOINED. Each observation declares a `record_kind`
   saying how its numbers were produced — forward simulation against live data
   with nothing at risk, or broker-executed and reconciled against actual
   fills. Those answer different questions and carry very different weight, so
   the page splits the record into one series per kind and computes every
   statistic within a single kind. Concatenating them would produce one curve
   whose early half is a simulator's marks and whose later half is real fills,
   with a single Sharpe over both — precisely the laundering this page exists
   to refuse. The kind selector switches series; it never merges them.
   ========================================================================== */

(function () {
  "use strict";

  /** Phi^-1(0.95), one-sided. */
  var Z95 = 1.6448536269514722;

  /** Returns needed before any inferential statistic is displayed. */
  var MIN_RETURNS = 20;

  /** Annualised Sharpe above this is a numerical artefact, not a result. */
  var MAX_PLAUSIBLE_SHARPE = 30;

  /** Relative floor for the standard deviation, guarding against a NAV series
      that is smooth to within floating-point noise. */
  var REL_SD_FLOOR = 1e-8;

  /** Record kinds, weakest evidence first. The order is the schema's, and the
      validator refuses any observation that moves back down it. */
  var RECORD_KINDS = ["forward_sim", "broker_executed"];

  var RECORD_KIND_LABEL = {
    forward_sim: "Forward simulation",
    broker_executed: "Broker-executed"
  };

  /** One clause naming what the kind does and does not establish. Shown with
      whichever series is on screen, so the weight a reader should give the
      numbers arrives at the same time as the numbers. */
  var RECORD_KIND_BLURB = {
    forward_sim:
      "live market data with nothing at risk; fills are modelled rather than " +
      "obtained from a broker",
    broker_executed:
      "reconciled against actual broker fills"
  };

  /* ---------------------------------------------------------------- math -- */

  /**
   * Error function, Abramowitz & Stegun 7.1.26.
   * Max absolute error 1.5e-7 — far below the precision of a displayed
   * percentage, so no higher-order method is warranted.
   * @param {number} x
   * @returns {number}
   */
  function erf(x) {
    var sign = x < 0 ? -1 : 1;
    x = Math.abs(x);
    var t = 1 / (1 + 0.3275911 * x);
    var y =
      1 -
      ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t -
        0.284496736) *
        t +
        0.254829592) *
        t *
        Math.exp(-x * x);
    return sign * y;
  }

  /** Standard normal CDF. @param {number} x @returns {number} */
  function normalCdf(x) {
    return 0.5 * (1 + erf(x / Math.SQRT2));
  }

  /** @param {number[]} xs @returns {number} */
  function mean(xs) {
    var s = 0;
    for (var i = 0; i < xs.length; i++) s += xs[i];
    return s / xs.length;
  }

  /**
   * Sample standard deviation (ddof = 1), matching the Sharpe convention.
   * @param {number[]} xs @param {number} mu @returns {number}
   */
  function stdev(xs, mu) {
    if (xs.length < 2) return NaN;
    var s = 0;
    for (var i = 0; i < xs.length; i++) s += (xs[i] - mu) * (xs[i] - mu);
    return Math.sqrt(s / (xs.length - 1));
  }

  /**
   * Biased standardised moment of order k — divides by the POPULATION sd, so
   * k=3 gives g1 and k=4 gives b2. Using the ddof=1 sd here instead would
   * produce a hybrid estimator matching neither scipy nor pandas.
   * @param {number[]} xs @param {number} mu @param {number} sdSample
   * @param {number} k @returns {number}
   */
  function standardisedMoment(xs, mu, sdSample, k) {
    var n = xs.length;
    var sdPop = sdSample * Math.sqrt((n - 1) / n);
    var s = 0;
    for (var i = 0; i < n; i++) s += Math.pow((xs[i] - mu) / sdPop, k);
    return s / n;
  }

  /* --------------------------------------------------------- statistics -- */

  /**
   * @typedef {Object} Stats
   * @property {number} n observations
   * @property {number} nReturns
   * @property {boolean} inferential whether the sample supports inference
   * @property {?number} cumulative
   * @property {?number} sharpeAnnual
   * @property {?number} psr
   * @property {?number} minTRL in RETURNS, not observations
   */

  /**
   * Derive every displayed statistic from the observation list.
   * @param {Array<Object>} observations sorted, validated
   * @param {number} periodsPerYear
   * @returns {Stats}
   */
  function computeStats(observations, periodsPerYear) {
    var navs = observations.map(function (o) {
      return o.nav;
    });

    var returns = [];
    for (var i = 1; i < navs.length; i++) {
      returns.push(navs[i] / navs[i - 1] - 1);
    }

    var out = {
      n: observations.length,
      nReturns: returns.length,
      inferential: false,
      returns: returns,
      cumulative: navs.length ? navs[navs.length - 1] / navs[0] - 1 : null,
      sharpeAnnual: null,
      volAnnual: null,
      returnAnnual: null,
      psr: null,
      minTRL: null,
      skew: null,
      kurtosis: null,
      maxDrawdown: null,
      currentDrawdown: null,
      costShare: null,
      costTotal: null,
      grossTotal: null,
      costsComplete: true
    };

    /* Descriptive: drawdowns. Always shown — these are facts, not estimates. */
    if (navs.length) {
      var peak = navs[0];
      var maxDd = 0;
      for (var j = 0; j < navs.length; j++) {
        if (navs[j] > peak) peak = navs[j];
        var dd = navs[j] / peak - 1;
        if (dd < maxDd) maxDd = dd;
      }
      out.maxDrawdown = maxDd;
      out.currentDrawdown = navs[navs.length - 1] / peak - 1;
    }

    /* Descriptive: costs. A missing field is NOT zero — reporting "$0 costs"
       on a page advertising "net of all modelled frictions" would be an
       affirmative false claim, so incompleteness suppresses the figure. */
    var grossTotal = 0;
    var costTotal = 0;
    observations.forEach(function (o) {
      if (typeof o.costs !== "number" || typeof o.gross_pnl !== "number") {
        out.costsComplete = false;
        return;
      }
      grossTotal += o.gross_pnl;
      costTotal += o.costs;
    });
    if (out.costsComplete) {
      out.grossTotal = grossTotal;
      out.costTotal = costTotal;
      if (grossTotal > 0) out.costShare = costTotal / grossTotal;
    }

    /* Everything below is inferential. */
    if (returns.length < MIN_RETURNS) return out;

    var mu = mean(returns);
    var sd = stdev(returns, mu);

    // A constant-growth NAV leaves a standard deviation of ~1e-16 — pure
    // floating-point residue, which a `sd <= 0` test does not catch and which
    // yields an annualised Sharpe of ~1e14.
    if (!isFinite(sd) || sd <= 1e-12 || sd <= REL_SD_FLOOR * Math.abs(mu)) {
      return out;
    }

    var srPeriod = mu / sd;
    var sharpeAnnual = srPeriod * Math.sqrt(periodsPerYear);
    if (!isFinite(sharpeAnnual) || Math.abs(sharpeAnnual) > MAX_PLAUSIBLE_SHARPE) {
      return out;
    }

    var g3 = standardisedMoment(returns, mu, sd, 3);
    var g4 = standardisedMoment(returns, mu, sd, 4);
    if (!isFinite(g3) || !isFinite(g4)) return out;

    out.inferential = true;
    out.skew = g3;
    out.kurtosis = g4;
    out.volAnnual = sd * Math.sqrt(periodsPerYear);
    out.sharpeAnnual = sharpeAnnual;

    if (out.cumulative > -1) {
      out.returnAnnual =
        Math.pow(1 + out.cumulative, periodsPerYear / returns.length) - 1;
    }

    /* PSR and MinTRL, benchmark Sharpe zero. The variance term corrects for
       the non-normality that makes a naive Sharpe optimistic. It can go
       non-positive on small or extreme samples, in which case neither
       statistic is defined and both stay null — the verdict must handle that
       rather than falling through to a significance claim. */
    var variance = 1 - g3 * srPeriod + ((g4 - 1) / 4) * srPeriod * srPeriod;
    if (variance > 0) {
      out.psr = normalCdf(
        (srPeriod * Math.sqrt(returns.length - 1)) / Math.sqrt(variance)
      );
      if (srPeriod > 0) {
        out.minTRL = 1 + variance * Math.pow(Z95 / srPeriod, 2);
      }
    }

    return out;
  }

  /* ------------------------------------------------------------ format -- */

  function isNum(x) {
    return typeof x === "number" && isFinite(x);
  }

  function pct(x, digits) {
    if (!isNum(x)) return "—";
    var s = (x * 100).toFixed(digits === undefined ? 2 : digits);
    if (/^-0\.?0*$/.test(s)) s = s.slice(1); // avoid "-0.0%"
    return s + "%";
  }

  function num(x, digits) {
    return isNum(x) ? x.toFixed(digits === undefined ? 2 : digits) : "—";
  }

  function money(x, currency) {
    if (!isNum(x)) return "—";
    var code = /^[A-Z]{3}$/.test(currency || "") ? currency : "USD";
    try {
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: code,
        maximumFractionDigits: 0
      }).format(x);
    } catch (e) {
      return String(Math.round(x));
    }
  }

  /** Parse as UTC so a rendered date never shifts by a day in some zones. */
  function parseDate(s) {
    return new Date(s + "T00:00:00Z");
  }

  /** Whole UTC days between two dates, floored — never rounded up. */
  function daysBetweenUTC(a, b) {
    var da = Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate());
    var db = Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate());
    return Math.floor((db - da) / 86400000);
  }

  function fmtDate(d) {
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      timeZone: "UTC"
    });
  }

  /* ------------------------------------------------------------- chart -- */

  /* The SVG chart engine lives in assets/js/chart.js as window.SiteChart, so
     the diagnostic pages can draw with the same code. This file keeps the
     statistics and the formatting; the chart keeps the pixels. */


  /* ------------------------------------------------------------ render -- */

  function setText(id, value) {
    var node = document.getElementById(id);
    if (node) node.textContent = value;
  }

  /**
   * Validate the fetched document before anything is rendered.
   * Bailing out here rather than mid-render is what prevents a half-built
   * page: partial statistics, NaN path data and an error banner at once.
   * @returns {Array<Object>} observations, sorted ascending by date
   */
  function normalise(doc) {
    if (!doc || typeof doc !== "object") throw new Error("data is not an object");
    var observations = doc.observations;
    if (!Array.isArray(observations)) throw new Error("observations is not an array");

    observations.forEach(function (o, i) {
      if (!o || typeof o !== "object") throw new Error("observation " + i + " is not an object");
      if (typeof o.date !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(o.date)) {
        throw new Error("observation " + i + " has an invalid date");
      }
      // The shape check above passes strings like "2026-13-45", and Date.parse
      // normalises some out-of-range days (Chromium treats "2026-02-30" as a
      // March date) instead of rejecting them, so compare the parsed UTC
      // components against the source string.
      var parts = o.date.split("-");
      var parsed = parseDate(o.date);
      if (!isFinite(parsed.getTime()) ||
          parsed.getUTCFullYear() !== +parts[0] ||
          parsed.getUTCMonth() !== +parts[1] - 1 ||
          parsed.getUTCDate() !== +parts[2]) {
        throw new Error("observation " + i + " has a non-existent date " + o.date);
      }
      if (!isNum(o.nav) || o.nav <= 0) {
        throw new Error("observation " + i + " has an invalid nav");
      }
      // Required, never inferred. Every figure below depends on which kind of
      // record a day belongs to, so a day that does not say is not a day this
      // page can render — guessing would attach a claim to it that nobody made.
      if (RECORD_KINDS.indexOf(o.record_kind) === -1) {
        throw new Error(
          "observation " + i + " has an unknown record_kind " +
          JSON.stringify(o.record_kind)
        );
      }
    });

    var sorted = observations.slice().sort(function (a, b) {
      return a.date < b.date ? -1 : a.date > b.date ? 1 : 0;
    });
    for (var i = 1; i < sorted.length; i++) {
      if (sorted[i].date === sorted[i - 1].date) {
        throw new Error("duplicate observation date " + sorted[i].date);
      }
      // The schema forbids falling back to weaker evidence, and the renderer
      // relies on it: one contiguous run per kind is what makes "this series
      // is broker-executed" a statement about a date range rather than about a
      // scatter of days. Refusing to draw is the right failure here — a page
      // that renders a mislabelled record is worse than one that says it could
      // not load.
      var step =
        RECORD_KINDS.indexOf(sorted[i].record_kind) -
        RECORD_KINDS.indexOf(sorted[i - 1].record_kind);
      if (step < 0) {
        throw new Error(
          "record kind regressed to " + sorted[i].record_kind + " on " +
          sorted[i].date
        );
      }
    }
    return sorted;
  }

  /**
   * Split the record into one contiguous segment per kind, in date order.
   * normalise() has already rejected a regressing sequence, so each kind
   * appears at most once and a segment is a date range, not a filter.
   * @param {Array<Object>} observations sorted ascending
   * @returns {Array<{kind: string, observations: Array<Object>}>}
   */
  function segmentByKind(observations) {
    var segments = [];
    observations.forEach(function (o) {
      var last = segments[segments.length - 1];
      if (last && last.kind === o.record_kind) {
        last.observations.push(o);
      } else {
        segments.push({ kind: o.record_kind, observations: [o] });
      }
    });
    return segments;
  }

  /**
   * @param {Array<Object>} observations the selected segment only
   * @param {Stats} stats
   * @param {{isLatest: boolean, multi: boolean}} opts isLatest — this segment
   *   is the one still running; multi — the record holds more than one kind.
   */
  function renderHero(observations, stats, opts) {
    var start = parseDate(observations[0].date);
    var latest = parseDate(observations[observations.length - 1].date);

    // Elapsed time accrues only for the segment that is still running. A
    // segment the record has moved on from is closed, and counting it up to
    // today would credit a finished series with days it never traded.
    var through = opts.isLatest ? new Date() : latest;
    // Clamp at 1: a viewer whose clock lags the first observation would
    // otherwise see "0" or negative days on a record that has demonstrably
    // started.
    setText("tr-days", String(Math.max(1, daysBetweenUTC(start, through) + 1)));

    // "Inception" belongs to the record as a whole. Once there is more than one
    // kind, the date below is where *this series* starts, which is a different
    // claim and has to be labelled as one.
    setText("tr-start-label", opts.multi ? "Series began" : "Inception");
    setText("tr-inception", fmtDate(start));
    setText("tr-latest", fmtDate(latest));
    setText("tr-obs", String(stats.n));

    var modeNode = document.getElementById("tr-mode");
    if (modeNode) {
      var current = observations[observations.length - 1].mode;
      modeNode.textContent = current === "live" ? "Real capital" : "Paper — simulated";
      modeNode.className =
        "badge badge--dot " + (current === "live" ? "badge--live" : "badge--active");
    }
  }

  function renderStats(doc, stats) {
    [
      ["tr-cum", pct(stats.cumulative)],
      ["tr-ann", pct(stats.returnAnnual)],
      ["tr-vol", pct(stats.volAnnual)],
      ["tr-sharpe", num(stats.sharpeAnnual)],
      ["tr-psr", isNum(stats.psr) ? pct(stats.psr, 1) : "—"],
      ["tr-mintrl", isNum(stats.minTRL) ? String(Math.ceil(stats.minTRL)) : "—"],
      ["tr-maxdd", pct(stats.maxDrawdown)],
      ["tr-curdd", pct(stats.currentDrawdown)],
      ["tr-skew", num(stats.skew)],
      ["tr-kurt", num(stats.kurtosis)],
      ["tr-costshare", isNum(stats.costShare) ? pct(stats.costShare, 1) : "—"],
      ["tr-costs", stats.costsComplete ? money(stats.costTotal, doc.base_currency) : "—"]
    ].forEach(function (pair) {
      setText(pair[0], pair[1]);
    });

    setText(
      "tr-ann-hint",
      stats.inferential
        ? "Geometric, " + (doc.periods_per_year || 252) + "-day basis"
        : "Withheld under " + (MIN_RETURNS + 1) + " observations"
    );
  }

  /**
   * The honest headline: whether the record is long enough to mean anything.
   * Every branch must terminate in a definite message — an undefined MinTRL
   * must never fall through to the significance claim.
   */
  function renderVerdict(stats) {
    var verdict = document.getElementById("tr-verdict");
    if (!verdict) return;

    var needed = isNum(stats.minTRL) ? Math.ceil(stats.minTRL) : null;
    var tone = "pending";
    var body;

    if (stats.nReturns < MIN_RETURNS) {
      body =
        "Too short to support any inference. Performance statistics are " +
        "withheld until there are at least " + MIN_RETURNS + " daily returns (" +
        (MIN_RETURNS + 1) + " observations); this record has " + stats.nReturns +
        ". A Sharpe ratio computed from a handful of days can run into the " +
        "thousands and means nothing, so it is not shown at all.";
    } else if (!stats.inferential) {
      body =
        "The return series is too smooth or too extreme for these statistics " +
        "to be numerically meaningful at this sample size, so they are withheld.";
    } else if (!isNum(stats.sharpeAnnual)) {
      body = "The Sharpe ratio is undefined for this sample.";
    } else if (stats.sharpeAnnual <= 0) {
      body =
        "The observed Sharpe ratio is at or below zero, so there is nothing to " +
        "distinguish from zero yet. That is reported rather than hidden.";
    } else if (needed === null) {
      body =
        "The Sharpe estimate is too unstable at this sample size for a minimum " +
        "track record length to be defined, so no significance claim is made.";
    } else if (stats.nReturns < needed) {
      body =
        "This track record is too short to be statistically meaningful. Given " +
        "the observed Sharpe, skewness, and kurtosis, distinguishing it from " +
        "zero at 95% confidence would take about " + needed + " returns. It has " +
        stats.nReturns + ". Read the numbers below as provisional.";
    } else {
      tone = "ok";
      body =
        "The observed Sharpe ratio is distinguishable from zero at 95% " +
        "confidence: the record has " + stats.nReturns + " returns against a " +
        "minimum of about " + needed + ". The probabilistic Sharpe ratio is " +
        pct(stats.psr, 1) + ".";
    }

    verdict.className = "verdict verdict--" + tone;
    setText("tr-verdict-body", body);
  }

  function buildSeries(doc, observations) {
    var base = observations[0].nav;
    var equity = observations.map(function (o) {
      return { date: parseDate(o.date), value: o.nav / base - 1 };
    });

    var peak = observations[0].nav;
    var drawdown = observations.map(function (o) {
      if (o.nav > peak) peak = o.nav;
      return { date: parseDate(o.date), value: o.nav / peak - 1 };
    });

    /* Boundaries: compare parsed dates, and skip any transition that falls
       outside the observed range rather than silently dropping or pinning it
       to index 0. */
    var boundaries = [];
    var changes = Array.isArray(doc.mode_changes) ? doc.mode_changes : [];
    changes.forEach(function (change) {
      if (!change || typeof change.date !== "string") return;
      var when = parseDate(change.date).getTime();
      for (var i = 0; i < observations.length; i++) {
        if (parseDate(observations[i].date).getTime() >= when) {
          if (i === 0 && when < parseDate(observations[0].date).getTime()) return;
          boundaries.push({
            index: i,
            label: change.to === "live" ? "Real capital" : "Paper"
          });
          return;
        }
      }
      // Dated after every observation — nothing to draw yet.
    });

    return { equity: equity, drawdown: drawdown, boundaries: boundaries };
  }

  /** Table view — the WCAG-clean twin. Built with textContent, never
      innerHTML: the JSON is author-controlled but public, and the CI
      validator is a schema check, not an HTML sanitiser. */
  function renderTable(observations) {
    var tbody = document.getElementById("tr-tbody");
    if (!tbody) return;
    tbody.textContent = "";

    for (var i = observations.length - 1; i >= 0; i--) {
      var o = observations[i];
      // A return spanning a kind boundary would divide a broker-executed NAV
      // by a simulated one. The charts and every statistic already reset at
      // that boundary; the table has to as well, or this column quietly
      // reintroduces the one number the whole page promises never to compute.
      // The first observation of each kind is a new baseline, not a return.
      var prev = i === 0 ? null : observations[i - 1];
      var ret = prev && prev.record_kind === o.record_kind
        ? o.nav / prev.nav - 1
        : null;
      var row = document.createElement("tr");

      [
        { text: o.date, cls: "" },
        { text: o.nav.toFixed(2), cls: "numeric" },
        {
          text: ret === null ? "—" : pct(ret),
          cls: "numeric " + (ret === null ? "" : ret >= 0 ? "pos" : "neg")
        },
        { text: isNum(o.gross_pnl) ? o.gross_pnl.toFixed(2) : "—", cls: "numeric" },
        { text: isNum(o.costs) ? o.costs.toFixed(2) : "—", cls: "numeric" },
        { text: isNum(o.positions) ? String(o.positions) : "—", cls: "numeric" },
        { text: typeof o.mode === "string" && o.mode ? o.mode : "—", cls: "" },
        // Per-row, so the table stays the complete record even while the
        // statistics above are deliberately confined to one kind.
        { text: RECORD_KIND_LABEL[o.record_kind] || "—", cls: "" }
      ].forEach(function (cell) {
        var td = document.createElement("td");
        if (cell.cls.trim()) td.className = cell.cls.trim();
        td.textContent = cell.text;
        row.appendChild(td);
      });

      tbody.appendChild(row);
    }
  }

  function hideLoading() {
    var loading = document.getElementById("tr-loading");
    if (loading) loading.hidden = true;
  }

  function showEmpty() {
    hideLoading();
    var empty = document.getElementById("tr-empty");
    var live = document.getElementById("tr-live");
    if (empty) empty.hidden = false;
    if (live) live.hidden = true;
  }

  function showError(message) {
    showFailure("Could not load the track record data (" + message + ").");
  }

  /**
   * A failure that is not about the data.
   *
   * Kept separate from showError because the two send a reader somewhere
   * different: a data failure means the record could not be fetched or parsed,
   * and a render failure means the page itself is broken while the record may
   * be perfectly fine. Reporting the second as the first sends whoever is
   * debugging it to look at the JSON.
   *
   * @param {string} message Full sentence, already punctuated.
   */
  function showFailure(message) {
    hideLoading();
    var fail = document.getElementById("tr-error");
    var empty = document.getElementById("tr-empty");
    var live = document.getElementById("tr-live");
    if (live) live.hidden = true;
    if (empty) empty.hidden = true;
    if (fail) {
      fail.hidden = false;
      fail.textContent = message;
    }
  }

  /**
   * State what the figures below are, and — when there is more than one kind —
   * what they deliberately exclude. This sentence is the page's defence
   * against the reader who scrolls to a Sharpe ratio and assumes it covers the
   * whole record, so it is rendered with the numbers, not in the prose above.
   */
  function renderKindNote(segments, selected) {
    var node = document.getElementById("tr-kind-note");
    if (!node) return;
    node.textContent = "";

    var count = selected.observations.length;
    var strong = document.createElement("strong");
    strong.textContent = RECORD_KIND_LABEL[selected.kind];
    node.appendChild(strong);

    var others = segments.filter(function (s) {
      return s.kind !== selected.kind;
    });
    var text =
      " — " + RECORD_KIND_BLURB[selected.kind] + ". Every figure below is " +
      "computed from these " + count + " observation" + (count === 1 ? "" : "s") +
      " alone.";
    if (others.length) {
      text +=
        " The " +
        others
          .map(function (s) {
            return (
              s.observations.length + " " +
              RECORD_KIND_LABEL[s.kind].toLowerCase() + " observation" +
              (s.observations.length === 1 ? "" : "s")
            );
          })
          .join(" and ") +
        " are reported as their own series and are never joined to this one. " +
        "The table below lists every observation of every kind.";
    }
    node.appendChild(document.createTextNode(text));
  }

  /** Draw everything that is scoped to a single record kind. */
  function renderSegment(doc, segments, selected) {
    var observations = selected.observations;
    var stats = computeStats(observations, doc.periods_per_year || 252);
    var isLatest = segments[segments.length - 1] === selected;

    renderKindNote(segments, selected);
    renderHero(observations, stats, { isLatest: isLatest, multi: segments.length > 1 });
    renderStats(doc, stats);
    renderVerdict(stats);

    var series = buildSeries(doc, observations);
    var label = RECORD_KIND_LABEL[selected.kind].toLowerCase();

    var eqNode = document.getElementById("tr-chart-equity");
    if (eqNode) {
      SiteChart.draw(eqNode, series.equity, {
        kind: "equity",
        boundaries: series.boundaries,
        formatValue: pct,
        formatDate: fmtDate,
        ariaLabel:
          "Cumulative return of the " + label + " series, indexed to its first " +
          "observation: " + pct(stats.cumulative) + " over " + stats.n +
          " observations. Full values are in the table below."
      });
    }

    var ddNode = document.getElementById("tr-chart-drawdown");
    if (ddNode) {
      SiteChart.draw(ddNode, series.drawdown, {
        kind: "drawdown",
        height: 180,
        formatValue: pct,
        formatDate: fmtDate,
        ariaLabel:
          "Drawdown from running peak of the " + label + " series. Maximum " +
          "drawdown " + pct(stats.maxDrawdown) +
          ". Full values are in the table below."
      });
    }
  }

  /**
   * Build the series selector, or leave it hidden when there is only one kind.
   *
   * Radios rather than a <select>: the set is tiny and fixed, and every option
   * stays visible, so a reader can see that a second series exists without
   * interacting with the control. Selecting one re-renders the section from
   * that segment; nothing is ever aggregated across segments.
   *
   * @returns {{kind: string, observations: Array<Object>}} the segment to show
   */
  function renderKindSwitch(doc, segments) {
    var host = document.getElementById("tr-kind-switch");
    if (segments.length < 2 || !host) {
      if (host) {
        host.textContent = "";
        host.hidden = true;
      }
      return segments[0];
    }
    host.textContent = "";
    host.hidden = false;

    var set = document.createElement("fieldset");
    set.className = "viewswitch__set";
    var legend = document.createElement("legend");
    legend.className = "viewswitch__legend";
    legend.textContent = "Series";
    set.appendChild(legend);

    // Default to the last segment: the kinds only ever climb, so the newest is
    // also the strongest evidence, and it is what the record currently is.
    var initial = segments[segments.length - 1];

    segments.forEach(function (segment) {
      var id = "tr-kind-" + segment.kind;
      var input = document.createElement("input");
      input.className = "viewswitch__input";
      input.type = "radio";
      input.name = "tr-kind";
      input.id = id;
      input.checked = segment === initial;
      input.addEventListener("change", function () {
        if (input.checked) renderSegment(doc, segments, segment);
      });

      var label = document.createElement("label");
      label.className = "viewswitch__label";
      label.htmlFor = id;
      label.textContent =
        RECORD_KIND_LABEL[segment.kind] + " (" + segment.observations.length + ")";

      set.appendChild(input);
      set.appendChild(label);
    });

    host.appendChild(set);
    return initial;
  }

  function render(doc) {
    var observations = normalise(doc);

    if (!observations.length) {
      showEmpty();
      return;
    }

    hideLoading();
    var empty = document.getElementById("tr-empty");
    var live = document.getElementById("tr-live");
    if (empty) empty.hidden = true;
    if (live) live.hidden = false;

    var segments = segmentByKind(observations);
    renderSegment(doc, segments, renderKindSwitch(doc, segments));

    // The table is the complete record and is never filtered by the selector:
    // the statistics are scoped, the raw data is not.
    renderTable(observations);
  }

  /* --------------------------------------------------------------- boot -- */

  document.addEventListener("DOMContentLoaded", function () {
    var root = document.getElementById("tr-root");
    if (!root) return;

    // chart.js is a separate file and a separate <script>. A page that forgot
    // it would render statistics with two empty boxes where the charts belong,
    // which reads as "no data" rather than "broken deployment".
    if (typeof window.SiteChart === "undefined" || typeof window.SiteChart.draw !== "function") {
      showFailure(
        "This page could not render: the chart module at /assets/js/chart.js did not load. " +
        "The track record itself is unaffected and can be read at /data/track-record.json."
      );
      return;
    }

    var src = root.getAttribute("data-source") || "/data/track-record.json";

    // A hung request would otherwise leave the page on the empty state
    // forever, silently claiming tracking has not started.
    var controller = typeof AbortController === "function" ? new AbortController() : null;
    var timer = setTimeout(function () {
      if (controller) controller.abort();
    }, 15000);

    fetch(src, { cache: "no-cache", signal: controller ? controller.signal : undefined })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (doc) {
        clearTimeout(timer);
        render(doc);
      })
      .catch(function (err) {
        clearTimeout(timer);
        showError(err && err.message ? err.message : String(err));
      });
  });
})();

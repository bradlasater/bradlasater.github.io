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

  var NS = "http://www.w3.org/2000/svg";

  function el(name, attrs) {
    var node = document.createElementNS(NS, name);
    for (var k in attrs) {
      if (Object.prototype.hasOwnProperty.call(attrs, k)) {
        node.setAttribute(k, attrs[k]);
      }
    }
    return node;
  }

  /**
   * Axis ticks at round values covering [min, max].
   * Computed by index rather than by accumulating `v += step`, because
   * accumulation drifts and leaves the zero tick at ~1e-18, which then fails
   * an equality test and silently loses the emphasised zero baseline.
   * @returns {number[]}
   */
  function niceTicks(min, max, count) {
    var span = max - min;
    if (!(span > 0)) return [min];
    var raw = span / count;
    var mag = Math.pow(10, Math.floor(Math.log10(raw)));
    var norm = raw / mag;
    var step = (norm > 5 ? 10 : norm > 2 ? 5 : norm > 1 ? 2 : 1) * mag;
    var start = Math.ceil(min / step);
    var ticks = [];
    for (var i = 0; start + i <= max / step + 1e-9; i++) {
      var v = (start + i) * step;
      if (Math.abs(v) < step * 1e-9) v = 0; // snap float dust to exact zero
      ticks.push(v);
    }
    return ticks;
  }

  /**
   * Render one chart into `container`.
   * @param {HTMLElement} container
   * @param {Array<{date: Date, value: number}>} series
   * @param {{kind: string, height?: number, boundaries?: Array, ariaLabel?: string}} opts
   */
  function drawChart(container, series, opts) {
    container.textContent = "";
    // An empty series would make lo/hi ±Infinity and emit NaN path data.
    if (!series.length) return;

    var W = 760;
    var H = opts.height || 260;
    // Bottom margin reserves the x-axis band so labels are never clipped.
    var M = { top: 16, right: 64, bottom: 34, left: 8 };
    var plotW = W - M.left - M.right;
    var plotH = H - M.top - M.bottom;

    var values = series.map(function (p) {
      return p.value;
    });
    var lo = Math.min.apply(null, values);
    var hi = Math.max.apply(null, values);

    if (opts.kind === "drawdown") {
      hi = 0;
      if (lo === 0) lo = -0.01;
    }
    if (lo === hi) {
      lo -= 0.01;
      hi += 0.01;
    }
    var pad = (hi - lo) * 0.12;
    lo -= pad;
    hi += pad;
    if (opts.kind === "drawdown" && hi > 0) hi = 0;

    var svg = el("svg", {
      viewBox: "0 0 " + W + " " + H,
      class: "chart__svg",
      role: "img",
      "aria-label": opts.ariaLabel || ""
    });

    function sx(i) {
      return series.length < 2
        ? M.left + plotW / 2
        : M.left + (i / (series.length - 1)) * plotW;
    }
    function sy(v) {
      return M.top + (1 - (v - lo) / (hi - lo)) * plotH;
    }

    /* Gridlines + y ticks — hairline, solid, recessive. */
    var seen = {};
    niceTicks(lo, hi, 4).forEach(function (t) {
      var label = pct(t, 1);
      if (seen[label]) return; // never two identically-labelled ticks
      seen[label] = true;
      var y = sy(t);
      svg.appendChild(
        el("line", {
          x1: M.left,
          y1: y,
          x2: M.left + plotW,
          y2: y,
          class: t === 0 ? "chart__zero" : "chart__grid"
        })
      );
      var text = el("text", {
        x: M.left + plotW + 8,
        y: y + 4,
        class: "chart__tick"
      });
      text.textContent = label;
      svg.appendChild(text);
    });

    /* Area wash then line. Anchor the wash to zero whenever zero is on screen,
       so area above the line reads as gain and below as loss; falling back to
       the plot floor would shade losses as though they were gains. */
    var linePts = series.map(function (p, i) {
      return sx(i) + "," + sy(p.value);
    });
    var zeroInRange = lo <= 0 && hi >= 0;
    var baseline = opts.kind === "drawdown" || zeroInRange ? sy(0) : sy(lo);

    if (series.length > 1) {
      svg.appendChild(
        el("path", {
          d:
            "M" + sx(0) + "," + baseline +
            " L" + linePts.join(" L") +
            " L" + sx(series.length - 1) + "," + baseline + " Z",
          class: "chart__area chart__area--" + opts.kind
        })
      );
      svg.appendChild(
        el("path", {
          d: "M" + linePts.join(" L"),
          class: "chart__line chart__line--" + opts.kind
        })
      );
    }

    /* Mode-change boundary: where paper trading became real capital. */
    (opts.boundaries || []).forEach(function (b) {
      var x = sx(b.index);
      svg.appendChild(
        el("line", {
          x1: x, y1: M.top, x2: x, y2: M.top + plotH,
          class: "chart__boundary"
        })
      );
      var t = el("text", { x: x + 6, y: M.top + 12, class: "chart__boundary-label" });
      t.textContent = b.label;
      svg.appendChild(t);
    });

    /* Endpoint marker + 2px surface ring — the only labelled point. */
    if (series.length) {
      var lastI = series.length - 1;
      var lx = sx(lastI);
      var ly = sy(series[lastI].value);
      svg.appendChild(el("circle", { cx: lx, cy: ly, r: 5, class: "chart__ring" }));
      svg.appendChild(
        el("circle", { cx: lx, cy: ly, r: 4, class: "chart__dot chart__dot--" + opts.kind })
      );
    }

    /* X-axis: first and last date only, so labels never collide. */
    if (series.length) {
      var first = el("text", { x: M.left, y: H - 10, class: "chart__tick" });
      first.textContent = fmtDate(series[0].date);
      svg.appendChild(first);
      if (series.length > 1) {
        var last = el("text", {
          x: M.left + plotW, y: H - 10,
          class: "chart__tick", "text-anchor": "end"
        });
        last.textContent = fmtDate(series[series.length - 1].date);
        svg.appendChild(last);
      }
    }

    /* Hover layer. Values stay reachable via the table view below, so the
       tooltip enhances rather than gates. */
    var hover = el("g", { class: "chart__hover", "aria-hidden": "true" });
    var vline = el("line", { y1: M.top, y2: M.top + plotH, class: "chart__crosshair" });
    var hdot = el("circle", { r: 4, class: "chart__dot chart__dot--" + opts.kind });
    hover.appendChild(vline);
    hover.appendChild(hdot);
    svg.appendChild(hover);

    var tip = document.createElement("div");
    tip.className = "chart__tip";
    tip.hidden = true;

    svg.addEventListener("pointermove", function (ev) {
      if (series.length < 2) return;
      var box = svg.getBoundingClientRect();
      var xInView = ((ev.clientX - box.left) / box.width) * W;
      var idx = Math.round(((xInView - M.left) / plotW) * (series.length - 1));
      idx = Math.max(0, Math.min(series.length - 1, idx));
      var p = series[idx];
      var px = sx(idx);
      var py = sy(p.value);
      vline.setAttribute("x1", px);
      vline.setAttribute("x2", px);
      hdot.setAttribute("cx", px);
      hdot.setAttribute("cy", py);
      hover.classList.add("is-on");
      tip.hidden = false;
      tip.textContent = "";
      var dateEl = document.createElement("span");
      dateEl.className = "chart__tip-date";
      dateEl.textContent = fmtDate(p.date);
      var valEl = document.createElement("span");
      valEl.className = "chart__tip-value";
      valEl.textContent = pct(p.value);
      tip.appendChild(dateEl);
      tip.appendChild(valEl);
      // Clamp by the tooltip's own half-width — it is translateX(-50%), so
      // clamping the centre to the box edges hangs it half off the chart.
      var half = tip.offsetWidth / 2;
      var left = (px / W) * box.width;
      tip.style.left = Math.max(half, Math.min(box.width - half, left)) + "px";
    });

    svg.addEventListener("pointerleave", function () {
      hover.classList.remove("is-on");
      tip.hidden = true;
    });

    container.appendChild(svg);
    container.appendChild(tip);
  }

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
      // The shape check above passes strings like "2026-13-45", which parse to
      // an Invalid Date and would render as "Invalid Date" / NaN on the page.
      if (!isFinite(parseDate(o.date).getTime())) {
        throw new Error("observation " + i + " has a non-existent date " + o.date);
      }
      if (!isNum(o.nav) || o.nav <= 0) {
        throw new Error("observation " + i + " has an invalid nav");
      }
    });

    var sorted = observations.slice().sort(function (a, b) {
      return a.date < b.date ? -1 : a.date > b.date ? 1 : 0;
    });
    for (var i = 1; i < sorted.length; i++) {
      if (sorted[i].date === sorted[i - 1].date) {
        throw new Error("duplicate observation date " + sorted[i].date);
      }
    }
    return sorted;
  }

  function renderHero(doc, observations, stats) {
    var inception = parseDate(observations[0].date);
    var latest = parseDate(observations[observations.length - 1].date);
    // Clamp at 1: a viewer whose clock lags inception would otherwise see "0"
    // or negative days on a record that has demonstrably started.
    setText("tr-days", String(Math.max(1, daysBetweenUTC(inception, new Date()) + 1)));
    setText("tr-inception", fmtDate(inception));
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
      var ret = i === 0 ? null : o.nav / observations[i - 1].nav - 1;
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
        { text: typeof o.mode === "string" && o.mode ? o.mode : "—", cls: "" }
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
    hideLoading();
    var fail = document.getElementById("tr-error");
    var empty = document.getElementById("tr-empty");
    var live = document.getElementById("tr-live");
    if (live) live.hidden = true;
    if (empty) empty.hidden = true;
    if (fail) {
      fail.hidden = false;
      fail.textContent = "Could not load the track record data (" + message + ").";
    }
  }

  function render(doc) {
    var observations = normalise(doc);

    if (!observations.length) {
      showEmpty();
      return;
    }

    var periods = doc.periods_per_year || 252;
    var stats = computeStats(observations, periods);

    hideLoading();
    var empty = document.getElementById("tr-empty");
    var live = document.getElementById("tr-live");
    if (empty) empty.hidden = true;
    if (live) live.hidden = false;

    renderHero(doc, observations, stats);
    renderStats(doc, stats);
    renderVerdict(stats);

    var series = buildSeries(doc, observations);

    var eqNode = document.getElementById("tr-chart-equity");
    if (eqNode) {
      drawChart(eqNode, series.equity, {
        kind: "equity",
        boundaries: series.boundaries,
        ariaLabel:
          "Cumulative return since inception: " + pct(stats.cumulative) +
          " over " + stats.n + " observations. Full values are in the table below."
      });
    }

    var ddNode = document.getElementById("tr-chart-drawdown");
    if (ddNode) {
      drawChart(ddNode, series.drawdown, {
        kind: "drawdown",
        height: 180,
        ariaLabel:
          "Drawdown from running peak. Maximum drawdown " + pct(stats.maxDrawdown) +
          ". Full values are in the table below."
      });
    }

    renderTable(observations);
  }

  /* --------------------------------------------------------------- boot -- */

  document.addEventListener("DOMContentLoaded", function () {
    var root = document.getElementById("tr-root");
    if (!root) return;
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

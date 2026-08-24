/* ==========================================================================
   Live out-of-sample track record.

   Reads data/track-record.json and derives every statistic in the browser —
   nothing is precomputed and pasted in, so the page cannot disagree with the
   append-only data file behind it.

   The headline statistic is deliberately NOT the Sharpe ratio. It is the
   Minimum Track Record Length: how long this record would have to run before
   its Sharpe could be distinguished from zero. A short record says so.

   References: Bailey & López de Prado (2012), "The Sharpe Ratio Efficient
   Frontier" — probabilistic Sharpe ratio and minimum track record length.
   ========================================================================== */

(function () {
  "use strict";

  var Z95 = 1.6448536269514722; // one-sided 95%

  /* ---------------------------------------------------------------- math -- */

  // Abramowitz & Stegun 7.1.26 — plenty accurate for a confidence readout.
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

  function normalCdf(x) {
    return 0.5 * (1 + erf(x / Math.SQRT2));
  }

  function mean(xs) {
    var s = 0;
    for (var i = 0; i < xs.length; i++) s += xs[i];
    return s / xs.length;
  }

  // Sample standard deviation (ddof = 1), matching the Sharpe convention.
  function stdev(xs, mu) {
    if (xs.length < 2) return NaN;
    var s = 0;
    for (var i = 0; i < xs.length; i++) s += (xs[i] - mu) * (xs[i] - mu);
    return Math.sqrt(s / (xs.length - 1));
  }

  // Standardised moment of order k. Kurtosis here is raw, so normal => 3.
  function moment(xs, mu, sd, k) {
    var s = 0;
    for (var i = 0; i < xs.length; i++) s += Math.pow((xs[i] - mu) / sd, k);
    return s / xs.length;
  }

  /* --------------------------------------------------------- statistics -- */

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
      costShare: null
    };

    /* Drawdowns work from the first observation. */
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

    /* Cost share of gross P&L. Only meaningful when gross P&L is positive —
       otherwise there is no gross edge for costs to be a share of. */
    var grossTotal = 0;
    var costTotal = 0;
    observations.forEach(function (o) {
      grossTotal += o.gross_pnl || 0;
      costTotal += o.costs || 0;
    });
    out.grossTotal = grossTotal;
    out.costTotal = costTotal;
    if (grossTotal > 0) out.costShare = costTotal / grossTotal;

    if (returns.length < 2) return out;

    var mu = mean(returns);
    var sd = stdev(returns, mu);
    if (!isFinite(sd) || sd <= 0) return out;

    var srPeriod = mu / sd;
    var g3 = moment(returns, mu, sd, 3);
    var g4 = moment(returns, mu, sd, 4);

    out.skew = g3;
    out.kurtosis = g4;
    out.volAnnual = sd * Math.sqrt(periodsPerYear);
    out.sharpeAnnual = srPeriod * Math.sqrt(periodsPerYear);

    // Annualising a return from a handful of days produces a number that is
    // arithmetically correct and practically nonsense, so it is gated.
    if (returns.length >= 20 && out.cumulative > -1) {
      out.returnAnnual =
        Math.pow(1 + out.cumulative, periodsPerYear / returns.length) - 1;
    }

    /* Probabilistic Sharpe Ratio and Minimum Track Record Length, both
       against a benchmark Sharpe of zero. The variance term corrects for
       the non-normality that makes a naive Sharpe optimistic. */
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

  function pct(x, digits) {
    if (x === null || x === undefined || !isFinite(x)) return "—";
    return (x * 100).toFixed(digits === undefined ? 2 : digits) + "%";
  }

  function num(x, digits) {
    if (x === null || x === undefined || !isFinite(x)) return "—";
    return x.toFixed(digits === undefined ? 2 : digits);
  }

  function money(x, currency) {
    if (x === null || x === undefined || !isFinite(x)) return "—";
    try {
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: currency || "USD",
        maximumFractionDigits: 0
      }).format(x);
    } catch (e) {
      return String(Math.round(x));
    }
  }

  function daysBetween(a, b) {
    return Math.round((b - a) / 86400000);
  }

  function parseDate(s) {
    // Parse as UTC so the rendered date never shifts by a day in some zones.
    return new Date(s + "T00:00:00Z");
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

  function niceTicks(min, max, count) {
    var span = max - min;
    if (span <= 0) return [min];
    var raw = span / count;
    var mag = Math.pow(10, Math.floor(Math.log10(raw)));
    var norm = raw / mag;
    var step = (norm >= 5 ? 10 : norm >= 2 ? 5 : norm >= 1 ? 2 : 1) * mag;
    var ticks = [];
    for (var v = Math.ceil(min / step) * step; v <= max + 1e-9; v += step) {
      ticks.push(v);
    }
    return ticks;
  }

  /**
   * One chart. `kind` is "equity" (line + wash, y in % return from inception)
   * or "drawdown" (area hanging from zero).
   */
  function drawChart(container, series, opts) {
    container.textContent = "";

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
    var ticks = niceTicks(lo, hi, 4);
    ticks.forEach(function (t) {
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
      var label = el("text", {
        x: M.left + plotW + 8,
        y: y + 4,
        class: "chart__tick"
      });
      label.textContent = pct(t, 1);
      svg.appendChild(label);
    });

    /* Area wash then line. */
    var linePts = series.map(function (p, i) {
      return sx(i) + "," + sy(p.value);
    });
    // Anchor the wash to zero whenever zero is on screen, so area above the
    // line reads as gain and area below as loss. Falling back to the plot
    // floor would shade losses as though they were gains.
    var zeroInRange = lo <= 0 && hi >= 0;
    var baseline = opts.kind === "drawdown" || zeroInRange ? sy(0) : sy(lo);

    if (series.length > 1) {
      svg.appendChild(
        el("path", {
          d:
            "M" +
            sx(0) +
            "," +
            baseline +
            " L" +
            linePts.join(" L") +
            " L" +
            sx(series.length - 1) +
            "," +
            baseline +
            " Z",
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
          x1: x,
          y1: M.top,
          x2: x,
          y2: M.top + plotH,
          class: "chart__boundary"
        })
      );
      var t = el("text", { x: x + 6, y: M.top + 12, class: "chart__boundary-label" });
      t.textContent = b.label;
      svg.appendChild(t);
    });

    /* Endpoint marker + direct label — the only labelled point. */
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
          x: M.left + plotW,
          y: H - 10,
          class: "chart__tick",
          "text-anchor": "end"
        });
        last.textContent = fmtDate(series[series.length - 1].date);
        svg.appendChild(last);
      }
    }

    /* Hover layer: crosshair + tooltip. Values stay reachable via the table
       view below, so the tooltip enhances rather than gates. */
    var hover = el("g", { class: "chart__hover", "aria-hidden": "true" });
    var vline = el("line", {
      y1: M.top,
      y2: M.top + plotH,
      class: "chart__crosshair"
    });
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
      var ratio = (xInView - M.left) / plotW;
      var idx = Math.round(ratio * (series.length - 1));
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
      tip.innerHTML =
        '<span class="chart__tip-date">' +
        fmtDate(p.date) +
        '</span><span class="chart__tip-value">' +
        pct(p.value) +
        "</span>";
      var left = (px / W) * box.width;
      tip.style.left = Math.max(0, Math.min(box.width - 10, left)) + "px";
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

  function render(doc) {
    var root = document.getElementById("tr-root");
    var observations = doc.observations || [];
    var periods = doc.periods_per_year || 252;

    var empty = document.getElementById("tr-empty");
    var live = document.getElementById("tr-live");

    if (!observations.length) {
      if (empty) empty.hidden = false;
      if (live) live.hidden = true;
      return;
    }

    if (empty) empty.hidden = true;
    if (live) live.hidden = false;

    var stats = computeStats(observations, periods);
    var inception = parseDate(observations[0].date);
    var latest = parseDate(observations[observations.length - 1].date);
    var calendarDays = daysBetween(inception, new Date()) + 1;

    /* Hero: elapsed time, because that is the thing that cannot be faked. */
    setText("tr-days", String(calendarDays));
    setText("tr-inception", fmtDate(inception));
    setText("tr-latest", fmtDate(latest));
    setText("tr-obs", String(stats.n));

    /* Capital mode. */
    var modes = {};
    observations.forEach(function (o) {
      modes[o.mode] = (modes[o.mode] || 0) + 1;
    });
    var modeNode = document.getElementById("tr-mode");
    if (modeNode) {
      var current = observations[observations.length - 1].mode;
      modeNode.textContent =
        current === "live" ? "Real capital" : "Paper — simulated";
      modeNode.className =
        "badge badge--dot " + (current === "live" ? "badge--live" : "badge--active");
    }

    setText("tr-cum", pct(stats.cumulative));
    setText("tr-ann", pct(stats.returnAnnual));
    setText(
      "tr-ann-hint",
      stats.returnAnnual === null
        ? "Withheld under 20 observations"
        : "Geometric, " + periods + "-day basis"
    );
    setText("tr-vol", pct(stats.volAnnual));
    setText("tr-sharpe", num(stats.sharpeAnnual));
    setText("tr-psr", stats.psr === null ? "—" : pct(stats.psr, 1));
    setText("tr-maxdd", pct(stats.maxDrawdown));
    setText("tr-curdd", pct(stats.currentDrawdown));
    setText("tr-skew", num(stats.skew));
    setText("tr-kurt", num(stats.kurtosis));
    setText(
      "tr-costshare",
      stats.costShare === null ? "—" : pct(stats.costShare, 1)
    );
    setText("tr-costs", money(stats.costTotal, doc.base_currency));

    /* The verdict banner. This is the honest headline: whether the record is
       long enough for its Sharpe to mean anything at all. */
    var verdict = document.getElementById("tr-verdict");
    if (verdict) {
      var needed = stats.minTRL === null ? null : Math.ceil(stats.minTRL);
      setText("tr-mintrl", needed === null ? "—" : String(needed));

      var body;
      var tone = "pending";
      if (stats.nReturns < 2) {
        body =
          "Too few observations to compute a Sharpe ratio at all. The record " +
          "needs to run before any performance statistic here is worth reading.";
      } else if (stats.sharpeAnnual === null || stats.sharpeAnnual <= 0) {
        body =
          "The observed Sharpe ratio is at or below zero, so there is nothing " +
          "to distinguish from zero yet. That is reported rather than hidden.";
      } else if (needed !== null && stats.nReturns < needed) {
        body =
          "This track record is too short to be statistically meaningful. Given " +
          "the observed Sharpe, skewness, and kurtosis, distinguishing it from " +
          "zero at 95% confidence would take about " +
          needed +
          " observations. It has " +
          stats.nReturns +
          ". Read the numbers below as provisional.";
      } else {
        tone = "ok";
        body =
          "The observed Sharpe ratio is distinguishable from zero at 95% " +
          "confidence: the record has " +
          stats.nReturns +
          " observations against a minimum of about " +
          needed +
          ". The probabilistic Sharpe ratio is " +
          pct(stats.psr, 1) +
          ".";
      }
      verdict.className = "verdict verdict--" + tone;
      var bodyNode = document.getElementById("tr-verdict-body");
      if (bodyNode) bodyNode.textContent = body;
    }

    /* Charts. Equity is indexed to 0% at inception; drawdown hangs from 0. */
    var base = observations[0].nav;
    var equitySeries = observations.map(function (o) {
      return { date: parseDate(o.date), value: o.nav / base - 1 };
    });

    var peak = observations[0].nav;
    var ddSeries = observations.map(function (o) {
      if (o.nav > peak) peak = o.nav;
      return { date: parseDate(o.date), value: o.nav / peak - 1 };
    });

    var boundaries = [];
    (doc.mode_changes || []).forEach(function (change) {
      for (var i = 0; i < observations.length; i++) {
        if (observations[i].date >= change.date) {
          boundaries.push({ index: i, label: change.to === "live" ? "Real capital" : "Paper" });
          break;
        }
      }
    });

    var eqNode = document.getElementById("tr-chart-equity");
    if (eqNode) {
      drawChart(eqNode, equitySeries, {
        kind: "equity",
        boundaries: boundaries,
        ariaLabel:
          "Cumulative return since inception: " +
          pct(stats.cumulative) +
          " over " +
          stats.n +
          " observations. Full values are in the table below."
      });
    }

    var ddNode = document.getElementById("tr-chart-drawdown");
    if (ddNode) {
      drawChart(ddNode, ddSeries, {
        kind: "drawdown",
        height: 180,
        ariaLabel:
          "Drawdown from running peak. Maximum drawdown " +
          pct(stats.maxDrawdown) +
          ". Full values are in the table below."
      });
    }

    /* Table view — the WCAG-clean twin. Every plotted value is here. */
    var tbody = document.getElementById("tr-tbody");
    if (tbody) {
      var rows = observations
        .map(function (o, i) {
          var ret = i === 0 ? null : o.nav / observations[i - 1].nav - 1;
          var cls = ret === null ? "" : ret >= 0 ? "pos" : "neg";
          return (
            "<tr><td>" +
            o.date +
            '</td><td class="numeric">' +
            o.nav.toFixed(2) +
            '</td><td class="numeric ' +
            cls +
            '">' +
            (ret === null ? "—" : pct(ret)) +
            '</td><td class="numeric">' +
            (o.gross_pnl || 0).toFixed(2) +
            '</td><td class="numeric">' +
            (o.costs || 0).toFixed(2) +
            '</td><td class="numeric">' +
            o.positions +
            "</td><td>" +
            o.mode +
            "</td></tr>"
          );
        })
        .reverse()
        .join("");
      tbody.innerHTML = rows;
    }

    if (root) root.setAttribute("data-state", "loaded");
  }

  /* --------------------------------------------------------------- boot -- */

  document.addEventListener("DOMContentLoaded", function () {
    var root = document.getElementById("tr-root");
    if (!root) return;
    var src = root.getAttribute("data-source") || "/data/track-record.json";

    fetch(src, { cache: "no-cache" })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(render)
      .catch(function (err) {
        var fail = document.getElementById("tr-error");
        if (fail) {
          fail.hidden = false;
          fail.textContent =
            "Could not load the track record data (" + err.message + ").";
        }
        var empty = document.getElementById("tr-empty");
        if (empty) empty.hidden = true;
      });
  });
})();

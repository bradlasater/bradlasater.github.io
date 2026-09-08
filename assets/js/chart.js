/**
 * Dependency-free SVG line charts for this site.
 *
 * Extracted from track-record.js when a second consumer appeared. It draws a
 * series, nothing more: it knows about pixels, ticks and pointers, and nothing
 * about returns, volatility or record kinds. Anything domain-shaped reaches it
 * through `opts` — including the two formatters, because a chart module that
 * hard-codes percentage formatting is not reusable by the next caller that
 * plots something else.
 *
 * Exposed as `window.SiteChart`. Load before any script that calls it.
 */
(function () {
  "use strict";


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
    // Formatting is the caller's, not the chart's. Defaults exist so a bare
    // call still renders something readable rather than "[object Object]".
    var fmtValue = opts.formatValue || function (v) { return String(v); };
    var fmtDateFn = opts.formatDate || function (d) { return String(d); };
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
      var label = fmtValue(t, 1);
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
      first.textContent = fmtDateFn(series[0].date);
      svg.appendChild(first);
      if (series.length > 1) {
        var last = el("text", {
          x: M.left + plotW, y: H - 10,
          class: "chart__tick", "text-anchor": "end"
        });
        last.textContent = fmtDateFn(series[series.length - 1].date);
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
      dateEl.textContent = fmtDateFn(p.date);
      var valEl = document.createElement("span");
      valEl.className = "chart__tip-value";
      valEl.textContent = fmtValue(p.value);
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

  window.SiteChart = { draw: drawChart, el: el, niceTicks: niceTicks };
})();

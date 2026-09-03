/* ==========================================================================
   GoatCounter analytics.

   SETUP (one step): create a free site at https://www.goatcounter.com, then
   put your site code below. The code is the subdomain GoatCounter gives you —
   for "https://bradlasater.goatcounter.com" the code is "bradlasater".

   Until CODE is set this file does nothing, so the site never ships a broken
   or half-configured tracker. Localhost is always excluded.

   No cookies are set and no personal data is collected, so no consent banner
   is required.
   ========================================================================== */

(function () {
  "use strict";

  var CODE = "bradlasater"; // <-- your GoatCounter site code goes here

  if (!CODE) return;

  // Idempotent: a page that includes this file twice must not inject the
  // tracker twice or register the click listener twice (double events).
  if (window.__analyticsLoaded) return;
  window.__analyticsLoaded = true;

  var host = location.hostname;
  if (host === "localhost" || host === "127.0.0.1" || host === "") return;

  // Respect an explicit opt-out (Do Not Track or Global Privacy Control).
  if (navigator.doNotTrack === "1" || window.doNotTrack === "1") return;
  if (navigator.globalPrivacyControl) return;

  var endpoint = "https://" + CODE + ".goatcounter.com/count";

  var script = document.createElement("script");
  script.async = true;
  script.src = "https://gc.zgo.at/count.js";
  script.setAttribute("data-goatcounter", endpoint);
  (document.head || document.documentElement).appendChild(script);

  /* Outbound and contact clicks as events. This is the question that actually
     matters for a job search: did anyone who landed here go on to email, or
     open the GitHub source? */
  document.addEventListener(
    "click",
    function (ev) {
      var link = ev.target && ev.target.closest && ev.target.closest("a[href]");
      if (!link) return;

      var href = link.getAttribute("href") || "";
      var label = null;

      if (href.indexOf("mailto:") === 0) {
        label = "contact-email";
      } else if (/^https?:/i.test(href) && link.hostname !== location.hostname) {
        label = "outbound-" + link.hostname.replace(/^www\./, "");
      }

      if (!label) return;

      // The tracker may be blocked, half-loaded, or replaced by an extension;
      // a failing count call must never surface as an uncaught page error.
      try {
        if (window.goatcounter && typeof window.goatcounter.count === "function") {
          window.goatcounter.count({
            path: label,
            title: link.textContent.trim().slice(0, 80),
            event: true
          });
        }
      } catch (err) {
        /* analytics must never break the page */
      }
    },
    true
  );
})();

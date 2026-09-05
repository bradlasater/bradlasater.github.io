/* ==========================================================================
   404 copy variants.

   The 404 page states the plain fact in markup and never moves it: the
   "Error 404" eyebrow and the "Page not found" headline are static, and no
   id is exposed that could swap them. A visitor with JavaScript off loses
   nothing that tells them where they are or what to do next.

   What this file swaps is the pair below the headline — the figure's caption
   and the body paragraph — as one unit, so the two always read as written
   together. Both elements' literal text in the HTML is the no-JavaScript
   fallback and reads correctly on its own; on load the pair is replaced by
   one of the variants below.

   Rules for editing:
     - A variant is a caption plus the paragraph that follows it. Edit the two
       together: the caption sits under a picture in small centred monospace,
       so keep it to roughly one or two lines, and the paragraph carries the
       rest.
     - Every variant must work with that image, which does not change.
     - Because the headline is never swapped, a variant is free to be oblique.
       The page has already said "Page not found" above it.
     - Every paragraph must still point at the links below it, since that is
       the only thing on the page that gets the visitor somewhere.
     - Text is set with textContent, never innerHTML, so a variant is copy and
       can never inject markup.
   ========================================================================== */

(function () {
  "use strict";

  var VARIANTS = [
    {
      caption: "You won’t know.",
      body: "That URL doesn’t exist. Or maybe it never did. The astronaut above is in a similar position: drifting, unmoored, and definitely not coming back. Try the links below before the blood in your head gets too loud."
    },
    {
      caption: "I am not your friend. I am just a page that knows how to 404.",
      body: "This page is not your friend. It is just a man who knows how to feel… nothing. The astronaut above tried to find what you were looking for. Today’s the day it got tired. Keep the blood in your head and your feet on the ground. The links below are exactly what you need."
    },
    {
      caption: "I’ve got a twenty-dollar bill that says this page is never coming back.",
      body: "That URL doesn’t exist. It faded. It passed. It was glorious once, maybe. The astronaut above is in a similar position: somewhere real, but not where anyone meant to end up. The links below are all that remain."
    }
  ];

  function render() {
    var caption = document.getElementById("error-caption");
    var body = document.getElementById("error-body");

    // Either element missing means this file was included on a page it was
    // not written for. Leave that page's own copy alone.
    if (!caption || !body) return;

    var pickIndex = Math.floor(Math.random() * VARIANTS.length);
    try {
      var previous = parseInt(window.sessionStorage.getItem("error-variant"), 10);
      if (VARIANTS.length > 1 && previous >= 0 && previous < VARIANTS.length) {
        pickIndex = (previous + 1 + Math.floor(Math.random() * (VARIANTS.length - 1))) % VARIANTS.length;
      }
      window.sessionStorage.setItem("error-variant", String(pickIndex));
    } catch (err) {
      /* Storage may be unavailable; keep the independently random fallback. */
    }
    caption.textContent = VARIANTS[pickIndex].caption;
    body.textContent = VARIANTS[pickIndex].body;
  }

  // The script is deferred, so the document is normally already parsed; the
  // readyState check covers the case where it is not.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
})();

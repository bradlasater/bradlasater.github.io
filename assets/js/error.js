/* ==========================================================================
   404 copy variants.

   On load this file replaces the astronaut's caption and the paragraph below
   it with one of the variants below, drawn at random. What ships in the HTML
   is the no-JavaScript fallback and must stay literal and useful on its own.

   Rules for editing:
     - The "Error 404" eyebrow and the "Page not found" headline are never
       swapped. The page states the plain fact above the image whichever
       variant is drawn, and that is what lets a variant be oblique.
     - Every variant must work with the astronaut image it sits under, which
       does not change.
     - The caption sets in small monospace under the image, so keep it to
       about a line; the body is the paragraph below the figure and has room.
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
    var pick = VARIANTS[pickIndex];
    caption.textContent = pick.caption;
    body.textContent = pick.body;
  }

  // The script is deferred, so the document is normally already parsed; the
  // readyState check covers the case where it is not.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
})();

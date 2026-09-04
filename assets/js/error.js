/* ==========================================================================
   404 image caption variants.

   The 404 page states the plain fact in markup and never moves it: the
   "Error 404" eyebrow, the "Page not found" headline, and the body paragraph
   that points at the links are all static. A visitor with JavaScript off
   loses nothing that tells them where they are or what to do next.

   What this file swaps is the figure's caption, and only that. The caption is
   the one place on the page where the copy can have a voice, because the
   astronaut image is already doing something other than wayfinding. The
   caption in the HTML is the no-JavaScript fallback and reads correctly on
   its own; on load it is replaced by one of the variants below.

   Rules for editing:
     - A variant is a caption for the astronaut image, not a headline. It sits
       under a picture in small centred monospace, so keep it to roughly one
       or two lines; a paragraph belongs in the body copy, which is static.
     - Every variant must work with that image, which does not change.
     - Because the headline is no longer swapped, a variant is free to be
       oblique. The page has already said "Page not found" above it.
     - Text is set with textContent, never innerHTML, so a variant is copy and
       can never inject markup.
   ========================================================================== */

(function () {
  "use strict";

  var VARIANTS = [
    "You won’t know.",
    "I am not your friend. I am just a page that knows how to 404.",
    "I’ve got a twenty-dollar bill that says this page is never coming back."
  ];

  function render() {
    var caption = document.getElementById("error-caption");

    // A missing element means this file was included on a page it was not
    // written for. Leave that page's own copy alone.
    if (!caption) return;

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
    caption.textContent = VARIANTS[pickIndex];
  }

  // The script is deferred, so the document is normally already parsed; the
  // readyState check covers the case where it is not.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
})();

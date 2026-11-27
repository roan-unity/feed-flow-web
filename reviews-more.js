/* Previous / next buttons for the review row in the #reviews section (the cards are generated weekly by the reviews job). */
(function () {
  var rail = document.getElementById('reviewRail');
  var prev = document.getElementById('reviewPrev');
  var next = document.getElementById('reviewNext');
  if (!rail || !prev || !next) return;
  function step(direction) {
    rail.scrollBy({ left: direction * Math.max(320, rail.clientWidth * 0.8), behavior: 'smooth' });
  }
  function sync() {
    prev.disabled = rail.scrollLeft <= 2;
    next.disabled = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 2;
  }
  prev.addEventListener('click', function () { step(-1); });
  next.addEventListener('click', function () { step(1); });
  rail.addEventListener('scroll', sync, { passive: true });
  window.addEventListener('resize', sync);
  sync();
})();

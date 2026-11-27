/* "Show more reviews" for the #reviews section (the cards are generated weekly by the reviews job). */
(function () {
  var button = document.getElementById('reviewMoreBtn');
  var more = document.getElementById('reviewMore');
  if (!button || !more) return;
  button.addEventListener('click', function () {
    var open = more.hidden;
    more.hidden = !open;
    button.setAttribute('aria-expanded', open ? 'true' : 'false');
    button.textContent = open ? button.getAttribute('data-less') : button.getAttribute('data-more');
  });
})();

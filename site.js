/* Shared navigation, theme and automatic App Store review localization. */
(function () {
  var root = document.documentElement;
  var themeButton = document.getElementById('themeToggle');
  if (themeButton) {
    themeButton.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      themeButton.setAttribute('aria-label', next === 'dark' ? 'Use light theme' : 'Use dark theme');
      try { localStorage.setItem('ff-web-theme', next); } catch (e) {}
    });
  }

  var menuButton = document.getElementById('menuToggle');
  var mobileNav = document.getElementById('mobileNav');
  if (menuButton && mobileNav) {
    function setMenu(open) {
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      mobileNav.hidden = !open;
      var use = menuButton.querySelector('use');
      if (use) use.setAttribute('href', (open ? '/assets/icons.svg#close' : '/assets/icons.svg#menu'));
    }
    menuButton.addEventListener('click', function () {
      setMenu(menuButton.getAttribute('aria-expanded') !== 'true');
    });
    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () { setMenu(false); });
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        menuButton.focus();
      }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 900) setMenu(false);
    });
  }

  var data = window.FF_REVIEWS;
  var cards = document.querySelectorAll('.review[data-review-index]');
  if (!data || !cards.length) return;

  var supported = Object.keys(data.translations);
  var names = {
    en: 'English', da: 'Dansk', nl: 'Nederlands', fi: 'Suomi', fr: 'Français', de: 'Deutsch',
    it: 'Italiano', nb: 'Norsk (bokmål)', pl: 'Polski', pt: 'Português', es: 'Español', sv: 'Svenska'
  };
  var select = document.getElementById('reviewLanguage');
  var status = document.getElementById('reviewLanguageStatus');
  var storageKey = 'ff-review-language';

  function normalize(tag) {
    var code = String(tag || '').toLowerCase().replace('_', '-').split('-')[0];
    if (code === 'no' || code === 'nn') return 'nb';
    return code;
  }
  function automaticLanguage() {
    var preferred = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || 'en'];
    for (var i = 0; i < preferred.length; i += 1) {
      var code = normalize(preferred[i]);
      if (supported.indexOf(code) !== -1) return code;
    }
    return 'en';
  }
  function storedLanguage() {
    try {
      var value = localStorage.getItem(storageKey);
      return value === 'auto' || supported.indexOf(value) !== -1 ? value : 'auto';
    } catch (e) { return 'auto'; }
  }

  var auto = automaticLanguage();
  var choice = storedLanguage();
  if (select) {
    var autoOption = select.querySelector('option[value="auto"]');
    if (autoOption) autoOption.textContent = 'Automatic (' + names[auto] + ')';
    select.value = choice;
  }

  function renderReviews() {
    var language = choice === 'auto' ? auto : choice;
    cards.forEach(function (card) {
      var index = Number(card.getAttribute('data-review-index'));
      var original = data.originals[index];
      var translated = data.translations[language] && data.translations[language][index];
      var hasTranslation = Boolean(translated);
      var quote = card.querySelector('blockquote');
      var note = card.querySelector('.translate-note');
      var button = card.querySelector('.review-toggle');
      var showingOriginal = false;

      function renderCard() {
        var useOriginal = showingOriginal || !hasTranslation;
        quote.textContent = useOriginal ? original.text : translated;
        quote.setAttribute('lang', useOriginal ? original.language : language);
        note.classList.toggle('visible', !useOriginal && hasTranslation);
        button.hidden = !hasTranslation;
        button.textContent = showingOriginal ? 'View translation' : 'View original';
        button.setAttribute('aria-pressed', showingOriginal ? 'true' : 'false');
        button.setAttribute('aria-label', (showingOriginal ? 'View translation of' : 'View original') + ' review ' + (index + 1));
      }
      button.onclick = function () {
        showingOriginal = !showingOriginal;
        renderCard();
      };
      renderCard();
    });
    if (status) {
      status.textContent = (choice === 'auto' ? 'Automatically showing ' : 'Showing ') + names[language] +
        ' where a translation is available. Every original review remains one tap away.';
    }
  }

  if (select) {
    select.addEventListener('change', function () {
      choice = select.value;
      try { localStorage.setItem(storageKey, choice); } catch (e) {}
      renderReviews();
    });
  }
  renderReviews();
})();

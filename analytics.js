/* Feed Flow! — privacy-first funnel tracking (cookieless, no PII).
 * Pairs with Plausible (loaded in <head>). Captures the campaign source from the
 * landing URL and fires custom events on the conversion clicks: applying for early
 * access, the affiliate link, and (ready for launch) the App Store button.
 * No cookies, no fingerprinting, no personal data — nothing that needs a consent banner. */
(function () {
  // Plausible stub so event calls never error, even before/without the script loading.
  window.plausible = window.plausible || function () {
    (window.plausible.q = window.plausible.q || []).push(arguments);
  };

  // 1) Remember where this visit came from (?utm_source=reddit&utm_campaign=formula-savings).
  try {
    var params = new URLSearchParams(location.search);
    var s = params.get("utm_source") || params.get("ref");
    var c = params.get("utm_campaign");
    if (s) sessionStorage.setItem("ff_src", s);
    if (c) sessionStorage.setItem("ff_camp", c);
  } catch (e) { /* private mode / no storage — degrade quietly */ }

  function source() {
    try { return sessionStorage.getItem("ff_src") || "direct"; } catch (e) { return "direct"; }
  }
  function campaign() {
    try { return sessionStorage.getItem("ff_camp") || ""; } catch (e) { return ""; }
  }

  function withParam(href, key, value) {
    if (href.indexOf(key + "=") !== -1) return href;
    return href + (href.indexOf("?") === -1 ? "?" : "&") + key + "=" + encodeURIComponent(value);
  }

  // 2) Tag the conversion clicks. Capture phase so we run before navigation.
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest ? ev.target.closest("a") : null;
    if (!a) return;
    var href = a.getAttribute("href") || "";

    // Primary conversion: apply for early access (the beta page).
    if (a.classList.contains("btn-primary") || /beta\.html/.test(href)) {
      window.plausible("Beta Apply", { props: { source: source(), campaign: campaign() } });
      // Carry the source into the beta page so a lead's origin is known on the form.
      if (/beta\.html/.test(href)) a.setAttribute("href", withParam(href, "utm_source", source()));
    }

    // Affiliate interest.
    if (/affiliate\.html/.test(href)) {
      window.plausible("Affiliate Click", { props: { source: source() } });
    }

    // App Store (fires once launched + the link exists). Attribution of the actual
    // install is done with an App Store Connect campaign link — see ANALYTICS.md.
    if (/apps\.apple\.com/.test(href)) {
      window.plausible("AppStore Click", { props: { source: source(), campaign: campaign() } });
    }
  }, true);
})();

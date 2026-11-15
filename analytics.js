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

  // No tag? Name the referring site (search engine, AI assistant, social app) so website downloads can be
  // split by origin in App Store Connect (2026-11-15). Host name only, nothing personal.
  var REFERRERS = [
    [/(^|\.)chatgpt\.com$|(^|\.)openai\.com$/, "chatgpt"], [/perplexity\.ai$/, "perplexity"], [/(^|\.)claude\.ai$/, "claude"],
    [/gemini\.google\.com$/, "gemini"], [/copilot\.microsoft\.com$/, "copilot"], [/(^|\.)google\./, "google"],
    [/(^|\.)bing\.com$/, "bing"], [/duckduckgo\.com$/, "duckduckgo"], [/instagram\.com$/, "instagram"],
    [/facebook\.com$|fb\.me$/, "facebook"], [/tiktok\.com$/, "tiktok"], [/youtube\.com$|youtu\.be$/, "youtube"],
    [/reddit\.com$/, "reddit"], [/linkedin\.com$|lnkd\.in$/, "linkedin"], [/^t\.co$|(^|\.)x\.com$/, "x"],
    [/pinterest\./, "pinterest"], [/linktr\.ee$/, "linktree"]
  ];
  try {
    if (!sessionStorage.getItem("ff_src") && document.referrer) {
      var host = new URL(document.referrer).hostname.replace(/^www\./, "");
      if (host && host !== location.hostname.replace(/^www\./, "")) {
        var hit = REFERRERS.filter(function (r) { return r[0].test(host); })[0];
        sessionStorage.setItem("ff_src", hit ? hit[1] : "ref-" + host.split(".").slice(-2, -1)[0]);
      }
    }
  } catch (e) { /* no storage or bad referrer: stay "direct" */ }

  function source() {
    try { return sessionStorage.getItem("ff_src") || "direct"; } catch (e) { return "direct"; }
  }

  // App Store campaign token: "web-<source>" (Apple allows up to 40 characters).
  function storeToken() {
    return ("web-" + source()).toLowerCase().replace(/[^a-z0-9_-]/g, "").slice(0, 40);
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

    // Primary conversion on the retired beta page only. App Store buttons are
    // tracked separately below and must not also fire the stale beta event.
    if (/beta\.html/.test(href)) {
      window.plausible("Beta Apply", { props: { source: source(), campaign: campaign() } });
      // Carry the source into the beta page so a lead's origin is known on the form.
      a.setAttribute("href", withParam(href, "utm_source", source()));
    }

    // Affiliate interest.
    if (/affiliate\.html/.test(href)) {
      window.plausible("Affiliate Click", { props: { source: source() } });
    }

    // LinkedIn outbound clicks, with placement but no personal data.
    if (/linkedin\.com/.test(href)) {
      window.plausible("LinkedIn Click", { props: { source: source(), campaign: campaign(), placement: a.getAttribute("data-placement") || "footer" } });
    }

    // App Store (fires once launched + the link exists). Attribution of the actual
    // install is done with an App Store Connect campaign link — see ANALYTICS.md.
    if (/apps\.apple\.com/.test(href)) {
      window.plausible("AppStore Click", { props: { source: source(), campaign: campaign() } });
      // Downloads (not reviews) carry the visitor's origin into App Store Connect's campaign report.
      if (/[?&]ct=/.test(href) && !/write-review/.test(href)) {
        a.setAttribute("href", href.replace(/([?&]ct=)[^&]*/, "$1" + storeToken()));
      }
    }
  }, true);
})();

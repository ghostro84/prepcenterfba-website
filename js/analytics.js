/**
 * js/analytics.js — Einwilligungsgesteuertes Tracking.
 *
 * Standard: KEIN Tracking. Erst wenn im Cookie-Banner „Alle akzeptieren"
 * geklickt wurde (localStorage ph_cookie_consent === "all"), wird das
 * konfigurierte Analyse-Skript nachgeladen. Ohne Einwilligung wird kein
 * Drittanbieter-Request ausgelöst – das ist die Voraussetzung dafür, dass
 * die Angaben in der Datenschutzerklärung stimmen (§ 25 TDDG / Art. 6 DSGVO).
 *
 * ►►► EINRICHTEN:
 *   1. PROVIDER auf "ga4", "plausible" oder "none" setzen.
 *   2. Die passende ID bzw. Domain eintragen.
 *   3. Bei GA4 zusätzlich in der Datenschutzerklärung den Abschnitt
 *      „Webanalyse" ergänzen (Anbieter, Zweck, Speicherdauer, Drittlandtransfer).
 *      Plausible ist datenschutzfreundlicher: keine Cookies, EU-Hosting,
 *      keine personenbezogenen Daten – dann genügt ein kurzer Hinweis.
 */
(function (global) {
  "use strict";

  var PROVIDER = "none";              // "none" | "ga4" | "plausible"
  var GA4_ID   = "G-XXXXXXXXXX";      // nur bei PROVIDER === "ga4"
  var PLAUSIBLE_DOMAIN = "prepcenterfba.eu";

  var CONSENT_KEY = "ph_cookie_consent";

  function hasConsent() {
    try { return localStorage.getItem(CONSENT_KEY) === "all"; } catch (_) { return false; }
  }

  function loadScript(src, attrs) {
    var s = document.createElement("script");
    s.async = true;
    s.src = src;
    Object.keys(attrs || {}).forEach(function (k) { s.setAttribute(k, attrs[k]); });
    document.head.appendChild(s);
    return s;
  }

  var loaded = false;
  function start() {
    if (loaded || PROVIDER === "none" || !hasConsent()) return;
    loaded = true;

    if (PROVIDER === "ga4") {
      loadScript("https://www.googletagmanager.com/gtag/js?id=" + GA4_ID);
      global.dataLayer = global.dataLayer || [];
      function gtag() { global.dataLayer.push(arguments); }
      global.gtag = gtag;
      gtag("js", new Date());
      gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied",
                                   ad_personalization: "denied", analytics_storage: "granted" });
      gtag("config", GA4_ID, { anonymize_ip: true });
    } else if (PROVIDER === "plausible") {
      loadScript("https://plausible.io/js/script.js", { "data-domain": PLAUSIBLE_DOMAIN });
    }
  }

  // Beim Laden prüfen …
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
  // … und erneut, sobald der Nutzer im Banner zustimmt.
  global.addEventListener("ph:consent", start);

  global.PH_ANALYTICS = { start: start, hasConsent: hasConsent, provider: PROVIDER };

}(typeof window !== "undefined" ? window : this));

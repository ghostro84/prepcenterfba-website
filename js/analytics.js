/**
 * js/analytics.js — Einwilligungsgesteuertes Tracking.
 *
 * ►►► DIESE DATEI IST DERZEIT NICHT EINGEBUNDEN.
 *
 * Die Website setzt aktuell KEIN Tracking ein (PROVIDER = "none") und zeigt
 * deshalb bewusst auch kein Cookie-Banner: Es werden ausschließlich technisch
 * notwendige localStorage-Schlüssel verwendet, für die nach § 25 Abs. 2 TDDDG
 * keine Einwilligung erforderlich ist. Ein Banner, das eine Einwilligung für
 * eine nicht stattfindende Verarbeitung einholt, wäre eine unrichtige Angabe.
 *
 * ►►► VOR AKTIVIERUNG VON ANALYTICS SIND DREI SCHRITTE NÖTIG:
 *   1. PROVIDER auf "plausible" (empfohlen: EU-Hosting, cookiefrei) oder
 *      "ga4" setzen und die passende ID bzw. Domain eintragen.
 *   2. Ein Consent-Banner wieder einbauen, das localStorage["ph_cookie_consent"]
 *      auf "all" setzt und das Event "ph:consent" auslöst — mit gleichwertigem
 *      Ablehnen-Button und einem jederzeit erreichbaren Widerrufslink.
 *   3. Diese Datei auf allen Seiten wieder als <script defer> einbinden und
 *      die Datenschutzerklärung um den Abschnitt „Webanalyse" ergänzen
 *      (Anbieter, Zweck, Speicherdauer, Drittlandtransfer).
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

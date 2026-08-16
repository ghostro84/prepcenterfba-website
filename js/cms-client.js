/**
 * cms-client.js — PrepCenter FBA CMS runtime
 * Fetches content overrides from the CMS API and applies them to the DOM.
 * Visual click-to-edit mode activates when ?cms_mode=1 is in the URL.
 */
(function () {
  "use strict";

  var API_BASE = (window.PH_CONFIG && window.PH_CONFIG.CMS_API_BASE) || "";

  /* ── Apply content overrides ─────────────────────────────────────────── */
  function applyText(key, value) {
    document.querySelectorAll('[data-i18n="' + key + '"], [data-cms="' + key + '"]').forEach(function (el) {
      el.textContent = value;
    });
  }

  function applyImage(key, value) {
    document.querySelectorAll('[data-cms-img="' + key + '"], img[data-cms="' + key + '"]').forEach(function (el) {
      el.src = value;
    });
    document.querySelectorAll('[data-cms-bg="' + key + '"]').forEach(function (el) {
      el.style.backgroundImage = "url(" + value + ")";
    });
  }

  function applyBrandOverrides(contentMap) {
    var mapping = {
      "brand.name":   function (v) { window.PH_CONFIG.BRAND.name  = v; },
      "brand.email":  function (v) { window.PH_CONFIG.BRAND.email = v; },
      "brand.phone":  function (v) { window.PH_CONFIG.BRAND.phone = v; },
      "brand.street": function (v) { window.PH_CONFIG.BRAND.street = v; },
      "brand.zip":    function (v) { window.PH_CONFIG.BRAND.zip   = v; },
      "brand.city":   function (v) { window.PH_CONFIG.BRAND.city  = v; },
      "brand.vatId":  function (v) { window.PH_CONFIG.BRAND.vatId = v; },
    };
    var hasBrand = false;
    Object.keys(mapping).forEach(function (key) {
      if (contentMap[key]) { mapping[key](contentMap[key].value); hasBrand = true; }
    });
    if (hasBrand && window.PH && window.PH.injectChrome) window.PH.injectChrome();
  }

  function applyPriceOverrides(contentMap) {
    var hasPrices = false;
    Object.keys(contentMap).forEach(function (key) {
      if (key.indexOf("price.") === 0 && contentMap[key].type === "price") {
        var priceKey = key.slice(6); // remove "price." prefix
        var val = parseFloat(contentMap[key].value);
        if (!isNaN(val) && window.PH_CONFIG && window.PH_CONFIG.DEFAULT_PRICES) {
          window.PH_CONFIG.DEFAULT_PRICES.forEach(function (p) {
            if (p.key === priceKey) { p.price = val; hasPrices = true; }
          });
        }
      }
    });
    if (hasPrices && window.PH) {
      if (window.PH.renderPriceTables) window.PH.renderPriceTables();
      if (window.PH.renderPriceCards)  window.PH.renderPriceCards();
    }
  }

  function applyAll(contentMap) {
    Object.keys(contentMap).forEach(function (key) {
      var entry = contentMap[key];
      if (entry.type === "image") {
        applyImage(key, entry.value);
      } else if (key.indexOf("brand.") !== 0 && key.indexOf("price.") !== 0) {
        applyText(key, entry.value);
      }
    });
    applyBrandOverrides(contentMap);
    applyPriceOverrides(contentMap);
  }

  /* ── Visual click-to-edit mode ────────────────────────────────────────── */
  function activateCmsMode(contentMap) {
    var style = document.createElement("style");
    style.textContent = [
      "[data-i18n]:hover, [data-cms]:hover, [data-cms-img]:hover, [data-cms-bg]:hover {",
      "  outline: 2px dashed #2563eb !important;",
      "  outline-offset: 2px;",
      "  cursor: pointer !important;",
      "}",
      "[data-i18n]:hover::before { content: attr(data-i18n); font-size:10px; background:#2563eb; color:#fff; padding:1px 4px; border-radius:2px; position:fixed; top:4px; left:50%; transform:translateX(-50%); z-index:99999; }"
    ].join("\n");
    document.head.appendChild(style);

    function addHandler(el, key, type) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        var value = type === "image" ? (el.src || "") : (el.textContent || "");
        window.parent.postMessage({ type: "cms-select", key: key, value: value, cmsType: type }, "*");
      });
    }

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      addHandler(el, el.getAttribute("data-i18n"), "text");
    });
    document.querySelectorAll("[data-cms]").forEach(function (el) {
      addHandler(el, el.getAttribute("data-cms"), el.getAttribute("data-cms-type") || "text");
    });
    document.querySelectorAll("[data-cms-img]").forEach(function (el) {
      addHandler(el, el.getAttribute("data-cms-img"), "image");
    });
    document.querySelectorAll("[data-cms-bg]").forEach(function (el) {
      addHandler(el, el.getAttribute("data-cms-bg"), "image");
    });

    window.parent.postMessage({ type: "cms-ready" }, "*");
  }

  /* ── Init ─────────────────────────────────────────────────────────────── */
  async function init() {
    // Skip entirely when the CMS is disabled (static hosting without the API
    // server) — unless edit mode is explicitly requested via ?cms_mode=1.
    var cmsRequested = new URLSearchParams(window.location.search).get("cms_mode") === "1";
    var cmsEnabled = !!(window.PH_CONFIG && window.PH_CONFIG.CMS_ENABLED);
    if (!cmsEnabled && !cmsRequested) return;
    try {
      var url = API_BASE + "/api/cms/content";
      var res = await fetch(url, { cache: "no-store" });
      if (!res.ok) return;
      var data = await res.json();
      applyAll(data);
      if (new URLSearchParams(window.location.search).get("cms_mode") === "1") {
        activateCmsMode(data);
      }
    } catch (e) { /* silent fallback */ }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

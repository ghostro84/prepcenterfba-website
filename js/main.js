/**
 * js/main.js — PrepHub Germany core runtime.
 *
 * Responsibilities:
 *  - PH.esc(str)           safe HTML escaping
 *  - Header/footer injection into #site-header / #site-footer
 *  - Active nav detection
 *  - Mobile burger menu
 *  - renderPriceTables()   renders [data-price-table] elements
 *  - Calculator engine     (#calculator)
 *  - Cookie banner         (#cookie-banner)
 *  - Language selector
 */
(function (global) {
  "use strict";

  /* ── Helpers ──────────────────────────────────────────────────────────── */
  function esc(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  /* ── Header template ──────────────────────────────────────────────────── */
  function buildHeader() {
    var b = PH_CONFIG.BRAND;
    var pages = [
      { href: "./index.html",      label: "Startseite",  key: "nav.home"       },
      { href: "./services.html",   label: "Leistungen",  key: "nav.services"   },
      { href: "./pricing.html",    label: "Preise",      key: "nav.pricing"    },
      { href: "./kalkulator.html", label: "Kalkulator",  key: "nav.calculator" },
    ];

    var navLinks = pages.map(function (p) {
      return '<a href="' + esc(p.href) + '" class="nav-link" data-i18n="' + esc(p.key) + '">' + esc(p.label) + '</a>';
    }).join("");

    var waIcon = '<svg width="18" height="18" viewBox="0 0 32 32" aria-hidden="true"><path fill="#fff" d="M16 4a12 12 0 0 0-10.4 18l-1.5 5.4a1 1 0 0 0 1.2 1.2l5.5-1.4A12 12 0 1 0 16 4Zm0 2a10 10 0 1 1-5 18.7 1 1 0 0 0-.8-.1l-3.7 1 1-3.6a1 1 0 0 0-.1-.8A10 10 0 0 1 16 6Zm-3.6 4.9c-.3 0-.7.1-1 .5-.3.3-1.1 1.1-1.1 2.6s1.1 3 1.3 3.2c.2.2 2.2 3.5 5.4 4.8 2.7 1.1 3.2.9 3.8.8.6-.1 1.9-.8 2.2-1.6.3-.8.3-1.4.2-1.6-.1-.2-.3-.3-.7-.5l-2.4-1.1c-.3-.1-.6-.2-.8.1l-1 1.3c-.2.2-.4.3-.7.1a8.6 8.6 0 0 1-2.5-1.6 9.5 9.5 0 0 1-1.8-2.2c-.2-.3 0-.5.1-.7l.6-.7c.2-.2.2-.4.3-.6.1-.2 0-.5 0-.7l-1-2.5c-.3-.7-.6-.6-.9-.6h-.7Z"/></svg>';
    var wa = PH_CONFIG.WHATSAPP || {};
    var waHref = wa.number
      ? "https://wa.me/" + encodeURIComponent(wa.number) + (wa.message ? "?text=" + encodeURIComponent(wa.message) : "")
      : "";
    var waHeaderBtn = waHref
      ? '      <a href="' + waHref + '" class="btn-wa-header" target="_blank" rel="noopener" aria-label="WhatsApp">' + waIcon + 'WhatsApp</a>'
      : "";
    var waMobileBtn = waHref
      ? '    <a href="' + waHref + '" class="btn-wa-header" target="_blank" rel="noopener" style="justify-content:center">' + waIcon + 'WhatsApp</a>'
      : "";

    return [
      '<header class="site-header" id="site-header" role="banner">',
      '  <style>',
      '    .header-row1{display:flex;align-items:center;gap:1.5rem;padding:8px 0 0}',
      '    .header-slogan{flex:1;min-width:0;overflow:hidden;text-align:center;white-space:nowrap;font-size:clamp(1rem,2.2vw,1.9rem);font-style:italic;font-weight:600;color:#475569;line-height:1.2}',
      '    .header-slogan b{color:#f4721e;font-style:normal}',
      '    .logo-img--header{height:172px;width:auto;display:block}',
      '    .header-row2{display:flex;align-items:center;justify-content:center;gap:1.25rem;padding:0 0 12px;flex-wrap:wrap}',
      '    .header-row2 .main-nav{flex:none;gap:.5rem}',
      '    .header-row2 .nav-link{font-size:1.2rem;font-weight:600;padding:.45rem .9rem}',
      '    .header-row2 .header-actions{margin-left:0}',
      '    .btn-wa-header{display:inline-flex;align-items:center;gap:.45rem;background:#25d366;color:#fff;font-weight:600;border-radius:999px;padding:.5rem 1rem;font-size:.9rem;text-decoration:none;transition:filter .15s}',
      '    .btn-wa-header:hover{filter:brightness(1.07);color:#fff}',
      '    .header-row1 .burger{margin-left:auto}',
      '    @media(max-width:1100px){.logo-img--header{height:120px}}',
      '    @media(max-width:900px){.header-slogan{display:none}}',
      '    @media(max-width:767px){.logo-img--header{height:96px}.header-row2{display:none}.header-row1{padding:8px 0}}',
      '  </style>',
      '  <div class="container header-row1">',
      '    <a href="./index.html" class="logo" aria-label="' + esc(b.name) + ' – Startseite" style="display:flex;align-items:center;text-decoration:none">',
      '      <img src="./img/logo-full.png" class="logo-img logo-img--header" alt="PrepCenter Germany FBA">',
      '    </a>',
      '    <span class="header-slogan" aria-hidden="false">Built on <b>Trust</b>. Defined by <b>Integrity</b>. Backed by <b>Quality</b>.</span>',
      '    <button class="burger" id="burger" aria-label="Menü öffnen" aria-expanded="false" aria-controls="main-nav-mobile">',
      '      <span></span><span></span><span></span>',
      '    </button>',
      '  </div>',
      '  <div class="container header-row2">',
      '    <nav class="main-nav" role="navigation" aria-label="Hauptnavigation">',
      '      ' + navLinks,
      '    </nav>',
      '    <div class="header-actions">',
      '      <div class="lang-dropdown" role="navigation" aria-label="Sprachauswahl">',
      '        <button class="lang-btn" aria-haspopup="listbox" aria-expanded="false" id="lang-btn" aria-label="Sprache wählen">',
      '          <span class="lang-current" id="lang-current">DE</span>',
      '          <svg width="10" height="6" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round"/></svg>',
      '        </button>',
      '        <ul class="lang-menu" role="listbox" id="lang-menu" aria-label="Sprachen">',
      '          <li role="option" data-lang="de" class="lang-option lang-option--active">DE – Deutsch</li>',
      '          <li role="option" data-lang="en" class="lang-option">EN – English</li>',
      '          <li role="option" data-lang="it" class="lang-option">IT – Italiano</li>',
      '          <li role="option" data-lang="fr" class="lang-option">FR – Français</li>',
      '        </ul>',
      '      </div>',
      '      <a href="#contact" class="btn btn--primary btn--sm" data-i18n="nav.cta">Jetzt anfragen</a>',
      waHeaderBtn,
      '    </div>',
      '  </div>',
      '  <nav class="mobile-nav" id="main-nav-mobile" aria-label="Mobile Navigation" hidden>',
      '    ' + navLinks,
      '    <a href="#contact" class="btn btn--primary" data-i18n="nav.cta">Jetzt anfragen</a>',
      waMobileBtn,
      '  </nav>',
      '</header>',
    ].join("\n");
  }

  /* ── Footer template ──────────────────────────────────────────────────── */
  function buildFooter() {
    var b = PH_CONFIG.BRAND;
    var year = new Date().getFullYear();
    return [
      '<footer class="site-footer" id="site-footer" role="contentinfo">',
      '  <div class="container footer-grid">',
      '    <div class="footer-col footer-col--brand">',
      '      <div class="logo logo--light" style="display:inline-block;background:#fff;border-radius:12px;padding:10px 14px">',
      '        <img src="./img/logo-full.png" class="logo-img" alt="PrepCenter Germany FBA" style="height:88px;width:auto;display:block;filter:none">',
      '      </div>',
      '      <p data-i18n="footer.tagline">Ihr zuverlässiger FBA Prep Partner in Deutschland. Schnell, transparent, zertifiziert.</p>',
      '      <address>',
      '        <span data-i18n="footer.address">' + esc(b.street) + ', ' + esc(b.zip) + ' ' + esc(b.city) + '</span><br>',
      '        <a href="mailto:' + esc(b.email) + '">' + esc(b.email) + '</a><br>',
      '        <a href="tel:' + esc(b.phone.replace(/\s/g, "")) + '">' + esc(b.phone) + '</a>',
      '        ' + (PH_CONFIG.WHATSAPP && PH_CONFIG.WHATSAPP.number
        ? '<br><a href="https://wa.me/' + esc(PH_CONFIG.WHATSAPP.number) + '?text=' + encodeURIComponent(PH_CONFIG.WHATSAPP.message || "") + '" target="_blank" rel="noopener" style="color:#25D366;font-weight:600" data-i18n="wa.footer">WhatsApp Chat</a>'
        : ''),
      '      </address>',
      '    </div>',
      '    <div class="footer-col">',
      '      <h3 data-i18n="footer.nav.title">Navigation</h3>',
      '      <ul>',
      '        <li><a href="./index.html" data-i18n="nav.home">Startseite</a></li>',
      '        <li><a href="./services.html" data-i18n="nav.services">Leistungen</a></li>',
      '        <li><a href="./pricing.html" data-i18n="nav.pricing">Preise</a></li>',
      '        <li><a href="./kalkulator.html" data-i18n="nav.calculator">Kalkulator</a></li>',
      '      </ul>',
      '    </div>',
      '    <div class="footer-col">',
      '      <h3 data-i18n="footer.services.title">Leistungen</h3>',
      '      <ul>',
      '        <li><a href="./services.html#receiving" data-i18n="service.receiving">Wareneingang</a></li>',
      '        <li><a href="./services.html#inspection" data-i18n="service.inspection">Qualitätskontrolle</a></li>',
      '        <li><a href="./services.html#labeling" data-i18n="service.labeling">FNSKU-Etikettierung</a></li>',
      '        <li><a href="./services.html#packaging" data-i18n="service.packaging">Verpackung &amp; Prep</a></li>',
      '        <li><a href="./services.html#bundling" data-i18n="service.bundling">Bundling</a></li>',
      '        <li><a href="./services.html#forwarding" data-i18n="service.forwarding">Einlieferung FBA</a></li>',
      '      </ul>',
      '    </div>',
      '    <div class="footer-col">',
      '      <h3 data-i18n="footer.legal.title">Rechtliches</h3>',
      '      <ul>',
      '        <li><a href="./impressum.html" data-i18n="footer.legal.imprint">Impressum</a></li>',
      '        <li><a href="./datenschutz.html" data-i18n="footer.legal.privacy">Datenschutzerklärung</a></li>',
      '        <li><a href="./agb.html" data-i18n="footer.legal.terms">AGB</a></li>',
      '      </ul>',
      '      <p class="vat-note" data-i18n="footer.vat">Alle Preise netto zzgl. gesetzlicher USt. · USt-ID: ' + esc(b.vatId) + '</p>',
      '    </div>',
      '  </div>',
      '  <div class="footer-bottom">',
      '    <div class="container">',
      '      <span>&copy; ' + year + ' ' + esc((b.legalName || b.name) + (b.legalForm ? " " + b.legalForm : "")) + ' · ' + esc(b.country) + '</span>',
      '    </div>',
      '  </div>',
      '</footer>',
    ].join("\n");
  }

  /* ── Inject header & footer ───────────────────────────────────────────── */
  // Idempotent: the injected <header>/<footer> keep the mount ids, so the
  // chrome can be re-rendered (e.g. after CMS brand overrides load).
  function injectChrome() {
    var headerMount = document.getElementById("site-header");
    var footerMount = document.getElementById("site-footer");
    if (headerMount) headerMount.outerHTML = buildHeader();
    if (footerMount) footerMount.outerHTML = buildFooter();
  }

  /* Full chrome refresh: re-inject AND re-bind all listeners + i18n.
     This is what external callers (cms-client.js) should use. */
  function refreshChrome() {
    injectChrome();
    markActiveNav();
    initBurger();
    initLangSelector();
    if (global.PH_I18N) PH_I18N.apply();
  }

  /* ── Active nav ────────────────────────────────────────────────────────── */
  function markActiveNav() {
    var path = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".nav-link").forEach(function (a) {
      var href = a.getAttribute("href").split("/").pop() || "index.html";
      if (href === path) {
        a.classList.add("nav-link--active");
        a.setAttribute("aria-current", "page");
      }
    });
  }

  /* ── Mobile burger ─────────────────────────────────────────────────────── */
  function initBurger() {
    var burger = document.getElementById("burger");
    var mobileNav = document.getElementById("main-nav-mobile");
    if (!burger || !mobileNav) return;
    burger.addEventListener("click", function () {
      var open = mobileNav.hidden === false;
      mobileNav.hidden = open;
      burger.setAttribute("aria-expanded", String(!open));
      burger.setAttribute("aria-label", open ? "Menü öffnen" : "Menü schließen");
    });
  }

  /* ── Language selector ─────────────────────────────────────────────────── */
  function initLangSelector() {
    var btn   = document.getElementById("lang-btn");
    var menu  = document.getElementById("lang-menu");
    var label = document.getElementById("lang-current");
    if (!btn || !menu) return;

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = menu.classList.toggle("lang-menu--open");
      btn.setAttribute("aria-expanded", String(open));
    });

    menu.querySelectorAll(".lang-option").forEach(function (opt) {
      opt.addEventListener("click", function () {
        var code = opt.getAttribute("data-lang");
        PH_I18N.setLang(code);
        renderPriceTables();
        renderPriceCards();
        if (label) label.textContent = code.toUpperCase();
        menu.querySelectorAll(".lang-option").forEach(function (o) {
          o.classList.toggle("lang-option--active", o === opt);
        });
        menu.classList.remove("lang-menu--open");
        btn.setAttribute("aria-expanded", "false");
      });
    });

    document.addEventListener("click", function () {
      menu.classList.remove("lang-menu--open");
      btn.setAttribute("aria-expanded", "false");
    });

    // Reflect stored language
    var cur = PH_I18N.getLang().toUpperCase();
    if (label) label.textContent = cur;
    menu.querySelectorAll(".lang-option").forEach(function (o) {
      o.classList.toggle("lang-option--active", o.getAttribute("data-lang") === PH_I18N.getLang());
    });
  }

  /* ── Price tables ──────────────────────────────────────────────────────── */
  // Exposed for CMS re-render after price overrides load
  function renderPriceTables() {
    var prices = PH_CONFIG.getPrices();
    // i18n helpers with German fallbacks
    function ti(key, fallback) { var v = PH_I18N.t(key); return (v === key) ? fallback : v; }
    var colSvc   = ti("price.col.service", "Leistung");
    var colUnit  = ti("price.col.unit",    "Einheit");
    var colPrice = ti("price.col.price",   "Preis (netto)");
    var freeStr  = ti("price.free",        "Kostenlos");

    document.querySelectorAll("[data-price-table]").forEach(function (container) {
      var group = container.getAttribute("data-price-table");
      var rows  = prices.filter(function (p) { return p.group === group; });
      if (!rows.length) return;

      var html = [
        '<table class="price-table" aria-label="' + esc(colSvc) + ' – ' + esc(group) + '">',
        '<thead><tr>',
        '  <th scope="col">' + colSvc + '</th>',
        '  <th scope="col">' + colUnit + '</th>',
        '  <th scope="col" class="text-right">' + colPrice + '</th>',
        '</tr></thead>',
        '<tbody>',
      ];
      rows.forEach(function (p) {
        // Format price: show translated "Kostenlos" for zero entries
        var priceStr = (p.price === 0) ? freeStr : PH_CONFIG.fmtEUR(p.price);
        // Translated label / unit / note / desc with German fallbacks from config
        var tLabel = ti("price.label." + p.key, p.label);
        var tUnit  = ti("price.unit."  + p.key, p.unit);
        var tNote  = ti("price.note."  + p.key, p.note || "");
        var tDesc  = ti("price.desc."  + p.key, p.desc || "");
        // Build label cell
        var labelCell = esc(tLabel);
        if (tDesc) labelCell += '<br><small class="price-table__desc">' + esc(tDesc) + '</small>';
        if (tNote) labelCell += '<br><small class="price-table__note">' + esc(tNote) + '</small>';
        html.push(
          '<tr' + (p.price === 0 ? ' class="price-row--free"' : '') + '>',
          '  <td>' + labelCell + '</td>',
          '  <td class="unit-cell">' + esc(tUnit) + '</td>',
          '  <td class="price-cell' + (p.price === 0 ? ' price-cell--free' : '') + '">' + esc(priceStr) + '</td>',
          '</tr>'
        );
      });
      html.push('</tbody></table>');
      container.innerHTML = html.join("\n");
    });
  }

  /* ── Pricing preview cards on index ───────────────────────────────────── */
  function renderPriceCards() {
    var container = document.getElementById("price-cards");
    if (!container) return;
    var prices = PH_CONFIG.getPrices();

    // i18n helper with German fallback (same pattern as renderPriceTables)
    function ti(key, fallback) { var v = PH_I18N.t(key); return (v === key) ? fallback : v; }

    var highlights = [
      { key: "fnsku",      icon: "🏷" },
      { key: "fba_prep",   icon: "⚡" },
      { key: "polybag",    icon: "🛡" },
      { key: "inspection", icon: "🔍" },
    ];

    var html = highlights.map(function (h) {
      var p = prices.find(function (x) { return x.key === h.key; });
      if (!p) return "";
      var tLabel = ti("price.label." + p.key, p.label);
      var tUnit  = ti("price.unit."  + p.key, p.unit);
      return [
        '<div class="price-card">',
        '  <div class="price-card__icon" aria-hidden="true">' + h.icon + '</div>',
        '  <div class="price-card__label">' + esc(tLabel) + '</div>',
        '  <div class="price-card__price">' + esc(PH_CONFIG.fmtEUR(p.price)) + '</div>',
        '  <div class="price-card__note">' + esc(tUnit) + '</div>',
        '</div>',
      ].join("\n");
    }).join("");

    container.innerHTML = html;
  }

  /* ── Calculator ────────────────────────────────────────────────────────── */
  function initCalculator() {
    var calc = document.getElementById("calculator");
    if (!calc) return;

    var prices = PH_CONFIG.getPrices();
    function price(key) {
      var p = prices.find(function (x) { return x.key === key; });
      return p ? p.price : 0;
    }

    function val(id) {
      var el = document.getElementById(id);
      return el ? (parseFloat(el.value) || 0) : 0;
    }
    function checked(id) {
      var el = document.getElementById(id);
      return el ? el.checked : false;
    }

    function update() {
      var units    = val("calc-units");
      var cartons  = val("calc-cartons");
      var pallets  = val("calc-pallets");
      var sPallets = val("calc-storage-pallets");
      var sMths    = val("calc-storage-months");

      var receiving = cartons * price("recv_carton") + pallets * price("recv_pallet");

      var prepCost = 0;
      if (checked("calc-fnsku"))      prepCost += units * price("fnsku");
      if (checked("calc-inspection")) prepCost += units * price("inspection");
      if (checked("calc-polybag"))    prepCost += units * price("polybag");
      if (checked("calc-bubblewrap")) prepCost += units * price("bubblewrap");
      if (checked("calc-repack"))     prepCost += units * price("repack");
      // Bundling is priced per SET, not per unit — use the dedicated set count
      var bundles = val("calc-bundles");
      prepCost += bundles * price("bundling");

      var storage  = sPallets * sMths * price("storage_pallet");

      // Discount: volume tiers (if configured) + new-customer discount select
      var discount = PH_CONFIG.getVolumeDiscount(units);
      var ncSel = document.getElementById("calc-newcustomer");
      var ncRate = ncSel ? (parseFloat(ncSel.value) || 0) : 0;
      discount = Math.min(discount + ncRate, 0.9);

      var prepNet  = prepCost * (1 - discount);
      var minFee   = price("min_order");

      // if total is below min fee, add the difference
      var subTotal = receiving + prepNet + storage;
      var minAdj   = (subTotal > 0 && subTotal < minFee) ? (minFee - subTotal) : 0;
      var total    = subTotal + minAdj;

      function set(id, v) {
        var el = document.getElementById(id);
        if (el) el.textContent = PH_CONFIG.fmtEUR(v);
      }

      set("result-receiving", receiving);
      set("result-prep",      prepCost);
      set("result-discount",  prepCost * discount);
      set("result-storage",   storage);
      set("result-minfee",    minAdj);
      set("result-total",     total);

      var discRow = document.getElementById("result-row-discount");
      if (discRow) discRow.style.display = discount > 0 ? "" : "none";

      var minRow = document.getElementById("result-row-minfee");
      if (minRow) minRow.style.display = minAdj > 0 ? "" : "none";

      // show live unit price on checkboxes
      [
        ["calc-fnsku",      "fnsku"],
        ["calc-inspection", "inspection"],
        ["calc-polybag",    "polybag"],
        ["calc-bubblewrap", "bubblewrap"],
        ["calc-bundles",    "bundling"],
        ["calc-repack",     "repack"],
      ].forEach(function (pair) {
        var badge = document.getElementById(pair[0] + "-price");
        if (badge) {
          var per = pair[1] === "bundling" ? " / Set" : " / Einheit";
          badge.textContent = PH_CONFIG.fmtEUR(price(pair[1])) + per;
        }
      });

      // discount label
      var dlabel = document.getElementById("discount-tier-label");
      if (dlabel) {
        if (discount > 0) {
          dlabel.textContent = "Rabatt: " + (discount * 100).toFixed(0) + " %";
          dlabel.style.display = "";
        } else {
          dlabel.style.display = "none";
        }
      }
    }

    calc.querySelectorAll("input, select").forEach(function (el) {
      el.addEventListener("input", update);
      el.addEventListener("change", update);
    });
    update();
  }

  /* ── Cookie banner ─────────────────────────────────────────────────────── */
  var COOKIE_KEY = "ph_cookie_consent";

  function initCookieBanner() {
    var banner = document.getElementById("cookie-banner");
    if (!banner) return;

    var stored = localStorage.getItem(COOKIE_KEY);
    if (stored) { banner.hidden = true; return; }

    banner.hidden = false;

    var btnNec = document.getElementById("cookie-necessary");
    var btnAll = document.getElementById("cookie-all");

    if (btnNec) btnNec.addEventListener("click", function () {
      localStorage.setItem(COOKIE_KEY, "necessary");
      banner.hidden = true;
    });
    if (btnAll) btnAll.addEventListener("click", function () {
      localStorage.setItem(COOKIE_KEY, "all");
      banner.hidden = true;
    });
  }

  /* ── Contact form → mailto ─────────────────────────────────────────────── */
  function initContactForm() {
    var form = document.getElementById("contact-form");
    if (!form) return;

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      var name    = (form.elements.name    ? form.elements.name.value.trim()    : "");
      var email   = (form.elements.email   ? form.elements.email.value.trim()   : "");
      var service = (form.elements.service ? form.elements.service.value.trim() : "");
      var message = (form.elements.message ? form.elements.message.value.trim() : "");

      // Basic HTML5 validation
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var subject = "Angebotsanfrage – PrepCenter FBA";
      var body =
        "Name: " + name + "\n" +
        "E-Mail: " + email + "\n" +
        "Leistung: " + (service || "Nicht angegeben") + "\n\n" +
        "Nachricht:\n" + message;

      window.location.href =
        "mailto:info@prepcenterfba.eu" +
        "?subject=" + encodeURIComponent(subject) +
        "&body="    + encodeURIComponent(body);
    });
  }

  /* ── Floating WhatsApp button ─────────────────────────────────────────── */
  function initWhatsApp() {
    var wa = PH_CONFIG.WHATSAPP;
    if (!wa || !wa.number) return; // hidden until a number is configured
    if (document.getElementById("wa-float")) return;
    var a = document.createElement("a");
    a.id = "wa-float";
    a.href = "https://wa.me/" + encodeURIComponent(wa.number) + "?text=" + encodeURIComponent(wa.message || "");
    a.target = "_blank";
    a.rel = "noopener";
    a.setAttribute("aria-label", "WhatsApp Chat");
    a.style.cssText = "position:fixed;right:22px;bottom:22px;z-index:9999;width:58px;height:58px;border-radius:50%;background:#25D366;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,.25);transition:transform .15s ease";
    a.onmouseenter = function () { a.style.transform = "scale(1.08)"; };
    a.onmouseleave = function () { a.style.transform = "scale(1)"; };
    a.innerHTML = '<svg width="32" height="32" viewBox="0 0 32 32" aria-hidden="true"><path fill="#fff" d="M16 4a12 12 0 0 0-10.4 18l-1.5 5.4a1 1 0 0 0 1.2 1.2l5.5-1.4A12 12 0 1 0 16 4Zm0 2a10 10 0 1 1-5 18.7 1 1 0 0 0-.8-.1l-3.7 1 1-3.6a1 1 0 0 0-.1-.8A10 10 0 0 1 16 6Zm-3.6 4.9c-.3 0-.7.1-1 .5-.3.3-1.1 1.1-1.1 2.6s1.1 3 1.3 3.2c.2.2 2.2 3.5 5.4 4.8 2.7 1.1 3.2.9 3.8.8.6-.1 1.9-.8 2.2-1.6.3-.8.3-1.4.2-1.6-.1-.2-.3-.3-.7-.5l-2.4-1.1c-.3-.1-.6-.2-.8.1l-1 1.3c-.2.2-.4.3-.7.1a8.6 8.6 0 0 1-2.5-1.6 9.5 9.5 0 0 1-1.8-2.2c-.2-.3 0-.5.1-.7l.6-.7c.2-.2.2-.4.3-.6.1-.2 0-.5 0-.7l-1-2.5c-.3-.7-.6-.6-.9-.6h-.7Z"/></svg>';
    document.body.appendChild(a);
  }

  /* ── Init ──────────────────────────────────────────────────────────────── */
  function init() {
    injectChrome();
    markActiveNav();
    initBurger();
    initLangSelector();
    renderPriceTables();
    renderPriceCards();
    initCalculator();
    initCookieBanner();
    initContactForm();
    initWhatsApp();
    PH_I18N.apply();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  /* ── Public API ────────────────────────────────────────────────────────── */
  global.PH = {
    esc: esc,
    // Exposed for CMS re-render hooks.
    // injectChrome points to the FULL refresh (re-inject + re-bind listeners
    // + re-apply i18n) so external callers can't end up with a dead header.
    renderPriceTables: renderPriceTables,
    renderPriceCards:  renderPriceCards,
    injectChrome:      refreshChrome,
    refreshChrome:     refreshChrome,
  };

}(typeof window !== "undefined" ? window : this));

/**
 * js/main.js — PrepCenter FBA core runtime.
 *
 * Responsibilities:
 *  - PH.esc(str)           safe HTML escaping
 *  - Header/footer injection into #site-header / #site-footer
 *  - Active nav detection
 *  - Mobile burger menu
 *  - renderPriceTables()   renders [data-price-table] elements
 *  - Language selector (tastaturbedienbar, auch im Mobilmenü)
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

  /* ── Interne Links ─────────────────────────────────────────────────────
     Deutsche Seiten liegen im Root, die Sprachversionen unter /en/, /it/
     und /fr/ mit eigenen Slugs. Vorgerenderte Seiten setzen window.PH_LINKS,
     damit dieselbe Navigation mit ihren URLs erzeugt wird. */
  var DEFAULT_LINKS = {
    home: "./index.html", services: "./services.html", pricing: "./pricing.html",
    calculator: "./kalkulator.html", about: "./ueber-uns.html", faq: "./faq.html",
    contact: "./kontakt.html", pillar: "./fba-prep-center-deutschland.html",
    labeling: "./fnsku-etikettierung.html", storage: "./fba-lagerung-deutschland.html",
    shipping: "./versand-an-amazon.html", returns: "./amazon-retouren-deutschland.html",
    imprint: "/impressum.html", privacy: "/datenschutz.html", terms: "/agb.html",
    blog: "/blog/"
  };
  function L(key) { var o = global.PH_LINKS || {}; return o[key] || DEFAULT_LINKS[key]; }

  /* Den Ratgeber gibt es bewusst nur auf Deutsch (siehe DE_ONLY in tools/seo.py),
     deshalb erscheint der Navigationspunkt nur auf den deutschen Seiten. */
  function isDe() { var f = global.PH_FORCE_LANG; return !f || f === "de"; }

  /* USt-Hinweis für den Footer: USt-IdNr. nur zeigen, wenn gepflegt. */
  function vatSuffix(b) {
    if (b.kleinunternehmer || !b.vatId) return "";
    return " \u00b7 USt-IdNr.: " + esc(b.vatId);
  }

  /* ── Sprachumschalter ─────────────────────────────────────────────────
     Die Optionen sind <button>-Elemente: nativ fokussierbar und mit
     Enter/Leertaste bedienbar. Wird zweimal gerendert (Kopf + Mobilmenü),
     deshalb bekommen die Instanzen eigene IDs. */
  var LANG_NAMES = { de: "DE – Deutsch", en: "EN – English", it: "IT – Italiano", fr: "FR – Français" };
  function langSwitcher(btnId, menuId, labelId) {
    var opts = ["de", "en", "it", "fr"].map(function (code) {
      return '<li><button type="button" class="lang-option" data-lang="' + code + '" lang="' + code + '">'
           + esc(LANG_NAMES[code]) + '</button></li>';
    }).join("");
    return [
      '      <div class="lang-dropdown" data-lang-switcher>',
      '        <button type="button" class="lang-btn" aria-haspopup="true" aria-expanded="false"'
        + ' aria-controls="' + menuId + '" id="' + btnId + '"'
        + ' data-i18n="a11y.lang.choose" data-i18n-attr="aria-label" aria-label="Sprache wählen">',
      '          <span class="lang-current" id="' + labelId + '">DE</span>',
      '          <svg width="10" height="6" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round"/></svg>',
      '        </button>',
      '        <ul class="lang-menu" id="' + menuId + '">',
      '          ' + opts,
      '        </ul>',
      '      </div>',
    ].join("\n");
  }

  /* Kompakte Sprachreihe fürs Mobilmenü: vier gleichrangige Schaltflächen,
     kein Overlay – dadurch nichts, was der sticky Header abschneiden könnte. */
  function langRow() {
    var opts = ["de", "en", "it", "fr"].map(function (code) {
      return '<button type="button" class="lang-pill" data-lang="' + code + '" lang="' + code + '">'
           + code.toUpperCase() + '</button>';
    }).join("");
    return [
      '    <div class="lang-row" data-lang-row role="group"'
        + ' data-i18n="a11y.lang.choose" data-i18n-attr="aria-label" aria-label="Sprache wählen">',
      '      ' + opts,
      '    </div>',
    ].join("\n");
  }

  /* ── Header template ──────────────────────────────────────────────────── */
  function buildHeader() {
    var b = PH_CONFIG.BRAND;
    var pages = [
      { href: L("home"),       label: "Startseite", key: "nav.home"       },
      { href: L("services"),   label: "Leistungen", key: "nav.services"   },
      { href: L("pricing"),    label: "Preise",     key: "nav.pricing"    },
      { href: L("calculator"), label: "Kalkulator", key: "nav.calculator" },
      { href: L("about"),      label: "Über uns",   key: "nav.about"      },
      { href: L("faq"),        label: "FAQ",        key: "nav.faq"        },
    ];
    if (isDe()) pages.push({ href: L("blog"), label: "Ratgeber", key: "nav.blog" });

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
      '    .header-flex{display:flex;align-items:stretch;gap:1.5rem;padding:8px 0}',
      '    .header-right{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;justify-content:space-evenly;gap:10px;padding:6px 0}',
      '    .header-slogan{max-width:100%;overflow:hidden;text-align:center;white-space:nowrap;font-size:clamp(.95rem,1.75vw,1.6rem);font-style:italic;font-weight:600;color:#475569;line-height:1.2}',
      '    .header-slogan b{color:#f4721e;font-style:normal}',
      '    .logo-img--header{height:172px;width:auto;display:block}',
      '    .header-navrow{display:flex;align-items:center;justify-content:center;gap:1.25rem;flex-wrap:wrap}',
      '    .header-navrow .main-nav{flex:none;gap:.5rem}',
      '    .header-navrow .nav-link{font-size:1.35rem;font-weight:600;padding:.45rem .95rem}',
      '    .header-navrow .header-actions{margin-left:0}',
      '    .btn-wa-header{display:inline-flex;align-items:center;gap:.45rem;background:#25d366;color:#fff;font-weight:600;border-radius:999px;padding:.5rem 1rem;font-size:.9rem;text-decoration:none;transition:filter .15s}',
      '    .btn-wa-header:hover{filter:brightness(1.07);color:#fff}',
      '    .header-flex .burger{align-self:center;margin-left:auto}',
      '    @media(max-width:1100px){.logo-img--header{height:120px}}',
      '    @media(max-width:900px){.header-slogan{display:none}}',
      '    .lang-menu li{list-style:none;margin:0}',
      '    .lang-menu .lang-option{display:block;width:100%;text-align:left;background:none;border:0;font-family:inherit;font-size:.85rem;line-height:inherit;cursor:pointer;border-radius:0}',
      '    .lang-menu li:last-child .lang-option{border-radius:0 0 8px 8px}',
      '    .mobile-nav .lang-dropdown{margin-top:.5rem}',
      '    .mobile-nav .lang-btn{width:100%;justify-content:center}',
      '    .lang-row{display:flex;gap:.4rem;margin-top:.75rem}',
      '    .lang-pill{flex:1;padding:.55rem 0;border:1px solid #cbd5e1;border-radius:8px;background:#fff;',
      '      font-family:inherit;font-size:.85rem;font-weight:600;color:#64748b;cursor:pointer}',
      '    .lang-pill[aria-current="true"]{background:#1d4ed8;border-color:#1d4ed8;color:#fff}',
      '    @media(max-width:767px){.logo-img--header{height:96px}.header-right{display:none}}',
      '  </style>',
      '  <div class="container header-flex">',
      '    <a href="' + esc(L("home")) + '" class="logo" data-i18n="a11y.logo.home" data-i18n-attr="aria-label" aria-label="' + esc(b.name) + ' – Startseite" style="display:flex;align-items:center;text-decoration:none">',
      '      <img src="/img/logo-full.png" class="logo-img logo-img--header" width="600" height="420" alt="PrepCenter FBA">',
      '    </a>',
      '    <div class="header-right">',
      '      <span class="header-slogan" aria-hidden="false"><span data-i18n="sl.s1">Auf </span><b data-i18n="sl.b1">Vertrauen</b><span data-i18n="sl.s2"> gebaut. Durch </span><b data-i18n="sl.b2">Qualität</b><span data-i18n="sl.s3"> gesichert. Von </span><b data-i18n="sl.b3">Integrität</b><span data-i18n="sl.s4"> geprägt.</span></span>',
      '      <div class="header-navrow">',
      '        <nav class="main-nav" role="navigation" data-i18n="a11y.nav.main" data-i18n-attr="aria-label" aria-label="Hauptnavigation">',
      '          ' + navLinks,
      '        </nav>',
      '        <div class="header-actions">',
      langSwitcher("lang-btn", "lang-menu", "lang-current"),
      '      <a href="' + esc(L("contact")) + '" class="btn btn--primary btn--sm" data-i18n="nav.cta">Jetzt anfragen</a>',
      waHeaderBtn,
      '        </div>',
      '      </div>',
      '    </div>',
      '    <button class="burger" id="burger" data-i18n="a11y.menu.open" data-i18n-attr="aria-label" aria-label="Menü öffnen" aria-expanded="false" aria-controls="main-nav-mobile">',
      '      <span></span><span></span><span></span>',
      '    </button>',
      '  </div>',
      '  <nav class="mobile-nav" id="main-nav-mobile" data-i18n="a11y.nav.mobile" data-i18n-attr="aria-label" aria-label="Mobile Navigation" hidden>',
      '    ' + navLinks,
      '    <a href="' + esc(L("contact")) + '" class="btn btn--primary" data-i18n="nav.cta">Jetzt anfragen</a>',
      waMobileBtn,
      langRow(),
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
      '        <img src="/img/logo-full.png" class="logo-img" width="600" height="420" alt="PrepCenter FBA" style="height:88px;width:auto;display:block;filter:none">',
      '      </div>',
      '      <p class="footer-legalname">' + esc(b.legalName) + '</p>',
      '      <p data-i18n="footer.tagline">Ihr FBA Prep Partner in Deutschland. Schnell, transparent, zuverlässig.</p>',
      '      <address>',
      '        <span data-i18n="footer.address">' + esc(b.street) + ', ' + esc(b.zip) + ' ' + esc(b.city) + '</span><br>',
      '        <a href="mailto:' + esc(b.email) + '">' + esc(b.email) + '</a><br>',
      '        ' + (b.phone ? '<a href="tel:' + esc(b.phone.replace(/\s/g, "")) + '">' + esc(b.phone) + '</a>' : ''),
      '        ' + (PH_CONFIG.WHATSAPP && PH_CONFIG.WHATSAPP.number
        ? '<br><a href="https://wa.me/' + esc(PH_CONFIG.WHATSAPP.number) + '?text=' + encodeURIComponent(PH_CONFIG.WHATSAPP.message || "") + '" target="_blank" rel="noopener" style="color:#25D366;font-weight:600" data-i18n="wa.footer">WhatsApp Chat</a>'
        : ''),
      '      </address>',
      '    </div>',
      '    <div class="footer-col">',
      '      <h3 data-i18n="footer.nav.title">Navigation</h3>',
      '      <ul>',
      '        <li><a href="' + esc(L("home")) + '" data-i18n="nav.home">Startseite</a></li>',
      '        <li><a href="' + esc(L("services")) + '" data-i18n="nav.services">Leistungen</a></li>',
      '        <li><a href="' + esc(L("pricing")) + '" data-i18n="nav.pricing">Preise</a></li>',
      '        <li><a href="' + esc(L("calculator")) + '" data-i18n="nav.calculator">Kalkulator</a></li>',
      '        <li><a href="' + esc(L("about")) + '" data-i18n="nav.about">Über uns</a></li>',
      '        <li><a href="' + esc(L("faq")) + '" data-i18n="nav.faq">FAQ</a></li>',
      (isDe() ? '        <li><a href="' + esc(L("blog")) + '" data-i18n="nav.blog">Ratgeber</a></li>' : ""),
      '        <li><a href="' + esc(L("contact")) + '" data-i18n="nav.contact">Kontakt</a></li>',
      '      </ul>',
      '    </div>',
      '    <div class="footer-col">',
      '      <h3 data-i18n="footer.services.title">Leistungen</h3>',
      '      <ul>',
      '        <li><a href="' + esc(L("pillar")) + '" data-i18n="nav.pillar">FBA Prep Center Deutschland</a></li>',
      '        <li><a href="' + esc(L("labeling")) + '" data-i18n="service.labeling">FNSKU-Etikettierung</a></li>',
      '        <li><a href="' + esc(L("storage")) + '" data-i18n="service.storage">Lagerung</a></li>',
      '        <li><a href="' + esc(L("shipping")) + '" data-i18n="service.forwarding">Einlieferung FBA</a></li>',
      '        <li><a href="' + esc(L("returns")) + '" data-i18n="service.returns">Retourenbearbeitung</a></li>',
      '        <li><a href="' + esc(L("services")) + '" data-i18n="nav.allservices">Alle Leistungen</a></li>',
      '      </ul>',
      '    </div>',
      '    <div class="footer-col">',
      '      <h3 data-i18n="footer.legal.title">Rechtliches</h3>',
      '      <ul>',
      '        <li><a href="' + esc(L("imprint")) + '" data-i18n="footer.legal.imprint">Impressum</a></li>',
      '        <li><a href="' + esc(L("privacy")) + '" data-i18n="footer.legal.privacy">Datenschutzerklärung</a></li>',
      '        <li><a href="' + esc(L("terms")) + '" data-i18n="footer.legal.terms">AGB</a></li>',
      '      </ul>',
      '      <p class="vat-note"><span data-i18n="footer.vat">Alle Preise netto zzgl. gesetzlicher USt.</span>' + vatSuffix(b) + '</p>',
      '    </div>',
      '  </div>',
      '  <div class="footer-bottom">',
      '    <div class="container">',
      '      <p class="footer-disclaimer" data-i18n="footer.disclaimer">Rechtlicher Hinweis: PrepCenter FBA (Zbranca MTZ World) ist ein unabhängiger Dienstleister und steht in keiner geschäftlichen Verbindung zu Amazon. Wir sind kein Partner, Vertreter, Wiederverkäufer oder Beauftragter von Amazon und werden von Amazon weder gesponsert noch unterstützt oder in sonstiger Weise unterhalten. „Amazon", „Amazon FBA", „FNSKU" und alle zugehörigen Logos sind Marken der Amazon.com, Inc. oder ihrer verbundenen Unternehmen. Die Nennung dieser Marken erfolgt ausschließlich beschreibend, um die von uns angebotenen Dienstleistungen zu erläutern (nominative Markennennung).</p>',
      '      <span>&copy; ' + year + ' ' + esc((b.legalName || b.name) + (b.legalForm ? " " + b.legalForm : "")) + ' · ' + esc(b.city) + ', ' + esc(b.country) + '</span>',
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
    // Ganze Pfade vergleichen, nicht nur Dateinamen: sonst waere "/blog/"
    // auf der Startseite aktiv (beide enden auf index.html).
    function norm(p) { return p.replace(/index\.html$/, "") || "/"; }
    var here = norm(location.pathname);
    document.querySelectorAll(".nav-link").forEach(function (a) {
      var there;
      try { there = norm(new URL(a.getAttribute("href"), location.href).pathname); }
      catch (e) { return; }
      // Beitragsseiten markieren ebenfalls den Ratgeber-Eintrag.
      if (there === here || (there === "/blog/" && here.indexOf("/blog/") === 0)) {
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

    function ti(key, fallback) {
      var v = global.PH_I18N ? PH_I18N.t(key) : key;
      return (v === key) ? fallback : v;
    }
    function setOpen(open) {
      mobileNav.hidden = !open;
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? ti("a11y.menu.close", "Menü schließen")
                                             : ti("a11y.menu.open",  "Menü öffnen"));
      if (open) {
        var first = mobileNav.querySelector("a, button");
        if (first) first.focus();
      }
    }
    burger.addEventListener("click", function () { setOpen(mobileNav.hidden); });
    // Escape schließt das Menü und gibt den Fokus zurück
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !mobileNav.hidden) { setOpen(false); burger.focus(); }
    });
  }

  /* ── Language selector ─────────────────────────────────────────────────
     Bedient beide Instanzen (Kopfzeile + Mobilmenü). Die Optionen sind
     Buttons, also von Haus aus per Tab/Enter/Leertaste erreichbar. */
  function initLangSelector() {
    document.querySelectorAll("[data-lang-switcher]").forEach(function (root) {
      var btn   = root.querySelector(".lang-btn");
      var menu  = root.querySelector(".lang-menu");
      var label = root.querySelector(".lang-current");
      if (!btn || !menu) return;

      function close() {
        menu.classList.remove("lang-menu--open");
        btn.setAttribute("aria-expanded", "false");
      }

      btn.addEventListener("click", function (e) {
        e.stopPropagation();
        var open = menu.classList.toggle("lang-menu--open");
        btn.setAttribute("aria-expanded", String(open));
        if (open) {
          var first = menu.querySelector(".lang-option");
          if (first) first.focus();
        }
      });

      menu.querySelectorAll(".lang-option").forEach(function (opt) {
        opt.addEventListener("click", function () {
          close();
          PH_I18N.setLang(opt.getAttribute("data-lang"));
          // Ohne eigene URL für diese Sprache bleiben wir auf der Seite:
          renderPriceTables();
          renderPriceCards();
          syncLangUI();
        });
      });

      root.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && menu.classList.contains("lang-menu--open")) {
          e.stopPropagation();
          close();
          btn.focus();
        }
      });

      document.addEventListener("click", function (e) {
        if (!root.contains(e.target)) close();
      });
    });
    document.querySelectorAll("[data-lang-row] .lang-pill").forEach(function (pill) {
      pill.addEventListener("click", function () {
        PH_I18N.setLang(pill.getAttribute("data-lang"));
        renderPriceTables();
        renderPriceCards();
        syncLangUI();
      });
    });
    syncLangUI();
  }

  /* Aktive Sprache in allen Umschalter-Instanzen markieren. */
  function syncLangUI() {
    var cur = global.PH_I18N ? PH_I18N.getLang() : "de";
    document.querySelectorAll("[data-lang-row] .lang-pill").forEach(function (pill) {
      if (pill.getAttribute("data-lang") === cur) pill.setAttribute("aria-current", "true");
      else pill.removeAttribute("aria-current");
    });
    document.querySelectorAll("[data-lang-switcher]").forEach(function (root) {
      var label = root.querySelector(".lang-current");
      if (label) label.textContent = cur.toUpperCase();
      root.querySelectorAll(".lang-option").forEach(function (o) {
        var active = o.getAttribute("data-lang") === cur;
        o.classList.toggle("lang-option--active", active);
        if (active) o.setAttribute("aria-current", "true");
        else o.removeAttribute("aria-current");
      });
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

      var groupTitle = ti("price.group." + group, group);
      var html = [
        '<table class="price-table" aria-label="' + esc(groupTitle) + '">',
        '<thead><tr>',
        '  <th scope="col">' + esc(colSvc) + '</th>',
        '  <th scope="col">' + esc(colUnit) + '</th>',
        '  <th scope="col" class="text-right">' + esc(colPrice) + '</th>',
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
    initWhatsApp();
    PH_I18N.apply();
    syncLangUI();
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

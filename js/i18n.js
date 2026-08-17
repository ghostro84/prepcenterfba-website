/**
 * js/i18n.js — Lightweight i18n engine für PrepCenter FBA.
 *
 * Global: PH_I18N
 *
 * Usage:
 *   PH_I18N.apply()              — apply current language to all data-i18n elements
 *   PH_I18N.setLang("en")        — switch language and persist choice
 *   PH_I18N.getLang()            — returns current language code
 *   PH_I18N.t("some.key")        — translate a single key (returns key if missing)
 *
 * Dictionaries are loaded lazily from js/lang/<code>.js which must call
 * PH_I18N.registerDict("<code>", { ... }).
 * Only "de" is available in Phase 1 — the German strings live directly in
 * the HTML, so the de dictionary is intentionally empty (keys fall through
 * to the existing HTML content).
 */
(function (global) {
  "use strict";

  var SUPPORTED = ["de", "en", "it", "fr"];
  var DEFAULT_LANG = "de";
  var STORAGE_KEY = "ph_lang";

  var _dicts = {};   // { langCode: { "key": "string" } }
  var _lang  = DEFAULT_LANG;

  function _loadStored() {
    // Auf vorgerenderten Sprachversionen (/en/, /it/, /fr/) bestimmt die URL
    // die Sprache – nicht localStorage.
    var forced = global.PH_FORCE_LANG;
    if (forced && SUPPORTED.indexOf(forced) !== -1) { _lang = forced; return; }
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (stored && SUPPORTED.indexOf(stored) !== -1) _lang = stored;
    } catch (_) { /* localStorage not available */ }
  }

  function getLang() {
    return _lang;
  }

  function setLang(code) {
    if (SUPPORTED.indexOf(code) === -1) return;
    // Existiert eine echte URL für diese Sprache, wird dorthin navigiert.
    var urls = global.PH_LANG_URLS;
    if (urls && urls[code] && code !== _lang) {
      try { localStorage.setItem(STORAGE_KEY, code); } catch (_) {}
      global.location.href = urls[code];
      return;
    }
    _lang = code;
    try { localStorage.setItem(STORAGE_KEY, code); } catch (_) {}
    apply();
    // update <html lang> attribute
    document.documentElement.setAttribute("lang", code);
    // update language selector UI
    var sel = document.getElementById("lang-select");
    if (sel) sel.value = code;
  }

  function registerDict(code, dict) {
    _dicts[code] = dict || {};
  }

  function t(key) {
    var dict = _dicts[_lang];
    if (dict && dict[key] !== undefined) return dict[key];
    // fall back to "de" dict, then return key itself
    var de = _dicts["de"];
    if (de && de[key] !== undefined) return de[key];
    return key;
  }

  /**
   * Snapshot the original German text of an element into the "de" dict
   * the first time we see it, so switching back to DE can restore it
   * without a page reload.
   */
  function _snapshotDe(el, key, attr) {
    var de = _dicts[DEFAULT_LANG];
    if (de[key] !== undefined) return;
    if (attr) {
      de[key] = el.getAttribute(attr) || "";
    } else if (el.children.length === 0) {
      de[key] = el.textContent;
    } else {
      for (var i = 0; i < el.childNodes.length; i++) {
        if (el.childNodes[i].nodeType === Node.TEXT_NODE) {
          de[key] = el.childNodes[i].textContent;
          return;
        }
      }
      de[key] = "";
    }
  }

  /**
   * Walk every [data-i18n] element and replace its textContent (or
   * [data-i18n-attr] attribute) with the translated string.
   * The original German HTML text is snapshotted into the "de" dict on
   * first pass, so DE ⇄ EN/IT/FR switching works both ways without reload.
   * If no translation exists the element is left untouched.
   */
  function apply() {
    // <html lang> immer der aktiven Sprache angleichen (Screenreader-Aussprache)
    try { document.documentElement.setAttribute("lang", _lang); } catch (_) {}
    var nodes = document.querySelectorAll("[data-i18n]");
    nodes.forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var attr = el.getAttribute("data-i18n-attr");
      _snapshotDe(el, key, attr);          // remember German original
      var val = t(key);                    // falls back to de snapshot
      if (val === key) return;             // no translation anywhere, leave as is
      if (attr) {
        el.setAttribute(attr, val);
      } else {
        // Preserve child elements (e.g. <strong>, <br>) — only replace
        // text node if the element has no child elements.
        if (el.children.length === 0) {
          el.textContent = val;
        } else {
          // Replace only the first text node
          for (var i = 0; i < el.childNodes.length; i++) {
            if (el.childNodes[i].nodeType === Node.TEXT_NODE) {
              el.childNodes[i].textContent = val;
              break;
            }
          }
        }
      }
    });
  }

  // Register an empty DE dict (HTML already in German)
  registerDict("de", {});

  // Initialise
  _loadStored();

  global.PH_I18N = { getLang, setLang, registerDict, t, apply };

}(typeof window !== "undefined" ? window : this));

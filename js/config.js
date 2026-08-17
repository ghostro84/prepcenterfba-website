/**
 * js/config.js — Single source of truth für PrepCenter FBA.
 * Firmendaten, Preisliste und Rabatte werden ausschließlich hier gepflegt.
 *
 * Global: PH_CONFIG
 */
(function (global) {
  "use strict";

  /* ─── Brand ──────────────────────────────────────────────────────────── */
  const BRAND = {
    name:        "PrepCenter FBA",        // Geschäftsbezeichnung / Marke
    legalName:   "Zbranca MTZ World",     // Firmierung des Einzelunternehmens
    legalForm:   "",                      // Einzelunternehmen → bleibt leer
    owner:       "Valentin Iulian Zbranca",   // nur fuer das Impressum (§ 5 DDG), nicht im Footer
    street:      "Lindenstraße 21",
    zip:         "83395",
    city:        "Freilassing",
    region:      "Bayern",
    country:     "Deutschland",
    countryCode: "DE",
    email:       "b2b@prepcenterfba.eu",
    phone:       "",                      // bewusst keine öffentliche Telefonnummer
    vatId:       "DE360335852",           // USt-IdNr. § 27a UStG
    kleinunternehmer: false,
    domain:      "https://prepcenterfba.eu",
    // Steuernummer wird bewusst NICHT veröffentlicht – die USt-IdNr. genügt.
  };


  /* ─── WhatsApp contact ───────────────────────────────────────────────── */
  // Set the number in international format WITHOUT "+" or spaces,
  // e.g. "4915112345678". While empty, all WhatsApp buttons stay hidden.
  const WHATSAPP = {
    number:  "436769559138",
    message: "Hallo PrepCenter FBA! Ich interessiere mich für Ihre Prep-Services.",
  };

  /* ─── Default price list ─────────────────────────────────────────────── */
  // Prices from official PrepCenter FBA Preisliste (DE/EN/IT/FR)
  // key        – stable identifier (used for CMS and localStorage overrides)
  // group      – receiving | prep | storage | outbound | returns | fees
  // label      – human-readable German name
  // unit       – per unit label shown in tables
  // price      – EUR, net (netto zzgl. USt.)
  // note       – optional footnote shown in table
  const DEFAULT_PRICES = [
    // ── Wareneingang ──────────────────────────────────────────────────────
    { key: "recv_carton",         group: "receiving", label: "Wareneingang Karton (mit Prep)",  unit: "pro Karton",          price: 0.00, note: "Kostenlos bei gebuchter Prep- oder Bundling-Leistung",        desc: "Annahme und Einbuchung Ihrer Einlieferungskartons inkl. Stückzahlkontrolle. Bei gleichzeitig gebuchter Prep-Leistung kostenfrei." },
    { key: "recv_carton_no_prep", group: "receiving", label: "Wareneingang Karton (ohne Prep)", unit: "pro Karton",          price: 1.50,                                                       desc: "Annahme und Einlagerung ohne begleitende Prep-Leistung – Karton wird eingebucht und eingelagert, aber nicht bearbeitet." },
    { key: "recv_pallet",         group: "receiving", label: "Palettenannahme",                 unit: "pro Palette",         price: 6.00,                                                       desc: "Annahme und Entladung von Einlieferungspaletten inkl. Stückzahlkontrolle und Einbuchung ins System." },
    // ── Prep & Etikettierung ──────────────────────────────────────────────
    { key: "fba_prep",    group: "prep", label: "FBA Komplett-Prep",       unit: "pro Einheit", price: 0.79, note: "Standardprozess gemäß Vereinbarung",   desc: "Vollständiger Amazon-konformer Prep-Prozess: Sichtkontrolle, FNSKU-Etikettierung, Verpackung und Versandvorbereitung gemäß Amazon-Richtlinien." },
    { key: "fnsku",       group: "prep", label: "FNSKU-Etikettierung",     unit: "pro Einheit", price: 0.39,                                                desc: "Aufkleben des FNSKU-Barcodes auf jede Produkteinheit. Etiketten von Ihnen bereitgestellt oder bei uns gedruckt." },
    { key: "inspection",  group: "prep", label: "Qualitätskontrolle",      unit: "pro Einheit", price: 0.25,                                                desc: "Sichtprüfung auf Beschädigungen, korrekte Artikelanzahl und Unversehrtheit der Verpackung. Prüfbericht mit Fotos erhalten Sie per E-Mail." },
    { key: "polybag",     group: "prep", label: "Polybag-Verpackung",      unit: "pro Einheit", price: 0.29,                                                desc: "Einschweißen der Produkte in transparente Polybeutel gemäß Amazon-Anforderungen. Material inklusive." },
    { key: "bubblewrap",  group: "prep", label: "Luftpolsterfolie",        unit: "pro Einheit", price: 0.29,                                                desc: "Einwickeln empfindlicher oder zerbrechlicher Artikel in Luftpolsterfolie zum Schutz beim Transport. Material inklusive." },
    { key: "bundling",    group: "prep", label: "Bundling / Multipacking", unit: "pro Set",     price: 0.69,                                                desc: "Zusammenfassen mehrerer Einzelartikel zu einem verkaufsfähigen Bundle oder Multipack nach Ihren Vorgaben. Übergreifendes Bundle-Etikett inklusive." },
    { key: "repack",      group: "prep", label: "Umverpackung",            unit: "pro Einheit", price: 0.49,                                                desc: "Umverpacken von Produkten in neue Kartons oder alternative Verpackungen auf Ihren Wunsch." },
    { key: "extra_label", group: "prep", label: "Zusätzliches Etikett",   unit: "pro Etikett", price: 0.25,                                                desc: "Anbringen zusätzlicher Etiketten, z. B. Warnaufkleber, Sprachübersetzungs-Overlays oder Mindesthaltbarkeitsdaten." },
    // ── Zusätzliche Services ──────────────────────────────────────────────
    { key: "doc_photo",   group: "prep", label: "Dokumentationsfoto",     unit: "pro Foto",    price: 0.30,                                                desc: "Fotodokumentation des fertig verpackten Artikels – ideal für Ihre Unterlagen oder zur Schadensabsicherung gegenüber Amazon." },
    { key: "photo",       group: "prep", label: "Produktfoto (einfach)",  unit: "pro Foto",    price: 3.90,                                                desc: "Einfaches Produktfoto auf weißem oder neutralem Hintergrund für Ihre Listings oder interne Dokumentation." },
    // ── Lagerung ──────────────────────────────────────────────────────────
    { key: "storage_free",   group: "storage", label: "Zwischenlagerung (FBA-Prep)", unit: "erste 14 Tage",      price: 0.00, note: "Kostenlos bei gebuchter Prep- oder Bundling-Leistung", desc: "Kostenlose Zwischenlagerung für alle Waren, für die gleichzeitig eine FBA-Prep-Leistung gebucht ist. Maximal 14 Tage." },
    { key: "storage_bin",    group: "storage", label: "Lagerung Kleinmengen",        unit: "pro Monat",          price: 2.00,                                                   desc: "Lagerung kleiner Warenmengen in einem dedizierten Lagerplatz oder Regalfach – ideal für Test-Sendungen." },
    { key: "storage_carton", group: "storage", label: "Lagerung Karton",             unit: "pro Karton / Monat", price: 1.20,                                                   desc: "Monatliche Lagergebühr pro eingelagertem Standardkarton – anteilig nach tatsächlicher Lagerdauer berechnet." },
    { key: "storage_pallet", group: "storage", label: "Lagerung Palette",            unit: "pro Palette / Monat",price: 19.00,                                                  desc: "Monatliche Lagergebühr pro eingelagerter Europalette – anteilig nach tatsächlicher Lagerdauer berechnet." },
    // ── FBA Auslieferung ──────────────────────────────────────────────────
    { key: "out_carton", group: "outbound", label: "FBA Karton-Handling",   unit: "pro Karton",  price: 2.90,  desc: "Handlinggebühr für das Kommissionieren, Konfektionieren und Übergeben Ihrer FBA-Sendungskartons an den Spediteur." },
    { key: "out_pallet", group: "outbound", label: "FBA Paletten-Handling", unit: "pro Palette", price: 18.00, desc: "Handlinggebühr für das Bereitstellen, Etikettieren und die Übergabe Ihrer FBA-Einlieferungspaletten an den Spediteur." },
    // ── Retouren ─────────────────────────────────────────────────────────
    { key: "ret_inspect", group: "returns", label: "Retourenannahme + Inspektion", unit: "pro Einheit", price: 0.90,                                            desc: "Annahme retournierter Sendungen mit Sichtprüfung jeder Einheit und schriftlichem Zustandsprotokoll." },
    { key: "ret_repack",  group: "returns", label: "Retouren-Umverpackung",        unit: "pro Einheit", price: 0.50, note: "Zusätzlich zur Retourenannahme",   desc: "Neuverpacken retournierter Einheiten für erneute FBA-Einlieferung oder Weiterverkauf (zusätzlich zur Retourenannahme)." },
    { key: "disposal",    group: "returns", label: "Entsorgung",                   unit: "pro Einheit", price: 0.30,                                            desc: "Fachgerechte Entsorgung nicht-wiederverwendbarer oder beschädigter Artikel gemäß gesetzlicher Vorschriften." },
    // ── Gebühren ──────────────────────────────────────────────────────────
    { key: "min_order", group: "fees", label: "Mindestauftragswert", unit: "pro Auftrag", price: 25.00, desc: "Gilt je Einzelauftrag für Prep-Leistungen. Liegt der Wert der beauftragten Prep-Leistungen unter 25,00 €, wird die Differenz als Mindestauftragszuschlag berechnet. Reine Lager-, Auslieferungs- und Retourenaufträge lösen keinen Zuschlag aus." },
  ];

  /* ─── New-customer discount (Neukundenrabatt) ────────────────────────── */
  // Not volume-based; applies to first two deliveries (Prep services only,
  // max 2.000 units per delivery; storage, shipping, third-party excluded).
  const NEW_CUSTOMER_DISCOUNT = [
    { delivery: 1, discount: 0.10, label: "1. Lieferung –10 %" },
    { delivery: 2, discount: 0.05, label: "2. Lieferung –5 %"  },
  ];

  /* ─── Price helpers ──────────────────────────────────────────────────── */

  /**
   * Returns a merged price list: DEFAULT_PRICES with any admin overrides
   * stored in localStorage under the key `ph_price_overrides`.
   * Override format: { [priceKey]: newPriceNumber }
   */
  function getPrices() {
    let overrides = {};
    try {
      const raw = localStorage.getItem("ph_price_overrides");
      if (raw) overrides = JSON.parse(raw);
    } catch (_) { /* ignore */ }
    return DEFAULT_PRICES.map(function (p) {
      return Object.assign({}, p, {
        price: typeof overrides[p.key] === "number" ? overrides[p.key] : p.price,
      });
    });
  }

  /**
   * EUR-Formatierung in der aktiven Sprache:
   * de → 1.234,56 €   en → €1,234.56   it → 1.234,56 €   fr → 1 234,56 €
   */
  const NUM_LOCALE = { de: "de-DE", en: "en-IE", it: "it-IT", fr: "fr-FR" };
  function fmtEUR(n) {
    var lang = "de";
    try { if (global.PH_I18N) lang = global.PH_I18N.getLang(); } catch (_) {}
    return new Intl.NumberFormat(NUM_LOCALE[lang] || "de-DE", {
      style:    "currency",
      currency: "EUR",
    }).format(n);
  }

  /* ─── Export ─────────────────────────────────────────────────────────── */
  /* ─── CMS ────────────────────────────────────────────────────────────── */
  // API base URL for the CMS backend.
  // Leave empty for Replit dev (served at /api via same-origin proxy).
  // Set to the deployed API URL for production, e.g. "https://abc.replit.app"
  const CMS_API_BASE = "";  // kein Backend im Einsatz
  // Master switch for the CMS runtime. Keep FALSE on static hosting without
  // the API server (avoids a failing /api/cms/content request on every page).
  // Set to true once the CMS backend is deployed. ?cms_mode=1 always tries.
  const CMS_ENABLED = false;

  global.PH_CONFIG = {
    BRAND,
    WHATSAPP,
    DEFAULT_PRICES,
    NEW_CUSTOMER_DISCOUNT,
    getPrices,
    fmtEUR,
    CMS_API_BASE,
    CMS_ENABLED,
  };

}(typeof window !== "undefined" ? window : this));

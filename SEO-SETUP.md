# SEO & Setup — prepcenterfba.eu

Kurzanleitung für alles, was nach dem Deploy noch einmal von Hand angefasst
werden muss. Alles andere ist bereits im Repository erledigt.

---

## 1. Was bereits eingebaut ist

| Bereich | Status |
|---|---|
| `canonical` auf jeder Seite | ✅ |
| `hreflang` DE / EN / IT / FR + `x-default` | ✅ |
| OpenGraph + Twitter Cards (inkl. Bild) | ✅ |
| JSON-LD: `ProfessionalService`, `WebSite`, `WebPage`, `Service`, `BreadcrumbList`, `FAQPage` | ✅ |
| `sitemap.xml` mit allen 51 URLs und hreflang-Alternates | ✅ |
| `robots.txt` mit Sitemap-Verweis | ✅ |
| Statische Sprachversionen unter `/en/`, `/it/`, `/fr/` mit eigenen Slugs | ✅ |
| Interne Verlinkung (Themen-Hub auf der Startseite, „Weiterführende Seiten“ je Landingpage) | ✅ |
| Aussagekräftige `alt`-Texte | ✅ |
| Skip-Link + sichtbarer Fokus-Ring (Barrierefreiheit) | ✅ |
| Amazon-Disclaimer im Footer jeder Seite (4 Sprachen) | ✅ |
| Einwilligungsgesteuertes Analytics-Gerüst | ✅ (deaktiviert) |

---

## 2. Google Search Console einrichten

1. [search.google.com/search-console](https://search.google.com/search-console) öffnen
   → **Property hinzufügen** → **Domain** → `prepcenterfba.eu`.
2. Google zeigt einen **TXT-Eintrag**. Diesen im Hostinger hPanel unter
   *Domains → prepcenterfba.eu → DNS* als TXT-Record für `@` anlegen.
   *(Die Domain-Property ist der HTML-Datei-Variante vorzuziehen: sie deckt
   `http`, `https`, `www` und alle Subdomains auf einmal ab.)*
3. Nach der Bestätigung unter **Sitemaps** eintragen: `sitemap.xml` → Senden.
4. Unter **Indexierung → Seiten** nach ein paar Tagen prüfen, welche URLs
   aufgenommen wurden.

**Sofort nach der Verifizierung sinnvoll:**

- Startseite und die sechs Landingpages einzeln über die **URL-Prüfung** →
  *Indexierung beantragen* einreichen. Das beschleunigt die Erstaufnahme.
- Unter **Einstellungen → Internationale Ausrichtung** prüfen, ob Google die
  hreflang-Angaben ohne Fehler liest.

## 3. Bing Webmaster Tools

Lohnt sich, weil der Import aus der Search Console mit zwei Klicks geht:
[bing.com/webmasters](https://www.bing.com/webmasters) → *Import from GSC*.

## 4. Google Business Profile (lokales SEO)

Für die Suchanfragen „FBA Prep Center Bayern / München / Freilassing“ ist ein
Eintrag im **Google Business Profile** der wirksamste einzelne Hebel:
[business.google.com](https://business.google.com) → Unternehmen anlegen →
Kategorie *Logistikdienstleister* bzw. *Lagerhaus* → Adresse Lindenstraße 21,
83395 Freilassing → Verifizierung per Postkarte abwarten.

Wichtig: Name, Adresse und E-Mail müssen **exakt** so geschrieben sein wie im
Impressum. Uneinheitliche NAP-Daten (Name/Address/Phone) schwächen das lokale
Ranking.

## 5. Analytics aktivieren (optional)

Standardmäßig ist **kein** Tracking aktiv – deshalb stimmt die aktuelle
Datenschutzerklärung. Zum Aktivieren in `js/analytics.js`:

```js
var PROVIDER = "plausible";        // oder "ga4"
var PLAUSIBLE_DOMAIN = "prepcenterfba.eu";
```

Das Skript lädt erst, wenn im Cookie-Banner **„Alle akzeptieren“** geklickt
wurde. Ohne Einwilligung geht kein einziger Request an den Anbieter.

**Bei Google Analytics 4 zusätzlich erforderlich:**
In `datenschutz.html` einen Abschnitt „Webanalyse mit Google Analytics“
ergänzen (Anbieter, Zweck, Rechtsgrundlage Art. 6 Abs. 1 lit. a DSGVO,
Speicherdauer, Drittlandtransfer in die USA, Widerrufsmöglichkeit).
Plausible ist die einfachere Variante: cookiefrei, EU-Hosting, keine
personenbezogenen Daten – dafür genügt ein kurzer Hinweis.

---

## 6. Wie die Sprachversionen gepflegt werden

**Die deutschen Dateien im Wurzelverzeichnis sind die Quelle.** Die Ordner
`/en/`, `/it/` und `/fr/` werden daraus erzeugt und sollten **nicht** von Hand
bearbeitet werden – Änderungen dort gehen beim nächsten Build verloren.

Ablauf bei einer Textänderung:

1. Deutschen Text in der Datei im Wurzelverzeichnis ändern.
2. Passt der Text zu einem `data-i18n="…"`-Schlüssel, die Übersetzungen in
   `js/lang/en.js`, `js/lang/it.js` und `js/lang/fr.js` nachziehen.
3. Neu bauen:

```bash
python3 tools/apply_seo.py      # canonical, hreflang, JSON-LD auffrischen
python3 tools/build_langs.py    # /en/ /it/ /fr/ neu erzeugen
python3 tools/gen_sitemap.py    # sitemap.xml + robots.txt
```

Wer das nicht lokal ausführen möchte: Der GitHub-Workflow
`.github/workflows/build-i18n.yml` erledigt genau diese drei Schritte bei
jedem Push automatisch und committet das Ergebnis zurück.

---

## 7. Nächste inhaltliche Schritte

Die Keyword-Analyse empfiehlt 30–50 unterstützende Artikel. Die Struktur dafür
steht bereits; sinnvolle Reihenfolge nach erwartetem Ertrag:

1. **Was ist ein FBA Prep Center?** – Einstiegsfrage mit dem größten Volumen.
2. **Amazon FBA Verpackungsanforderungen** – ausführliche Checkliste.
3. **FNSKU vs. EAN – der Unterschied** – klassische Verständnisfrage.
4. **Amazon FBA Kartonanforderungen** (Gewicht, Etikett, Beschriftung).
5. **FBA vs. FBM – was lohnt sich wann?**
6. **Prep Center oder 3PL – was brauche ich?**
7. **Ware aus China nach Amazon Deutschland liefern** – Einfuhr, Zoll, Prep.
8. **Amazon Lagergebühren vs. externe Lagerung** – Rechenbeispiel.

Jeder Artikel sollte auf die passende kommerzielle Seite verlinken
(z. B. Verpackungsartikel → `fnsku-etikettierung.html`) und auf zwei bis drei
thematisch benachbarte Artikel.

**Was den Ausschlag gibt, sobald die Technik steht:** echte Fotos vom eigenen
Lager statt Stockmaterial, überprüfbare Referenzen und Fallbeispiele. Die
Wettbewerber, die in der Analyse vorne liegen, unterscheiden sich vor allem
dadurch – nicht durch mehr Keywords.

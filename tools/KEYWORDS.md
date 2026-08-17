# Keyword-Mapping — prepcenterfba.eu

Umsetzung der Keyword-Analyse vom 17.08.2026. Eine dominante Suchintention
pro URL; jede URL hat genau ein Haupt-Keyword im `<title>` und in der `<h1>`.

---

## Umgesetzte Seiten

| URL (DE) | Haupt-Keyword | Neben-Keywords |
|---|---|---|
| `/` | FBA Prep Center Deutschland | Amazon Prep Center Germany · FBA Prep Services Germany · Prep Center Deutschland |
| `/fba-prep-center-deutschland.html` | FBA Prep Center Deutschland | Was ist ein FBA Prep Center · FBA Prep Kosten · Amazon Prep Service Deutschland · FBA Vorbereitung Deutschland |
| `/services.html` | Amazon FBA Prep Services | FBA Preparation · Amazon Packaging Service · FBA Product Preparation |
| `/fnsku-etikettierung.html` | FNSKU-Etikettierung | FNSKU Labeling Germany · Amazon Produkte etikettieren · FBA Etikettierung · Amazon Relabeling |
| `/fba-lagerung-deutschland.html` | FBA Lagerung Deutschland | FBA Storage Germany · Pre FBA Storage · Amazon Lagerung Deutschland · Amazon Seller Warehouse |
| `/versand-an-amazon.html` | Versand an Amazon FBA | Shipping to Amazon Germany · FBA Inbound Germany · Amazon Pallet Shipping · FBM Fulfillment |
| `/amazon-retouren-deutschland.html` | Amazon Retouren Deutschland | Amazon Returns Germany · FBA Removal Orders · Amazon Returns Processing · Retourenbearbeitung |
| `/fba-prep-center-bayern.html` | FBA Prep Center Bayern | FBA Prep Center Bavaria · Prep Center München · Fulfillment Center Bayern · 3PL Bayern |
| `/pricing.html` | FBA Prep Preise | FBA Prep Center Germany Prices · Amazon Prep Center Kosten · FBA Prep Costs |
| `/faq.html` | FBA Prep FAQ | Wie lange dauert FBA Prep · Amazon FBA Prep Requirements · FBA Prep Checklist |
| `/ueber-uns.html` | (Marke) | reliable FBA prep center Germany · inhabergeführtes Prep Center |
| `/kontakt.html` | (Marke/lokal) | FBA Prep Center Freilassing · Anlieferung Prep Center |

Slugs je Sprache siehe `tools/seo.py` → `PAGES`. Beispiel:
`/en/fba-prep-center-germany.html`, `/it/fba-prep-center-germania.html`,
`/fr/fba-prep-center-allemagne.html`.

---

## Noch offene Cluster aus der Analyse

Diese Themen haben laut Analyse eigenes Suchvolumen, sind aber noch nicht
umgesetzt. Reihenfolge = empfohlene Priorität.

| Geplante URL | Haupt-Keyword | Warum lohnend |
|---|---|---|
| `/fulfillment-deutschland.html` | Fulfillment Germany | Großer Cluster (3PL, E-Commerce Fulfillment, Fulfillment Center Deutschland) |
| `/fbm-versand.html` | FBM Fulfillment Germany | Eigenständige Intention neben FBA |
| `/bundling-multipacking.html` | FBA Bundling | Konkrete Serviceanfrage, wenig Wettbewerb |
| `/qualitaetskontrolle-amazon.html` | Amazon Qualitätskontrolle | „Inspection before FBA“ als Kaufauslöser |
| `/polybag-verpackung.html` | Polybagging Service | Sehr spezifisch, hohe Konversion |
| `/gefahrgut-fba.html` | Amazon Hazmat Germany | Kleiner Markt, kaum Wettbewerb — **nur anlegen, wenn wirklich angeboten** |
| `/online-arbitrage-prep-center.html` | Online Arbitrage Prep Center | Käufergruppe mit hoher Frequenz |
| `/wholesale-fba-prep.html` | Wholesale FBA Prep | Größere Volumina pro Kunde |
| `/private-label-fba-prep.html` | Private Label Prep Center | Höherwertige Kunden |
| `/prep-center-fuer-internationale-verkaeufer.html` | FBA Prep for international sellers | Deckt „Selling on Amazon Germany from USA/UK/China“ ab |

---

## Regeln, an die sich der Bestand hält

1. **Eine Intention pro URL.** Die Startseite versucht nicht, für alle
   Begriffe zu ranken, sondern verlinkt über den Themen-Hub auf die
   Detailseiten.
2. **Keyword in `<title>`, `<h1>` und in den ersten 100 Wörtern** — aber im
   Fließtext, nicht als Aufzählung.
3. **Keine Doorway-Pages.** Lokale Seiten nur für Regionen mit echtem Bezug.
   Deshalb gibt es `fba-prep-center-bayern.html` (dort steht das Lager), aber
   keine austauschbaren Klone für Berlin, Hamburg oder Köln.
4. **Interne Verlinkung in beide Richtungen:** Hub → Detailseite über den
   Themen-Hub der Startseite, Detailseite → Hub und Nachbarseiten über
   „Weiterführende Seiten“.
5. **Preise sichtbar.** Konkrete Zahlen im Text (0,39 € / 0,79 € / 25,00 €)
   bedienen Long-Tail-Suchen wie „FBA prep center Germany prices“ und
   erzeugen Rich Results über das `Offer`-Markup.
6. **Marken-Disclaimer** im Footer jeder Seite — nominative Markennennung,
   damit die zahlreichen „Amazon …“-Keywords rechtlich unbedenklich bleiben.

---

## Vollständige Keyword-Listen

Die kompletten Listen aus der Analyse (13 Kategorien, rund 250 Begriffe)
stehen in `Analiza_SEO_FBA_Prep_Germania.pdf`. Dieses Dokument bildet nur die
Zuordnung Keyword → URL ab; die Rohlisten gehören nicht in die Website.

**Nächster sinnvoller Schritt:** 100–200 dieser Begriffe in der Google Search
Console gegen die tatsächlichen Impressionen prüfen und die Seiten mit
Positionen zwischen 8 und 20 gezielt ausbauen. Das bringt mehr als neue
Seiten für Begriffe ohne nachgewiesene Nachfrage.

# -*- coding: utf-8 -*-
"""Generiert die deutschsprachige Blog-/Ratgeber-Sektion unter /blog/.

Aufruf aus dem Projekt-Root:

    python3 tools/gen_blog.py

Erzeugt /blog/index.html (Uebersicht) und je Eintrag aus ARTICLES eine
Detailseite /blog/<slug>.html.

Die Sektion existiert bewusst nur auf Deutsch: Zielgruppe der Ratgeber sind
deutschsprachige Haendler. Die Seiten sind deshalb in seo.py unter DE_ONLY
registriert und werden von build_langs.py NICHT uebersetzt.

Neuen Artikel anlegen: einen Eintrag ans ENDE von ARTICLES haengen
(neueste zuerst = Liste wird nach date absteigend sortiert), danach

    python3 tools/gen_blog.py && python3 tools/gen_sitemap.py
"""
import os, re, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo import DOMAIN, breadcrumbs

BLOG_DIR  = "blog"
BLOG_URL  = DOMAIN + "/blog/"
ORG_ID    = DOMAIN + "/#organization"
SITE_ID   = DOMAIN + "/#website"
OG_FALLBACK = "/assets/hero-bg-De6VYLKg.jpg"

# Wurzel-relative Links: die Blog-Seiten liegen in /blog/, deshalb duerfen
# hier keine "./"-Pfade stehen. main.js liest das aus window.PH_LINKS.
LINKS = {
    "home": "/", "services": "/services.html", "pricing": "/pricing.html",
    "calculator": "/kalkulator.html", "about": "/ueber-uns.html", "faq": "/faq.html",
    "contact": "/kontakt.html", "pillar": "/fba-prep-center-deutschland.html",
    "labeling": "/fnsku-etikettierung.html", "storage": "/fba-lagerung-deutschland.html",
    "shipping": "/versand-an-amazon.html", "returns": "/amazon-retouren-deutschland.html",
    "imprint": "/impressum.html", "privacy": "/datenschutz.html", "terms": "/agb.html",
    "blog": "/blog/",
}

MONTHS = {1:"Januar",2:"Februar",3:"März",4:"April",5:"Mai",6:"Juni",7:"Juli",
          8:"August",9:"September",10:"Oktober",11:"November",12:"Dezember"}


def de_date(iso):
    y, m, d = iso.split("-")
    return "%d. %s %s" % (int(d), MONTHS[int(m)], y)


def detect_css():
    """Fingerprint der CSS-Datei aus index.html lesen, damit Rebuilds passen."""
    try:
        m = re.search(r'href="(/assets/style-[^"]+\.css)"', open("index.html", encoding="utf-8").read())
        if m:
            return m.group(1)
    except OSError:
        pass
    return "/assets/style-STZ1_Fzx.css"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


# ── Bausteine ───────────────────────────────────────────────────────────────

PROSE_CSS = """
    .prose{max-width:none}
    .prose h2{font-size:1.45rem;line-height:1.3;margin:2.4rem 0 .85rem}
    .prose h2:first-child{margin-top:0}
    .prose h3{font-size:1.12rem;line-height:1.35;margin:1.8rem 0 .6rem}
    .prose p{margin-bottom:1rem;max-width:none}
    .prose ul,.prose ol{margin:0 0 1.15rem 1.15rem;padding:0}
    .prose li{margin-bottom:.45rem;padding-left:.2rem}
    .prose li>strong{color:#0f172a}
    .prose table{width:100%;border-collapse:collapse;margin:0 0 1.3rem;font-size:.92rem}
    .prose th,.prose td{border:1px solid #e2e8f0;padding:.6rem .7rem;text-align:left;vertical-align:top}
    .prose th{background:#f8fafc;font-weight:600}
    .prose td.num,.prose th.num{text-align:right;white-space:nowrap}
    .prose blockquote{margin:0 0 1.3rem;padding:.85rem 1.1rem;border-left:3px solid #1d4ed8;
      background:#f0f5ff;border-radius:0 8px 8px 0;font-size:.95rem;color:#1e3a8a}
    .prose blockquote p:last-child{margin-bottom:0}
    .article-meta{display:flex;flex-wrap:wrap;gap:.5rem 1rem;align-items:center;
      font-size:.85rem;color:#64748b;margin-top:.9rem}
    .article-meta time{font-variant-numeric:tabular-nums}
    .article-cover{width:100%;height:auto;aspect-ratio:16/7;object-fit:cover;
      border-radius:12px;margin-bottom:2rem;display:block}
    .toc{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:1rem 1.25rem;margin-bottom:2rem}
    .toc h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;color:#64748b;margin:0 0 .55rem}
    .toc ol{margin:0 0 0 1.1rem;font-size:.92rem}
    .toc li{margin-bottom:.3rem}
    .post-card{display:flex;flex-direction:column;background:#fff;border:1px solid #e2e8f0;
      border-radius:12px;overflow:hidden;box-shadow:0 1px 2px rgba(15,23,42,.04);
      transition:box-shadow .2s,transform .2s,border-color .2s;text-decoration:none;height:100%}
    .post-card:hover{box-shadow:0 8px 24px rgba(15,23,42,.09);transform:translateY(-2px);border-color:#1d4ed8}
    .post-card__img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}
    .post-card__body{padding:1.15rem 1.25rem 1.35rem;display:flex;flex-direction:column;gap:.5rem;flex:1}
    .post-card__title{font-size:1.02rem;font-weight:700;color:#0f172a;line-height:1.35;margin:0}
    .post-card__teaser{font-size:.9rem;color:#475569;margin:0;flex:1}
    .post-card__meta{font-size:.78rem;color:#94a3b8}
    .post-card__more{font-size:.88rem;font-weight:600;color:#1d4ed8}
    .post-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:1.5rem}
    @media(max-width:640px){.prose table{display:block;overflow-x:auto}}
"""

STAND_NOTE = ('<p class="muted-note" style="margin-top:2rem">Stand: %s. Amazon '
              'ändert Anforderungen und Gebühren regelmäßig – maßgeblich ist immer die '
              'aktuelle Fassung in Seller Central. Dieser Beitrag ist eine allgemeine '
              'Information und ersetzt keine Rechts- oder Steuerberatung.</p>')


def head(title, desc, canonical, image, extra_ld, published=None, modified=None):
    css = detect_css()
    ld = json.dumps({"@context": "https://schema.org", "@graph": extra_ld},
                    ensure_ascii=False, indent=2)
    og_img = DOMAIN + image
    return """<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%(title)s</title>
  <meta name="description" content="%(desc)s">
  <meta name="robots" content="index, follow">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="stylesheet" href="%(css)s">
  <link rel="canonical" href="%(canon)s">
  <link rel="alternate" hreflang="de" href="%(canon)s">
  <link rel="alternate" hreflang="x-default" href="%(canon)s">
  <meta property="og:type" content="%(ogtype)s">
  <meta property="og:title" content="%(title)s">
  <meta property="og:description" content="%(desc)s">
  <meta property="og:url" content="%(canon)s">
  <meta property="og:image" content="%(ogimg)s">
  <meta property="og:site_name" content="PrepCenter FBA">
  <meta property="og:locale" content="de_DE">%(artmeta)s
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="%(title)s">
  <meta name="twitter:description" content="%(desc)s">
  <meta name="twitter:image" content="%(ogimg)s">
  <script type="application/ld+json">
%(ld)s
  </script>
  <style>%(prose)s  </style>
</head>
<body>

<a href="#main-content" class="skip-link">Zum Inhalt springen</a>

<div id="site-header"></div>

<main id="main-content">
""" % {
        "title": esc(title), "desc": esc(desc), "css": css, "canon": canonical,
        "ogimg": og_img, "ld": ld, "prose": PROSE_CSS,
        "ogtype": "article" if published else "website",
        "artmeta": ("\n  <meta property=\"article:published_time\" content=\"%s\">"
                    "\n  <meta property=\"article:modified_time\" content=\"%s\">"
                    % (published, modified or published)) if published else "",
    }


def tail(self_url):
    links = json.dumps(LINKS, ensure_ascii=False)
    langs = json.dumps({"de": self_url.replace(DOMAIN, ""), "en": "/en/",
                        "it": "/it/", "fr": "/fr/"}, ensure_ascii=False)
    return """
</main>

<div id="site-footer"></div>

<script>window.PH_FORCE_LANG="de";window.PH_LINKS=%s;window.PH_LANG_URLS=%s;</script>
<script defer src="/js/config.js"></script>
<script defer src="/js/i18n.js"></script>
<script defer src="/js/main.js"></script>
</body>
</html>
""" % (links, langs)


def cta_band(title, sub):
    return """
<section class="cta-band" aria-labelledby="post-cta">
  <div class="container">
    <h2 id="post-cta">%s</h2>
    <p>%s</p>
    <div class="btn-group">
      <a href="/kontakt.html" class="btn btn--primary btn--lg">Angebot anfragen</a>
      <a href="/kalkulator.html" class="btn btn--outline-light btn--lg">Kosten berechnen</a>
    </div>
  </div>
</section>
""" % (esc(title), esc(sub))


# ── Artikel ─────────────────────────────────────────────────────────────────
# body: reines HTML (h2/h3/p/ul/table). Keine data-i18n-Attribute – die
# Sektion ist deutschsprachig und wird nicht uebersetzt.

ARTICLES = []

ARTICLES.append({
 "slug": "fba-prep-selbst-machen-oder-auslagern.html",
 "title": "FBA Prep selbst machen oder auslagern? Ein ehrlicher Kostenvergleich",
 "meta_title": "FBA Prep selbst machen oder auslagern – Kostenvergleich 2026 | PrepCenter FBA",
 "desc": "Lohnt sich ein FBA Prep Center oder machen Sie es besser selbst? Wir rechnen beide Varianten mit echten Zahlen durch – inklusive der Kosten, die die meisten Händler vergessen.",
 "badge": "Kosten & Kalkulation", "badge_class": "badge--blue",
 "date": "2026-08-04", "modified": "2026-08-18", "reading": 8,
 "image": "/assets/quality-control-BXDDtJQ9.jpg",
 "image_alt": "Qualitätskontrolle von Amazon-FBA-Ware im Prep Center",
 "teaser": "Die Frage ist nicht „0,79 € pro Einheit – ist das viel?“, sondern: Was kostet Sie eine Stunde Ihrer Zeit, und was kostet eine abgelehnte Sendung?",
 "toc": [("Die falsche Rechnung", "falsch"), ("Was Selbermachen wirklich kostet", "selbst"),
         ("Rechenbeispiel: 500 Einheiten", "beispiel"), ("Was ein Prep Center kostet", "prep"),
         ("Wann Selbermachen die bessere Wahl ist", "wann-selbst"),
         ("Wann sich Auslagern rechnet", "wann-auslagern"),
         ("Die Kosten, die niemand einplant", "versteckt")],
 "body": """
<h2 id="falsch">Die falsche Rechnung</h2>
<p>Fast jeder Händler, der zum ersten Mal über ein Prep Center nachdenkt, rechnet so: „0,79 € pro Einheit mal 500 Einheiten sind 395 €. Das mache ich lieber selbst.“ Diese Rechnung ist nicht falsch – sie ist nur unvollständig. Sie vergleicht einen Preis mit null, statt zwei Kostenblöcke miteinander.</p>
<p>Selbermachen ist nicht kostenlos. Es kostet Zeit, Material, Lagerfläche und – der teuerste Posten – Fehler. Die ehrliche Frage lautet: <strong>Was kostet mich eine Einheit, wenn ich sie selbst vorbereite, alles eingerechnet?</strong></p>

<h2 id="selbst">Was Selbermachen wirklich kostet</h2>
<p>Fünf Posten, die in der Kalkulation auftauchen müssen:</p>
<ul>
  <li><strong>Ihre Arbeitszeit.</strong> Eine geübte Person schafft bei einfachen Artikeln etwa 60–120 Einheiten pro Stunde (etikettieren, polybaggen, in den Versandkarton packen). Bei Bundles, empfindlicher Ware oder Sets sind es deutlich weniger.</li>
  <li><strong>Material.</strong> Polybeutel in zulässiger Stärke, Luftpolsterfolie, Etiketten, Versandkartons, Klebeband, Füllmaterial. Im Kleineinkauf zahlen Sie hier ein Vielfaches dessen, was ein Betrieb zahlt, der palettenweise bestellt.</li>
  <li><strong>Fläche.</strong> Ein Kubikmeter Ware im Wohnzimmer ist gratis. Zwanzig Kubikmeter sind es nicht – spätestens dann mieten Sie an, und die Miete läuft auch in schwachen Monaten weiter.</li>
  <li><strong>Wege.</strong> Anfahrt zum Paketshop oder Warten auf die Spedition, pro Sendung, immer wieder.</li>
  <li><strong>Fehlerkosten.</strong> Der Posten, den niemand einplant – dazu unten mehr.</li>
</ul>

<h2 id="beispiel">Rechenbeispiel: 500 Einheiten</h2>
<p>Nehmen wir einen typischen Fall: 500 Einheiten eines einfachen Artikels, die etikettiert, in einen Polybeutel verpackt und als FBA-Sendung an Amazon geschickt werden. Die Annahmen stehen offen daneben – ersetzen Sie sie durch Ihre eigenen.</p>
<table>
  <thead><tr><th>Posten</th><th>Annahme</th><th class="num">Kosten</th></tr></thead>
  <tbody>
    <tr><td>Arbeitszeit</td><td>80 Einheiten/Std. → 6,25 Std., bewertet mit 25 €/Std.</td><td class="num">156,25 €</td></tr>
    <tr><td>Material</td><td>Polybeutel, Etiketten, Kartons, Klebeband im Kleineinkauf</td><td class="num">ca. 60,00 €</td></tr>
    <tr><td>Wege / Übergabe</td><td>1 Std. inkl. Fahrt und Wartezeit</td><td class="num">25,00 €</td></tr>
    <tr><td>Fläche</td><td>anteilig, wenn Sie ohnehin Lager zahlen</td><td class="num">variabel</td></tr>
    <tr><td><strong>Summe selbst</strong></td><td>ohne Fehlerkosten</td><td class="num"><strong>ca. 241 € = 0,48 €/Einheit</strong></td></tr>
  </tbody>
</table>
<p>Auf dem Papier gewinnt das Selbermachen – solange Ihre Stunde 25 € wert ist, nichts schiefgeht und Sie die Fläche ohnehin haben. Setzen Sie Ihre Stunde mit 60 € an, weil Sie in dieser Zeit Produkte recherchieren, Listings optimieren oder mit Lieferanten verhandeln könnten, dreht sich das Ergebnis: dieselbe Sendung kostet Sie dann rund 0,94 € pro Einheit.</p>
<blockquote><p>Der ehrliche Maßstab ist nicht Ihr Mindestlohn, sondern das, was Sie in derselben Stunde sonst verdient hätten. Wer 6 Stunden etikettiert statt einen Lieferanten zu verhandeln, zahlt den teuersten Stundensatz im Unternehmen.</p></blockquote>

<h2 id="prep">Was ein Prep Center kostet</h2>
<p>Unsere Preise sind netto und öffentlich – Sie müssen dafür kein Angebot anfordern:</p>
<table>
  <thead><tr><th>Leistung</th><th>Einheit</th><th class="num">Preis</th></tr></thead>
  <tbody>
    <tr><td>FBA Komplett-Prep</td><td>pro Einheit</td><td class="num">0,79 €</td></tr>
    <tr><td>Nur FNSKU-Etikettierung</td><td>pro Einheit</td><td class="num">0,39 €</td></tr>
    <tr><td>Qualitätskontrolle</td><td>pro Einheit</td><td class="num">0,25 €</td></tr>
    <tr><td>Polybag-Verpackung inkl. Material</td><td>pro Einheit</td><td class="num">0,29 €</td></tr>
    <tr><td>Wareneingang Karton (mit Prep)</td><td>pro Karton</td><td class="num">0,00 €</td></tr>
    <tr><td>FBA Karton-Handling (Ausgang)</td><td>pro Karton</td><td class="num">2,90 €</td></tr>
  </tbody>
</table>
<p>Für die 500 Einheiten aus dem Beispiel: 500 × 0,79 € = 395 € Komplett-Prep, plus Karton-Handling für den Ausgang. Wer nur etikettieren lässt und selbst verpackt, zahlt 500 × 0,39 € = 195 €. Es gibt keine Mindestmenge an Einheiten, sondern nur einen Mindestauftragswert von 25,00 € netto je Prep-Auftrag – und für die ersten beiden Lieferungen einen Neukundenrabatt von 10 % und 5 %.</p>
<p>Den vollständigen Vergleich mit Ihren eigenen Mengen rechnen Sie in zwei Minuten im <a href="/kalkulator.html">Kostenkalkulator</a> durch.</p>

<h2 id="wann-selbst">Wann Selbermachen die bessere Wahl ist</h2>
<p>Wir verkaufen Prep-Leistungen – trotzdem ist die ehrliche Antwort manchmal „machen Sie es selbst“:</p>
<ul>
  <li><strong>Kleine Testmengen.</strong> Bei 30 Einheiten eines neuen Produkts lohnt der Transportweg zu uns oft nicht. Testen Sie erst, skalieren Sie danach.</li>
  <li><strong>Sehr erklärungsbedürftige Handgriffe.</strong> Wenn jede Einheit eine Sichtprüfung braucht, die nur Sie leisten können, weil Sie das Produkt entwickelt haben.</li>
  <li><strong>Freie Zeit ohne Alternative.</strong> Wer nebenberuflich startet und abends ohnehin Zeit hat, für die es keinen anderen Verwendungszweck gibt, kalkuliert anders.</li>
  <li><strong>Ware liegt bereits bei Ihnen.</strong> Bestand, der schon in Ihrem Lager steht, noch einmal quer durch Deutschland zu fahren, ergibt selten Sinn.</li>
</ul>

<h2 id="wann-auslagern">Wann sich Auslagern rechnet</h2>
<ul>
  <li><strong>Der Container kommt direkt aus Asien.</strong> Dann geht die Ware ohnehin an eine Adresse in Deutschland – und Ihre Wohnung ist die falsche.</li>
  <li><strong>Ab etwa 300–500 Einheiten pro Monat regelmäßig.</strong> Ab da ist Prep kein Nebenbei mehr, sondern ein zweiter Job.</li>
  <li><strong>Sie sitzen nicht in Deutschland.</strong> Für Händler aus dem Ausland ist ein deutscher Eingangspunkt fast immer günstiger als jede Eigenlösung.</li>
  <li><strong>Sie wachsen.</strong> Prep-Kapazität, die Sie nicht selbst aufbauen, müssen Sie auch nicht wieder abbauen, wenn ein Produkt ausläuft.</li>
  <li><strong>Saisonspitzen.</strong> Im Q4 kostet Sie jeder Tag, an dem die Ware nicht im FBA-Netz liegt, echten Umsatz.</li>
</ul>

<h2 id="versteckt">Die Kosten, die niemand einplant</h2>
<p>Der Posten, der beide Rechnungen kippt, taucht in keiner Tabelle auf: <strong>eine Sendung, die Amazon beanstandet.</strong></p>
<ul>
  <li>Ware, die falsch oder gar nicht etikettiert ankommt, kann Amazon kostenpflichtig nachbearbeiten – oder die Sendung wird beanstandet und Ihr Bestand ist tagelang nicht verkäuflich.</li>
  <li>Fehlende Erstickungswarnung, falsche Beutelstärke oder ein sichtbarer Herstellerbarcode sind Klassiker, die eine ganze Palette betreffen können – nicht eine Einheit.</li>
  <li>Im Q4 kostet eine verlorene Woche Verfügbarkeit oft mehr als die gesamte Prep-Rechnung des Jahres.</li>
</ul>
<p>Welche Fehler das konkret sind und wie Sie sie vermeiden, steht ausführlich in unserem Beitrag <a href="/blog/amazon-wareneingang-abgelehnt-prep-fehler.html">Amazon-Wareneingang abgelehnt</a>.</p>

<h2>Fazit</h2>
<p>Rechnen Sie nicht Prep-Preis gegen null, sondern Vollkosten gegen Vollkosten. Setzen Sie Ihre Stunde mit dem an, was sie in Ihrem Unternehmen tatsächlich wert ist, addieren Sie Material und Wege und legen Sie ein realistisches Risiko für Beanstandungen dazu. Bei kleinen Testmengen gewinnt fast immer das Selbermachen. Ab dem Punkt, an dem Prep regelmäßig Ihre Woche blockiert, gewinnt fast immer das Auslagern – nicht wegen des Preises pro Einheit, sondern wegen der Stunden, die Sie zurückbekommen.</p>
""",
 "faq": [
   ("Gibt es eine Mindestmenge an Einheiten?",
    "Nein. Es gilt lediglich ein Mindestauftragswert von 25,00 € netto je Einzelauftrag für Prep-Leistungen. Reine Lager-, Auslieferungs- und Retourenaufträge lösen keinen Zuschlag aus."),
   ("Rechnet sich ein Prep Center auch bei niedrigen Margen?",
    "Das hängt vom Deckungsbeitrag pro Einheit ab, nicht vom Verkaufspreis. Bei 0,79 € Komplett-Prep brauchen Sie rund 1 € zusätzlichen Deckungsbeitrag pro Einheit, um die Auslagerung zu tragen. Bei sehr dünnen Margen kann es sinnvoller sein, nur die Etikettierung auszulagern und selbst zu verpacken."),
   ("Was passiert, wenn Amazon meine Sendung trotzdem beanstandet?",
    "Wir dokumentieren jede Charge mit Stückzahl und Fotos. Diese Dokumentation können Sie in einem Fall gegenüber Amazon verwenden. Fehler, die auf unserer Seite entstanden sind, korrigieren wir auf unsere Kosten."),
 ],
 "related": [("/kalkulator.html", "Kostenkalkulator – eigene Mengen durchrechnen"),
             ("/pricing.html", "Vollständige Preisliste"),
             ("/was-kostet-fba-prep.html", "Was kostet FBA Prep? Überblick"),
             ("/fba-prep-center-deutschland.html", "FBA Prep Center Deutschland – Überblick")],
 "cta": ("Rechnen wir Ihren Fall durch", "Sagen Sie uns Produkt, Menge und Prep-Schritte – Sie bekommen eine konkrete Kalkulation, keine Preisspanne."),
})

ARTICLES.append({
 "slug": "amazon-wareneingang-abgelehnt-prep-fehler.html",
 "title": "Amazon-Wareneingang abgelehnt: die 8 häufigsten Prep-Fehler",
 "meta_title": "Amazon Wareneingang abgelehnt – 8 häufige Prep-Fehler vermeiden | PrepCenter FBA",
 "desc": "Warum Amazon FBA-Sendungen beanstandet: Polybeutel, Erstickungswarnung, FNSKU, Sets, Flüssigkeiten, Kartongewicht. Die häufigsten Prep-Fehler und wie Sie sie vermeiden.",
 "badge": "Prep-Praxis", "badge_class": "badge--amber",
 "date": "2026-08-11", "modified": "2026-08-18", "reading": 9,
 "image": "/assets/polybag-packaging-CJ17IaPp.jpg",
 "image_alt": "Produkte werden nach Amazon-Vorgaben in Polybeutel verpackt",
 "teaser": "Fast alle Beanstandungen gehen auf eine Handvoll immer gleicher Fehler zurück. Wer sie kennt, vermeidet sie in fünf Minuten Vorbereitung.",
 "toc": [("1 · Falsche Beutelstärke", "f1"), ("2 · Fehlende Erstickungswarnung", "f2"),
         ("3 · Sichtbarer Herstellerbarcode", "f3"), ("4 · Unlesbares oder falsch platziertes Etikett", "f4"),
         ("5 · Sets, die auseinanderfallen", "f5"), ("6 · Flüssigkeiten ohne sichere Verschlüsse", "f6"),
         ("7 · Scharfe und zerbrechliche Artikel", "f7"), ("8 · Kartongewicht und Palettenvorgaben", "f8"),
         ("Vor dem Versand: kurze Checkliste", "checkliste")],
 "body": """
<p>Eine beanstandete FBA-Sendung kostet selten nur Geld. Sie kostet vor allem Zeit: Der Bestand ist nicht verkäuflich, die Klärung dauert, und im schlimmsten Fall betrifft der Fehler nicht eine Einheit, sondern die ganze Palette. Die gute Nachricht: Es sind fast immer dieselben acht Fehler.</p>
<p>Die folgenden Vorgaben stammen aus Amazons Versand- und Verpackungsleitfaden für Deutschland. Amazon passt die Anforderungen regelmäßig an – prüfen Sie im Zweifel die aktuelle Fassung in Seller Central.</p>

<h2 id="f1">1 · Falsche Beutelstärke</h2>
<p>Polybeutel müssen eine <strong>Folienstärke von mindestens 0,09 mm</strong> haben. Die dünnen Beutel aus dem Bürobedarf reißen im FBA-Netz und erfüllen die Vorgabe nicht. Zweite, oft übersehene Regel: Der Beutel darf <strong>nicht mehr als 7,5 cm länger oder breiter</strong> sein als das Produkt selbst. Ein „passt schon“-Beutel, in dem der Artikel herumrutscht, ist ein Grund für Beanstandungen.</p>
<p>Der Beutel muss außerdem transparent sein, und der Barcode muss durch die Folie hindurch scanbar bleiben – oder außen auf dem Beutel sitzen.</p>

<h2 id="f2">2 · Fehlende Erstickungswarnung</h2>
<p>Kunststoffbeutel mit einer <strong>Öffnung von 12 cm oder mehr</strong> müssen eine Erstickungswarnung tragen. Sie kann aufgedruckt oder als Etikett aufgebracht sein. Das ist der mit Abstand häufigste Einzelfehler bei Erstlieferungen – und einer, der eine komplette Charge betrifft, weil der Beutel für alle Einheiten derselbe ist.</p>
<p>Der Warnhinweis muss lesbar sein; bei Ware für den deutschen Markt gehört der deutsche Text dazu.</p>

<h2 id="f3">3 · Sichtbarer Herstellerbarcode</h2>
<p>Wenn Sie mit einem Amazon-Barcode (FNSKU) arbeiten, muss der <strong>Original-Barcode des Herstellers – UPC, EAN, ISBN – vollständig abgedeckt</strong> sein. Bleiben zwei scanbare Codes auf der Einheit, entscheidet der Zufall, welchen der Scanner liest. Genau daraus entstehen falsch eingebuchte Bestände und Vermischungen mit fremder Ware.</p>
<p>Abdecken heißt: überkleben, nicht durchstreichen. Ein durchgestrichener Code bleibt maschinenlesbar.</p>

<h2 id="f4">4 · Unlesbares oder falsch platziertes Etikett</h2>
<ul>
  <li>Das Etikett muss <strong>außen an jeder Einheit</strong> sitzen und <strong>leicht zugänglich</strong> sein – nicht unter der Schrumpffolie, nicht auf der Unterseite eines schweren Kartons.</li>
  <li>Es darf nicht über Kanten, Falze oder Nähte geklebt werden: Der Scanner scheitert an jeder Knickstelle im Barcode.</li>
  <li>Jedes Etikett muss <strong>24 Monate lang lesbar und scanfähig</strong> bleiben. Thermodirekt-Etiketten, die in einem warmen Lager verblassen, erfüllen das nicht zuverlässig.</li>
  <li>Kein Klebeband über dem Barcode – glänzendes Band bricht die Lesbarkeit.</li>
</ul>
<p>Details zur richtigen Auszeichnung finden Sie unter <a href="/fnsku-etikettierung.html">FNSKU-Etikettierung</a> und im Beitrag <a href="/blog/fnsku-ean-asin-barcodes-amazon.html">FNSKU, EAN und ASIN im Vergleich</a>.</p>

<h2 id="f5">5 · Sets, die auseinanderfallen</h2>
<p>Ein Bundle ist für Amazon eine Einheit – aber nur, wenn es auch so gekennzeichnet ist. Auf dem Set muss ein Hinweis wie <strong>„Wird im Set verkauft“ oder „Versandfertig, nicht trennen“</strong> stehen. Fehlt er, werden die Einzelteile im Wareneingang getrennt, und Ihr Bundle existiert im Bestand nicht mehr.</p>
<p>Das Set braucht außerdem eine eigene, übergreifende Auszeichnung – die Einzelbarcodes der Bestandteile dürfen nicht mehr scanbar sein.</p>

<h2 id="f6">6 · Flüssigkeiten ohne sichere Verschlüsse</h2>
<ul>
  <li>Einzeleinheiten mit <strong>maximal 1 Liter</strong> Volumen.</li>
  <li><strong>Doppelt versiegelter Schraubverschluss</strong> – Induktionssiegel plus Deckel, nicht nur ein aufgesteckter Verschluss.</li>
  <li>Die Einheit muss einen <strong>Falltest</strong> überstehen, ohne dass etwas ausläuft oder bricht.</li>
</ul>
<p>Auslaufende Ware beschädigt nicht nur die eigene Sendung, sondern auch fremde Bestände im Regal – Amazon reagiert hier entsprechend deutlich.</p>

<h2 id="f7">7 · Scharfe und zerbrechliche Artikel</h2>
<p>Bei scharfen Gegenständen muss die Verpackung das scharfe Element <strong>vollständig abdecken</strong>, sodass sich beim Greifen niemand verletzen kann. Zerbrechliche Artikel brauchen eine Polsterung, die einen Sturz im Fördersystem übersteht – Luftpolsterfolie ist hier kein Nice-to-have, sondern die Voraussetzung dafür, dass Ihre Retourenquote nicht Ihre Marge auffrisst.</p>

<h2 id="f8">8 · Kartongewicht und Palettenvorgaben</h2>
<ul>
  <li>Versandkartons sollen die <strong>Standardgrenze von 15 kg</strong> nicht überschreiten.</li>
  <li>Wiegt eine einzelne versandfähige Einheit mehr als <strong>30 kg</strong>, gehört sie auf eine Europalette und muss entsprechend gekennzeichnet werden.</li>
  <li>Mindesthaltbarkeitsdaten sind im Format <strong>TT-MM-JJJJ</strong> anzugeben – sowohl auf der Umverpackung als auch auf der Einzeleinheit.</li>
</ul>

<h2 id="checkliste">Vor dem Versand: kurze Checkliste</h2>
<ul class="checklist" role="list">
  <li class="checklist-item"><span class="checklist-item__icon"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8l3.5 3.5L13 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg></span><span>Beutelstärke mindestens 0,09 mm, maximal 7,5 cm größer als das Produkt</span></li>
  <li class="checklist-item"><span class="checklist-item__icon"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8l3.5 3.5L13 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg></span><span>Erstickungswarnung ab 12 cm Beutelöffnung vorhanden</span></li>
  <li class="checklist-item"><span class="checklist-item__icon"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8l3.5 3.5L13 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg></span><span>Herstellerbarcode überklebt, nur der FNSKU ist scanbar</span></li>
  <li class="checklist-item"><span class="checklist-item__icon"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8l3.5 3.5L13 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg></span><span>Etikett plan, außen, nicht über Kanten oder Klebeband</span></li>
  <li class="checklist-item"><span class="checklist-item__icon"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8l3.5 3.5L13 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg></span><span>Sets tragen den Hinweis „Wird im Set verkauft“</span></li>
  <li class="checklist-item"><span class="checklist-item__icon"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8l3.5 3.5L13 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg></span><span>Karton unter 15 kg, Schwergut auf Palette</span></li>
</ul>
<p>Wenn Sie diese Punkte nicht bei jeder Charge selbst durchgehen wollen: Genau das ist der Teil, den ein Prep Center übernimmt – inklusive Fotodokumentation, mit der Sie im Streitfall gegenüber Amazon etwas in der Hand haben.</p>
""",
 "faq": [
   ("Was passiert, wenn Amazon die Sendung beanstandet?",
    "Je nach Fehler bearbeitet Amazon die Ware kostenpflichtig nach, fordert Sie zur Korrektur auf oder nimmt die Einheiten nicht in den verkäuflichen Bestand auf. In allen Fällen ist Ihr Bestand für die Dauer der Klärung nicht verfügbar."),
   ("Muss die Erstickungswarnung auf Deutsch sein?",
    "Für Ware, die auf dem deutschen Markt verkauft wird, gehört der Warnhinweis in deutscher Sprache dazu. Mehrsprachige Aufdrucke sind üblich und zulässig."),
   ("Können Sie fehlende Warnhinweise nachträglich anbringen?",
    "Ja. Zusätzliche Etiketten – Warnhinweise, Sprach-Overlays oder Mindesthaltbarkeitsdaten – bringen wir für 0,25 € pro Etikett an. Bei falscher Beutelstärke verpacken wir neu."),
 ],
 "related": [("/fnsku-etikettierung.html", "FNSKU-Etikettierung – Ablauf und Preise"),
             ("/services.html", "Alle Prep-Leistungen im Überblick"),
             ("/versand-an-amazon.html", "Einlieferung an Amazon FBA"),
             ("/blog/fba-prep-selbst-machen-oder-auslagern.html", "Prep selbst machen oder auslagern?")],
 "cta": ("Erstlieferung ohne Beanstandung", "Schicken Sie uns Produktfotos und die geplante Menge – wir sagen Ihnen vorab, welche Prep-Schritte Amazon für diesen Artikel verlangt."),
})

ARTICLES.append({
 "slug": "fnsku-ean-asin-barcodes-amazon.html",
 "title": "FNSKU, EAN, ASIN und SKU: welcher Code wann auf die Ware gehört",
 "meta_title": "FNSKU, EAN, ASIN, SKU – welcher Barcode wann? Erklärung für FBA-Händler | PrepCenter FBA",
 "desc": "FNSKU, EAN, ASIN und SKU einfach erklärt: wofür jeder Code steht, wann Amazon welchen verlangt, was Bestandsvermischung bedeutet und welche Etikettierfehler teuer werden.",
 "badge": "Grundlagen", "badge_class": "badge--slate",
 "date": "2026-08-14", "modified": "2026-08-18", "reading": 7,
 "image": "/assets/fnsku-labeling-DqwPDHdL.jpg",
 "image_alt": "FNSKU-Etiketten werden auf Produkteinheiten aufgebracht",
 "teaser": "Vier Abkürzungen, die dauernd verwechselt werden – und eine Entscheidung dahinter, die darüber bestimmt, ob Ihre Ware im Amazon-Lager mit fremder Ware vermischt wird.",
 "toc": [("Die vier Codes in einem Satz", "ueberblick"), ("ASIN", "asin"), ("EAN/GTIN", "ean"),
         ("SKU", "sku"), ("FNSKU", "fnsku"),
         ("Die eigentliche Entscheidung: FNSKU oder Herstellerbarcode", "entscheidung"),
         ("Wann ein FNSKU zwingend ist", "pflicht"), ("Etiketten richtig drucken", "drucken"),
         ("Die fünf häufigsten Etikettierfehler", "fehler")],
 "body": """
<h2 id="ueberblick">Die vier Codes in einem Satz</h2>
<table>
  <thead><tr><th>Code</th><th>Vergeben von</th><th>Beantwortet die Frage</th></tr></thead>
  <tbody>
    <tr><td><strong>ASIN</strong></td><td>Amazon</td><td>Welches Produkt ist das im Amazon-Katalog?</td></tr>
    <tr><td><strong>EAN / GTIN</strong></td><td>GS1 (weltweit)</td><td>Welches Produkt ist das im Handel allgemein?</td></tr>
    <tr><td><strong>SKU</strong></td><td>Sie selbst</td><td>Wie nenne <em>ich</em> diesen Artikel intern?</td></tr>
    <tr><td><strong>FNSKU</strong></td><td>Amazon</td><td>Wem gehört diese konkrete Einheit im Lager?</td></tr>
  </tbody>
</table>
<p>Der letzte Punkt ist der entscheidende – und der Grund, warum es den FNSKU überhaupt gibt.</p>

<h2 id="asin">ASIN – die Produktseite</h2>
<p>Die ASIN (Amazon Standard Identification Number) identifiziert das <em>Listing</em>, nicht Ihre Ware. Verkaufen zehn Händler denselben Artikel, teilen sie sich eine ASIN und konkurrieren auf derselben Produktseite. Die ASIN wird nie auf die Ware geklebt.</p>

<h2 id="ean">EAN / GTIN – der Herstellerbarcode</h2>
<p>Die EAN ist der Barcode, den Sie aus dem Supermarkt kennen. Sie gehört zum Produkt, nicht zum Händler, und wird über GS1 vergeben. Für neue Listings verlangt Amazon in der Regel eine gültige GTIN – gekaufte „Billig-EANs“ aus zweifelhaften Quellen führen früher oder später zu Sperrungen, weil sie nicht auf Ihr Unternehmen registriert sind.</p>

<h2 id="sku">SKU – Ihre interne Nummer</h2>
<p>Die SKU (Stock Keeping Unit) vergeben Sie selbst, beim Anlegen des Angebots. Sie taucht in keinem Barcode auf der Ware auf, ist aber Ihr Anker in Berichten und in der Buchhaltung. Ein sprechendes Schema zahlt sich später aus, etwa <code>MARKE-PRODUKT-VARIANTE-CHARGE</code>.</p>

<h2 id="fnsku">FNSKU – das Etikett auf der Einheit</h2>
<p>Der FNSKU (Fulfillment Network Stock Keeping Unit) ist der Code, der tatsächlich auf jede physische Einheit kommt. Er verbindet die Einheit mit <strong>Ihrem</strong> Verkäuferkonto. Er beginnt typischerweise mit „X00…“ und wird von Amazon erzeugt, sobald Sie einen Artikel für den Versand durch Amazon anlegen.</p>
<p>Auf dem Etikett stehen neben dem Barcode der Titel und der Zustand der Ware – Amazon gibt das Layout vor, Sie laden es als PDF aus Seller Central herunter.</p>

<h2 id="entscheidung">Die eigentliche Entscheidung: FNSKU oder Herstellerbarcode</h2>
<p>Amazon lässt bei bestimmten Produkten zu, dass Sie statt eines FNSKU den Herstellerbarcode nutzen. Das klingt bequem – spart es doch das Etikettieren. Der Preis dafür heißt <strong>Bestandsvermischung</strong> (englisch: commingling, oft auch „stickerless“ genannt).</p>
<p>Bei Vermischung wandert Ihre Ware in denselben Bestandstopf wie die identische Ware anderer Händler. Bestellt ein Kunde bei Ihnen, kann er die Einheit eines anderen Verkäufers erhalten – und umgekehrt. Die Konsequenzen:</p>
<ul>
  <li><strong>Fremde Qualität wird Ihr Problem.</strong> Liefert ein anderer Händler Fälschungen oder beschädigte Ware ein, landen die Beschwerden und Rücksendungen unter Umständen bei Ihnen.</li>
  <li><strong>Kein Nachweis.</strong> Sie können im Streitfall nicht belegen, dass die beanstandete Einheit nicht aus Ihrer Lieferung stammte.</li>
  <li><strong>Kontorisiko.</strong> Authentizitätsbeschwerden gehören zu den härtesten Gründen für Kontosperrungen.</li>
</ul>
<blockquote><p>Unsere Empfehlung an jeden Markeninhaber und jeden Händler mit Eigenmarke: immer FNSKU, ohne Ausnahme. Die 0,39 € pro Einheit sind die günstigste Versicherung, die Sie im FBA-Geschäft kaufen können.</p></blockquote>

<h2 id="pflicht">Wann ein FNSKU zwingend ist</h2>
<ul>
  <li>Bei Produkten mit Mindesthaltbarkeitsdatum – hier ist die Vermischung ausgeschlossen.</li>
  <li>Bei gebrauchter oder generalüberholter Ware.</li>
  <li>Bei Bundles und Multipacks, die Sie selbst zusammenstellen.</li>
  <li>Bei Produkten ohne gültige, scanbare Herstellergültigkeit auf der Verpackung.</li>
  <li>Sobald Sie die Vermischung in Ihren Einstellungen deaktiviert haben – dann für alle Artikel.</li>
</ul>

<h2 id="drucken">Etiketten richtig drucken</h2>
<ul>
  <li><strong>Format:</strong> Amazon stellt die Etiketten als PDF in einem vorgegebenen Raster bereit. Drucken Sie sie in Originalgröße – „an Seite anpassen“ verkleinert den Barcode und macht ihn unlesbar.</li>
  <li><strong>Material:</strong> Ein Thermotransfer- oder Laserdruck auf mattem Etikettenpapier bleibt lange lesbar. Reine Thermodirekt-Etiketten können bei Wärme verblassen – Amazon verlangt 24 Monate Lesbarkeit.</li>
  <li><strong>Kein Glanz, kein Tesa:</strong> Klebeband über dem Barcode und glänzende Folien erzeugen Reflexionen, an denen Scanner scheitern.</li>
  <li><strong>Kontrolle:</strong> Scannen Sie das erste Etikett jeder Charge mit dem Handy. Zehn Sekunden, die eine ganze Palette retten.</li>
</ul>

<h2 id="fehler">Die fünf häufigsten Etikettierfehler</h2>
<ol>
  <li>Der Herstellerbarcode bleibt sichtbar – zwei scanbare Codes auf einer Einheit.</li>
  <li>Das Etikett sitzt unter der Schrumpffolie statt außen.</li>
  <li>Das Etikett klebt über einer Kante oder Falz und knickt den Barcode.</li>
  <li>Ein FNSKU aus einer alten Charge wird für einen neu angelegten Artikel wiederverwendet.</li>
  <li>Etiketten aus der falschen SKU-Datei – passiert reihenweise bei Varianten in mehreren Farben oder Größen.</li>
</ol>
<p>Wenn Sie die Etikettierung abgeben möchten: Wir drucken die Etiketten aus Ihrer PDF-Datei oder kleben von Ihnen gelieferte Etiketten auf – 0,39 € pro Einheit, Details unter <a href="/fnsku-etikettierung.html">FNSKU-Etikettierung</a>.</p>
""",
 "faq": [
   ("Kann ich EAN und FNSKU gleichzeitig auf der Einheit lassen?",
    "Nein. Wenn Sie mit FNSKU arbeiten, muss der Herstellerbarcode vollständig überklebt sein. Zwei scanbare Codes führen zu Fehlbuchungen im Wareneingang."),
   ("Wer erstellt die FNSKU-Etiketten – Sie oder ich?",
    "Beides ist möglich. Sie laden die PDF-Datei aus Seller Central herunter und senden sie uns, oder Sie schicken bereits gedruckte Etiketten mit. Wir haben keinen Zugriff auf Kundenkonten und erzeugen die Etiketten deshalb nicht selbst."),
   ("Was ist der Unterschied zwischen SKU und FNSKU?",
    "Die SKU vergeben Sie selbst und nutzen sie intern. Der FNSKU wird von Amazon erzeugt und ist der Code, der physisch auf jeder Einheit klebt."),
 ],
 "related": [("/fnsku-etikettierung.html", "FNSKU-Etikettierung – Ablauf und Preise"),
             ("/blog/amazon-wareneingang-abgelehnt-prep-fehler.html", "Die 8 häufigsten Prep-Fehler"),
             ("/services.html", "Alle Prep-Leistungen"),
             ("/faq.html", "Häufige Fragen zum Ablauf")],
 "cta": ("Etikettierung abgeben", "Schicken Sie uns Ihre Etiketten-PDF – wir kleben, kontrollieren und dokumentieren jede Einheit."),
})

ARTICLES.append({
 "slug": "amazon-de-verkaufen-aus-dem-ausland-ustid-eori-lucid.html",
 "title": "Aus dem Ausland auf Amazon.de verkaufen: USt-IdNr., EORI, LUCID und WEEE",
 "meta_title": "Amazon.de aus dem Ausland: USt-IdNr., EORI, LUCID, WEEE – die Pflichtnummern | PrepCenter FBA",
 "desc": "Welche Registrierungen ausländische Händler für Amazon.de brauchen: deutsche Umsatzsteuer, EORI-Nummer, LUCID-Verpackungsregister, WEEE und Batterien – und in welcher Reihenfolge.",
 "badge": "Für Händler aus dem Ausland", "badge_class": "badge--green",
 "date": "2026-08-16", "modified": "2026-08-18", "reading": 9,
 "image": "/assets/receiving-pallet-CDFVfUKN.jpg",
 "image_alt": "Wareneingang einer Palette im deutschen Prep Center",
 "teaser": "Wer aus China, Großbritannien oder den USA nach Deutschland liefert, scheitert selten am Produkt – sondern an vier Nummern, die vor der ersten Lieferung existieren müssen.",
 "toc": [("Die Reihenfolge, die Zeit spart", "reihenfolge"),
         ("1 · Deutsche Umsatzsteuer-Registrierung", "ust"),
         ("2 · EORI-Nummer für die Einfuhr", "eori"),
         ("3 · LUCID / Verpackungsregister", "lucid"),
         ("4 · WEEE und Batterien", "weee"),
         ("Wer ist Importeur? Der wichtigste Punkt", "importeur"),
         ("Was ein Prep Center übernimmt – und was nicht", "prepcenter")],
 "body": """
<p>Der Markt ist attraktiv, das Produkt ist fertig, der Container ist gebucht – und dann steht die Ware im Hafen, weil eine Nummer fehlt. Dieser Beitrag ordnet die vier Registrierungen, die ausländische Händler für Amazon.de in aller Regel brauchen, und sagt, welche davon Sie vor der ersten Lieferung erledigt haben müssen.</p>
<div class="notice-box">Dies ist eine allgemeine Orientierung, keine Rechts- oder Steuerberatung. Welche Pflichten in Ihrem konkreten Fall gelten, hängt von Ihrer Unternehmensform, Ihrem Sitzland und Ihren Produkten ab. Lassen Sie das vor der ersten Lieferung von einem Steuerberater prüfen.</div>

<h2 id="reihenfolge">Die Reihenfolge, die Zeit spart</h2>
<ol>
  <li><strong>Deutsche Umsatzsteuer-Registrierung</strong> beantragen – dauert am längsten, deshalb zuerst.</li>
  <li><strong>EORI-Nummer</strong> beantragen – geht schnell, wird aber für jede Einfuhr gebraucht.</li>
  <li><strong>LUCID-Registrierung</strong> plus Systembeteiligung – ohne diese Nummer verlangt Amazon Nachweise.</li>
  <li><strong>WEEE / Batterien</strong>, sofern Ihre Produkte darunter fallen – hier ist ein Bevollmächtigter in Deutschland nötig.</li>
</ol>
<p>Erst danach: Ware auf den Weg bringen.</p>

<h2 id="ust">1 · Deutsche Umsatzsteuer-Registrierung</h2>
<p>Der Punkt, der die meisten überrascht: <strong>Sobald Sie Ware in Deutschland lagern, brauchen Sie in aller Regel eine deutsche umsatzsteuerliche Registrierung</strong> – unabhängig davon, wie viel Sie verkaufen. Das gilt für FBA-Bestand in einem Amazon-Lager genauso wie für Ware, die bei einem Prep Center oder in einem eigenen Lager liegt.</p>
<p>Das <strong>OSS-Verfahren (One-Stop-Shop)</strong> ersetzt diese Registrierung nicht. OSS vereinfacht die Meldung grenzüberschreitender Verkäufe an Privatkunden aus einem Lagerland heraus – es befreit Sie aber nicht von der Registrierung in dem Land, in dem Ihre Ware physisch liegt.</p>
<p>Aus der Registrierung folgt eine deutsche Steuernummer und – auf Antrag – eine <strong>USt-IdNr.</strong> Amazon verlangt diese Angaben im Verkäuferkonto; fehlen sie, kann der Verkauf eingeschränkt werden. Rechnen Sie je nach Finanzamt mit mehreren Wochen bis Monaten Bearbeitungszeit.</p>
<p>Für Händler außerhalb der EU kommt hinzu, dass Amazon in bestimmten Konstellationen die Umsatzsteuer als sogenannter fiktiver Lieferer selbst einbehält und abführt. Das ändert nichts an Ihrer Registrierungspflicht für die Lagerung.</p>

<h2 id="eori">2 · EORI-Nummer für die Einfuhr</h2>
<p>Die EORI-Nummer (Economic Operators Registration and Identification) ist die Kennnummer, unter der der Zoll Wirtschaftsbeteiligte führt. Ohne EORI wird keine Einfuhranmeldung abgegeben. Sie beantragen sie beim Zoll; in Deutschland ist die Beantragung kostenlos und dauert üblicherweise wenige Tage bis Wochen.</p>
<p>Wichtig: Die EORI-Nummer gehört zu dem Unternehmen, das als Einführer auftritt – siehe den Abschnitt zum Importeur weiter unten.</p>

<h2 id="lucid">3 · LUCID / Verpackungsregister</h2>
<p>Wer Verpackungen in Deutschland in Verkehr bringt – also Produktverpackungen, Umverpackungen und Versandkartons –, muss sich vor dem ersten Inverkehrbringen bei der <strong>Zentralen Stelle Verpackungsregister (ZSVR)</strong> im Register LUCID registrieren <em>und</em> sich an einem dualen System beteiligen. Beides gehört zusammen: Die Registrierung allein genügt nicht.</p>
<p>Amazon fragt die LUCID-Nummer im Verkäuferkonto ab. Fehlt sie, drohen Einschränkungen des Angebots. Die Registrierung ist kostenlos und in Ihrem Namen vorzunehmen – ein Dienstleister kann das nicht für Sie „mitmachen“, weil die Registrierung an den Hersteller im Sinne des Gesetzes gebunden ist.</p>
<p>Seit dem 12. August 2026 gilt zusätzlich die EU-Verpackungsverordnung PPWR. Was sich dadurch ändert, steht in unserem Beitrag <a href="/blog/ppwr-2026-amazon-haendler-deutschland.html">PPWR seit August 2026</a>.</p>

<h2 id="weee">4 · WEEE und Batterien</h2>
<p>Verkaufen Sie Elektro- oder Elektronikgeräte, greift das <strong>ElektroG</strong>: Registrierung bei der stiftung elektro-altgeräte register (stiftung ear) vor dem ersten Anbieten, mit einer WEEE-Registrierungsnummer je Marke und Geräteart. Händler ohne Niederlassung in Deutschland benötigen dafür einen <strong>Bevollmächtigten mit Sitz in Deutschland</strong>.</p>
<p>Enthalten Ihre Produkte Batterien oder Akkus – auch fest verbaute –, kommt das <strong>Batteriegesetz</strong> hinzu, ebenfalls mit Registrierungspflicht. „Da ist nur eine kleine Knopfzelle drin“ ist kein Ausnahmetatbestand.</p>

<h2 id="importeur">Wer ist Importeur? Der wichtigste Punkt</h2>
<p>Die Frage, an der die meisten Lieferungen tatsächlich hängen bleiben, lautet nicht „welche Nummer fehlt“, sondern: <strong>Wer tritt gegenüber dem Zoll als Einführer auf?</strong></p>
<ul>
  <li>Der Einführer (Importer of Record) haftet für die korrekte Einfuhranmeldung, für Zölle und Einfuhrumsatzsteuer sowie für die Produktkonformität.</li>
  <li>Ein Unternehmen ohne Sitz in der EU kann diese Rolle nicht ohne Weiteres selbst ausfüllen – üblich ist die Einschaltung eines Zollagenten als indirekter Vertreter oder eine eigene EU-Gesellschaft.</li>
  <li><strong>Ein Prep Center ist nicht automatisch Ihr Importeur.</strong> Wir nehmen Ware entgegen, bearbeiten sie und liefern sie an Amazon ein – wir treten aber nicht als Einführer auf und übernehmen keine zollrechtliche Haftung für Ihre Sendungen.</li>
</ul>
<p>Klären Sie diese Rolle mit Ihrem Spediteur, bevor der Container ausläuft. Eine Sendung, die im Hafen ohne benannten Einführer ankommt, verursacht Standgeld – und das läuft pro Tag.</p>

<h2 id="prepcenter">Was ein Prep Center übernimmt – und was nicht</h2>
<table>
  <thead><tr><th>Aufgabe</th><th>Wer</th></tr></thead>
  <tbody>
    <tr><td>Umsatzsteuer-, EORI-, LUCID- und WEEE-Registrierung</td><td>Sie bzw. Ihr Steuerberater und Bevollmächtigter</td></tr>
    <tr><td>Einfuhr und Verzollung</td><td>Ihr Spediteur / Zollagent</td></tr>
    <tr><td>Deutsche Lieferadresse für Ware und Retouren</td><td>Wir</td></tr>
    <tr><td>Wareneingang, Stückzahlkontrolle, Zustandsprüfung mit Fotos</td><td>Wir</td></tr>
    <tr><td>FNSKU-Etikettierung, Polybag, Bundling, Umverpackung</td><td>Wir</td></tr>
    <tr><td>Zwischenlagerung und Einlieferung an Amazon FBA</td><td>Wir</td></tr>
    <tr><td>Shipping Plan in Seller Central anlegen</td><td>Sie – wir haben keinen Zugriff auf Kundenkonten</td></tr>
  </tbody>
</table>
<p>Die Arbeitsteilung ist bewusst so geschnitten: Alles, was eine Registrierung auf Ihren Namen voraussetzt, bleibt bei Ihnen. Alles, was physisch mit der Ware passiert, übernehmen wir.</p>
""",
 "faq": [
   ("Brauche ich eine deutsche Umsatzsteuernummer, wenn meine Ware nur beim Prep Center liegt?",
    "In aller Regel ja: Maßgeblich ist, dass die Ware physisch in Deutschland lagert – nicht, ob sie in einem Amazon-Lager oder bei einem Dienstleister liegt. Lassen Sie Ihren Fall vor der ersten Lieferung steuerlich prüfen."),
   ("Können Sie die LUCID-Registrierung für mich übernehmen?",
    "Nein. Die Registrierung im Verpackungsregister ist an den Hersteller im Sinne des Gesetzes gebunden und muss auf Ihren Namen erfolgen. Sie ist kostenlos und online möglich."),
   ("Treten Sie als Importeur meiner Sendung auf?",
    "Nein. Wir sind Dienstleister für die Bearbeitung der Ware und nicht Einführer. Die Einfuhr organisieren Sie mit Ihrem Spediteur oder Zollagenten."),
   ("Kann ich Ware direkt vom Hersteller aus China an Sie liefern lassen?",
    "Ja, das ist der häufigste Fall. Kündigen Sie die Lieferung vorab per E-Mail an und stellen Sie sicher, dass Einfuhr und Verzollung geregelt sind, bevor die Sendung ankommt."),
 ],
 "related": [("/fba-prep-center-deutschland.html", "FBA Prep Center Deutschland – Überblick"),
             ("/kontakt.html", "Anschrift und Anlieferhinweise"),
             ("/blog/ppwr-2026-amazon-haendler-deutschland.html", "PPWR seit August 2026"),
             ("/services.html", "Alle Leistungen")],
 "cta": ("Eingangspunkt in Deutschland", "Wir sind Ihre deutsche Adresse für Wareneingang, Prep und Retouren – Sie behalten Konto und Registrierungen in Ihrer Hand."),
})

ARTICLES.append({
 "slug": "ppwr-2026-amazon-haendler-deutschland.html",
 "title": "PPWR seit 12. August 2026: was sich für Amazon-Händler ändert",
 "meta_title": "PPWR seit August 2026 – was Amazon-Händler jetzt wissen müssen | PrepCenter FBA",
 "desc": "Die EU-Verpackungsverordnung PPWR gilt seit dem 12. August 2026. Was das für Online- und Amazon-Händler bedeutet, warum LUCID Pflicht bleibt und welche Schritte jetzt anstehen.",
 "badge": "Recht & Compliance", "badge_class": "badge--amber",
 "date": "2026-08-18", "modified": "2026-08-18", "reading": 6,
 "image": "/assets/warehouse-storage-B1dzTsVq.jpg",
 "image_alt": "Verpackte Ware im Lager eines FBA Prep Centers",
 "teaser": "Seit dem 12. August 2026 gilt die EU-Verpackungsverordnung unmittelbar in allen Mitgliedstaaten. Für Online-Händler ändert sich vor allem eines: Wer den Versandkarton packt, ist Hersteller dieser Verpackung.",
 "toc": [("Was die PPWR ist", "was"), ("LUCID bleibt Pflicht", "lucid"),
         ("Der Kern für Online-Händler", "kern"), ("Neue Pflichten im Überblick", "pflichten"),
         ("Grenzüberschreitender Verkauf in der EU", "eu"),
         ("Was das für FBA-Händler praktisch heißt", "fba"),
         ("Was wir als Prep Center übernehmen", "wir")],
 "body": """
<div class="notice-box">Stand dieses Beitrags: August 2026. Die PPWR wird in den kommenden Jahren schrittweise konkretisiert; einzelne Pflichten und Fristen können sich ändern. Dieser Text ist eine allgemeine Information und keine Rechtsberatung – verbindliche Auskünfte erteilen die Zentrale Stelle Verpackungsregister (ZSVR) und Ihre Rechtsberatung.</div>

<h2 id="was">Was die PPWR ist</h2>
<p>Die PPWR – Packaging and Packaging Waste Regulation, auf Deutsch EU-Verpackungsverordnung – ersetzt die bisherige europäische Verpackungsrichtlinie. Anders als eine Richtlinie muss eine Verordnung nicht erst in nationales Recht umgesetzt werden: Sie gilt unmittelbar. Anwendbar ist sie seit dem <strong>12. August 2026</strong>.</p>
<p>Ziel der Verordnung ist weniger Verpackungsmüll: Vorgaben zu Recyclingfähigkeit, Materialeinsatz, Leerraum in Versandverpackungen, einheitlicher Kennzeichnung und erweiterter Herstellerverantwortung.</p>

<h2 id="lucid">LUCID bleibt Pflicht</h2>
<p>Die wichtigste Entwarnung zuerst: <strong>Die Registrierung bei der ZSVR im Register LUCID bleibt bestehen.</strong> Die PPWR ersetzt sie nicht, sondern baut die Herstellerverantwortung darauf auf. Wer heute registriert ist und an einem dualen System teilnimmt, verliert diese Pflicht nicht – im Gegenteil, sie wird ausgeweitet.</p>
<p>Wer bislang nicht registriert war, sollte das umgehend nachholen. Nicht registrierte Verpackungen dürfen in Deutschland nicht in Verkehr gebracht werden; Marktplätze wie Amazon prüfen die Registrierungsnummern ihrer Händler.</p>

<h2 id="kern">Der Kern für Online-Händler</h2>
<p>Der Punkt, der im Versandhandel am meisten verändert: <strong>Wer eine Versandverpackung befüllt, gilt als Hersteller dieser Verpackung.</strong> Eine vollständige Verpackung entsteht in dem Moment, in dem ein Online-Händler den Versandkarton mit Ware füllt.</p>
<p>Damit hängt die Herstellerrolle nicht mehr allein daran, wer den Karton eingekauft hat, sondern daran, wer ihn zum Versand fertig macht. Für Händler, die bisher davon ausgingen, ihr Lieferant kümmere sich schon um die Verpackungsregistrierung, ist das eine echte Verschiebung.</p>

<h2 id="pflichten">Neue Pflichten im Überblick</h2>
<ul>
  <li><strong>Konformität:</strong> Verpackungen müssen den Anforderungen der Verordnung entsprechen; dafür sind Konformitätsbewertungen und EU-Konformitätserklärungen vorgesehen.</li>
  <li><strong>Kennzeichnung:</strong> Verpackungen sind zu kennzeichnen, und Angaben zum Hersteller – Name, Anschrift, elektronische Kontaktmöglichkeit – müssen zuordenbar sein.</li>
  <li><strong>Prüfpflichten im Handel:</strong> Wer Verpackungen weitergibt, muss prüfen, ob der Hersteller registriert ist und die Kennzeichnungsvorgaben eingehalten sind.</li>
  <li><strong>Kleinstunternehmen:</strong> Für sehr kleine Unternehmen sind Erleichterungen bei einzelnen Verfahren vorgesehen – Registrierung und Systembeteiligung bleiben davon unberührt.</li>
</ul>
<p>Ein Teil der Vorgaben – etwa zu harmonisierten Kennzeichnungssymbolen und Rezyklatanteilen – greift gestaffelt in den Folgejahren. Prüfen Sie die aktuellen Fristen bei der ZSVR, statt sich auf Sekundärquellen zu verlassen.</p>

<h2 id="eu">Grenzüberschreitender Verkauf in der EU</h2>
<p>Wer in andere EU-Länder liefert, braucht die erweiterte Herstellerverantwortung auch dort. Vorgesehen ist, dass Hersteller ohne Niederlassung im jeweiligen Mitgliedstaat einen <strong>Bevollmächtigten</strong> benennen und sich im dortigen Verpackungsregister eintragen. Für Händler, die über Amazon in mehreren europäischen Marktplätzen verkaufen, ist das der aufwendigste Teil.</p>

<h2 id="fba">Was das für FBA-Händler praktisch heißt</h2>
<ol>
  <li><strong>LUCID-Eintrag prüfen.</strong> Stimmen Firmierung, Marken und Verpackungsarten noch? Änderungen der letzten Monate nachtragen.</li>
  <li><strong>Systembeteiligung abgleichen.</strong> Melden Sie realistische Mengen – zu niedrige Mengenmeldungen fallen im Abgleich auf.</li>
  <li><strong>Versandverpackung mitdenken.</strong> Auch Karton, Klebeband und Füllmaterial sind Verpackung, nicht nur die Produktverpackung.</li>
  <li><strong>Lieferantenangaben einsammeln.</strong> Wer liefert Ihnen Kartons und Beutel, und welche Konformitätsangaben liegen dazu vor?</li>
  <li><strong>Andere EU-Märkte durchgehen.</strong> Für jeden Marktplatz, in dem Sie lagern oder liefern, die dortige Registrierung klären.</li>
</ol>

<h2 id="wir">Was wir als Prep Center übernehmen</h2>
<p>Klar getrennt, damit es keine Missverständnisse gibt:</p>
<ul>
  <li><strong>Wir verpacken nach Ihren Vorgaben</strong> und dokumentieren, welche Materialien eingesetzt wurden – das hilft Ihnen bei Ihren Mengenmeldungen.</li>
  <li><strong>Wir halten uns an die Amazon-Prep-Vorgaben</strong> für Beutelstärke, Kennzeichnung und Warnhinweise.</li>
  <li><strong>Wir übernehmen nicht Ihre Registrierung.</strong> LUCID, Systembeteiligung und Mengenmeldungen sind an Ihr Unternehmen als Hersteller gebunden und lassen sich nicht delegieren.</li>
</ul>
<p>Wenn Sie ohnehin gerade Ihre Verpackungen überarbeiten: Das ist der richtige Moment, Beutelstärke, Kartongrößen und Füllmaterial einmal gemeinsam durchzugehen – kleinere Kartons sparen doppelt, bei den Verpackungsmengen und bei den Amazon-Gebühren.</p>
""",
 "faq": [
   ("Muss ich mich wegen der PPWR neu registrieren?",
    "Die Registrierung bei der ZSVR im Register LUCID bleibt bestehen. Ob und wann Bestandsregistrierungen anzupassen sind, hängt von den Vorgaben der ZSVR ab – prüfen Sie den aktuellen Stand direkt dort."),
   ("Gilt die PPWR auch für Versandkartons?",
    "Ja. Versandverpackungen sind Verpackungen im Sinne der Verordnung. Wer den Karton mit Ware befüllt, gilt als Hersteller dieser Verpackung."),
   ("Wir sind ein sehr kleines Unternehmen – gilt das auch für uns?",
    "Für Kleinstunternehmen sind Erleichterungen bei einzelnen Verfahren vorgesehen. Registrierung und Beteiligung an einem Rücknahmesystem entfallen dadurch aber nicht."),
 ],
 "related": [("/blog/amazon-de-verkaufen-aus-dem-ausland-ustid-eori-lucid.html", "USt-IdNr., EORI, LUCID und WEEE für ausländische Händler"),
             ("/services.html", "Verpackungs- und Prep-Leistungen"),
             ("/fba-lagerung-deutschland.html", "Lagerung in Deutschland"),
             ("/kontakt.html", "Kontakt aufnehmen")],
 "cta": ("Verpackung einmal richtig aufsetzen", "Wir gehen Beutelstärke, Kartongrößen und Materialien mit Ihnen durch – und dokumentieren, was wir für Sie verbrauchen."),
})


# ── Rendering ───────────────────────────────────────────────────────────────

def picture(src, alt, cls, sizes_attr=""):
    """<picture> mit webp-Quelle, falls vorhanden."""
    webp = src.rsplit(".", 1)[0] + ".webp"
    has_webp = os.path.exists(webp.lstrip("/"))
    src_tag = ('<source srcset="%s" type="image/webp">' % webp) if has_webp else ""
    return ('<picture>%s<img src="%s" alt="%s" class="%s" loading="lazy" decoding="async"%s></picture>'
            % (src_tag, src, esc(alt), cls, sizes_attr))


def faq_html(pairs):
    if not pairs:
        return ""
    items = []
    for q, a in pairs:
        items.append(
            '      <details class="faq-item">\n'
            '        <summary><span>%s</span><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true">'
            '<path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
            '</svg></summary>\n'
            '        <div class="faq-item__body">%s</div>\n'
            '      </details>' % (esc(q), esc(a)))
    return ("""
<section class="section section--surface">
  <div class="container" style="max-width:820px">
    <span class="section-label">FAQ</span>
    <h2 class="section-title">Häufige Fragen</h2>
    <div class="faq-list">
%s
    </div>
    <p class="vat-notice" style="margin-top:1.25rem;margin-bottom:0">Unser Angebot richtet sich ausschließlich an Unternehmer im Sinne des § 14 BGB.</p>
  </div>
</section>
""" % "\n".join(items))


def related_html(items):
    lis = "\n".join('        <li><a href="%s">%s</a></li>' % (h, esc(t)) for h, t in items)
    return """
<section class="section section--sm">
  <div class="container" style="max-width:820px">
    <h2 class="section-title" style="font-size:1.15rem">Weiterführende Seiten</h2>
    <ul class="related-links" role="list">
%s
    </ul>
    <p style="margin-top:1rem"><a href="/blog/">← Zurück zur Übersicht aller Beiträge</a></p>
  </div>
</section>
""" % lis


def toc_html(items):
    if not items:
        return ""
    lis = "\n".join('        <li><a href="#%s">%s</a></li>' % (anchor, esc(label))
                    for label, anchor in items)
    return ('    <nav class="toc" aria-label="Inhaltsverzeichnis">\n'
            '      <h2>Inhalt</h2>\n      <ol>\n%s\n      </ol>\n    </nav>\n' % lis)


def render_article(a):
    canon = BLOG_URL + a["slug"]
    ld = [
        {"@type": "WebPage", "@id": canon + "#webpage", "url": canon,
         "name": a["meta_title"], "description": a["desc"], "inLanguage": "de-DE",
         "isPartOf": {"@id": SITE_ID}, "about": {"@id": ORG_ID}},
        {"@type": "BlogPosting", "@id": canon + "#article",
         "headline": a["title"], "description": a["desc"],
         "datePublished": a["date"], "dateModified": a.get("modified", a["date"]),
         "inLanguage": "de-DE", "image": DOMAIN + a["image"],
         "articleSection": a["badge"], "wordCount": len(strip_tags(a["body"]).split()),
         "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID},
         "isPartOf": {"@id": BLOG_URL + "#blog"},
         "mainEntityOfPage": {"@id": canon + "#webpage"}},
        breadcrumbs([("Startseite", DOMAIN + "/"), ("Ratgeber", BLOG_URL), (a["title"], canon)]),
    ]
    if a.get("faq"):
        ld.append({"@type": "FAQPage", "@id": canon + "#faq", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a["faq"]]})

    out = [head(a["meta_title"], a["desc"], canon, a["image"], ld,
                published=a["date"], modified=a.get("modified", a["date"]))]
    out.append("""
<section class="page-hero" aria-labelledby="page-title">
  <div class="container" style="max-width:820px">
    <p style="font-size:.85rem;color:#64748b;margin-bottom:.6rem"><a href="/">Startseite</a> › <a href="/blog/">Ratgeber</a></p>
    <span class="badge %(badge_class)s">%(badge)s</span>
    <h1 id="page-title">%(title)s</h1>
    <p class="lead">%(teaser)s</p>
    <p class="article-meta">
      <time datetime="%(date)s">%(date_de)s</time>
      <span aria-hidden="true">·</span>
      <span>%(reading)s Min. Lesezeit</span>
      <span aria-hidden="true">·</span>
      <span>PrepCenter FBA Redaktion</span>
    </p>
  </div>
</section>

<article class="section">
  <div class="container" style="max-width:820px">
%(cover)s
%(toc)s
    <div class="prose">
%(body)s
    </div>
%(stand)s
  </div>
</article>
""" % {
        "badge_class": a.get("badge_class", "badge--blue"), "badge": esc(a["badge"]),
        "title": esc(a["title"]), "teaser": a["teaser"], "date": a["date"],
        "date_de": de_date(a["date"]), "reading": a["reading"],
        "cover": "    " + picture(a["image"], a["image_alt"], "article-cover"),
        "toc": toc_html(a.get("toc")),
        "body": a["body"].strip(),
        "stand": "    " + (STAND_NOTE % de_date(a.get("modified", a["date"]))),
    })
    out.append(faq_html(a.get("faq")))
    out.append(related_html(a["related"]))
    out.append(cta_band(*a["cta"]))
    out.append(tail(canon))
    return "".join(out)


def render_index(posts):
    canon = BLOG_URL
    desc = ("Ratgeber für Amazon-FBA-Händler: Prep-Kosten, Verpackungsvorgaben, "
            "FNSKU-Etikettierung, Pflichten für Händler aus dem Ausland und aktuelle "
            "Regeln rund um den Versand an Amazon FBA in Deutschland.")
    ld = [
        {"@type": "WebPage", "@id": canon + "#webpage", "url": canon,
         "name": "Ratgeber für Amazon-FBA-Händler | PrepCenter FBA",
         "description": desc, "inLanguage": "de-DE",
         "isPartOf": {"@id": SITE_ID}, "about": {"@id": ORG_ID}},
        {"@type": "Blog", "@id": canon + "#blog", "url": canon,
         "name": "PrepCenter FBA Ratgeber", "description": desc, "inLanguage": "de-DE",
         "publisher": {"@id": ORG_ID},
         "blogPost": [{"@type": "BlogPosting", "@id": BLOG_URL + p["slug"] + "#article",
                       "headline": p["title"], "url": BLOG_URL + p["slug"],
                       "datePublished": p["date"],
                       "dateModified": p.get("modified", p["date"]),
                       "image": DOMAIN + p["image"],
                       "author": {"@id": ORG_ID}} for p in posts]},
        breadcrumbs([("Startseite", DOMAIN + "/"), ("Ratgeber", canon)]),
    ]
    cards = []
    for p in posts:
        cards.append("""      <a class="post-card" href="/blog/%(slug)s">
        %(img)s
        <div class="post-card__body">
          <span class="badge %(bc)s" style="align-self:flex-start">%(badge)s</span>
          <h2 class="post-card__title">%(title)s</h2>
          <p class="post-card__teaser">%(teaser)s</p>
          <p class="post-card__meta"><time datetime="%(date)s">%(date_de)s</time> · %(reading)s Min.</p>
          <span class="post-card__more">Beitrag lesen →</span>
        </div>
      </a>""" % {
            "slug": p["slug"], "bc": p.get("badge_class", "badge--blue"),
            "badge": esc(p["badge"]), "title": esc(p["title"]), "teaser": p["teaser"],
            "date": p["date"], "date_de": de_date(p["date"]), "reading": p["reading"],
            "img": picture(p["image"], p["image_alt"], "post-card__img"),
        })

    body = """
<section class="page-hero" aria-labelledby="page-title">
  <div class="container">
    <span class="badge badge--blue">Ratgeber</span>
    <h1 id="page-title">Ratgeber für Amazon-FBA-Händler</h1>
    <p class="lead">Praxiswissen zu Prep, Verpackung, Etikettierung und den Pflichten rund um den Versand an Amazon FBA in Deutschland – ohne Marketing-Nebel, mit konkreten Zahlen.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="post-grid">
%(cards)s
    </div>
  </div>
</section>

<section class="section section--surface section--sm">
  <div class="container" style="max-width:820px">
    <h2 class="section-title" style="font-size:1.15rem">Sie suchen etwas Bestimmtes?</h2>
    <ul class="related-links" role="list">
      <li><a href="/services.html">Alle Prep-Leistungen im Überblick</a></li>
      <li><a href="/pricing.html">Preisliste</a></li>
      <li><a href="/kalkulator.html">Kostenkalkulator</a></li>
      <li><a href="/faq.html">Häufige Fragen zum Ablauf</a></li>
      <li><a href="/kontakt.html">Kontakt und Anlieferhinweise</a></li>
    </ul>
  </div>
</section>
""" % {"cards": "\n".join(cards)}

    return (head("Ratgeber für Amazon-FBA-Händler | PrepCenter FBA", desc, canon,
                 posts[0]["image"] if posts else OG_FALLBACK, ld)
            + body
            + cta_band("Frage offen geblieben?",
                       "Schreiben Sie uns – wir antworten mit konkreten Zahlen zu Ihrem Produkt, nicht mit einer Broschüre.")
            + tail(canon))


def main():
    if not os.path.exists("index.html"):
        sys.exit("Bitte aus dem Projekt-Root aufrufen: python3 tools/gen_blog.py")
    os.makedirs(BLOG_DIR, exist_ok=True)
    posts = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)

    slugs = [a["slug"] for a in ARTICLES]
    if len(set(slugs)) != len(slugs):
        sys.exit("Doppelter Slug in ARTICLES: %s" % slugs)

    for a in ARTICLES:
        path = os.path.join(BLOG_DIR, a["slug"])
        open(path, "w", encoding="utf-8").write(render_article(a))
        print("  ", path)
    open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8").write(render_index(posts))
    print("   blog/index.html")
    print("gen_blog.py: %d Beitraege + Uebersicht erzeugt." % len(ARTICLES))
    print("Nicht vergessen: python3 tools/gen_sitemap.py")


if __name__ == "__main__":
    main()

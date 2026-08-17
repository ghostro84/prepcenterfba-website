# -*- coding: utf-8 -*-
import sys, os, re, json, glob
sys.path.insert(0, os.path.dirname(__file__))
from seo import (DOMAIN, OG_IMAGE, LANGS, PAGES, LEGAL, url, head_block,
                 ORG, WEBSITE, service_node, breadcrumbs, faq_node)

HOME = ("Startseite", DOMAIN + "/")

EXTRA = {  # Datei → (Breadcrumb-Name, Service-Name, Service-Beschreibung|None)
 "services.html": ("Leistungen", "FBA Prep Services", "Wareneingang, Qualitätskontrolle, FNSKU-Etikettierung, Verpackung, Bundling, Lagerung und Einlieferung an Amazon FBA."),
 "pricing.html": ("Preise", None, None),
 "fba-prep-center-deutschland.html": ("FBA Prep Center Deutschland", "FBA Prep Center Deutschland", "Komplette Vorbereitung von Handelsware für die Einlieferung an Amazon FBA in Deutschland."),
 "fnsku-etikettierung.html": ("FNSKU-Etikettierung", "FNSKU-Etikettierung", "Amazon-konforme FNSKU-Etikettierung inklusive Überkleben vorhandener Fremdbarcodes und Scan-Kontrolle."),
 "fba-lagerung-deutschland.html": ("FBA Lagerung", "Lagerung vor der FBA-Einlieferung", "Zwischenlagerung von Handelsware in Deutschland mit Abruf in Teilmengen für die Amazon-Einlieferung."),
 "versand-an-amazon.html": ("Versand an Amazon", "Einlieferung an Amazon FBA", "Amazon-konforme Konfektionierung und Übergabe von Karton- und Palettensendungen an den Spediteur."),
 "amazon-retouren-deutschland.html": ("Amazon Retouren", "Retourenbearbeitung", "Annahme, Zustandsprüfung, Wiederaufbereitung und Entsorgung von Amazon-Retouren und Removal Orders."),
 "fba-prep-center-bayern.html": ("FBA Prep Center Bayern", "FBA Prep Center Bayern", "FBA Prep Leistungen am Standort Freilassing in Bayern."),
 "kalkulator.html": ("Kostenrechner", None, None),
 "ueber-uns.html": ("Über uns", None, None),
 "faq.html": ("FAQ", None, None),
 "kontakt.html": ("Kontakt", None, None),
 "impressum.html": ("Impressum", None, None),
 "agb.html": ("AGB", None, None),
 "datenschutz.html": ("Datenschutzerklärung", None, None),
}

def meta(html, name=None, prop=None):
    pat = r'<meta %s="%s" content="([^"]*)"' % ("name" if name else "property", name or prop)
    m = re.search(pat, html)
    return m.group(1) if m else ""

def apply(f):
    s = open(f, encoding="utf-8").read()
    # alten SEO-Block entfernen (idempotent)
    s = re.sub(r'\n?  <!-- SEO -->.*?  <!-- /SEO -->\n?', '\n', s, flags=re.S)

    title = re.search(r'<title>(.*?)</title>', s, re.S).group(1).strip()
    desc  = meta(s, name="description")

    blk = head_block(f, "de").replace("__TITLE__", title.replace('"', "&quot;")) \
                             .replace("__DESC__", desc.replace('"', "&quot;"))

    # ── JSON-LD Graph ──
    graph = []
    if f == "index.html":
        graph += [ORG, WEBSITE]
    else:
        graph.append({"@type": "WebPage",
                      "@id": (url("de", PAGES[f][0]["de"]) if f in PAGES else DOMAIN + "/" + f) + "#webpage",
                      "url": url("de", PAGES[f][0]["de"]) if f in PAGES else DOMAIN + "/" + f,
                      "name": title, "description": desc, "inLanguage": "de-DE",
                      "isPartOf": {"@id": DOMAIN + "/#website"},
                      "about": {"@id": DOMAIN + "/#organization"}})
    if f in EXTRA:
        bcname, svcname, svcdesc = EXTRA[f]
        page_url = url("de", PAGES[f][0]["de"]) if f in PAGES else DOMAIN + "/" + f
        graph.append(breadcrumbs([HOME, (bcname, page_url)]))
        if svcname:
            graph.append(service_node(svcname, svcdesc, page_url))
    fq = faq_node(s)
    if fq: graph.append(fq)

    ld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                    ensure_ascii=False, indent=2)
    seo = ("  <!-- SEO -->\n" + blk +
           '  <script type="application/ld+json">\n' + ld + '\n  </script>\n'
           "  <!-- /SEO -->\n")
    s = s.replace("</head>", seo + "</head>", 1)
    open(f, "w", encoding="utf-8").write(s)
    return title

if __name__ == "__main__":
    for f in list(PAGES) + LEGAL:
        print("seo →", f, "|", apply(f)[:60])

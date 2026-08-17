# -*- coding: utf-8 -*-
"""Technisches SEO: canonical, hreflang, OpenGraph, Twitter, JSON-LD, sitemap."""
import json, re, os, glob

DOMAIN = "https://prepcenterfba.eu"
OG_IMAGE = DOMAIN + "/assets/hero-bg-De6VYLKg.jpg"
LANGS = ["de", "en", "it", "fr"]

# deutsche Datei  →  (Slug je Sprache, sitemap-Priorität, changefreq)
PAGES = {
  "index.html":                        ({"de":"index.html","en":"index.html","it":"index.html","fr":"index.html"}, "1.0","weekly"),
  "services.html":                     ({"de":"services.html","en":"services.html","it":"servizi.html","fr":"services.html"}, "0.9","monthly"),
  "pricing.html":                      ({"de":"pricing.html","en":"pricing.html","it":"prezzi.html","fr":"tarifs.html"}, "0.9","monthly"),
  "fba-prep-center-deutschland.html":  ({"de":"fba-prep-center-deutschland.html","en":"fba-prep-center-germany.html","it":"fba-prep-center-germania.html","fr":"fba-prep-center-allemagne.html"}, "0.9","monthly"),
  "fnsku-etikettierung.html":          ({"de":"fnsku-etikettierung.html","en":"fnsku-labeling.html","it":"etichettatura-fnsku.html","fr":"etiquetage-fnsku.html"}, "0.8","monthly"),
  "fba-lagerung-deutschland.html":     ({"de":"fba-lagerung-deutschland.html","en":"fba-storage-germany.html","it":"stoccaggio-fba-germania.html","fr":"stockage-fba-allemagne.html"}, "0.8","monthly"),
  "versand-an-amazon.html":            ({"de":"versand-an-amazon.html","en":"shipping-to-amazon-germany.html","it":"spedizione-ad-amazon.html","fr":"expedition-vers-amazon.html"}, "0.8","monthly"),
  "amazon-retouren-deutschland.html":  ({"de":"amazon-retouren-deutschland.html","en":"amazon-returns-germany.html","it":"resi-amazon-germania.html","fr":"retours-amazon-allemagne.html"}, "0.8","monthly"),
  "fba-prep-center-bayern.html":       ({"de":"fba-prep-center-bayern.html","en":"fba-prep-center-bavaria.html","it":"fba-prep-center-baviera.html","fr":"fba-prep-center-baviere.html"}, "0.7","monthly"),
  "kalkulator.html":                   ({"de":"kalkulator.html","en":"calculator.html","it":"calcolatore.html","fr":"calculateur.html"}, "0.8","monthly"),
  "ueber-uns.html":                    ({"de":"ueber-uns.html","en":"about-us.html","it":"chi-siamo.html","fr":"a-propos.html"}, "0.6","yearly"),
  "faq.html":                          ({"de":"faq.html","en":"faq.html","it":"faq.html","fr":"faq.html"}, "0.7","monthly"),
  "kontakt.html":                      ({"de":"kontakt.html","en":"contact.html","it":"contatti.html","fr":"contact.html"}, "0.7","yearly"),
}
LEGAL = ["impressum.html", "agb.html", "datenschutz.html"]

# Rechtstexte je Sprache. Quelle der Übersetzungen: src-legal/<lang>/<slug>.html
LEGAL_SLUGS = {
  "impressum.html":   {"de":"impressum.html",   "en":"imprint.html", "it":"note-legali.html", "fr":"mentions-legales.html"},
  "datenschutz.html": {"de":"datenschutz.html", "en":"privacy.html", "it":"privacy.html",     "fr":"confidentialite.html"},
  "agb.html":         {"de":"agb.html",         "en":"terms.html",   "it":"condizioni.html",  "fr":"cgv.html"},
}

def url(lang, slug):
    base = DOMAIN + ("/" if lang == "de" else "/%s/" % lang)
    return base if slug == "index.html" else base + slug

def head_block(de_file, lang="de"):
    """canonical + hreflang + og:url + og:image + twitter"""
    if de_file in PAGES:
        slugs = PAGES[de_file][0]
        canon = url(lang, slugs[lang])
        alts = "\n".join(
            '  <link rel="alternate" hreflang="%s" href="%s">' % (l, url(l, slugs[l])) for l in LANGS)
        alts += '\n  <link rel="alternate" hreflang="x-default" href="%s">' % url("de", slugs["de"])
    elif de_file in LEGAL_SLUGS:  # Rechtstexte: alle vier Sprachen
        slugs = LEGAL_SLUGS[de_file]
        canon = url(lang, slugs[lang])
        alts = "\n".join(
            '  <link rel="alternate" hreflang="%s" href="%s">' % (l, url(l, slugs[l])) for l in LANGS)
        alts += '\n  <link rel="alternate" hreflang="x-default" href="%s">' % url("de", slugs["de"])
    else:
        canon = DOMAIN + "/" + de_file
        alts = '  <link rel="alternate" hreflang="de" href="%s">' % canon
    return ('  <link rel="canonical" href="%s">\n%s\n'
            '  <meta property="og:url" content="%s">\n'
            '  <meta property="og:image" content="%s">\n'
            '  <meta property="og:site_name" content="PrepCenter FBA">\n'
            '  <meta property="og:locale" content="%s">\n'
            '  <meta name="twitter:card" content="summary_large_image">\n'
            '  <meta name="twitter:title" content="__TITLE__">\n'
            '  <meta name="twitter:description" content="__DESC__">\n'
            '  <meta name="twitter:image" content="%s">\n'
            % (canon, alts, canon, OG_IMAGE,
               {"de":"de_DE","en":"en_GB","it":"it_IT","fr":"fr_FR"}[lang], OG_IMAGE))

# ─────────────────── JSON-LD ───────────────────
ORG = {
  "@type": "ProfessionalService",
  "@id": DOMAIN + "/#organization",
  "name": "PrepCenter FBA",
  "legalName": "Zbranca MTZ World",
  "alternateName": "PrepCenter FBA – Zbranca MTZ World",
  "description": "FBA Prep Center in Deutschland: Wareneingang, FNSKU-Etikettierung, Qualitätskontrolle, Verpackung, Bundling, Lagerung, Retourenbearbeitung und Einlieferung an Amazon FBA.",
  "url": DOMAIN + "/",
  "email": "b2b@prepcenterfba.eu",
  "vatID": "DE360335852",
  "address": {"@type": "PostalAddress", "streetAddress": "Lindenstraße 21",
              "postalCode": "83395", "addressLocality": "Freilassing",
              "addressRegion": "Bayern", "addressCountry": "DE"},
  "geo": {"@type": "GeoCoordinates", "latitude": 47.8375, "longitude": 12.9764},
  "areaServed": [{"@type":"Country","name":"Deutschland"},{"@type":"Country","name":"Österreich"},
                 {"@type":"Country","name":"Italien"},{"@type":"Country","name":"Frankreich"},
                 {"@type":"Place","name":"Europäische Union"}],
  "priceRange": "€€",
  "currenciesAccepted": "EUR",
  "openingHoursSpecification": [{"@type":"OpeningHoursSpecification",
     "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],
     "opens":"09:00","closes":"17:00"}],
  "knowsLanguage": ["de","en","it","fr"],
  "disambiguatingDescription": "Unabhängiger Dienstleister ohne geschäftliche Verbindung zu Amazon.com, Inc.",
  "hasOfferCatalog": {"@type":"OfferCatalog","name":"FBA Prep Leistungen","itemListElement":[
     {"@type":"Offer","itemOffered":{"@type":"Service","name":"FBA Komplett-Prep"},
      "price":"0.79","priceCurrency":"EUR","priceSpecification":{"@type":"UnitPriceSpecification","price":"0.79","priceCurrency":"EUR","unitText":"Einheit","valueAddedTaxIncluded":False}},
     {"@type":"Offer","itemOffered":{"@type":"Service","name":"FNSKU-Etikettierung"},
      "price":"0.39","priceCurrency":"EUR","priceSpecification":{"@type":"UnitPriceSpecification","price":"0.39","priceCurrency":"EUR","unitText":"Einheit","valueAddedTaxIncluded":False}},
     {"@type":"Offer","itemOffered":{"@type":"Service","name":"Qualitätskontrolle"},
      "price":"0.25","priceCurrency":"EUR","priceSpecification":{"@type":"UnitPriceSpecification","price":"0.25","priceCurrency":"EUR","unitText":"Einheit","valueAddedTaxIncluded":False}},
     {"@type":"Offer","itemOffered":{"@type":"Service","name":"Polybag-Verpackung"},
      "price":"0.29","priceCurrency":"EUR","priceSpecification":{"@type":"UnitPriceSpecification","price":"0.29","priceCurrency":"EUR","unitText":"Einheit","valueAddedTaxIncluded":False}},
     {"@type":"Offer","itemOffered":{"@type":"Service","name":"Bundling / Multipacking"},
      "price":"0.69","priceCurrency":"EUR","priceSpecification":{"@type":"UnitPriceSpecification","price":"0.69","priceCurrency":"EUR","unitText":"Set","valueAddedTaxIncluded":False}},
     {"@type":"Offer","itemOffered":{"@type":"Service","name":"Lagerung Palette"},
      "price":"19.00","priceCurrency":"EUR","priceSpecification":{"@type":"UnitPriceSpecification","price":"19.00","priceCurrency":"EUR","unitText":"Palette/Monat","valueAddedTaxIncluded":False}},
  ]},
}
WEBSITE = {"@type":"WebSite","@id":DOMAIN+"/#website","url":DOMAIN+"/",
           "name":"PrepCenter FBA","inLanguage":"de-DE",
           "publisher":{"@id":DOMAIN+"/#organization"}}

def service_node(name, desc, page_url):
    return {"@type":"Service","name":name,"description":desc,"serviceType":name,
            "url":page_url,"provider":{"@id":DOMAIN+"/#organization"},
            "areaServed":{"@type":"Country","name":"Deutschland"}}

def breadcrumbs(items):
    return {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}

def faq_node(html):
    """FAQPage aus den <details>-Blöcken der Seite."""
    qs = re.findall(r'<summary><span data-i18n="[^"]+">(.*?)</span>.*?'
                    r'<div class="faq-item__body"[^>]*>(.*?)</div>', html, re.S)
    if not qs: return None
    out=[]
    for q,a in qs:
        q=re.sub(r'<[^>]+>','',q).strip()
        a=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',a)).strip()
        if q and a: out.append({"@type":"Question","name":q,
                                "acceptedAnswer":{"@type":"Answer","text":a}})
    return {"@type":"FAQPage","mainEntity":out} if out else None

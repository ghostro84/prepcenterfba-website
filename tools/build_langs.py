# -*- coding: utf-8 -*-
"""Rendert die deutschen Seiten als statische EN/IT/FR-Versionen unter /en/, /it/, /fr/."""
import sys, os, re, json, shutil, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from seo import DOMAIN, OG_IMAGE, LANGS, PAGES, LEGAL, url, ORG, WEBSITE, service_node, breadcrumbs, faq_node
from meta_i18n import META, SKIP_LINK
from apply_seo import EXTRA, HOME
from bs4 import BeautifulSoup

def rel(lang, slug):
    """Wurzel-relative URL – funktioniert lokal wie auf der Domain."""
    return url(lang, slug).replace(DOMAIN, "") or "/"

OG_LOCALE = {"de":"de_DE","en":"en_GB","it":"it_IT","fr":"fr_FR"}
HTML_LANG = {"de":"de","en":"en","it":"it","fr":"fr"}
SCHEMA_LANG = {"de":"de-DE","en":"en-GB","it":"it-IT","fr":"fr-FR"}

def load_dict(lang):
    """Wörterbuch aus js/lang/<lang>.js über Node auslesen."""
    js = ('global.PH_I18N={registerDict:(c,d)=>process.stdout.write(JSON.stringify(d))};'
          'require("./js/lang/%s.js");' % lang)
    return json.loads(subprocess.run(["node","-e",js],capture_output=True,text=True,check=True).stdout)

def link_map(lang):
    m = {}
    keymap = {"index.html":"home","services.html":"services","pricing.html":"pricing",
              "ueber-uns.html":"about","faq.html":"faq","kontakt.html":"contact",
              "fba-prep-center-deutschland.html":"pillar","fnsku-etikettierung.html":"labeling",
              "fba-lagerung-deutschland.html":"storage","versand-an-amazon.html":"shipping",
              "amazon-retouren-deutschland.html":"returns"}
    for de_file, key in keymap.items():
        m[key] = "./" + PAGES[de_file][0][lang]
    m.update({"imprint":"/impressum.html","privacy":"/datenschutz.html","terms":"/agb.html"})
    return m

def translate(soup, d):
    for el in soup.select("[data-i18n]"):
        key = el.get("data-i18n"); attr = el.get("data-i18n-attr")
        if key not in d: continue
        val = d[key]
        if attr:
            el[attr] = val
        elif not el.find(True):
            el.string = val
        else:
            for node in el.contents:
                if isinstance(node, str) and node.strip():
                    node.replace_with(val); break

def fix_paths(soup):
    """Relative Pfade auf absolute umstellen, damit sie in /en/ … funktionieren."""
    for tag, attr in (("script","src"),("link","href"),("img","src"),("a","href")):
        for el in soup.find_all(tag):
            v = el.get(attr)
            if v and v.startswith("./") and not v.endswith(".html"):
                el[attr] = "/" + v[2:]

def build(lang):
    d = load_dict(lang)
    links = link_map(lang)
    outdir = lang
    os.makedirs(outdir, exist_ok=True)
    for de_file, (slugs, prio, freq) in PAGES.items():
        soup = BeautifulSoup(open(de_file, encoding="utf-8").read(), "lxml")

        soup.html["lang"] = HTML_LANG[lang]
        translate(soup, d)
        fix_paths(soup)

        # interne Seitenlinks auf die Slugs dieser Sprache umschreiben
        for a in soup.find_all("a", href=True):
            h = a["href"].lstrip("./").split("#")[0]
            frag = "#" + a["href"].split("#",1)[1] if "#" in a["href"] else ""
            if h in PAGES:
                a["href"] = "./" + PAGES[h][0][lang] + frag
            elif h in LEGAL:
                a["href"] = "/" + h + frag

        # Titel + Description
        title, desc = META[de_file][lang]
        soup.title.string = title
        for name, val in (("description", desc),):
            m = soup.find("meta", attrs={"name": name})
            if m: m["content"] = val
        for prop, val in (("og:title", title), ("og:description", desc)):
            m = soup.find("meta", attrs={"property": prop})
            if m: m["content"] = val
        for name, val in (("twitter:title", title), ("twitter:description", desc)):
            m = soup.find("meta", attrs={"name": name})
            if m: m["content"] = val
        m = soup.find("meta", attrs={"property": "og:locale"})
        if m: m["content"] = OG_LOCALE[lang]

        # canonical dieser Sprachfassung
        c = soup.find("link", rel="canonical")
        if c: c["href"] = url(lang, slugs[lang])
        m = soup.find("meta", attrs={"property": "og:url"})
        if m: m["content"] = url(lang, slugs[lang])

        # Skip-Link
        sl = soup.select_one("a.skip-link")
        if sl: sl.string = SKIP_LINK[lang]

        # JSON-LD neu aufbauen
        page_url = url(lang, slugs[lang])
        graph = []
        if de_file == "index.html":
            org = json.loads(json.dumps(ORG)); org["url"] = DOMAIN + "/"
            web = json.loads(json.dumps(WEBSITE)); web["inLanguage"] = SCHEMA_LANG[lang]
            graph += [org, web]
        else:
            graph.append({"@type":"WebPage","@id":page_url+"#webpage","url":page_url,
                          "name":title,"description":desc,"inLanguage":SCHEMA_LANG[lang],
                          "isPartOf":{"@id":DOMAIN+"/#website"},
                          "about":{"@id":DOMAIN+"/#organization"}})
        if de_file in EXTRA:
            bcname, svcname, svcdesc = EXTRA[de_file]
            graph.append(breadcrumbs([(d.get("nav.home","Startseite"), url(lang,"index.html")),
                                      (title.split(" – ")[0].split(" | ")[0], page_url)]))
            if svcname:
                graph.append(service_node(svcname, svcdesc, page_url))
        html_now = str(soup)
        fq = faq_node(html_now)
        if fq: graph.append(fq)
        ld = soup.find("script", attrs={"type": "application/ld+json"})
        if ld: ld.string = json.dumps({"@context":"https://schema.org","@graph":graph},
                                      ensure_ascii=False, indent=2)

        # vorhandene (deutsche) Sprach-URL-Tags entfernen
        for sc in soup.find_all("script"):
            if not sc.get("src") and sc.string and "PH_LANG_URLS" in sc.string:
                sc.decompose()

        # Laufzeit-Konfiguration für diese Sprachversion
        cfg = soup.new_tag("script")
        cfg.string = ("window.PH_FORCE_LANG=%s;window.PH_LINKS=%s;window.PH_LANG_URLS=%s;"
                      % (json.dumps(lang), json.dumps(links, ensure_ascii=False),
                         json.dumps({l: rel(l, slugs[l]) for l in LANGS}, ensure_ascii=False)))
        first = soup.find("script", src=True)
        first.insert_before(cfg)

        open(os.path.join(outdir, slugs[lang]), "w", encoding="utf-8").write(str(soup))
    print("built /%s/ – %d pages" % (lang, len(PAGES)))

# Sprachumschalter auch auf den deutschen Seiten auf echte URLs zeigen lassen
def annotate_de():
    for de_file, (slugs, _p, _f) in PAGES.items():
        s = open(de_file, encoding="utf-8").read()
        s = re.sub(r'<script>window\.PH_LANG_URLS=.*?</script>\n', '', s, flags=re.S)
        tag = ('<script>window.PH_LANG_URLS=%s;</script>\n'
               % json.dumps({l: rel(l, slugs[l]) for l in LANGS}, ensure_ascii=False))
        s = s.replace('<script src="./js/config.js"></script>', tag + '<script src="./js/config.js"></script>', 1)
        open(de_file, "w", encoding="utf-8").write(s)
    print("german pages annotated with language URLs")

if __name__ == "__main__":
    for l in ("en", "it", "fr"):
        shutil.rmtree(l, ignore_errors=True)
        build(l)
    annotate_de()

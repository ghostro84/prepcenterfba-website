# -*- coding: utf-8 -*-
"""Rendert die deutschen Seiten als statische EN/IT/FR-Versionen unter /en/, /it/, /fr/."""
import sys, os, re, json, shutil, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from seo import DOMAIN, OG_IMAGE, LANGS, PAGES, LEGAL, LEGAL_SLUGS, url, ORG, WEBSITE, service_node, breadcrumbs, faq_node
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
              "kalkulator.html":"calculator",
              "ueber-uns.html":"about","faq.html":"faq","kontakt.html":"contact",
              "fba-prep-center-deutschland.html":"pillar","fnsku-etikettierung.html":"labeling",
              "fba-lagerung-deutschland.html":"storage","versand-an-amazon.html":"shipping",
              "amazon-retouren-deutschland.html":"returns"}
    for de_file, key in keymap.items():
        m[key] = "./" + PAGES[de_file][0][lang]
    legal_key = {"impressum.html":"imprint","datenschutz.html":"privacy","agb.html":"terms"}
    for de_file, key in legal_key.items():
        m[key] = rel(lang, LEGAL_SLUGS[de_file][lang])
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
            if v and v.startswith("./") and not v.split("#")[0].endswith(".html"):
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
                a["href"] = rel(lang, LEGAL_SLUGS[h][lang]) + frag

        # FormSubmit: Weiterleitung und Betreff in der jeweiligen Sprache
        for inp in soup.find_all("input", attrs={"name": "_next"}):
            inp["value"] = url(lang, slugs[lang]) + "?sent=1"
        for inp in soup.find_all("input", attrs={"name": "_subject"}):
            if d.get("kt.form.subject"):
                inp["value"] = d["kt.form.subject"]

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

        # Genau ein Wörterbuch laden – das der eigenen Sprache
        main_js = soup.find("script", src=lambda v: v and v.endswith("js/main.js"))
        if main_js:
            dict_tag = soup.new_tag("script", src="/js/lang/%s.js" % lang)
            dict_tag["defer"] = ""
            main_js.insert_before(dict_tag)

        open(os.path.join(outdir, slugs[lang]), "w", encoding="utf-8").write(str(soup))
    print("built /%s/ – %d pages" % (lang, len(PAGES)))

def build_legal(lang):
    """Übersetzte Rechtstexte aus src-legal/<lang>/ nach <lang>/ übernehmen und
       die Laufzeit-Konfiguration (Sprache, Navigation, Sprach-URLs) einsetzen."""
    links = link_map(lang)
    built = 0
    for de_file, slugs in LEGAL_SLUGS.items():
        src = os.path.join("src-legal", lang, slugs[lang])
        if not os.path.exists(src):
            print("  ! fehlt:", src); continue
        soup = BeautifulSoup(open(src, encoding="utf-8").read(), "lxml")
        soup.html["lang"] = HTML_LANG[lang]
        fix_paths(soup)

        # canonical / og:url / og:locale / hreflang für diese Sprachfassung
        page_url = url(lang, slugs[lang])
        c = soup.find("link", rel="canonical")
        if c: c["href"] = page_url
        m = soup.find("meta", attrs={"property": "og:url"})
        if m: m["content"] = page_url
        m = soup.find("meta", attrs={"property": "og:locale"})
        if m: m["content"] = OG_LOCALE[lang]
        for alt in soup.find_all("link", rel="alternate"):
            alt.decompose()
        head = soup.find("head")
        for l in LANGS:
            t = soup.new_tag("link", rel="alternate", href=url(l, LEGAL_SLUGS[de_file][l]))
            t["hreflang"] = l
            head.append(t)
        t = soup.new_tag("link", rel="alternate", href=url("de", LEGAL_SLUGS[de_file]["de"]))
        t["hreflang"] = "x-default"
        head.append(t)

        for sc in soup.find_all("script"):
            if not sc.get("src") and sc.string and ("PH_LANG_URLS" in sc.string or "PH_FORCE_LANG" in sc.string):
                sc.decompose()
        cfg = soup.new_tag("script")
        cfg.string = ("window.PH_FORCE_LANG=%s;window.PH_LINKS=%s;window.PH_LANG_URLS=%s;"
                      % (json.dumps(lang), json.dumps(links, ensure_ascii=False),
                         json.dumps({l: rel(l, LEGAL_SLUGS[de_file][l]) for l in LANGS}, ensure_ascii=False)))
        first = soup.find("script", src=True)
        if first:
            first.insert_before(cfg)
            main_js = soup.find("script", src=lambda v: v and v.endswith("js/main.js"))
            if main_js:
                dict_tag = soup.new_tag("script", src="/js/lang/%s.js" % lang)
                dict_tag["defer"] = ""
                main_js.insert_before(dict_tag)
        open(os.path.join(lang, slugs[lang]), "w", encoding="utf-8").write(str(soup))
        built += 1
    print("built /%s/ – %d Rechtstexte" % (lang, built))

# Sprachumschalter auch auf den deutschen Seiten auf echte URLs zeigen lassen
def annotate_de():
    targets = [(f, sl) for f, (sl, _p, _f) in PAGES.items()] + list(LEGAL_SLUGS.items())
    for de_file, slugs in targets:
        s = open(de_file, encoding="utf-8").read()
        s = re.sub(r'<script>window\.(PH_FORCE_LANG|PH_LANG_URLS)=.*?</script>\n', '', s, flags=re.S)
        tag = ('<script>window.PH_FORCE_LANG="de";window.PH_LANG_URLS=%s;</script>\n'
               % json.dumps({l: rel(l, slugs[l]) for l in LANGS}, ensure_ascii=False))
        s = s.replace('<script defer src="./js/config.js"></script>', tag + '<script defer src="./js/config.js"></script>', 1)
        open(de_file, "w", encoding="utf-8").write(s)
    print("deutsche Seiten mit Sprach-URLs versehen (inkl. Rechtstexte)")

if __name__ == "__main__":
    for l in ("en", "it", "fr"):
        shutil.rmtree(l, ignore_errors=True)
        build(l)
        build_legal(l)
    annotate_de()

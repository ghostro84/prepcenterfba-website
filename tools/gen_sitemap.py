# -*- coding: utf-8 -*-
import sys, os, datetime
sys.path.insert(0, os.path.dirname(__file__))
from seo import DOMAIN, LANGS, PAGES, LEGAL, DE_ONLY, url

TODAY = os.environ.get("BUILD_DATE") or datetime.date.today().isoformat()

def lastmod(path):
    """Echtes Änderungsdatum der Datei statt eines pauschalen Build-Datums."""
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()
    except OSError:
        return TODAY

out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9"'.replace("sitemap.org","sitemaps.org"),
       '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']

for de_file, (slugs, prio, freq) in PAGES.items():
    for lang in LANGS:
        loc = url(lang, slugs[lang])
        out.append("  <url>")
        out.append("    <loc>%s</loc>" % loc)
        for alt in LANGS:
            out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (alt, url(alt, slugs[alt])))
        out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % url("de", slugs["de"]))
        out.append("    <lastmod>%s</lastmod>" % lastmod(os.path.join(lang, slugs[lang]) if lang != "de" else de_file))
        out.append("    <changefreq>%s</changefreq>" % freq)
        out.append("    <priority>%s</priority>" % (prio if lang == "de" else "%.1f" % max(0.1, float(prio) - 0.2)))
        out.append("  </url>")

for f, (prio, freq) in DE_ONLY.items():
    out += ["  <url>", "    <loc>%s/%s</loc>" % (DOMAIN, f),
            '    <xhtml:link rel="alternate" hreflang="de" href="%s/%s"/>' % (DOMAIN, f),
            '    <xhtml:link rel="alternate" hreflang="x-default" href="%s/%s"/>' % (DOMAIN, f),
            "    <lastmod>%s</lastmod>" % lastmod(f),
            "    <changefreq>%s</changefreq>" % freq,
            "    <priority>%s</priority>" % prio, "  </url>"]

# Rechtstexte stehen bewusst NICHT in der Sitemap: sie tragen
# <meta name="robots" content="noindex"> – beides zusammen wäre ein
# widersprüchliches Signal und erzeugt Fehler in der Search Console.

out.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("sitemap.xml:", sum(1 for l in out if l.strip().startswith("<loc>")), "URLs")

open("robots.txt", "w", encoding="utf-8").write(
"""User-agent: *
Allow: /

# Interne Build-Dateien (werden zusätzlich per _config.yml vom Deploy ausgeschlossen)
Disallow: /tools/
Disallow: /README-DEPLOY.md
Disallow: /SEO-SETUP.md

Sitemap: %s/sitemap.xml
""" % DOMAIN)
print("robots.txt written")

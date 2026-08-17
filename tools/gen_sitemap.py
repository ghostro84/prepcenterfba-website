# -*- coding: utf-8 -*-
import sys, os, datetime
sys.path.insert(0, os.path.dirname(__file__))
from seo import DOMAIN, LANGS, PAGES, LEGAL, url

TODAY = os.environ.get("BUILD_DATE", "2026-08-17")

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
        out.append("    <lastmod>%s</lastmod>" % TODAY)
        out.append("    <changefreq>%s</changefreq>" % freq)
        out.append("    <priority>%s</priority>" % (prio if lang == "de" else "%.1f" % max(0.1, float(prio) - 0.2)))
        out.append("  </url>")

for f in LEGAL:
    out += ["  <url>", "    <loc>%s/%s</loc>" % (DOMAIN, f),
            "    <lastmod>%s</lastmod>" % TODAY,
            "    <changefreq>yearly</changefreq>", "    <priority>0.2</priority>", "  </url>"]

out.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("sitemap.xml:", sum(1 for l in out if l.strip().startswith("<loc>")), "URLs")

open("robots.txt", "w", encoding="utf-8").write(
"""User-agent: *
Allow: /

# Keine Suchmaschinen-Indexierung interner Build-Dateien
Disallow: /tools/

Sitemap: %s/sitemap.xml
""" % DOMAIN)
print("robots.txt written")

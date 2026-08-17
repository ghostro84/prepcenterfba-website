# -*- coding: utf-8 -*-
"""Erzeugt die neuen deutschen Inhaltsseiten für prepcenterfba.eu."""
import io, os

HEAD = '''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{ogdesc}">
  <meta property="og:type" content="website">
  <link rel="icon" href="./favicon.ico" sizes="any">
  <link rel="icon" href="./favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="./apple-touch-icon.png">
  <link rel="stylesheet" crossorigin href="/assets/style-STZ1_Fzx.css">
</head>
<body>

<a href="#main-content" class="skip-link">Zum Inhalt springen</a>

<div id="site-header"></div>

<main id="main-content">

<section class="page-hero" aria-labelledby="page-title">
  <div class="container">
    <span class="badge badge--blue" data-i18n="{k}.badge">{badge}</span>
    <h1 id="page-title" data-i18n="{k}.h1">{h1}</h1>
    <p class="lead" data-i18n="{k}.lead">{lead}</p>
  </div>
</section>

'''

FOOT = '''
</main>

<div id="site-footer"></div>

<div id="cookie-banner" class="cookie-banner" role="alertdialog" aria-label="Cookie-Einstellungen" aria-live="polite" hidden>
  <div class="cookie-banner__inner">
    <p data-i18n="cookie.text">Wir verwenden ausschließlich technisch notwendige Cookies bzw. lokalen Speicher für den Betrieb dieser Website. <a href="./datenschutz.html">Mehr erfahren</a>.</p>
    <div class="cookie-actions">
      <button id="cookie-necessary" class="btn btn--primary btn--sm" data-i18n="cookie.necessary">Nur notwendige</button>
      <button id="cookie-all" class="btn btn--outline-light btn--sm" data-i18n="cookie.all">Alle akzeptieren</button>
    </div>
  </div>
</div>

<script src="./js/config.js"></script>
<script src="./js/i18n.js"></script>
<script src="./js/lang/en.js"></script>
<script src="./js/lang/it.js"></script>
<script src="./js/lang/fr.js"></script>
<script src="./js/main.js"></script>
<script src="./js/cms-client.js"></script>
<script src="./js/analytics.js"></script>
</body>
</html>
'''

CTA = '''
<section class="cta-band" aria-labelledby="{k}-cta-heading">
  <div class="container">
    <h2 id="{k}-cta-heading" data-i18n="{k}.cta.title">{title}</h2>
    <p data-i18n="{k}.cta.sub">{sub}</p>
    <div class="btn-group">
      <a href="./kontakt.html" class="btn btn--primary btn--lg" data-i18n="{k}.cta.primary">Angebot anfragen</a>
      <a href="./pricing.html" class="btn btn--outline-light btn--lg" data-i18n="{k}.cta.secondary">Preise ansehen</a>
    </div>
  </div>
</section>
'''

def section(k, i, heading, paras, cls="section", label=None, extra=""):
    out = ['<section class="%s" aria-labelledby="%s-h%d">' % (cls, k, i),
           '  <div class="container" style="max-width:820px;">']
    if label:
        out.append('    <span class="section-label" data-i18n="%s.s%d.label">%s</span>' % (k, i, label))
    out.append('    <h2 class="section-title" id="%s-h%d" data-i18n="%s.s%d.h">%s</h2>' % (k, i, k, i, heading))
    for n, p in enumerate(paras, 1):
        out.append('    <p data-i18n="%s.s%d.p%d" style="max-width:none">%s</p>' % (k, i, n, p))
    if extra:
        out.append(extra)
    out += ['  </div>', '</section>', '']
    return "\n".join(out)

def checklist(k, i, items):
    rows = []
    for n, it in enumerate(items, 1):
        rows.append('        <li class="checklist-item"><span class="checklist-item__icon">'
                    '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8l3.5 3.5L13 5" stroke="currentColor" '
                    'stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
                    '<span data-i18n="%s.s%d.li%d">%s</span></li>' % (k, i, n, it))
    return ('    <ul class="checklist" role="list" style="margin-top:1.25rem">\n' +
            "\n".join(rows) + '\n    </ul>')

def faq_items(k, qas, start=1):
    out = ['    <div class="faq-list">']
    for n, (q, a) in enumerate(qas, start):
        out.append('      <details class="faq-item">')
        out.append('        <summary><span data-i18n="%s.q%d">%s</span>'
                   '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true">'
                   '<path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.6" fill="none" '
                   'stroke-linecap="round"/></svg></summary>' % (k, n, q))
        out.append('        <div class="faq-item__body" data-i18n="%s.a%d">%s</div>' % (k, n, a))
        out.append('      </details>')
    out.append('    </div>')
    return "\n".join(out)

# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from newpages import HEAD, FOOT, CTA, section, checklist as CL, faq_items

W = lambda n, s: open(n, "w", encoding="utf-8").write(s)

def build(fname, k, title, desc, ogdesc, badge, h1, lead, blocks, faqs, cta, related):
    s = HEAD.format(title=title, desc=desc, ogdesc=ogdesc, k=k, badge=badge, h1=h1, lead=lead)
    for i, b in enumerate(blocks, 1):
        s += section(k, i, b["h"], b["p"], cls=b.get("cls", "section"),
                     label=b.get("label"), extra=b.get("extra", ""))
    if faqs:
        s += ('<section class="section section--surface">\n  <div class="container" style="max-width:820px;">\n'
              '    <span class="section-label" data-i18n="%s.faq.label">FAQ</span>\n'
              '    <h2 class="section-title" data-i18n="%s.faq.h">Häufige Fragen</h2>\n' % (k, k))
        s += faq_items(k, faqs) + "\n  </div>\n</section>\n"
    if related:
        rows = "\n".join('        <li><a href="%s" data-i18n="%s.rel%d">%s</a></li>' % (h, k, n, t)
                         for n, (h, t) in enumerate(related, 1))
        s += ('<section class="section section--sm">\n  <div class="container" style="max-width:820px;">\n'
              '    <h2 class="section-title" style="font-size:1.15rem" data-i18n="%s.rel.h">Weiterführende Seiten</h2>\n'
              '    <ul class="related-links" role="list">\n%s\n    </ul>\n  </div>\n</section>\n' % (k, rows))
    s += CTA.format(k=k, title=cta[0], sub=cta[1])
    s += FOOT
    W(fname, s); print("wrote", fname)

from newpages import section

# ══════════════════ 3. LAGERUNG ══════════════════
k = "storage"
build("fba-lagerung-deutschland.html", k,
 "FBA Lagerung Deutschland – Zwischenlager vor der Amazon-Einlieferung | PrepCenter FBA",
 "Lagerung vor der FBA-Einlieferung in Deutschland: 14 Tage kostenfrei bei gebuchtem Prep, danach 1,20 € pro Karton und 19,00 € pro Palette im Monat. Abrufbar in Teilmengen.",
 "Pre-FBA-Lagerung in Deutschland – kostenfreie Zwischenlagerung und planbare Nachschublieferungen.",
 "Lagerung",
 "Lagerung vor der Amazon-Einlieferung",
 "Ware in Deutschland puffern und in Teilmengen an Amazon nachliefern – statt das komplette Volumen sofort ins FBA-Lager zu schieben.",
 [
  {"label":"Nutzen","h":"Warum eine Zwischenlagerung sinnvoll ist","p":[
    "Amazon berechnet Lagergebühren nach belegtem Volumen und erhöht sie im vierten Quartal deutlich. Zusätzlich begrenzt Amazon über die Kapazitätslimits, wie viel Bestand ein Verkäuferkonto überhaupt einlagern darf. Wer eine ganze Containerlieferung auf einmal ins FBA-Lager schickt, zahlt daher doppelt: einmal für Lagerplatz, den er noch nicht braucht, und einmal in Form von Limits, die für schnelldrehende Artikel fehlen.",
    "Die praktikable Alternative ist ein Puffer in Deutschland: Die Gesamtmenge kommt zu uns, wird geprüft und vorbereitet, und Sie rufen in Teilmengen ab, wenn der Bestand bei Amazon zur Neige geht.",
    "Damit bleibt die Kapitalbindung dieselbe, die Lagerkosten sinken, und Sie behalten die Kontrolle darüber, welche Menge wann im FBA-Netz liegt."]},

  {"label":"Konditionen","cls":"section section--surface","h":"Was die Lagerung kostet","p":[
    "Für Ware, für die gleichzeitig eine FBA-Prep-Leistung gebucht ist, sind die ersten 14 Tage Zwischenlagerung kostenfrei. Danach berechnen wir anteilig nach tatsächlicher Lagerdauer."],
   "extra": CL(k,2,[
    "<strong>Zwischenlagerung mit gebuchtem FBA-Prep:</strong> erste 14 Tage 0,00 €.",
    "<strong>Lagerung Karton:</strong> 1,20 € pro Karton und Monat.",
    "<strong>Lagerung Palette:</strong> 19,00 € pro Europalette und Monat.",
    "<strong>Lagerung Kleinmengen:</strong> 2,00 € pro Monat für ein dediziertes Regalfach – passend für Testsendungen.",
    "<strong>Wareneingang ohne Prep:</strong> 1,50 € pro Karton, 6,00 € pro Palette.",
   ])},

  {"label":"Ablauf","h":"Nachschub abrufen","p":[
    "Wenn Sie eine Teilmenge an Amazon nachliefern möchten, erstellen Sie den Shipping Plan in Seller Central und schicken uns die Shipment-ID mit den Versandetiketten und der gewünschten Stückzahl.",
    "Wir kommissionieren aus dem eingelagerten Bestand, konfektionieren die Sendungskartons oder Paletten nach den Amazon-Vorgaben und übergeben sie an den Spediteur. Das FBA Karton-Handling kostet 2,90 € pro Karton, das Paletten-Handling 18,00 € pro Palette.",
    "Der verbleibende Bestand bleibt eingelagert und steht für den nächsten Abruf bereit."]},

  {"label":"Grenzen","cls":"section section--surface","h":"Was wir nicht einlagern","p":[
    "Wir lagern keine Gefahrgüter, keine kühlpflichtige Ware und keine Artikel, die besonderen behördlichen Auflagen unterliegen, sofern dies nicht ausdrücklich und schriftlich vereinbart wurde.",
    "Bei Ware, die länger als 60 Tage ohne Auslieferungsauftrag liegt, melden wir uns schriftlich mit einer Frist von 14 Tagen, bevor wir eine anderweitige Einlagerung oder Entsorgung veranlassen. Die Einzelheiten regeln § 7 unserer AGB."]},
 ],
 [
  ("Wie lange kann ich Ware bei Ihnen lagern?",
   "Grundsätzlich unbefristet. Kostenfrei sind die ersten 14 Tage bei gebuchter FBA-Prep-Leistung; danach rechnen wir monatlich anteilig ab. Nach 60 Tagen ohne Auslieferungsauftrag melden wir uns bei Ihnen."),
  ("Wird taggenau oder monatlich abgerechnet?",
   "Anteilig nach tatsächlicher Lagerdauer, ausgehend von den monatlichen Sätzen pro Karton bzw. Palette."),
  ("Kann ich Teilmengen abrufen?",
   "Ja, das ist der Regelfall. Sie melden Shipment-ID und gewünschte Stückzahl, wir kommissionieren und liefern ein; der Rest bleibt eingelagert."),
  ("Ist die Ware versichert?",
   "Für Sachschäden an eingelagerter Ware gelten die Haftungsregelungen aus § 6 unserer AGB. Eine darüber hinausgehende Warenversicherung schließen Sie bitte selbst ab."),
 ],
 ("Lagerbedarf besprechen",
  "Sagen Sie uns, wie viele Kartons oder Paletten Sie puffern möchten – wir kalkulieren die Lagerkosten konkret."),
 [("./fba-prep-center-deutschland.html","FBA Prep Center Deutschland – Überblick"),
  ("./versand-an-amazon.html","Einlieferung und Versand an Amazon"),
  ("./pricing.html","Preisliste und Kostenrechner")])

# ══════════════════ 4. VERSAND / EINLIEFERUNG ══════════════════
k = "shipping"
build("versand-an-amazon.html", k,
 "Versand an Amazon FBA – Einlieferung aus Deutschland | PrepCenter FBA",
 "Einlieferung an Amazon FBA aus Deutschland: Kartons und Paletten Amazon-konform konfektioniert, beschriftet und an den Spediteur übergeben. 2,90 € pro Karton, 18,00 € pro Palette.",
 "Amazon-konforme Einlieferung an FBA – Kartons und Paletten aus Deutschland.",
 "Einlieferung",
 "Versand und Einlieferung an Amazon FBA",
 "Wir konfektionieren Ihre Sendung nach den Amazon-Vorgaben und übergeben sie an den Spediteur – Sie behalten die Kontrolle über Shipping Plan und Carrier.",
 [
  {"label":"Ablauf","h":"Wie die Einlieferung abläuft","p":[
    "Die Einlieferung an Amazon beginnt in Ihrem Seller Central: Sie erstellen den Shipping Plan, legen fest, welche Artikel in welcher Menge an welches Fulfillment-Center gehen, und erhalten Shipment-ID sowie Versandetiketten.",
    "Diese Angaben übermitteln Sie uns. Wir kommissionieren die Ware aus dem Bestand, verpacken sie nach den Vorgaben für Karton- und Palettensendungen, bringen die Box- bzw. Palettenetiketten an und übergeben die Sendung an den von Ihnen gewählten Spediteur – auch über das Amazon Partnered Carrier Programm.",
    "Sie erhalten von uns eine Bestätigung mit Anzahl der Packstücke, sobald die Sendung übergeben wurde."]},

  {"label":"Anforderungen","cls":"section section--surface","h":"Was Amazon von der Sendung verlangt","p":[
    "Die Anforderungen für eingehende Sendungen sind detailliert und werden im Wareneingang geprüft:"],
   "extra": CL(k,2,[
    "Kartons dürfen in der Regel 23 kg nicht überschreiten; schwerere Einheiten brauchen einen entsprechenden Warnaufkleber.",
    "Jeder Karton trägt ein eigenes, scanbares FBA-Boxetikett zusätzlich zum Versandetikett des Carriers.",
    "Paletten müssen den Vorgaben für Höhe, Umreifung und Stapelbarkeit entsprechen und ein Palettenetikett auf allen vier Seiten tragen.",
    "Mehrere Artikel in einem Karton sind zulässig, sofern der Karteninhalt dem Shipping Plan entspricht.",
    "Alte Versand- und Barcodeetiketten auf Umkartons müssen entfernt oder überklebt sein.",
   ])},

  {"label":"Preise","h":"Was die Einlieferung kostet","p":[
    "Das FBA Karton-Handling kostet 2,90 € pro Karton und umfasst Kommissionierung, Konfektionierung, Etikettierung des Packstücks und Übergabe an den Spediteur. Das Paletten-Handling liegt bei 18,00 € pro Palette.",
    "Die Transportkosten selbst stellt Ihr Spediteur bzw. Amazon direkt in Rechnung – wir schlagen darauf nichts auf und verdienen an der Fracht nichts.",
    "Alle Preise verstehen sich netto zuzüglich der gesetzlichen Umsatzsteuer."]},

  {"label":"FBM","cls":"section section--surface","h":"Auch für FBM-Sendungen","p":[
    "Wenn Sie Bestellungen selbst versenden (Fulfillment by Merchant), bereiten wir die Sendungen ebenso vor: Kommissionierung aus dem eingelagerten Bestand, Verpackung und Übergabe an den Paketdienst mit Ihrem Versandetikett.",
    "So können Sie denselben Lagerbestand für FBA-Nachschub und für den Eigenversand nutzen, ohne die Ware doppelt vorzuhalten."]},
 ],
 [
  ("Erstellen Sie den Shipping Plan für mich?",
   "Der Shipping Plan wird in Ihrem Seller Central erstellt – wir haben keinen Zugriff auf Ihr Konto. Sie übermitteln uns Shipment-ID und Etiketten, den Rest übernehmen wir."),
  ("Kann ich meinen eigenen Spediteur nutzen?",
   "Ja. Wir übergeben an den Carrier Ihrer Wahl, einschließlich Amazon Partnered Carrier."),
  ("Liefern Sie an mehrere Fulfillment-Center gleichzeitig ein?",
   "Ja. Wenn Amazon Ihre Sendung auf mehrere Standorte aufteilt, konfektionieren wir entsprechend getrennte Sendungen."),
  ("Was passiert, wenn Amazon eine Sendung beanstandet?",
   "Wir dokumentieren Packstückzahl und Etikettierung bei der Übergabe. Bei einer Beanstandung können Sie diese Dokumentation für Ihren Fall bei Amazon verwenden."),
 ],
 ("Einlieferung planen",
  "Nennen Sie uns Volumen und Zielmarkt – wir sagen Ihnen, wie wir die Sendung am effizientesten konfektionieren."),
 [("./fba-prep-center-deutschland.html","FBA Prep Center Deutschland – Überblick"),
  ("./fba-lagerung-deutschland.html","Lagerung vor der Einlieferung"),
  ("./pricing.html","Preisliste und Kostenrechner")])

# ══════════════════ 5. RETOUREN ══════════════════
k = "returns"
build("amazon-retouren-deutschland.html", k,
 "Amazon Retouren & Removal Orders Deutschland | PrepCenter FBA",
 "Retourenbearbeitung für Amazon-Händler in Deutschland: Annahme, Zustandsprüfung mit Protokoll, Wiederaufbereitung für die erneute FBA-Einlieferung oder fachgerechte Entsorgung. Ab 0,90 € pro Einheit.",
 "Amazon-Retouren und Removal Orders in Deutschland prüfen, aufbereiten und wieder einliefern.",
 "Retouren",
 "Retouren und Removal Orders bearbeiten",
 "Statt Retouren pauschal abzuschreiben: prüfen, dokumentieren und den verkaufsfähigen Teil wieder in den Bestand bringen.",
 [
  {"label":"Ausgangslage","h":"Warum Retouren eine Adresse in Deutschland brauchen","p":[
    "Amazon sendet Retouren und Removal Orders an eine Adresse in dem Land, in dem der Bestand liegt. Verkäufer ohne eigenen Standort in Deutschland stehen damit vor der Wahl, entweder eine teure internationale Rücksendung zu organisieren oder die Ware bei Amazon entsorgen zu lassen.",
    "Beides ist selten wirtschaftlich, denn ein erheblicher Teil der Retouren ist unbeschädigt: Fehlbestellungen, geöffnete, aber intakte Verpackungen, Größenrückgaben. Diese Einheiten lassen sich nach einer Sichtprüfung und gegebenenfalls einer Umverpackung erneut einliefern.",
    "Wir stellen die deutsche Retourenadresse und übernehmen die Bearbeitung."]},

  {"label":"Leistungen","cls":"section section--surface","h":"Was wir mit einer Retoure machen","p":[
    "Jede eingehende Einheit durchläuft denselben Ablauf:"],
   "extra": CL(k,2,[
    "<strong>Annahme und Zuordnung</strong> der Rücksendung zu Ihrem Bestand.",
    "<strong>Sichtprüfung jeder Einheit</strong> auf Vollständigkeit, Beschädigung und Verpackungszustand – 0,90 € pro Einheit inklusive schriftlichem Zustandsprotokoll.",
    "<strong>Fotodokumentation</strong> auf Wunsch, 0,30 € pro Foto.",
    "<strong>Umverpackung</strong> verkaufsfähiger Einheiten für die erneute FBA-Einlieferung – 0,50 € pro Einheit zusätzlich zur Retourenannahme.",
    "<strong>Neue FNSKU-Etikettierung</strong>, falls das Originaletikett beschädigt ist – 0,39 € pro Einheit.",
    "<strong>Fachgerechte Entsorgung</strong> nicht mehr verkaufsfähiger Artikel – 0,30 € pro Einheit.",
   ])},

  {"label":"Removals","h":"Removal Orders aus dem FBA-Lager","p":[
    "Auch Removal Orders – also Bestände, die Sie aus dem Amazon-Lager zurückholen, etwa vor der Erhöhung der Langzeitlagergebühren – können Sie an uns adressieren.",
    "Wir nehmen die Sendung an, gleichen sie gegen die Removal-Liste ab und prüfen den Zustand. Danach entscheiden Sie pro Position: erneut einliefern, für den Eigenversand einlagern oder entsorgen.",
    "Da Amazon Removal-Sendungen häufig in gemischten Kartons versendet, ist die Sortierung und Zuordnung Teil der Leistung."]},
 ],
 [
  ("Kann ich Ihre Adresse als Retourenadresse in Seller Central hinterlegen?",
   "Ja. Sprechen Sie uns vorher an, damit wir die zu erwartenden Volumina einplanen und die eingehenden Sendungen korrekt Ihrem Konto zuordnen können."),
  ("Was kostet die Bearbeitung einer Retoure?",
   "Die Annahme inklusive Sichtprüfung und Zustandsprotokoll kostet 0,90 € pro Einheit. Umverpackung schlägt mit 0,50 € pro Einheit zu Buche, Entsorgung mit 0,30 €."),
  ("Wie erfahre ich, in welchem Zustand die Ware ist?",
   "Sie erhalten ein schriftliches Zustandsprotokoll je Charge. Auf Wunsch dokumentieren wir einzelne Einheiten zusätzlich per Foto."),
  ("Können Sie beschädigte Ware reparieren?",
   "Nein. Wir prüfen, sortieren, verpacken um und entsorgen – Reparaturen oder Aufarbeitungen über die Umverpackung hinaus gehören nicht zu unserem Leistungsumfang."),
 ],
 ("Retourenprozess besprechen",
  "Schildern Sie uns Ihr Retourenaufkommen – wir schlagen einen Ablauf vor, der zu Ihrem Volumen passt."),
 [("./fba-prep-center-deutschland.html","FBA Prep Center Deutschland – Überblick"),
  ("./fba-lagerung-deutschland.html","Lagerung und Nachschub"),
  ("./services.html","Alle Leistungen im Überblick")])

# ══════════════════ 6. LOKAL: BAYERN ══════════════════
k = "bayern"
build("fba-prep-center-bayern.html", k,
 "FBA Prep Center Bayern – Freilassing bei Salzburg | PrepCenter FBA",
 "FBA Prep Center in Bayern: Standort Freilassing an der Grenze zu Salzburg, kurze Wege nach München, Österreich und Norditalien. Wareneingang, Etikettierung, Lagerung und FBA-Einlieferung.",
 "Ihr FBA Prep Center in Bayern – Standort Freilassing, direkt an der Grenze zu Salzburg.",
 "Standort Bayern",
 "FBA Prep Center in Bayern – Standort Freilassing",
 "Im Südosten Bayerns, direkt an der Grenze zu Salzburg: kurze Wege für Händler aus Süddeutschland, Österreich und Norditalien.",
 [
  {"label":"Lage","h":"Warum der Standort für süddeutsche Händler funktioniert","p":[
    "Freilassing liegt im Berchtesgadener Land unmittelbar an der bayerisch-österreichischen Grenze und damit an der Achse zwischen München, Salzburg und dem Alpenübergang Richtung Italien. Für Händler aus Bayern, Baden-Württemberg, Österreich und Norditalien ist der Weg zu uns kurz – und der Weg von uns zu den Amazon-Standorten in Süddeutschland ebenfalls.",
    "Für Sie bedeutet das niedrigere Anfahrtskosten bei der Anlieferung und weniger Transporttage, bevor Ihre Ware im FBA-Netz verfügbar ist.",
    "Wir arbeiten selbstverständlich auch für Händler aus dem übrigen Bundesgebiet und aus ganz Europa – die Anlieferung erfolgt dann per Spedition oder Paketdienst."]},

  {"label":"Leistungen","cls":"section section--surface","h":"Leistungen am Standort","p":[
    "Am Standort Freilassing erbringen wir den kompletten Leistungsumfang: Wareneingang für Kartons und Paletten, Qualitätskontrolle, FNSKU-Etikettierung, Polybag- und Bubble-Wrap-Verpackung, Bundling, Zwischenlagerung sowie die Konfektionierung und Übergabe der FBA-Sendungen an den Spediteur.",
    "Auch Retouren und Removal Orders können Sie an unsere Adresse in Bayern senden lassen.",
    "Anlieferungen kündigen Sie bitte vorab per E-Mail an, damit wir die Annahme einplanen können."]},

  {"label":"Einzugsgebiet","h":"Für welche Regionen wir typischerweise arbeiten","p":[
    "Der überwiegende Teil unserer Anlieferungen kommt aus Bayern – insbesondere aus dem Großraum München, aus Rosenheim, Traunstein und dem Berchtesgadener Land –, dazu aus Salzburg und Oberösterreich sowie von europäischen Verkäufern, die einen Eingangspunkt nach Deutschland benötigen.",
    "Wir betreiben bewusst nur diesen einen Standort. Seiten, die Prep-Leistungen für Städte versprechen, an denen kein Lager existiert, helfen niemandem weiter – die Ware muss ohnehin dorthin transportiert werden, wo sie bearbeitet wird."]},
 ],
 [
  ("Kann ich die Ware persönlich vorbeibringen?",
   "Ja, nach vorheriger Terminabsprache per E-Mail. Bitte melden Sie sich vorab, damit die Annahme eingeplant werden kann."),
  ("Nehmen Sie Speditionslieferungen mit Palette an?",
   "Ja. Die Palettenannahme kostet 6,00 € pro Palette und umfasst Entladung, Stückzahlkontrolle und Einbuchung. Bitte kündigen Sie Speditionslieferungen vorab an."),
  ("Arbeiten Sie auch für Händler aus Österreich?",
   "Ja. Durch die unmittelbare Grenzlage zu Salzburg ist der Weg für österreichische Händler besonders kurz."),
 ],
 ("Anlieferung aus Ihrer Region planen",
  "Sagen Sie uns, woher die Ware kommt und wie sie anliefert wird – wir stimmen den Ablauf mit Ihnen ab."),
 [("./fba-prep-center-deutschland.html","FBA Prep Center Deutschland – Überblick"),
  ("./kontakt.html","Anschrift und Anlieferhinweise"),
  ("./ueber-uns.html","Über uns")])

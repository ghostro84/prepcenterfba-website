# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from newpages import HEAD, FOOT, CTA, section, checklist, faq_items

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
        rows = "\n".join(
            '        <li><a href="%s" data-i18n="%s.rel%d">%s</a></li>' % (h, k, n, t)
            for n, (h, t) in enumerate(related, 1))
        s += ('<section class="section section--sm">\n  <div class="container" style="max-width:820px;">\n'
              '    <h2 class="section-title" style="font-size:1.15rem" data-i18n="%s.rel.h">Weiterführende Seiten</h2>\n'
              '    <ul class="related-links" role="list">\n%s\n    </ul>\n  </div>\n</section>\n' % (k, rows))
    s += CTA.format(k=k, title=cta[0], sub=cta[1])
    s += FOOT
    W(fname, s)
    print("wrote", fname)

CL = checklist

# ══════════════════ 1. PILLAR ══════════════════
k = "pillar"
build("fba-prep-center-deutschland.html", k,
 "FBA Prep Center Deutschland – Amazon Prep Service | PrepCenter FBA",
 "FBA Prep Center in Deutschland: Wareneingang, FNSKU-Etikettierung, Qualitätskontrolle, Polybag, Bundling, Lagerung und Einlieferung an Amazon FBA. Feste Preise ab 0,39 €, Durchlaufzeit 24–48 Stunden.",
 "Amazon FBA Prep Center in Deutschland – alle Prep-Schritte aus einer Hand, zu festen Preisen.",
 "FBA Prep Center",
 "FBA Prep Center Deutschland – alle Prep-Schritte aus einer Hand",
 "Wir übernehmen die komplette Vorbereitung Ihrer Ware für Amazon FBA: Annahme, Prüfung, Etikettierung, Verpackung und Einlieferung – an einem Standort in Deutschland, zu festen Preisen pro Einheit.",
 [
  {"label":"Grundlagen","h":"Was ist ein FBA Prep Center?","p":[
    "Ein FBA Prep Center ist ein Dienstleister, der Ware im Auftrag eines Amazon-Händlers so vorbereitet, dass Amazon sie im Fulfillment-Center annimmt. Amazon stellt an eingehende Sendungen konkrete Anforderungen: Jede verkaufsfähige Einheit braucht ein scanbares FNSKU-Etikett, bestimmte Produktgruppen müssen in Polybeutel oder Luftpolsterfolie verpackt sein, Sets müssen als Bundle gekennzeichnet werden, und Kartons und Paletten müssen den Vorgaben für Gewicht, Beschriftung und Stapelung entsprechen.",
    "Wird auch nur einer dieser Punkte nicht erfüllt, drohen Bearbeitungsgebühren („Unplanned Prep Service Fee“), verzögerte Einbuchungen oder im Extremfall die Rücksendung der kompletten Lieferung. Ein Prep Center übernimmt genau diese Arbeitsschritte – und die Verantwortung dafür, dass die Sendung Amazon-konform ankommt.",
    "Für Händler bedeutet das vor allem eines: Sie kaufen Ware ein und verkaufen sie, ohne selbst Lagerfläche, Etikettendrucker und Personal für das Handling vorzuhalten."]},

  {"label":"Leistungen","cls":"section section--surface","h":"Welche Leistungen wir übernehmen","p":[
    "Unser Leistungsumfang deckt die gesamte Kette zwischen Wareneingang und FBA-Einlieferung ab. Sie können alles als Komplettpaket buchen oder einzelne Schritte kombinieren."],
   "extra": CL(k,2,[
    "<strong>Wareneingang:</strong> Annahme von Kartons und Paletten inklusive Stückzahlkontrolle und Einbuchung.",
    "<strong>Qualitätskontrolle:</strong> Sichtprüfung auf Transportschäden, Vollständigkeit und Verpackungszustand.",
    "<strong>FNSKU-Etikettierung:</strong> Anbringen des Amazon-Barcodes auf jeder Einheit, mit Ihren oder unseren Etiketten.",
    "<strong>Verpackung:</strong> Polybag mit Erstickungswarnung, Luftpolsterfolie für empfindliche Artikel, Umverpackung in neue Kartons.",
    "<strong>Bundling und Multipacking:</strong> Zusammenstellung mehrerer Artikel zu einer verkaufsfähigen Einheit inklusive Bundle-Etikett.",
    "<strong>Zwischenlagerung:</strong> Bei gebuchtem FBA-Prep die ersten 14 Tage kostenfrei.",
    "<strong>Einlieferung an Amazon FBA:</strong> Konfektionierung der Sendungskartons oder Paletten und Übergabe an den Spediteur.",
    "<strong>Retourenbearbeitung:</strong> Annahme, Zustandsprüfung, Wiederaufbereitung oder fachgerechte Entsorgung.",
   ])},

  {"label":"Ablauf","h":"So läuft die Zusammenarbeit ab","p":[
    "<strong>1. Anfrage.</strong> Sie schildern uns Produkte, monatliches Volumen und die gewünschten Leistungen. Sie erhalten innerhalb von 24 Stunden ein Angebot auf Basis unserer veröffentlichten Preisliste.",
    "<strong>2. Anlieferung.</strong> Sie kündigen die Sendung per E-Mail an und lassen sie per Paketdienst oder Spedition zu uns liefern. Wir nehmen die Ware an, zählen sie und bestätigen den Eingang.",
    "<strong>3. Bearbeitung.</strong> Innerhalb von 24–48 Stunden führen wir die beauftragten Prep-Schritte durch. Auffälligkeiten melden wir Ihnen, bevor wir weiterarbeiten.",
    "<strong>4. Einlieferung.</strong> Sie erstellen den Shipping Plan in Seller Central und übermitteln uns die Shipment-ID sowie die Versandetiketten. Wir konfektionieren die Sendung und übergeben sie an den Spediteur.",
    "<strong>5. Abrechnung.</strong> Wir rechnen nach tatsächlich erbrachten Leistungen zu den Preisen ab, die Sie vorher gesehen haben. Zahlungsziel 14 Tage."]},

  {"label":"Preise","cls":"section section--surface","h":"Was kostet ein FBA Prep Center in Deutschland?","p":[
    "Wir arbeiten mit festen Preisen pro Einheit statt mit Paketen oder monatlichen Grundgebühren. Der FBA Komplett-Prep kostet 0,79 € pro Einheit, die reine FNSKU-Etikettierung 0,39 €, die Qualitätskontrolle 0,25 € und die Polybag-Verpackung 0,29 € pro Einheit. Die Palettenannahme liegt bei 6,00 €, das FBA Karton-Handling bei 2,90 € pro Karton.",
    "Es gibt keine Mindestmenge an Einheiten. Es gilt lediglich ein Mindestauftragswert von 25,00 € netto je Einzelauftrag für Prep-Leistungen. Neukunden erhalten 10 % Rabatt auf die erste und 5 % auf die zweite Lieferung. Alle Preise verstehen sich netto zuzüglich der gesetzlichen Umsatzsteuer.",
    "Die vollständige Preisliste mit allen Positionen sowie ein Kostenrechner stehen auf der Preisseite zur Verfügung."]},

  {"label":"Auswahl","h":"Worauf Sie bei der Auswahl eines Prep Centers achten sollten","p":[
    "Der Preis pro Einheit ist nur die halbe Information. Entscheidend ist, was darin enthalten ist und was zusätzlich berechnet wird – Etikettendruck, Material für Polybeutel, Kartonhandling, Lagerung nach der Freifrist. Lassen Sie sich die Positionen einzeln aufschlüsseln, bevor Sie sich festlegen.",
    "Ebenso wichtig ist die zugesagte Durchlaufzeit ab Wareneingang und die Frage, was passiert, wenn eine Lieferung beschädigt oder unvollständig ankommt. Ein belastbarer Prozess meldet solche Fälle vor der weiteren Bearbeitung und dokumentiert sie, statt sie stillschweigend durchlaufen zu lassen.",
    "Prüfen Sie schließlich, ob der Dienstleister eine physische Adresse in Deutschland und ein vollständiges Impressum hat. Für die Einfuhr und die umsatzsteuerliche Behandlung Ihrer Ware ist das kein Detail, sondern Voraussetzung."]},
 ],
 [
  ("Was ist der Unterschied zwischen einem Prep Center und einem 3PL?",
   "Ein Prep Center bereitet Ware für die Einlieferung an Amazon FBA vor – Amazon übernimmt danach Lagerung und Versand an den Endkunden. Ein 3PL lagert Ihre Ware dauerhaft und versendet selbst an Endkunden (FBM). Wir decken beides ab: Prep für FBA sowie Lagerung und Versandvorbereitung für FBM-Sendungen."),
  ("Wie lange dauert die Bearbeitung?",
   "Bei Standardaufträgen 24–48 Stunden ab Wareneingang. Größere oder aufwendige Sendungen stimmen wir vorab terminlich mit Ihnen ab."),
  ("Kann ich Ware direkt vom Hersteller zu Ihnen liefern lassen?",
   "Ja. Viele Auftraggeber lassen Ware direkt vom Lieferanten oder aus einem Container zu uns liefern. Bitte kündigen Sie die Sendung vorab an und geben Sie an, wie viele Packstücke erwartet werden."),
  ("Brauche ich eine deutsche Umsatzsteuer-Nummer?",
   "Für den Verkauf über Amazon in Deutschland ist in der Regel eine umsatzsteuerliche Registrierung in Deutschland erforderlich. Das ist eine steuerliche Frage, die Sie mit Ihrem Steuerberater klären sollten – wir erbringen ausschließlich die logistische Leistung und keine Steuerberatung."),
  ("Arbeiten Sie mit Händlern aus dem Ausland?",
   "Ja. Ein großer Teil unserer Auftraggeber sitzt außerhalb Deutschlands. Die Kommunikation ist auf Deutsch, Englisch, Italienisch und Französisch möglich."),
 ],
 ("Angebot für Ihr Volumen anfragen",
  "Schicken Sie uns Ihre Produktliste und das monatliche Volumen – Sie erhalten innerhalb von 24 Stunden ein konkretes Angebot."),
 [("./fnsku-etikettierung.html","FNSKU-Etikettierung im Detail"),
  ("./fba-lagerung-deutschland.html","Lagerung vor der FBA-Einlieferung"),
  ("./versand-an-amazon.html","Einlieferung und Versand an Amazon"),
  ("./amazon-retouren-deutschland.html","Retouren und Removal Orders"),
  ("./pricing.html","Vollständige Preisliste und Kostenrechner")])

# ══════════════════ 2. FNSKU ══════════════════
k = "fnsku"
build("fnsku-etikettierung.html", k,
 "FNSKU-Etikettierung für Amazon FBA – 0,39 € pro Einheit | PrepCenter FBA",
 "FNSKU-Etikettierung nach Amazon-Vorgaben: Barcode-Prüfung, Überkleben fremder Barcodes, Etikettendruck und Sichtkontrolle. 0,39 € pro Einheit, Bearbeitung in 24–48 Stunden.",
 "Amazon-konforme FNSKU-Etikettierung in Deutschland – 0,39 € pro Einheit.",
 "Etikettierung",
 "FNSKU-Etikettierung nach Amazon-Vorgaben",
 "Jede Einheit bekommt den richtigen Barcode – sauber aufgebracht, scanbar und ohne durchscheinende Fremdbarcodes.",
 [
  {"label":"Grundlagen","h":"Was ist eine FNSKU?","p":[
    "Die FNSKU (Fulfillment Network Stock Keeping Unit) ist die Kennung, mit der Amazon eine Produkteinheit einem bestimmten Verkäufer zuordnet. Sie unterscheidet sich von der ASIN und vom EAN: Während ASIN und EAN das Produkt beschreiben, verknüpft die FNSKU eine physische Einheit mit Ihrem Verkäuferkonto.",
    "Genau deshalb ist sie in einem FBA-Lager unverzichtbar. Ohne FNSKU-Etikett landet Ihre Ware im sogenannten Commingled Inventory und wird mit Beständen anderer Verkäufer vermischt – mit dem Risiko, dass Ihre Kunden Ware eines fremden Anbieters erhalten und Sie für deren Zustand einstehen müssen."]},

  {"label":"Anforderungen","cls":"section section--surface","h":"Was Amazon vom Etikett verlangt","p":[
    "Die Vorgaben sind konkret und werden im Wareneingang maschinell geprüft."],
   "extra": CL(k,2,[
    "Der Barcode muss vollständig scanbar sein – kein Knick, keine Wölbung, keine Folie darüber, die spiegelt.",
    "Vorhandene Fremdbarcodes (EAN, UPC, Hersteller-Codes) müssen vollständig überdeckt sein.",
    "Das Etikett darf nicht über Kanten, Öffnungen oder Verschlüsse geklebt werden.",
    "Bei Polybag-Ware gehört das Etikett von außen sichtbar auf den Beutel.",
    "Bei Sets und Multipacks trägt die äußere Verkaufseinheit das Etikett, nicht die einzelnen Bestandteile.",
    "Etiketten müssen im Thermodruck oder Laserdruck erstellt sein – Tintenstrahl verwischt und wird abgelehnt.",
   ])},

  {"label":"Ablauf","h":"So arbeiten wir","p":[
    "Sie stellen uns die Etiketten als PDF aus Seller Central bereit, oder Sie übermitteln uns FNSKU und Stückzahl und wir drucken die Etiketten bei uns. In beiden Fällen gleichen wir vor dem Aufbringen ab, ob FNSKU, ASIN und Stückzahl zur angekündigten Sendung passen.",
    "Anschließend wird jede Einheit einzeln etikettiert: Fremdbarcodes werden vollständig überklebt, das Etikett auf einer glatten, ebenen Fläche platziert und abschließend stichprobenartig mit dem Scanner geprüft.",
    "Fällt dabei auf, dass eine Charge nicht zur Ankündigung passt – abweichende Stückzahl, andere Variante, beschädigte Verpackung – melden wir das, bevor wir weiterarbeiten."]},

  {"label":"Preis","cls":"section section--surface","h":"Preis und Kombination mit anderen Leistungen","p":[
    "Die reine FNSKU-Etikettierung kostet 0,39 € pro Einheit. Wenn zusätzlich Sichtprüfung, Verpackung und Versandvorbereitung anfallen, ist der FBA Komplett-Prep zu 0,79 € pro Einheit in der Regel die günstigere Wahl – darin ist die Etikettierung bereits enthalten.",
    "Zusätzliche Etiketten, etwa Warnhinweise, Mindesthaltbarkeitsdaten oder sprachliche Overlays, berechnen wir mit 0,25 € pro Etikett. Der Wareneingang ist bei gebuchter Prep-Leistung kostenfrei.",
    "Alle Preise verstehen sich netto zuzüglich der gesetzlichen Umsatzsteuer. Es gilt ein Mindestauftragswert von 25,00 € netto je Einzelauftrag."]},

  {"label":"Fehlerquellen","h":"Die häufigsten Fehler bei der Etikettierung","p":[
    "Der mit Abstand häufigste Fehler ist ein nicht vollständig überdeckter Herstellerbarcode. Der Scanner im Fulfillment-Center liest dann den falschen Code, und die Einheit wird dem falschen Bestand zugeordnet.",
    "Fast ebenso häufig sind Etiketten auf gewölbten Flächen oder auf der Kartonkante: Der Barcode lässt sich nicht in einem Zug scannen, die Einheit wird manuell nachbearbeitet und Amazon berechnet dafür eine Gebühr.",
    "Der dritte Klassiker ist die falsche FNSKU aus einer früheren Charge – etwa wenn eine Variante gewechselt hat, das Etikettenset aber unverändert übernommen wurde. Deshalb gleichen wir vor jedem Auftrag ab, statt Etiketten ungeprüft aufzubringen."]},
 ],
 [
  ("Kann ich die Etiketten selbst liefern?",
   "Ja. Sie können uns die PDF-Datei aus Seller Central schicken, wir drucken und bringen die Etiketten auf. Alternativ übermitteln Sie uns nur FNSKU und Stückzahl und wir erstellen die Etiketten."),
  ("Was kostet das Überkleben eines vorhandenen Barcodes?",
   "Das ist im Preis von 0,39 € pro Einheit bereits enthalten. Ein separater Aufschlag fällt nicht an."),
  ("Etikettieren Sie auch Polybag- und Bundle-Ware?",
   "Ja. Bei Polybag-Ware wird das Etikett von außen sichtbar auf den Beutel aufgebracht, bei Bundles auf die äußere Verkaufseinheit mit einem entsprechenden Bundle-Hinweis."),
  ("Wie schnell geht das?",
   "Bei Standardaufträgen erfolgt die Etikettierung innerhalb von 24–48 Stunden ab Wareneingang."),
 ],
 ("Etikettierung anfragen",
  "Nennen Sie uns Artikelanzahl und Verpackungsart – Sie bekommen innerhalb von 24 Stunden ein Festpreisangebot."),
 [("./fba-prep-center-deutschland.html","FBA Prep Center Deutschland – Überblick"),
  ("./services.html","Alle Prep-Leistungen im Detail"),
  ("./pricing.html","Preisliste und Kostenrechner")])

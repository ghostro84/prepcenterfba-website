# -*- coding: utf-8 -*-
import sys, io, os
sys.path.insert(0, os.path.dirname(__file__))
from newpages import HEAD, FOOT, CTA, section, checklist, faq_items

W = lambda name, s: open(name, "w", encoding="utf-8").write(s)

# ─────────────────────────── ÜBER UNS ───────────────────────────
k = "about"
s = HEAD.format(
    title="Über uns – PrepCenter FBA | FBA Prep Center Freilassing",
    desc="PrepCenter FBA ist ein inhabergeführtes FBA Prep Center in Freilassing bei Salzburg. Feste Preise, 24–48 Stunden Durchlaufzeit, direkte Ansprechpartner.",
    ogdesc="Inhabergeführtes FBA Prep Center in Freilassing: kurze Wege, feste Preise, persönliche Betreuung.",
    k=k, badge="Über uns",
    h1="Ein inhabergeführtes Prep Center – kein Callcenter",
    lead="Wir bereiten Ihre Ware für Amazon FBA vor: sorgfältig, nachvollziehbar und zu Preisen, die vorher feststehen.")

s += section(k, 1, "Wer wir sind", [
 "PrepCenter FBA ist ein inhabergeführtes Logistik- und Prep-Unternehmen mit Sitz in Freilassing. Wir übernehmen für Amazon-Händler alle Arbeitsschritte zwischen Wareneingang und Einlieferung ins FBA-Lager – von der Palettenannahme über die FNSKU-Etikettierung bis zur fertig konfektionierten Sendung.",
 "Statt anonymer Ticketsysteme sprechen Sie bei uns direkt mit der Person, die Ihre Ware auch tatsächlich in der Hand hat. Rückfragen zu einer Charge sind damit eine Nachricht und keine Eskalationsstufe.",
], label="Das Unternehmen")

s += section(k, 2, "Warum der Standort Freilassing", [
 "Freilassing liegt im Südosten Bayerns direkt an der Grenze zu Salzburg und damit an der Verbindungsachse zwischen Deutschland und Österreich. Für Händler aus dem DACH-Raum bedeutet das kurze Transportwege in beide Richtungen und eine schnelle Anbindung an die Amazon-Standorte in Süddeutschland.",
 "Gleichzeitig sind wir nah genug an den österreichischen und italienischen Warenströmen, um auch für internationale Verkäufer als Eingangstor nach Deutschland zu funktionieren.",
], cls="section section--surface", label="Standort")

s += section(k, 3, "Wofür wir stehen", [
 "Wir haben das Unternehmen gestartet, weil Prep-Dienstleistungen in der Praxis oft an denselben drei Punkten scheitern: unklare Abrechnung, unklare Laufzeiten und unklare Zuständigkeit. Unsere Antwort darauf ist bewusst schlicht.",
], label="Prinzipien",
 extra=checklist(k, 3, [
  "Feste Preise pro Einheit – die Preisliste auf dieser Website ist die Preisliste, die abgerechnet wird.",
  "Durchlaufzeit von 24–48 Stunden ab Wareneingang bei Standardaufträgen.",
  "Jede Charge wird dokumentiert: Stückzahlkontrolle beim Eingang, Sichtprüfung vor der Verpackung.",
  "Amazon-konforme Arbeitsweise nach den aktuellen FBA-Anforderungen für Etikettierung und Verpackung.",
  "Ein fester Ansprechpartner statt wechselnder Bearbeiter.",
 ]))

s += section(k, 4, "Für wen wir arbeiten", [
 "Unsere Auftraggeber sind überwiegend kleine und mittlere Amazon-Händler, die zwischen einigen hundert und einigen tausend Einheiten pro Monat einliefern – dazu europäische Verkäufer, die einen Anlaufpunkt in Deutschland brauchen, ohne selbst eine Niederlassung zu gründen.",
 "Wir arbeiten ausschließlich B2B, also mit Unternehmern im Sinne des § 14 BGB. Für Privatpersonen erbringen wir keine Leistungen.",
], cls="section section--surface", label="Kunden")

s += CTA.format(k=k, title="Lernen wir uns kennen",
                sub="Schicken Sie uns Ihre Produktliste – Sie bekommen innerhalb von 24 Stunden ein konkretes Angebot.")
s += FOOT
W("ueber-uns.html", s)

# KONTAKT: kontakt.html wird NICHT generiert – die Live-Seite hat ein
# echtes FormSubmit-Formular und wird von Hand gepflegt.

# ─────────────────────────── FAQ ───────────────────────────
k = "faqpage"
s = HEAD.format(
    title="FAQ – Häufige Fragen zum FBA Prep | PrepCenter FBA",
    desc="Antworten auf die häufigsten Fragen zum FBA Prep: Durchlaufzeit, Mindestauftragswert, FNSKU-Etiketten, Lagerung, Retouren, Anlieferung und Abrechnung.",
    ogdesc="Die häufigsten Fragen zu FBA Prep Services in Deutschland – kurz und konkret beantwortet.",
    k=k, badge="FAQ",
    h1="Häufige Fragen zum FBA Prep",
    lead="Die Fragen, die uns Händler vor der ersten Zusammenarbeit am häufigsten stellen.")

QAS = [
 ("Wie lange dauert die Bearbeitung meiner Ware?",
  "Bei Standardaufträgen bearbeiten wir Ihre Ware innerhalb von 24–48 Stunden ab Wareneingang. Bei sehr großen Sendungen oder aufwendigen Sonderprozessen stimmen wir den Termin vorab mit Ihnen ab."),
 ("Gibt es eine Mindestmenge?",
  "Nein. Es gibt keine Mindesteinheitenzahl. Es gilt jedoch ein Mindestauftragswert von 25,00 € netto je Einzelauftrag für Prep-Leistungen. Liegt der Auftragswert darunter, berechnen wir die Differenz als Mindestauftragszuschlag."),
 ("Was kostet der FBA Prep?",
  "Der FBA Komplett-Prep kostet 0,79 € pro Einheit, die reine FNSKU-Etikettierung 0,39 € pro Einheit. Alle weiteren Positionen finden Sie in der vollständigen Preisliste. Alle Preise verstehen sich netto zuzüglich der gesetzlichen Umsatzsteuer."),
 ("Gibt es einen Rabatt für Neukunden?",
  "Ja. Neukunden erhalten 10 % Rabatt auf die erste und 5 % auf die zweite Lieferung. Der Rabatt gilt für Prep-Leistungen bis maximal 2.000 Einheiten je Lieferung; Lagerung, Versandkosten und Fremdleistungen sind ausgenommen."),
 ("Muss ich die FNSKU-Etiketten selbst liefern?",
  "Beides ist möglich. Sie können uns fertige Etiketten als PDF zur Verfügung stellen, oder wir drucken die Etiketten anhand Ihrer Vorgaben bei uns. In beiden Fällen prüfen wir vor dem Aufbringen, ob Barcode und ASIN zur Sendung passen."),
 ("Wie liefere ich meine Ware an?",
  "Sie können Kartons per Paketdienst oder Paletten per Spedition anliefern. Bitte kündigen Sie jede Sendung vorab per E-Mail an – mit Anzahl der Packstücke, Termin und Spediteur. Beschriften Sie die Packstücke außen mit Ihrem Firmennamen."),
 ("Wie lange kann meine Ware bei Ihnen liegen?",
  "Für Ware mit gebuchter FBA-Prep-Leistung ist die Zwischenlagerung in den ersten 14 Tagen kostenfrei. Danach berechnen wir die Lagerung anteilig nach tatsächlicher Lagerdauer: 1,20 € je Karton und Monat bzw. 19,00 € je Palette und Monat."),
 ("Übernehmen Sie auch Retouren?",
  "Ja. Wir nehmen Retouren an, prüfen jede Einheit auf ihren Zustand und dokumentieren das Ergebnis. Wiederverkaufsfähige Ware bereiten wir auf Wunsch für die erneute FBA-Einlieferung auf; nicht mehr verkaufsfähige Artikel entsorgen wir fachgerecht."),
 ("Arbeiten Sie auch mit Verkäufern aus dem europäischen Ausland?",
  "Ja. Ein erheblicher Teil unserer Auftraggeber sitzt außerhalb Deutschlands und nutzt uns als Eingangspunkt für den deutschen und europäischen Amazon-Markt. Die Kommunikation ist auf Deutsch, Englisch, Italienisch und Französisch möglich."),
 ("Wie wird abgerechnet?",
  "Wir rechnen nach tatsächlich erbrachten Leistungen auf Basis der veröffentlichten Preisliste ab. Rechnungen sind innerhalb von 14 Tagen nach Rechnungsdatum ohne Abzug fällig, sofern nichts anderes schriftlich vereinbart ist."),
 ("Kann ich den Status meiner Sendung einsehen?",
  "Zu jeder Charge erhalten Sie eine Eingangsbestätigung mit Stückzahl sowie eine Meldung, sobald die Sendung fertig konfektioniert an den Spediteur übergeben wurde. Auf Wunsch dokumentieren wir einzelne Einheiten zusätzlich per Foto."),
 ("Was passiert, wenn Ware beschädigt ankommt?",
  "Beschädigungen, die uns bei der Eingangskontrolle auffallen, melden wir Ihnen vor der weiteren Bearbeitung – auf Wunsch mit Fotodokumentation. Sie entscheiden dann, ob die betroffenen Einheiten trotzdem eingeliefert, umverpackt oder entsorgt werden sollen."),
]
s += '<section class="section">\n  <div class="container" style="max-width:820px;">\n'
s += faq_items(k, QAS) + "\n  </div>\n</section>\n"
s += CTA.format(k=k, title="Frage nicht dabei?",
                sub="Schreiben Sie uns – wir antworten werktags innerhalb von 24 Stunden.")
s += FOOT
W("faq.html", s)
print("ueber-uns.html, faq.html written")

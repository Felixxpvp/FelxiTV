# /task-audit: Aufgaben kartieren, Bandbreite zurückholen

> "Was du nicht kartiert hast, kannst du nicht automatisieren."

## Anleitung

Du führst einen **Aufgaben-Audit** durch. Das ist ein geführtes Interview, das jede wiederkehrende Aufgabe, jede Verantwortung und jeden Zeitfresser im Business kartiert. Das Ergebnis ist der persönliche Punktestand des Geschäftsführers für die Kennzahl Aufgaben-Automatisierungsquote.

### Verhalten

- Gründlich, aber im Gesprächston. Lauf es wie ein Gespräch, nicht wie eine Abfrage.
- Frag nach einem Geschäftsbereich nach dem anderen. Nicht durchrasen.
- Bohr nach: "Sonst noch was in diesem Bereich?" Weitermachen, bis er Nein sagt.
- Nutz die `context/`-Dateien, um vorab zu wissen, was bereits klar ist.
- Wenn der Geschäftsführer etwas erwähnt, das sich nach mehreren Aufgaben anhört, zerleg es.
- Sei ermutigend: "Das ist ein dickes Brett, klar automatisierbar." Oder: "Das ist eine Mensch-Aufgabe, alles gut."

### Interview-Ablauf

**Phase 1: Kontext-Check**

Lies die Kontext-Dateien (`context/business-info.md`, `context/strategy.md`, etc.), um das Business zu verstehen. Damit kannst du klügere Fragen stellen und Offensichtliches vorab eintragen.

Sag: "Ich geh mit dir jeden Bereich deines Geschäfts durch und kartier, wo deine Zeit hingeht. In jedem Bereich erzählst du mir alles, was du regelmäßig machst, täglich, wöchentlich, monatlich. Filter nichts, auch das Kleine zählt. Wir bewerten am Ende."

**Phase 2: Bereich für Bereich**

Geh diese Bereiche durch (an das Business anpassen):

1. **Marketing und Content**: Content-Produktion, Social Media, E-Mail, Anzeigen, SEO
2. **Sales und Pipeline**: Lead-Follow-up, Angebote, Demos, CRM-Pflege
3. **Kunden- oder Mandanten-Lieferung**: Onboarding, Projekt-Management, Deliverables, Kommunikation
4. **Operations und Admin**: Rechnungen, Buchhaltung, Termine, Tool-Pflege, Reports
5. **Team und Menschen**: Einstellen, Onboarding, Einzelgespräche, Performance, Delegation
6. **Daten und Reporting**: Dashboards checken, Kennzahlen verfolgen, Reports erstellen
7. **Kommunikation**: E-Mail, Chat, Termine, Check-ins, Updates
8. **Strategisches und Kreatives**: Planung, Recherche, Brainstorming, Produktentwicklung
9. **Persönliches und Lebens-Admin**: alles Geschäftsnahe, das Bandbreite frisst

Pro Bereich:

- Frag: "In [Bereich], was machst du regelmäßig? Erzähl mir eine typische Woche."
- Bohr nach mit "Sonst noch was?", mindestens zwei Mal pro Bereich
- Notier Häufigkeit (täglich, wöchentlich, monatlich) und geschätzte Zeit pro Vorkommen

**Phase 3: Bewerten und priorisieren**

Wenn alle Bereiche durch sind, bewerte jede Aufgabe:

- **Grün, voll automatisierbar**: KI und Skripte können das End-zu-End mit minimaler Aufsicht
- **Gelb, teilweise automatisierbar**: KI macht den Großteil, braucht aber Mensch zum Prüfen oder Anstoßen
- **Rot, noch nicht**: Aktuelle KI kriegt das noch nicht zuverlässig, später vielleicht möglich
- **Weiß, nur Mensch**: Braucht Mensch-Urteil, Beziehung oder physische Anwesenheit

Dann priorisieren nach: **Wirkung (Zeit gespart × Häufigkeit) × Aufwand (wie schwer zu automatisieren)**

Reihenfolge: Schnelle Siege (hohe Wirkung, leicht) → Strategische Siege (hohe Wirkung, schwerer) → Nice-to-Have (geringe Wirkung, leicht) → Hintenan (geringe Wirkung, schwer)

**Phase 4: Aufgaben-Audit schreiben**

Speicher in `context/task-audit.md` mit dieser Struktur:

```
# Aufgaben-Audit

> Persönlicher Punktestand für die Aufgaben-Automatisierungsquote.
> Erstellt: [Datum] | Start-Quote: [X]%
>
> Pflegen, sobald du Aufgaben automatisierst. Häkchen setzen. Notieren, womit du es gelöst hast.
> Jederzeit erneut `/task-audit` laufen, um neu zu bewerten.

## Zusammenfassung
- Kartierte Aufgaben gesamt: [N]
- Voll automatisierbar: [N] (Grün)
- Teilweise: [N] (Gelb)
- Noch nicht: [N] (Rot)
- Nur Mensch: [N] (Weiß)
- **Aktuelle Aufgaben-Automatisierungsquote: [X]%**

## Schnelle Siege (hier anfangen)
| Erledigt | Aufgabe | Bereich | Häufigkeit | Zeit | Bewertung | Gelöst durch |
|---|---|---|---|---|---|---|
| [ ] | ... | ... | ... | ... | Grün | |

## Strategische Siege
| Erledigt | Aufgabe | Bereich | Häufigkeit | Zeit | Bewertung | Gelöst durch |
|---|---|---|---|---|---|---|
| [ ] | ... | ... | ... | ... | Grün / Gelb | |

## Nice-to-Have
| Erledigt | Aufgabe | Bereich | Häufigkeit | Zeit | Bewertung | Gelöst durch |
|---|---|---|---|---|---|---|
| [ ] | ... | ... | ... | ... | Gelb | |

## Hintenan
| Erledigt | Aufgabe | Bereich | Häufigkeit | Zeit | Bewertung | Gelöst durch |
|---|---|---|---|---|---|---|
| [ ] | ... | ... | ... | ... | Rot | |

## Nur Mensch (so lassen)
| Aufgabe | Bereich | Häufigkeit | Zeit | Notiz |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
```

**Phase 5: Feiern und nach vorn zeigen**

Sag: "Dein Aufgaben-Audit steht. Du hast [N] Aufgaben in [N] Bereichen kartiert. [X]% sind voll automatisierbar und [Y]% teilweise. Das sind [Z] Aufgaben, die du nach und nach abhaken kannst.

Deine Start-Quote ist [X]%. Jede Aufgabe, die du automatisierst, hebt diese Zahl an.

**Was als Nächstes:**

1. Prüf erst, ob es für diese Aufgaben schon fertige Fähigkeiten gibt, die du dir holen kannst.
2. Wenn du eine konkrete Idee hast, was du bauen willst, beschreib sie, und wir machen einen Plan mit `/create-plan`.
3. Komm zurück und setz Häkchen, wenn du Aufgaben automatisiert hast. Beobachte, wie deine Quote steigt."

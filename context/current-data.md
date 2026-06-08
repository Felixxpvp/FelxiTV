# Aktuelle Zahlen

> Diese Datei wird automatisch von `scripts/update_daten.py` aktualisiert.
> Quellen: `scripts/produktion.xlsx`, `scripts/finanzen.xlsx`

---

## Wie das zusammenhängt

- **`business-info.md`** beschreibt das Business drumherum
- **`personal-info.md`** beschreibt deine Verantwortung
- **`strategy.md`** sagt, worauf du optimierst
- **Diese Datei** zeigt die Zahlen hinter der Erzählung

---

**Stand:** 08.06.2026 _(automatisch generiert)_

## Kennzahlen

| Kennzahl | Wert | Notiz |
|---|---|---|
| Gesamteinnahmen (lfd. Jahr) | 155 € | Aus finanzen.xlsx |
| Gesamtausgaben (lfd. Jahr) | 225 € | Aus finanzen.xlsx |
| Ergebnis (Einnahmen − Ausgaben) | -70 € | |
| Met produziert (gesamt) | 140 Flaschen | Aus produktion.xlsx |
| Met verkauft (gesamt) | 55 Flaschen | |
| Gemüse verkauft | 18 kg | |
| Obst verkauft | 0 kg | |

## Einnahmen nach Sparte

| Posten | Betrag | Notiz |
|---|---|---|
| Einnahmen Gemüse | 35 € | |
| Einnahmen Met | 120 € | |

## Ausgaben nach Sparte

| Posten | Betrag | Notiz |
|---|---|---|
| Ausgaben Gemüse | 45 € | |
| Ausgaben Met | 180 € | |

## Stand zur Strategie

- Met-Raum: noch nicht gebaut → Produktion gedeckelt
- Pick-your-own: noch nicht gestartet
- Fleischerei: noch nicht gebaut
- 3-Hektar-Grenze: noch nicht erreicht

## Laufendes

- Daten manuell in `scripts/produktion.xlsx` und `scripts/finanzen.xlsx` pflegen
- Nach jedem Update: `python scripts/update_daten.py` ausführen

## Datenquellen

- `scripts/produktion.xlsx` — Produktion und Verkauf je Sparte
- `scripts/finanzen.xlsx` — Einnahmen und Ausgaben

---

## Automatisierungs-Notiz

_Diese Datei wird von `update_daten.py` neu geschrieben. Direkte Änderungen hier werden beim nächsten Lauf überschrieben. Zahlen immer in den Excel-Dateien pflegen._

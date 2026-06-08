"""
update_daten.py
Liest produktion.xlsx und finanzen.xlsx und schreibt die Zusammenfassung
in context/current-data.md.

Aufruf: python scripts/update_daten.py
"""

import openpyxl
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPTS = ROOT / "scripts"
CONTEXT = ROOT / "context"

# ── Excel-Dateien laden ──────────────────────────────────────────────────────

def lade_tabelle(pfad):
    if not pfad.exists():
        return None
    return openpyxl.load_workbook(pfad, data_only=True)


def zeilen(ws):
    """Alle Zeilen ab Zeile 2 (ohne Header) als Listen zurückgeben."""
    result = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if any(v is not None for v in row):
            result.append(row)
    return result


# ── Produktion auslesen ──────────────────────────────────────────────────────

def met_zahlen(wb):
    ws = wb["Met"]
    rows = zeilen(ws)
    prod = sum(r[2] or 0 for r in rows)
    verk = sum(r[3] or 0 for r in rows)
    return int(prod), int(verk)


def gemüse_kg(wb):
    ws = wb["Gemüse"]
    rows = zeilen(ws)
    return sum(r[3] or 0 for r in rows)  # verkaufte kg


def obst_kg(wb):
    ws = wb["Obst"]
    rows = zeilen(ws)
    return sum(r[3] or 0 for r in rows)


# ── Finanzen auslesen ────────────────────────────────────────────────────────

def finanzen(wb):
    einnahmen = {}
    for row in zeilen(wb["Einnahmen"]):
        sparte = row[2] or "Sonstiges"
        betrag = row[3] or 0
        einnahmen[sparte] = einnahmen.get(sparte, 0) + betrag

    ausgaben = {}
    for row in zeilen(wb["Ausgaben"]):
        sparte = row[2] or "Sonstiges"
        betrag = row[3] or 0
        ausgaben[sparte] = ausgaben.get(sparte, 0) + betrag

    return einnahmen, ausgaben


# ── current-data.md schreiben ────────────────────────────────────────────────

def schreibe_datei(met_prod, met_verk, gem_kg, obst_kg_verk, einnahmen, ausgaben):
    gesamt_ein = sum(einnahmen.values())
    gesamt_aus = sum(ausgaben.values())
    gewinn = gesamt_ein - gesamt_aus
    heute = date.today().strftime("%d.%m.%Y")

    # Einnahmen-Tabelle
    ein_zeilen = "\n".join(
        f"| Einnahmen {s} | {v:.0f} € | |" for s, v in sorted(einnahmen.items())
    )
    aus_zeilen = "\n".join(
        f"| Ausgaben {s} | {v:.0f} € | |" for s, v in sorted(ausgaben.items())
    )

    inhalt = f"""# Aktuelle Zahlen

> Diese Datei wird automatisch von `scripts/update_daten.py` aktualisiert.
> Quellen: `scripts/produktion.xlsx`, `scripts/finanzen.xlsx`

---

## Wie das zusammenhängt

- **`business-info.md`** beschreibt das Business drumherum
- **`personal-info.md`** beschreibt deine Verantwortung
- **`strategy.md`** sagt, worauf du optimierst
- **Diese Datei** zeigt die Zahlen hinter der Erzählung

---

**Stand:** {heute} _(automatisch generiert)_

## Kennzahlen

| Kennzahl | Wert | Notiz |
|---|---|---|
| Gesamteinnahmen (lfd. Jahr) | {gesamt_ein:.0f} € | Aus finanzen.xlsx |
| Gesamtausgaben (lfd. Jahr) | {gesamt_aus:.0f} € | Aus finanzen.xlsx |
| Ergebnis (Einnahmen − Ausgaben) | {gewinn:.0f} € | |
| Met produziert (gesamt) | {met_prod} Flaschen | Aus produktion.xlsx |
| Met verkauft (gesamt) | {met_verk} Flaschen | |
| Gemüse verkauft | {gem_kg:.0f} kg | |
| Obst verkauft | {obst_kg_verk:.0f} kg | |

## Einnahmen nach Sparte

| Posten | Betrag | Notiz |
|---|---|---|
{ein_zeilen if ein_zeilen else "| (noch keine Einträge) | — | |"}

## Ausgaben nach Sparte

| Posten | Betrag | Notiz |
|---|---|---|
{aus_zeilen if aus_zeilen else "| (noch keine Einträge) | — | |"}

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
"""
    (CONTEXT / "current-data.md").write_text(inhalt, encoding="utf-8")
    print(f"current-data.md aktualisiert ({heute})")
    print(f"  Einnahmen: {gesamt_ein:.0f} €  |  Ausgaben: {gesamt_aus:.0f} €  |  Ergebnis: {gewinn:.0f} €")
    print(f"  Met: {met_prod} prod. / {met_verk} verk.  |  Gemüse: {gem_kg:.0f} kg  |  Obst: {obst_kg_verk:.0f} kg")


# ── Hauptprogramm ────────────────────────────────────────────────────────────

def main():
    prod_wb = lade_tabelle(SCRIPTS / "produktion.xlsx")
    fin_wb  = lade_tabelle(SCRIPTS / "finanzen.xlsx")

    if not prod_wb:
        print("FEHLER: scripts/produktion.xlsx nicht gefunden.")
        return
    if not fin_wb:
        print("FEHLER: scripts/finanzen.xlsx nicht gefunden.")
        return

    mp, mv = met_zahlen(prod_wb)
    gk     = gemüse_kg(prod_wb)
    ok     = obst_kg(prod_wb)
    ein, aus_ = finanzen(fin_wb)

    schreibe_datei(mp, mv, gk, ok, ein, aus_)


if __name__ == "__main__":
    main()

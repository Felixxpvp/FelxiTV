"""
Excel-Kassenbuch in Supabase importieren.
Liest Mappe1.xlsx und trägt alle Buchungen ein.
Einmalig ausführen: python scripts/import_kassenbuch.py
"""

import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")
from supabase import create_client

client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

df = pd.read_excel(r"C:\Users\Felix\Desktop\Mappe1.xlsx", sheet_name=0, header=None)

# Monats-Blöcke: (datum_col, ausgaben_col, einnahmen_col)
MONATE = [
    (2, 3, 4),   # Januar
    (6, 7, 8),   # Februar
    (10, 11, 12), # März
    (14, 15, 16), # April
    (18, 19, 20), # Mai
    (22, 23, 24), # Juni
]

buchungen = []

for datum_col, aus_col, ein_col in MONATE:
    for row_idx in range(3, 34):  # Zeilen 3-33, Zeile 34 = Summe
        row = df.iloc[row_idx]

        datum_val = row[datum_col]
        ausgabe   = row[aus_col]
        einnahme  = row[ein_col]

        if pd.isna(datum_val):
            continue

        datum_str = pd.to_datetime(datum_val).strftime("%Y-%m-%d")

        if pd.notna(ausgabe) and float(ausgabe) > 0:
            buchungen.append({
                "datum":        datum_str,
                "typ":          "Ausgabe",
                "kategorie":    "Sonstiges",
                "betrag":       round(float(ausgabe), 2),
                "beschreibung": "Import aus Kassenbuch"
            })

        if pd.notna(einnahme) and float(einnahme) > 0:
            buchungen.append({
                "datum":        datum_str,
                "typ":          "Einnahme",
                "kategorie":    "Sonstiges",
                "betrag":       round(float(einnahme), 2),
                "beschreibung": "Import aus Kassenbuch"
            })

print(f"{len(buchungen)} Buchungen gefunden. Importiere...")

ok = fehler = 0
for b in buchungen:
    try:
        client.table("buchhaltung").insert(b).execute()
        ok += 1
    except Exception as e:
        print(f"  FEHLER {b['datum']} {b['typ']} {b['betrag']}: {e}")
        fehler += 1

# Summen ausgeben
einnahmen = sum(b["betrag"] for b in buchungen if b["typ"] == "Einnahme")
ausgaben  = sum(b["betrag"] for b in buchungen if b["typ"] == "Ausgabe")

print(f"\nFertig: {ok} eingetragen, {fehler} Fehler")
print(f"Einnahmen gesamt: {einnahmen:.2f} EUR")
print(f"Ausgaben gesamt:  {ausgaben:.2f} EUR")
print(f"Saldo:            {einnahmen - ausgaben:.2f} EUR")

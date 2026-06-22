"""
Lager: Bestandsverwaltung

Liest und schreibt lager.csv. Berechnet Verbrauch automatisch
wenn Felix sagt "Ich hab X Liter gemacht".

Verbrauchsregeln (pro Liter Produkt):
    Met     → 2x Met-Flasche 0.5L, 2x Bügelverschluss, 2x Etikett Met
    Saft    → 2x Saft-Flasche 0.5L, 2x Bügelverschluss, 2x Etikett Saft

Nutzung über Claude-Befehl /lager oder direkt:
    python scripts/lager.py status          → Bestand anzeigen
    python scripts/lager.py warnungen       → Nur Artikel unter Mindestbestand
    python scripts/lager.py verbrauch met 50 → 50 Liter Met verbuchen
    python scripts/lager.py verbrauch saft 30 → 30 Liter Saft verbuchen
"""

import csv
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
LAGER_PATH = WORKSPACE_ROOT / "lager.csv"

# --- Verbrauchsregeln: Wie viele Einheiten pro Liter Produkt ---
VERBRAUCH_PRO_LITER = {
    "met": {
        "Met-Flaschen 0.5L": 2,
        "Bügelverschlüsse": 2,
        "Etiketten Met": 2,
    },
    "saft": {
        "Saft-Flaschen 0.5L": 2,
        "Bügelverschlüsse": 2,
        "Etiketten Saft": 2,
    },
}


def lager_lesen():
    """lager.csv einlesen, gibt Liste von Dicts zurück."""
    if not LAGER_PATH.exists():
        print(f"FEHLER: lager.csv nicht gefunden unter {LAGER_PATH}")
        return []
    with open(LAGER_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def lager_schreiben(rows):
    """Liste von Dicts in lager.csv zurückschreiben."""
    if not rows:
        return
    fieldnames = rows[0].keys()
    with open(LAGER_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bestand_anzeigen(nur_warnungen=False):
    """Bestand anzeigen. Bei nur_warnungen=True nur Artikel unter Mindestbestand."""
    rows = lager_lesen()
    if not rows:
        return

    warnungen = []
    ok = []
    for row in rows:
        try:
            bestand = float(row["bestand"]) if row["bestand"] else 0
            mindest = float(row["mindestbestand"]) if row["mindestbestand"] else 0
        except ValueError:
            bestand, mindest = 0, 0

        if mindest > 0 and bestand <= mindest:
            warnungen.append(row)
        else:
            ok.append(row)

    if warnungen:
        print("ACHTUNG: NACHBESTELLEN — diese Artikel sind unter dem Mindestbestand:")
        print(f"{'Artikel':<30} {'Bestand':>10} {'Mindest':>10} {'Einheit':<10}")
        print("-" * 62)
        for r in warnungen:
            print(f"{r['artikel']:<30} {r['bestand']:>10} {r['mindestbestand']:>10} {r['einheit']:<10}")
        print()

    if not nur_warnungen:
        print(f"{'Artikel':<30} {'Bestand':>10} {'Mindest':>10} {'Einheit':<10} {'Kategorie'}")
        print("-" * 72)
        for r in sorted(rows, key=lambda x: x["kategorie"]):
            try:
                bestand = float(r["bestand"]) if r["bestand"] else 0
                mindest = float(r["mindestbestand"]) if r["mindestbestand"] else 0
                warnung = " ⚠️" if mindest > 0 and bestand <= mindest else ""
            except ValueError:
                warnung = ""
            print(f"{r['artikel']:<30} {r['bestand']:>10} {r['mindestbestand']:>10} {r['einheit']:<10} {r['kategorie']}{warnung}")

    if not warnungen:
        print("OK Alle Artikel über Mindestbestand.")


def verbrauch_verbuchen(produkt: str, liter: float):
    """
    Verbrauch für ein Produkt berechnen und vom Lager abziehen.
    Gibt Liste der veränderten Artikel und Warnungen zurück.
    """
    produkt_key = produkt.lower().strip()
    if produkt_key not in VERBRAUCH_PRO_LITER:
        print(f"Unbekanntes Produkt: '{produkt}'. Bekannte Produkte: {', '.join(VERBRAUCH_PRO_LITER.keys())}")
        return

    regeln = VERBRAUCH_PRO_LITER[produkt_key]
    rows = lager_lesen()

    verändert = []
    nicht_gefunden = []
    warnungen = []

    for artikel, menge_pro_liter in regeln.items():
        verbrauch = menge_pro_liter * liter
        gefunden = False
        for row in rows:
            if row["artikel"].strip() == artikel:
                gefunden = True
                try:
                    alt = float(row["bestand"]) if row["bestand"] else 0
                    neu = max(0, alt - verbrauch)
                    row["bestand"] = str(int(neu) if neu == int(neu) else round(neu, 2))
                    verändert.append((artikel, alt, verbrauch, neu, row["einheit"]))

                    mindest = float(row["mindestbestand"]) if row["mindestbestand"] else 0
                    if mindest > 0 and neu <= mindest:
                        warnungen.append((artikel, neu, mindest, row["einheit"]))
                except ValueError:
                    pass
                break
        if not gefunden:
            nicht_gefunden.append(artikel)

    lager_schreiben(rows)

    # Ergebnis ausgeben
    print(f"OK {liter:.0f} Liter {produkt.capitalize()} verbucht:")
    print()
    for artikel, alt, verbrauch, neu, einheit in verändert:
        print(f"  {artikel:<30} {alt:>6.0f} -> {neu:>6.0f} {einheit}  (-{verbrauch:.0f})")

    if nicht_gefunden:
        print(f"\nACHTUNG: Artikel nicht in lager.csv gefunden: {', '.join(nicht_gefunden)}")

    if warnungen:
        print("\nNACHBESTELLEN:")
        for artikel, bestand, mindest, einheit in warnungen:
            print(f"  {artikel}: noch {bestand:.0f} {einheit} (Mindest: {mindest:.0f})")
    else:
        print("\nOK Alle Bestände noch über Mindestmenge.")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] == "status":
        bestand_anzeigen(nur_warnungen=False)
    elif args[0] == "warnungen":
        bestand_anzeigen(nur_warnungen=True)
    elif args[0] == "verbrauch" and len(args) >= 3:
        try:
            liter = float(args[2].replace(",", "."))
            verbrauch_verbuchen(args[1], liter)
        except ValueError:
            print(f"Ungültige Literzahl: {args[2]}")
    else:
        print("Nutzung:")
        print("  python scripts/lager.py status")
        print("  python scripts/lager.py warnungen")
        print("  python scripts/lager.py verbrauch met 50")
        print("  python scripts/lager.py verbrauch saft 30")

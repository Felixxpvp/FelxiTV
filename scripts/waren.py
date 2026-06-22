"""
Warenwirtschaft: Fertigprodukte-Verwaltung

Verwaltet den Bestand an verkaufsfertigen Produkten (waren.csv).
Koppelt automatisch mit lager.py (Materialverbrauch) und buchhaltung.csv (Einnahmen).

Produktionsregeln (Materialverbrauch pro Liter):
    met  -> 2x Met-Flaschen 0.5L, 2x Bugelverschlusse, 2x Etiketten Met
    saft -> 2x Saft-Flaschen 0.5L, 2x Bugelverschlusse, 2x Etiketten Saft

Nutzung:
    python scripts/waren.py status
    python scripts/waren.py produktion met 20       -> 20 Liter Met abgefuellt
    python scripts/waren.py produktion saft 15      -> 15 Liter Saft abgefuellt
    python scripts/waren.py verkauf "Met 0.5L" 5   -> 5 Flaschen Met verkauft
    python scripts/waren.py verkauf "Tomaten" 3    -> 3 kg Tomaten verkauft
"""

import csv
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
WAREN_PATH = WORKSPACE_ROOT / "waren.csv"
LAGER_PATH = WORKSPACE_ROOT / "lager.csv"
VERKAUF_PATH = WORKSPACE_ROOT / "verkauf.csv"

# --- Produktionsregeln: Was kommt rein bei X Litern ---
PRODUKTION_WAREN = {
    "met": {
        "produkt": "Met 0.5L",
        "menge_pro_liter": 2,
        "einheit": "Flasche",
    },
    "saft": {
        "produkt": "Gemischter Fruchtsaft 0.5L",
        "menge_pro_liter": 2,
        "einheit": "Flasche",
    },
    "apfelsaft": {
        "produkt": "Apfelsaft 0.5L",
        "menge_pro_liter": 2,
        "einheit": "Flasche",
    },
    "birnensaft": {
        "produkt": "Birnensaft 0.5L",
        "menge_pro_liter": 2,
        "einheit": "Flasche",
    },
}

# --- Materialverbrauch pro Liter (spiegelt lager.py) ---
LAGER_VERBRAUCH = {
    "met": {
        "Met-Flaschen 0.5L": 2,
        "Bugelverschlusse": 2,
        "Etiketten Met": 2,
    },
    "saft": {
        "Saft-Flaschen 0.5L": 2,
        "Bugelverschlusse": 2,
        "Etiketten Saft": 2,
    },
    "apfelsaft": {
        "Saft-Flaschen 0.5L": 2,
        "Bugelverschlusse": 2,
        "Etiketten Saft": 2,
    },
    "birnensaft": {
        "Saft-Flaschen 0.5L": 2,
        "Bugelverschlusse": 2,
        "Etiketten Saft": 2,
    },
}


def csv_lesen(pfad):
    if not pfad.exists():
        return []
    with open(pfad, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def csv_schreiben(pfad, rows):
    if not rows:
        return
    with open(pfad, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def waren_status():
    """Warenbestand anzeigen."""
    rows = csv_lesen(WAREN_PATH)
    if not rows:
        print("waren.csv nicht gefunden.")
        return

    print(f"{'Produkt':<35} {'Bestand':>8} {'Mindest':>8} {'Einheit':<10} {'Preis':>8}")
    print("-" * 75)
    for r in rows:
        try:
            bestand = float(r["bestand"]) if r["bestand"] else 0
            mindest = float(r["mindestbestand"]) if r["mindestbestand"] else 0
            preis = f"{float(r['verkaufspreis']):.2f} EUR" if r.get("verkaufspreis") and r["verkaufspreis"] else "-"
            warnung = " !" if mindest > 0 and bestand <= mindest else ""
        except ValueError:
            preis = "-"
            warnung = ""
        print(f"{r['produkt']:<35} {r['bestand']:>8} {r['mindestbestand']:>8} {r['einheit']:<10} {preis}{warnung}")

    warnungen = [r for r in rows if r["bestand"] and r["mindestbestand"]
                 and float(r.get("bestand") or 0) <= float(r.get("mindestbestand") or 0)
                 and float(r.get("mindestbestand") or 0) > 0]
    if warnungen:
        print(f"\nNACHPRODUZIEREN ({len(warnungen)} Artikel unter Mindestbestand):")
        for r in warnungen:
            print(f"  {r['produkt']}: {r['bestand']} {r['einheit']} (Mindest: {r['mindestbestand']})")


def produktion_verbuchen(produkt_key: str, liter: float):
    """
    Produktion verbuchen: Waren erhoeht, Lager verringert.
    """
    produkt_key = produkt_key.lower().strip()

    if produkt_key not in PRODUKTION_WAREN:
        print(f"Unbekanntes Produkt: '{produkt_key}'")
        print(f"Bekannte Produkte: {', '.join(PRODUKTION_WAREN.keys())}")
        return

    regel = PRODUKTION_WAREN[produkt_key]
    produkt_name = regel["produkt"]
    menge = regel["menge_pro_liter"] * liter

    # 1. Waren erhoehen
    waren = csv_lesen(WAREN_PATH)
    gefunden = False
    for row in waren:
        if row["produkt"].strip() == produkt_name:
            gefunden = True
            alt = float(row["bestand"]) if row["bestand"] else 0
            neu = alt + menge
            row["bestand"] = str(int(neu) if neu == int(neu) else round(neu, 2))
            print(f"Waren: {produkt_name}: {alt:.0f} -> {neu:.0f} {regel['einheit']} (+{menge:.0f})")
            break

    if not gefunden:
        print(f"ACHTUNG: '{produkt_name}' nicht in waren.csv gefunden. Eintrag hinzufuegen.")
    else:
        csv_schreiben(WAREN_PATH, waren)

    # 2. Lager verringern (Materialverbrauch)
    if produkt_key in LAGER_VERBRAUCH:
        lager = csv_lesen(LAGER_PATH)
        verbrauch_regeln = LAGER_VERBRAUCH[produkt_key]
        lager_warnungen = []

        for material, menge_pro_liter in verbrauch_regeln.items():
            verbrauch = menge_pro_liter * liter
            for row in lager:
                # Flexible Suche (mit/ohne Umlaute)
                if (row["artikel"].strip() == material or
                        row["artikel"].strip().replace("ü", "u").replace("ä", "a") == material):
                    alt = float(row["bestand"]) if row["bestand"] else 0
                    neu = max(0, alt - verbrauch)
                    row["bestand"] = str(int(neu) if neu == int(neu) else round(neu, 2))
                    print(f"Lager:  {row['artikel']}: {alt:.0f} -> {neu:.0f} {row['einheit']} (-{verbrauch:.0f})")
                    mindest = float(row["mindestbestand"]) if row["mindestbestand"] else 0
                    if mindest > 0 and neu <= mindest:
                        lager_warnungen.append(f"{row['artikel']}: noch {neu:.0f} {row['einheit']} (Mindest: {mindest:.0f})")
                    break

        csv_schreiben(LAGER_PATH, lager)

        if lager_warnungen:
            print("\nNACHBESTELLEN (Betriebsmittel):")
            for w in lager_warnungen:
                print(f"  {w}")

    print(f"\nDone: {liter:.0f} Liter {produkt_key.capitalize()} verbucht.")


def verkauf_verbuchen(produkt_name: str, menge: float, preis_gesamt: float = None, kanal: str = "Direktverkauf"):
    """
    Verkauf verbuchen: Waren reduzieren, Eintrag in verkauf.csv.
    """
    waren = csv_lesen(WAREN_PATH)
    gefunden = False
    einheit = "Stueck"
    einzelpreis = None

    for row in waren:
        if row["produkt"].strip().lower() == produkt_name.strip().lower():
            gefunden = True
            einheit = row.get("einheit", "Stueck")
            alt = float(row["bestand"]) if row["bestand"] else 0
            neu = max(0, alt - menge)
            row["bestand"] = str(int(neu) if neu == int(neu) else round(neu, 2))
            try:
                einzelpreis = float(row.get("verkaufspreis") or 0)
            except ValueError:
                einzelpreis = None
            print(f"Waren: {produkt_name}: {alt:.0f} -> {neu:.0f} {einheit} (-{menge:.0f})")

            mindest = float(row.get("mindestbestand") or 0)
            if mindest > 0 and neu <= mindest:
                print(f"ACHTUNG: {produkt_name} unter Mindestbestand ({neu:.0f} {einheit})!")
            break

    if not gefunden:
        print(f"ACHTUNG: '{produkt_name}' nicht in waren.csv gefunden.")
        print("Verkauf wird trotzdem in verkauf.csv eingetragen.")
    else:
        csv_schreiben(WAREN_PATH, waren)

    # Preis berechnen
    if preis_gesamt is None and einzelpreis:
        preis_gesamt = einzelpreis * menge

    # In verkauf.csv eintragen
    verkauf_rows = csv_lesen(VERKAUF_PATH)
    neuer_eintrag = {
        "datum": datetime.now().strftime("%Y-%m-%d"),
        "produkt": produkt_name,
        "menge": str(menge),
        "einheit": einheit,
        "preis_pro_einheit": str(einzelpreis) if einzelpreis else "",
        "gesamtpreis": str(round(preis_gesamt, 2)) if preis_gesamt else "",
        "kanal": kanal,
        "kunde": "Privatkunde",
        "notiz": "",
    }

    if verkauf_rows:
        verkauf_rows.append(neuer_eintrag)
    else:
        verkauf_rows = [neuer_eintrag]

    csv_schreiben(VERKAUF_PATH, verkauf_rows)
    preis_str = f" | {preis_gesamt:.2f} EUR" if preis_gesamt else ""
    print(f"Verkauf eingetragen: {menge:.0f}x {produkt_name}{preis_str}")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] == "status":
        waren_status()
    elif args[0] == "produktion" and len(args) >= 3:
        try:
            liter = float(args[2].replace(",", "."))
            produktion_verbuchen(args[1], liter)
        except ValueError as e:
            print(f"Fehler: {e}")
    elif args[0] == "verkauf" and len(args) >= 3:
        try:
            menge = float(args[2].replace(",", "."))
            preis = float(args[3].replace(",", ".")) if len(args) >= 4 else None
            verkauf_verbuchen(args[1], menge, preis)
        except ValueError as e:
            print(f"Fehler: {e}")
    else:
        print("Nutzung:")
        print("  python scripts/waren.py status")
        print("  python scripts/waren.py produktion met 20")
        print("  python scripts/waren.py verkauf \"Met 0.5L\" 5")
        print("  python scripts/waren.py verkauf \"Met 0.5L\" 5 47.50")

"""
Daten: Verkaufs-Sammler

Liest Felix' Verkaufsjournal (verkauf.csv) im CEO-GPT-Root
und schreibt Tagesstände in die Datenbank.

Spalten in verkauf.csv:
    datum                 - Verkaufsdatum (JJJJ-MM-TT)
    produkt               - Was verkauft wurde
    menge                 - Anzahl oder Gewicht
    einheit               - Flasche, kg, Liter, Stück
    preis_pro_einheit     - Preis pro Einheit (optional)
    gesamtpreis           - Endpreis des Verkaufs
    kanal                 - Direktverkauf, Onlineshop, Markt, Hofladen
    kunde                 - Privatkunde, Name, oder leer
    notiz                 - Freitext

Erzeugte Tabelle: verkauf
"""

import csv
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = WORKSPACE_ROOT / "verkauf.csv"


def collect():
    """Verkaufsdaten aus verkauf.csv lesen."""
    if not CSV_PATH.exists():
        return {
            "source": "verkauf",
            "status": "skipped",
            "reason": f"verkauf.csv nicht gefunden unter {CSV_PATH}"
        }

    rows = []
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get("datum") or not row.get("produkt"):
                    continue
                rows.append({
                    "datum": row.get("datum", "").strip(),
                    "produkt": row.get("produkt", "").strip(),
                    "menge": row.get("menge", "").strip(),
                    "einheit": row.get("einheit", "").strip(),
                    "preis_pro_einheit": row.get("preis_pro_einheit", "").strip(),
                    "gesamtpreis": row.get("gesamtpreis", "").strip(),
                    "kanal": row.get("kanal", "").strip(),
                    "kunde": row.get("kunde", "").strip(),
                    "notiz": row.get("notiz", "").strip(),
                })
    except Exception as e:
        return {"source": "verkauf", "status": "error", "reason": str(e)}

    return {
        "source": "verkauf",
        "status": "success",
        "data": {"rows": rows}
    }


def write(conn, result, date):
    """Verkaufsdaten in die Datenbank schreiben. Ersetzt immer den kompletten Stand."""
    if result.get("status") != "success":
        return 0

    conn.execute("""
        CREATE TABLE IF NOT EXISTS verkauf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT NOT NULL,
            produkt TEXT NOT NULL,
            menge TEXT,
            einheit TEXT,
            preis_pro_einheit TEXT,
            gesamtpreis REAL,
            kanal TEXT,
            kunde TEXT,
            notiz TEXT,
            eingelesen_am TEXT
        )
    """)
    # Tabelle immer komplett neu befüllen — CSV ist die einzige Quelle der Wahrheit
    conn.execute("DELETE FROM verkauf")

    records = 0
    for row in result["data"]["rows"]:
        try:
            gesamtpreis = float(row["gesamtpreis"].replace(",", ".")) if row["gesamtpreis"] else None
        except ValueError:
            gesamtpreis = None

        conn.execute("""
            INSERT INTO verkauf
                (datum, produkt, menge, einheit, preis_pro_einheit, gesamtpreis, kanal, kunde, notiz, eingelesen_am)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["datum"], row["produkt"], row["menge"], row["einheit"],
            row["preis_pro_einheit"], gesamtpreis, row["kanal"],
            row["kunde"], row["notiz"],
            datetime.now(timezone.utc).isoformat()
        ))
        records += 1

    conn.commit()
    return records


if __name__ == "__main__":
    result = collect()
    if result["status"] == "success":
        print(f"Verkäufe gelesen: {len(result['data']['rows'])} Einträge")
        for row in result["data"]["rows"]:
            print(f"  {row['datum']} | {row['produkt']} | {row['gesamtpreis']} € | {row['kanal']}")
    else:
        print(f"{result['status']}: {result.get('reason', '')}")

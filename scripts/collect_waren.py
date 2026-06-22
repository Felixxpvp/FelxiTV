"""
Daten: Waren-Sammler

Liest waren.csv und schreibt den Produktbestand in die Datenbank.
Dein Mitarbeiter sieht bei /prime den aktuellen Warenbestand.

Erzeugte Tabelle: waren
"""

import csv
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = WORKSPACE_ROOT / "waren.csv"


def collect():
    if not CSV_PATH.exists():
        return {"source": "waren", "status": "skipped", "reason": "waren.csv nicht gefunden"}

    rows = []
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if not row.get("produkt"):
                    continue
                rows.append({
                    "produkt": row.get("produkt", "").strip(),
                    "kategorie": row.get("kategorie", "").strip(),
                    "einheit": row.get("einheit", "").strip(),
                    "bestand": row.get("bestand", "").strip(),
                    "mindestbestand": row.get("mindestbestand", "").strip(),
                    "verkaufspreis": row.get("verkaufspreis", "").strip(),
                })
    except Exception as e:
        return {"source": "waren", "status": "error", "reason": str(e)}

    return {"source": "waren", "status": "success", "data": {"rows": rows}}


def write(conn, result, date):
    if result.get("status") != "success":
        return 0

    conn.execute("""
        CREATE TABLE IF NOT EXISTS waren (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produkt TEXT NOT NULL,
            kategorie TEXT,
            einheit TEXT,
            bestand REAL,
            mindestbestand REAL,
            verkaufspreis REAL,
            eingelesen_am TEXT
        )
    """)
    conn.execute("DELETE FROM waren")

    records = 0
    for row in result["data"]["rows"]:
        try:
            bestand = float(row["bestand"].replace(",", ".")) if row["bestand"] else 0.0
            mindest = float(row["mindestbestand"].replace(",", ".")) if row["mindestbestand"] else None
            preis = float(row["verkaufspreis"].replace(",", ".")) if row["verkaufspreis"] else None
        except ValueError:
            bestand, mindest, preis = 0.0, None, None

        conn.execute("""
            INSERT INTO waren (produkt, kategorie, einheit, bestand, mindestbestand, verkaufspreis, eingelesen_am)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            row["produkt"], row["kategorie"], row["einheit"],
            bestand, mindest, preis,
            datetime.now(timezone.utc).isoformat()
        ))
        records += 1

    conn.commit()
    return records


if __name__ == "__main__":
    result = collect()
    if result["status"] == "success":
        print(f"{len(result['data']['rows'])} Produkte eingelesen")
    else:
        print(f"{result['status']}: {result.get('reason', '')}")

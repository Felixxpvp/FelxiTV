"""
Daten: Lager-Sammler

Liest lager.csv und schreibt den Bestandsstand in die Datenbank.
Dein Mitarbeiter sieht bei /prime automatisch welche Artikel nachbestellt werden müssen.

Erzeugte Tabelle: lager
"""

import csv
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = WORKSPACE_ROOT / "lager.csv"


def collect():
    if not CSV_PATH.exists():
        return {"source": "lager", "status": "skipped", "reason": "lager.csv nicht gefunden"}

    rows = []
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if not row.get("artikel"):
                    continue
                rows.append({
                    "artikel": row.get("artikel", "").strip(),
                    "kategorie": row.get("kategorie", "").strip(),
                    "einheit": row.get("einheit", "").strip(),
                    "bestand": row.get("bestand", "").strip(),
                    "mindestbestand": row.get("mindestbestand", "").strip(),
                })
    except Exception as e:
        return {"source": "lager", "status": "error", "reason": str(e)}

    return {"source": "lager", "status": "success", "data": {"rows": rows}}


def write(conn, result, date):
    if result.get("status") != "success":
        return 0

    conn.execute("""
        CREATE TABLE IF NOT EXISTS lager (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artikel TEXT NOT NULL,
            kategorie TEXT,
            einheit TEXT,
            bestand REAL,
            mindestbestand REAL,
            eingelesen_am TEXT
        )
    """)
    conn.execute("DELETE FROM lager")

    records = 0
    for row in result["data"]["rows"]:
        try:
            bestand = float(row["bestand"].replace(",", ".")) if row["bestand"] else None
            mindest = float(row["mindestbestand"].replace(",", ".")) if row["mindestbestand"] else None
        except ValueError:
            bestand, mindest = None, None

        conn.execute("""
            INSERT INTO lager (artikel, kategorie, einheit, bestand, mindestbestand, eingelesen_am)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["artikel"], row["kategorie"], row["einheit"], bestand, mindest,
            datetime.now(timezone.utc).isoformat()
        ))
        records += 1

    conn.commit()
    return records


if __name__ == "__main__":
    result = collect()
    if result["status"] == "success":
        rows = result["data"]["rows"]
        print(f"{len(rows)} Artikel eingelesen")
        warnungen = [r for r in rows if r["bestand"] and r["mindestbestand"]
                     and float(r["bestand"]) <= float(r["mindestbestand"])]
        if warnungen:
            print(f"⚠️  {len(warnungen)} Artikel unter Mindestbestand:")
            for r in warnungen:
                print(f"  {r['artikel']}: {r['bestand']} {r['einheit']} (Mindest: {r['mindestbestand']})")
    else:
        print(f"{result['status']}: {result.get('reason', '')}")

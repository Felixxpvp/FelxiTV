"""
Daten: Buchhaltungs-Sammler

Liest Felix' Kassenbuch (buchhaltung.csv) und schreibt
Ein- und Ausgaben in die Datenbank.

Spalten in buchhaltung.csv:
    datum        - Buchungsdatum (JJJJ-MM-TT)
    typ          - Einnahme / Ausgabe
    kategorie    - z.B. Met-Verkauf, Saatgut, Jagd, Imkerei, ...
    beschreibung - Freitext, was genau
    betrag       - Betrag in Euro (z.B. 19.00)
    zahlungsart  - Bar, Überweisung, Karte, PayPal
    notiz        - Freitext

Erzeugte Tabelle: buchhaltung
"""

import csv
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = WORKSPACE_ROOT / "buchhaltung.csv"


def collect():
    """Buchhaltungsdaten aus buchhaltung.csv lesen."""
    if not CSV_PATH.exists():
        return {
            "source": "buchhaltung",
            "status": "skipped",
            "reason": f"buchhaltung.csv nicht gefunden unter {CSV_PATH}"
        }

    rows = []
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get("datum") or not row.get("typ"):
                    continue
                rows.append({
                    "datum": row.get("datum", "").strip(),
                    "typ": row.get("typ", "").strip(),
                    "kategorie": row.get("kategorie", "").strip(),
                    "beschreibung": row.get("beschreibung", "").strip(),
                    "betrag": row.get("betrag", "").strip(),
                    "zahlungsart": row.get("zahlungsart", "").strip(),
                    "notiz": row.get("notiz", "").strip(),
                })
    except Exception as e:
        return {"source": "buchhaltung", "status": "error", "reason": str(e)}

    return {
        "source": "buchhaltung",
        "status": "success",
        "data": {"rows": rows}
    }


def write(conn, result, date):
    """Buchhaltungsdaten in die Datenbank schreiben. CSV ist immer die Quelle der Wahrheit."""
    if result.get("status") != "success":
        return 0

    conn.execute("""
        CREATE TABLE IF NOT EXISTS buchhaltung (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT NOT NULL,
            typ TEXT NOT NULL,
            kategorie TEXT,
            beschreibung TEXT,
            betrag REAL,
            zahlungsart TEXT,
            notiz TEXT,
            eingelesen_am TEXT
        )
    """)
    conn.execute("DELETE FROM buchhaltung")

    records = 0
    for row in result["data"]["rows"]:
        try:
            betrag = float(row["betrag"].replace(",", ".")) if row["betrag"] else None
        except ValueError:
            betrag = None

        conn.execute("""
            INSERT INTO buchhaltung
                (datum, typ, kategorie, beschreibung, betrag, zahlungsart, notiz, eingelesen_am)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["datum"], row["typ"], row["kategorie"], row["beschreibung"],
            betrag, row["zahlungsart"], row["notiz"],
            datetime.now(timezone.utc).isoformat()
        ))
        records += 1

    conn.commit()
    return records


if __name__ == "__main__":
    result = collect()
    if result["status"] == "success":
        rows = result["data"]["rows"]
        einnahmen = sum(float(r["betrag"]) for r in rows if r["typ"] == "Einnahme" and r["betrag"])
        ausgaben = sum(float(r["betrag"]) for r in rows if r["typ"] == "Ausgabe" and r["betrag"])
        print(f"Buchungen gelesen: {len(rows)} Einträge")
        print(f"  Einnahmen: €{einnahmen:.2f}")
        print(f"  Ausgaben:  €{ausgaben:.2f}")
        print(f"  Saldo:     €{einnahmen - ausgaben:.2f}")
    else:
        print(f"{result['status']}: {result.get('reason', '')}")

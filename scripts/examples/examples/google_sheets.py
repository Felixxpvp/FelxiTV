"""
Daten: Google Sheets Sammler (Beispiel)

Der universelle Connector. Liest beliebige Google-Tabellen in die Datenbank.
Wenn deine Daten in einer Tabelle liegen (P&L, KPIs, CRM, Outreach-Tracker),
holt sie dieser Sammler raus.

Diese Datei nach scripts/collect_sheets.py (oder collect_pnl.py etc.) kopieren.

Voraussetzungen:
    GOOGLE_SERVICE_ACCOUNT_JSON : Pfad zur Service-Account-JSON
    GOOGLE_SHEET_ID             : Spreadsheet-ID aus der URL

Optional:
    GOOGLE_SHEET_TAB : Tab-Name (Standard: erster Tab)

Erzeugte Tabellen: dynamisch, benannt nach dem Tab (z.B. sheet_feb_26)
Zusätzliches pip: google-api-python-client google-auth

HINWEIS: Dieses Beispiel liest ein einfaches Layout aus Datum und Kennzahlen:
  Zeile 1: Spaltenüberschriften (datum, kennzahl1, kennzahl2, ...)
  Zeile 2 und folgende: Datenzeilen
Pass die Verarbeitung an dein konkretes Tabellen-Layout an.
"""

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
except ImportError:
    raise ImportError(
        "Pakete fehlen, installier sie mit: pip install google-api-python-client google-auth"
    )


def _get_sheets_service():
    """Authentifizierten Google-Sheets-API-Client anlegen."""
    creds_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if not creds_path:
        return None
    full_path = Path(creds_path)
    if not full_path.is_absolute():
        full_path = Path(__file__).resolve().parent.parent.parent / creds_path
    if not full_path.exists():
        return None
    creds = Credentials.from_service_account_file(
        str(full_path),
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    return build("sheets", "v4", credentials=creds)


def collect():
    """Daten aus einer Google-Tabelle lesen."""
    sheet_id = os.getenv("GOOGLE_SHEET_ID", "").strip()
    if not sheet_id:
        return {
            "source": "google_sheets", "status": "skipped",
            "reason": "GOOGLE_SHEET_ID fehlt, kopier die ID aus deiner "
                      "Spreadsheet-URL (alles zwischen /d/ und /edit)"
        }

    service = _get_sheets_service()
    if not service:
        return {
            "source": "google_sheets", "status": "skipped",
            "reason": "GOOGLE_SERVICE_ACCOUNT_JSON fehlt oder ungültig"
        }

    tab = os.getenv("GOOGLE_SHEET_TAB", "").strip()

    try:
        # Verfügbare Tabs holen
        spreadsheet = service.spreadsheets().get(
            spreadsheetId=sheet_id
        ).execute()
        sheets = [
            s["properties"]["title"]
            for s in spreadsheet.get("sheets", [])
        ]

        # Angegebenen Tab oder den ersten nehmen
        target_tab = tab if tab and tab in sheets else sheets[0]

        # Alle Daten aus dem Tab lesen
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=f"'{target_tab}'!A:ZZ"
        ).execute()
        values = result.get("values", [])

        if not values or len(values) < 2:
            return {
                "source": "google_sheets", "status": "skipped",
                "reason": f"Tab '{target_tab}' ist leer oder enthält nur Überschriften"
            }

        # Aufteilen: erste Zeile = Überschriften, Rest = Daten
        headers = [
            str(h).strip().lower().replace(" ", "_").replace("-", "_")
            for h in values[0]
        ]
        rows = []
        for row in values[1:]:
            padded = row + [""] * (len(headers) - len(row))
            row_dict = {headers[i]: padded[i] for i in range(len(headers))}
            rows.append(row_dict)

        return {
            "source": "google_sheets",
            "status": "success",
            "data": {
                "tab": target_tab,
                "available_tabs": sheets,
                "headers": headers,
                "rows": rows,
                "row_count": len(rows),
            }
        }

    except Exception as e:
        return {"source": "google_sheets", "status": "error", "reason": str(e)}


def write(conn, result, date):
    """
    Google-Sheets-Daten in die Datenbank schreiben. Gibt Anzahl der Datensätze zurück.

    HINWEIS: Das ist ein generischer Schreiber, der eine Tabelle anlegt, deren Spalten
    den Überschriften der Tabelle entsprechen. Während der Installation passt dein
    Mitarbeiter Tabellen-Namen, Spalten-Typen und Primary Key an deinen Anwendungsfall an.
    """
    if result.get("status") != "success":
        return 0

    data = result["data"]
    headers = data["headers"]
    rows = data["rows"]

    # Tabellen-Name aus dem Tab abgeleitet (z.B. "Feb 26" -> "sheet_feb_26")
    tab_clean = data["tab"].lower().replace(" ", "_").replace("-", "_")
    table_name = f"sheet_{tab_clean}"

    # CREATE TABLE bauen, alle Spalten TEXT
    # (Spalten-Typen für deine konkrete Tabelle anpassen)
    columns = ", ".join(f'"{h}" TEXT' for h in headers)
    pk = ""
    if headers and "date" in headers[0]:
        pk = f', PRIMARY KEY ("{headers[0]}")'
    conn.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns}{pk})')

    records = 0
    for row in rows:
        if not any(row.values()):
            continue
        placeholders = ", ".join("?" for _ in headers)
        col_names = ", ".join(f'"{h}"' for h in headers)
        values = [row.get(h, "") for h in headers]
        conn.execute(
            f'INSERT OR REPLACE INTO "{table_name}" ({col_names}) '
            f'VALUES ({placeholders})',
            values
        )
        records += 1

    conn.commit()
    return records


if __name__ == "__main__":
    result = collect()
    if result["status"] == "success":
        data = result["data"]
        print(f"Tab: {data['tab']} ({data['row_count']} Zeilen)")
        print(f"Verfügbare Tabs: {', '.join(data['available_tabs'])}")
        print(f"Überschriften: {', '.join(data['headers'])}")
        if data["rows"]:
            print(f"Erste Zeile: {data['rows'][0]}")
    else:
        print(f"{result['status']}: {result.get('reason', '')}")

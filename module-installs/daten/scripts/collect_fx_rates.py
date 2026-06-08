"""
Daten: Wechselkurs-Sammler (Starter)

Holt Wechselkurse von der Frankfurter-API (Daten der Europäischen Zentralbank).
Kein API-Key nötig, ideal als erster Sammler zum Testen der Pipeline.

Erzeugt die Tabelle: fx_rates
"""

import sqlite3
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    raise ImportError(
        "Paket 'requests' fehlt, installier es mit: pip install requests"
    )

API_URL = "https://api.frankfurter.app/latest"

# Pass die Liste an die Währungen an, die dich interessieren
TARGET_CURRENCIES = ["EUR", "GBP", "CHF", "USD", "CAD", "AUD", "JPY"]


def collect():
    """Aktuelle Wechselkurse holen. Keine Authentifizierung nötig."""
    try:
        currencies = ",".join(TARGET_CURRENCIES)
        response = requests.get(
            f"{API_URL}?from=USD&to={currencies}", timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return {
            "source": "fx_rates",
            "status": "success",
            "data": {
                "base": data.get("base", "USD"),
                "date": data.get("date"),
                "rates": data.get("rates", {}),
            }
        }
    except Exception as e:
        return {"source": "fx_rates", "status": "error", "reason": str(e)}


def write(conn, result, date):
    """Wechselkurse in die Datenbank schreiben. Gibt Anzahl der Datensätze zurück."""
    # Tabelle anlegen, falls noch nicht da
    conn.execute("""
        CREATE TABLE IF NOT EXISTS fx_rates (
            date TEXT NOT NULL,
            currency TEXT NOT NULL,
            rate REAL NOT NULL,
            base TEXT DEFAULT 'USD',
            collected_at TEXT,
            PRIMARY KEY (date, currency)
        )
    """)

    if result.get("status") != "success":
        conn.commit()
        return 0

    data = result["data"]
    rates = data.get("rates", {})
    rate_date = data.get("date", date)
    collected_at = datetime.now(timezone.utc).isoformat()
    records = 0

    for currency, rate in rates.items():
        conn.execute(
            "INSERT OR REPLACE INTO fx_rates "
            "(date, currency, rate, base, collected_at) VALUES (?, ?, ?, ?, ?)",
            (rate_date, currency, rate, "USD", collected_at)
        )
        records += 1

    conn.commit()
    return records


if __name__ == "__main__":
    # Schneller Test, prüft ob die Pipeline läuft
    result = collect()
    if result["status"] == "success":
        print(f"Wechselkurse vom {result['data']['date']}:")
        for curr, rate in sorted(result["data"]["rates"].items()):
            print(f"  USD -> {curr}: {rate:.4f}")
    else:
        print(f"Fehler: {result.get('reason')}")

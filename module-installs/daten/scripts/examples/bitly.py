"""
Daten: Bitly Link-Tracking Sammler (Beispiel)

Holt Klick-Daten für alle deine Bitly-Links.
Nützlich, um zu sehen, welche Inhalte den meisten Traffic bringen.

Diese Datei nach scripts/collect_bitly.py kopieren, um sie zu aktivieren.

Voraussetzungen:
    BITLY_ACCESS_TOKEN : holen unter app.bitly.com/settings/api/

Erzeugte Tabelle: bitly_daily
Zusätzliches pip: requests (ist schon Basis-Paket)
"""

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

try:
    import requests
except ImportError:
    raise ImportError("Paket 'requests' fehlt, installier es mit: pip install requests")

API_BASE = "https://api-ssl.bitly.com/v4"


def _api_get(token, endpoint, params=None):
    """Authentifizierten Bitly-API-GET-Aufruf machen."""
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        f"{API_BASE}{endpoint}",
        headers=headers, params=params, timeout=15
    )
    resp.raise_for_status()
    return resp.json()


def collect():
    """Bitly Link-Klick-Daten holen."""
    token = os.getenv("BITLY_ACCESS_TOKEN", "").strip()
    if not token:
        return {
            "source": "bitly", "status": "skipped",
            "reason": "BITLY_ACCESS_TOKEN fehlt, "
                      "holen unter app.bitly.com/settings/api/"
        }

    try:
        # Alle Gruppen holen
        groups = _api_get(token, "/groups")
        if not groups.get("groups"):
            return {
                "source": "bitly", "status": "error",
                "reason": "Keine Bitly-Gruppen gefunden"
            }

        group_guid = groups["groups"][0]["guid"]

        # Alle Bitlinks mit Pagination holen
        all_links = []
        page = 1
        while True:
            resp = _api_get(
                token, f"/groups/{group_guid}/bitlinks",
                {"size": 100, "page": page}
            )
            links = resp.get("links", [])
            if not links:
                break
            all_links.extend(links)
            pagination = resp.get("pagination", {})
            if page >= pagination.get("total", 1):
                break
            page += 1

        # Klick-Zahlen pro Link holen
        link_data = []
        for link in all_links:
            bitlink_id = link.get("id", "")
            try:
                clicks_1d = _api_get(
                    token, f"/bitlinks/{bitlink_id}/clicks/summary",
                    {"unit": "day", "units": 1}
                )
                clicks_30d = _api_get(
                    token, f"/bitlinks/{bitlink_id}/clicks/summary",
                    {"unit": "day", "units": 30}
                )
                link_data.append({
                    "bitlink_id": bitlink_id,
                    "long_url": link.get("long_url", ""),
                    "title": link.get("title", ""),
                    "created_at": link.get("created_at", ""),
                    "tags": link.get("tags", []),
                    "clicks_1d": clicks_1d.get("total_clicks", 0),
                    "clicks_30d": clicks_30d.get("total_clicks", 0),
                })
            except Exception:
                continue

        link_data.sort(key=lambda x: x["clicks_30d"], reverse=True)

        return {
            "source": "bitly",
            "status": "success",
            "data": {
                "total_links": len(link_data),
                "total_clicks_1d": sum(l["clicks_1d"] for l in link_data),
                "total_clicks_30d": sum(l["clicks_30d"] for l in link_data),
                "links": link_data,
            }
        }

    except Exception as e:
        return {"source": "bitly", "status": "error", "reason": str(e)}


def write(conn, result, date):
    """Bitly-Daten in die Datenbank schreiben. Gibt Anzahl der Datensätze zurück."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bitly_daily (
            date TEXT NOT NULL,
            bitlink_id TEXT NOT NULL,
            long_url TEXT,
            title TEXT,
            clicks_1d INTEGER,
            clicks_30d INTEGER,
            tags TEXT,
            collected_at TEXT,
            PRIMARY KEY (date, bitlink_id)
        )
    """)

    if result.get("status") != "success":
        conn.commit()
        return 0

    collected_at = datetime.now(timezone.utc).isoformat()
    records = 0

    for link in result["data"]["links"]:
        tags = ",".join(link.get("tags", []))
        conn.execute(
            "INSERT OR REPLACE INTO bitly_daily "
            "(date, bitlink_id, long_url, title, clicks_1d, clicks_30d, "
            "tags, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (date, link["bitlink_id"], link["long_url"], link["title"],
             link["clicks_1d"], link["clicks_30d"], tags, collected_at)
        )
        records += 1

    conn.commit()
    return records


if __name__ == "__main__":
    result = collect()
    if result["status"] == "success":
        data = result["data"]
        print(f"Links gesamt: {data['total_links']}")
        print(f"Klicks heute: {data['total_clicks_1d']}")
        print(f"Klicks (30 Tage): {data['total_clicks_30d']}")
        print(f"\nTop 5:")
        for link in data["links"][:5]:
            print(f"  {link['title'] or link['bitlink_id']}: "
                  f"{link['clicks_30d']} Klicks")
    else:
        print(f"{result['status']}: {result.get('reason', '')}")

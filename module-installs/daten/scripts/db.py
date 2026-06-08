"""
Daten: Datenbank-Grundgerüst

Lokale SQLite-Datenbank für deine Geschäftszahlen.
Legt die Datenbank an, verwaltet Verbindungen und stellt Abfrage-Helfer bereit.

Jeder Sammler legt seine eigenen Tabellen beim ersten Lauf an,
das Schema muss nicht vorher definiert werden. Die Datenbank wächst
mit, je mehr Sammler du dazu nimmst.
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

# Datenbank lebt im data/ Ordner im Workspace-Root
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = WORKSPACE_ROOT / "data" / "data.db"


def init_db():
    """
    Datenbank initialisieren. Legt sie an, falls sie noch nicht existiert.
    Gibt eine Verbindung mit WAL-Modus und Row-Factory zurück.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    # Sammel-Log, hält jeden Lauf fest
    conn.execute("""
        CREATE TABLE IF NOT EXISTS collection_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            collected_at TEXT NOT NULL,
            source TEXT NOT NULL,
            status TEXT NOT NULL,
            reason TEXT,
            records_written INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn


def get_connection():
    """Datenbank-Verbindung holen. Initialisiert die DB, falls noch nicht da."""
    if not DB_PATH.exists():
        return init_db()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def log_collection(conn, source, status, records=0, reason=None):
    """Sammel-Lauf in die collection_log Tabelle eintragen."""
    conn.execute(
        "INSERT INTO collection_log (collected_at, source, status, reason, records_written) "
        "VALUES (?, ?, ?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), source, status, reason, records)
    )
    conn.commit()


def query_one(conn, sql, params=None):
    """Abfrage ausführen, erste Zeile als dict zurückgeben oder None."""
    try:
        row = conn.execute(sql, params or ()).fetchone()
        return dict(row) if row else None
    except Exception:
        return None


def query_all(conn, sql, params=None):
    """Abfrage ausführen, alle Zeilen als Liste von dicts zurückgeben."""
    try:
        rows = conn.execute(sql, params or ()).fetchall()
        return [dict(row) for row in rows]
    except Exception:
        return []


def table_exists(conn, table_name):
    """Prüfen, ob eine Tabelle existiert."""
    result = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,)
    ).fetchone()
    return result is not None


def get_latest_date(conn, table_name, date_column="date"):
    """Aktuellstes Datum aus einer Tabelle holen. Gibt String oder None zurück."""
    try:
        row = conn.execute(
            f"SELECT MAX({date_column}) as d FROM {table_name}"
        ).fetchone()
        return row["d"] if row else None
    except Exception:
        return None


def get_table_list(conn):
    """Alle Nutzer-Tabellen auflisten (ohne SQLite-Internas und collection_log)."""
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' AND name != 'collection_log' "
        "ORDER BY name"
    ).fetchall()
    return [row["name"] for row in rows]


if __name__ == "__main__":
    # Schneller Test, legt die Datenbank an und zeigt den Stand
    conn = init_db()
    print(f"Datenbank initialisiert: {DB_PATH}")
    print(f"Größe: {DB_PATH.stat().st_size / 1024:.1f} KB")
    tables = get_table_list(conn)
    print(f"Tabellen: {tables if tables else '(noch keine, lass einen Sammler laufen, dann werden welche angelegt)'}")
    conn.close()

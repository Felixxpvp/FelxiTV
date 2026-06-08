"""
Daten: Kennzahlen-Generator

Liest die Datenbank und erzeugt eine lesbare key-metrics.md.
Diese Datei wird vom /prime-Befehl geladen, damit dein Mitarbeiter
immer frische Zahlen sieht.

Findet automatisch, welche Tabellen es gibt, und erzeugt pro Tabelle
eine Sektion. Dein Mitarbeiter passt die Datei während der Installation
an deine echten Quellen an.

Nutzung:
    python scripts/generate_metrics.py
"""

import sqlite3
from datetime import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = WORKSPACE_ROOT / "data" / "data.db"
OUTPUT_PATH = WORKSPACE_ROOT / "context" / "group" / "key-metrics.md"


# --- Formatierungs-Helfer ---

def fmt_number(value, prefix="", suffix=""):
    """Zahl mit Tausender-Trennzeichen. Gibt 'Keine Daten' bei None zurück."""
    if value is None:
        return "Keine Daten"
    if isinstance(value, float):
        return f"{prefix}{value:,.0f}{suffix}"
    return f"{prefix}{value:,}{suffix}"


def fmt_currency(value, symbol="€"):
    """Währungsbetrag mit Symbol und Tausender-Trennzeichen."""
    if value is None:
        return "Keine Daten"
    return f"{symbol}{value:,.0f}"


def fmt_pct(value):
    """Prozentwert auf 1 Nachkommastelle."""
    if value is None:
        return "Keine Daten"
    return f"{value:.1f}%"


def query_one(conn, sql):
    """Abfrage-Helfer, gibt erste Zeile als dict oder None zurück."""
    try:
        row = conn.execute(sql).fetchone()
        return dict(row) if row else None
    except Exception:
        return None


def query_all(conn, sql):
    """Abfrage-Helfer, gibt alle Zeilen als Liste von dicts zurück."""
    try:
        return [dict(r) for r in conn.execute(sql).fetchall()]
    except Exception:
        return []


def table_exists(conn, name):
    """Prüfen, ob eine Tabelle existiert."""
    r = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    return r is not None


# ============================================================
# SEKTIONS-GENERATOREN
# Jede Funktion gibt eine Liste von Markdown-Zeilen zurück.
# Während der Installation legt dein Mitarbeiter hier eigene
# Sektions-Funktionen für deine angebundenen Quellen an.
# ============================================================


def section_fx_rates(conn):
    """Wechselkurse, der Starter-Sammler (immer verfügbar)."""
    if not table_exists(conn, "fx_rates"):
        return []
    lines = []
    lines.append("## Wechselkurse")
    lines.append("| Währung | Kurs (von USD) | Stand |")
    lines.append("|---------|----------------|-------|")
    rows = query_all(conn, """
        SELECT date, currency, rate FROM fx_rates
        WHERE date = (SELECT MAX(date) FROM fx_rates)
        ORDER BY currency
    """)
    for r in rows:
        lines.append(f"| {r['currency']} | {r['rate']:.4f} | {r['date']} |")
    lines.append("")
    return lines


def section_finanzen(conn):
    """Einnahmen, Ausgaben und Ergebnis."""
    if not table_exists(conn, "finanzen_stand"):
        return []
    import json
    row = query_one(conn, "SELECT * FROM finanzen_stand ORDER BY date DESC LIMIT 1")
    if not row:
        return []
    lines = ["## Finanzen"]
    lines.append(f"| Kennzahl | Wert | Stand |")
    lines.append(f"|---|---|---|")
    lines.append(f"| Einnahmen gesamt | {fmt_currency(row['einnahmen_gesamt'])} | {row['date']} |")
    lines.append(f"| Ausgaben gesamt | {fmt_currency(row['ausgaben_gesamt'])} | {row['date']} |")
    ergebnis = row['ergebnis']
    pfeil = "+" if ergebnis >= 0 else ""
    lines.append(f"| Ergebnis | {pfeil}{fmt_currency(ergebnis)} | {row['date']} |")
    ein = json.loads(row["einnahmen_json"] or "{}")
    aus = json.loads(row["ausgaben_json"] or "{}")
    if ein:
        lines.append("")
        lines.append("**Einnahmen nach Sparte:**")
        for sparte, betrag in sorted(ein.items()):
            lines.append(f"- {sparte}: {fmt_currency(betrag)}")
    if aus:
        lines.append("")
        lines.append("**Ausgaben nach Sparte:**")
        for sparte, betrag in sorted(aus.items()):
            lines.append(f"- {sparte}: {fmt_currency(betrag)}")
    lines.append("")
    return lines


def section_produktion(conn):
    """Produktions- und Verkaufszahlen."""
    if not table_exists(conn, "produktion_stand"):
        return []
    row = query_one(conn, "SELECT * FROM produktion_stand ORDER BY date DESC LIMIT 1")
    if not row:
        return []
    lines = ["## Produktion & Verkauf"]
    lines.append(f"| Sparte | Produziert | Verkauft | Stand |")
    lines.append(f"|---|---|---|---|")
    lines.append(f"| Met | {fmt_number(row['met_produziert'])} Fl. | {fmt_number(row['met_verkauft'])} Fl. | {row['date']} |")
    lines.append(f"| Gemüse | {fmt_number(row['gemuese_produziert'])} kg | {fmt_number(row['gemuese_verkauft'])} kg | {row['date']} |")
    lines.append(f"| Obst | {fmt_number(row['obst_produziert'])} kg | {fmt_number(row['obst_verkauft'])} kg | {row['date']} |")
    lines.append(f"| Jagd & Fleisch | {fmt_number(row['jagd_produziert'])} kg | {fmt_number(row['jagd_verkauft'])} kg | {row['date']} |")
    lines.append("")
    return lines


# ============================================================
# HAUPT-GENERATOR
# ============================================================

SECTIONS = [
    section_finanzen,
    section_produktion,
    section_fx_rates,
]


def generate(conn):
    """Erzeugt den Markdown-Inhalt der Kennzahlen-Datei."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "# Kennzahlen",
        "",
        f"> Automatisch aus der Datenbank erzeugt. Letztes Update: {today}",
        f"> Quelle: `data/data.db` | Neu erzeugen: `python scripts/generate_metrics.py`",
        "",
    ]

    # Alle registrierten Sektions-Generatoren laufen
    for section_fn in SECTIONS:
        try:
            section_lines = section_fn(conn)
            if section_lines:
                lines.extend(section_lines)
        except Exception as e:
            lines.append(f"<!-- Fehler in {section_fn.__name__}: {e} -->")
            lines.append("")

    # Frische-Tabelle (findet alle Tabellen automatisch)
    lines.append("## Datenfrische")
    lines.append("| Quelle | Letzter Datensatz | Status |")
    lines.append("|--------|-------------------|--------|")

    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name != 'collection_log' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name"
    ).fetchall()

    for t in tables:
        name = t["name"]
        try:
            row = conn.execute(f"SELECT MAX(date) as d FROM {name}").fetchone()
            if row and row["d"]:
                lines.append(f"| {name} | {row['d']} | verbunden |")
            else:
                lines.append(f"| {name} |: | leer |")
        except Exception:
            lines.append(f"| {name} |: | keine Datums-Spalte |")

    lines.append("")
    return "\n".join(lines)


def main():
    """Erzeugt key-metrics.md aus der Datenbank."""
    if not DB_PATH.exists():
        print(f"Datenbank nicht gefunden unter {DB_PATH}")
        print("Erst sammeln: python scripts/collect.py")
        return

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    content = generate(conn)
    conn.close()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Kennzahlen geschrieben nach: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

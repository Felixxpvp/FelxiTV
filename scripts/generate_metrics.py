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


# --- ANPASSUNGS-ZONE ---

def section_lager(conn):
    """Lagerbestand — zeigt nur Artikel unter Mindestbestand."""
    if not table_exists(conn, "lager"):
        return []

    warnungen = query_all(conn, """
        SELECT artikel, kategorie, bestand, mindestbestand, einheit
        FROM lager
        WHERE mindestbestand IS NOT NULL AND bestand IS NOT NULL
        AND bestand <= mindestbestand
        ORDER BY kategorie, artikel
    """)

    if not warnungen:
        return ["## Lager", "✅ Alle Artikel über Mindestbestand.", ""]

    lines = ["## Lager — Nachbestellen ⚠️"]
    lines.append("| Artikel | Bestand | Mindest | Einheit |")
    lines.append("|---------|---------|---------|---------|")
    for r in warnungen:
        lines.append(f"| {r['artikel']} | {r['bestand']:.0f} | {r['mindestbestand']:.0f} | {r['einheit']} |")
    lines.append("")
    return lines


def section_buchhaltung(conn):
    """Ein- und Ausgaben aus dem Kassenbuch."""
    if not table_exists(conn, "buchhaltung"):
        return []
    lines = ["## Kassenbuch"]

    # Gesamtsaldo
    totals = query_all(conn, """
        SELECT typ, SUM(betrag) as summe, COUNT(*) as anzahl
        FROM buchhaltung WHERE betrag IS NOT NULL
        GROUP BY typ
    """)
    einnahmen = next((r["summe"] for r in totals if r["typ"] == "Einnahme"), 0)
    ausgaben = next((r["summe"] for r in totals if r["typ"] == "Ausgabe"), 0)
    saldo = (einnahmen or 0) - (ausgaben or 0)
    lines.append(f"| | Betrag |")
    lines.append(f"|---|---|")
    lines.append(f"| Einnahmen gesamt | {fmt_currency(einnahmen)} |")
    lines.append(f"| Ausgaben gesamt | {fmt_currency(ausgaben)} |")
    lines.append(f"| **Saldo** | **{fmt_currency(saldo)}** |")
    lines.append("")

    # Diesen Monat
    mtd = query_all(conn, """
        SELECT typ, SUM(betrag) as summe
        FROM buchhaltung
        WHERE strftime('%Y-%m', datum) = strftime('%Y-%m', 'now')
        AND betrag IS NOT NULL
        GROUP BY typ
    """)
    if mtd:
        ein_m = next((r["summe"] for r in mtd if r["typ"] == "Einnahme"), 0)
        aus_m = next((r["summe"] for r in mtd if r["typ"] == "Ausgabe"), 0)
        lines.append(f"**Diesen Monat:** Einnahmen {fmt_currency(ein_m)} | Ausgaben {fmt_currency(aus_m)} | Saldo {fmt_currency((ein_m or 0) - (aus_m or 0))}")
        lines.append("")

    # Letzte 5 Buchungen
    recent = query_all(conn, "SELECT datum, typ, kategorie, beschreibung, betrag FROM buchhaltung ORDER BY datum DESC, id DESC LIMIT 5")
    if recent:
        lines.append("**Letzte Buchungen:**")
        lines.append("| Datum | Typ | Kategorie | Betrag |")
        lines.append("|-------|-----|-----------|--------|")
        for r in recent:
            betrag = f"€{r['betrag']:.2f}" if r["betrag"] else "-"
            lines.append(f"| {r['datum']} | {r['typ']} | {r['kategorie'] or '-'} | {betrag} |")
    lines.append("")
    return lines


def section_verkauf(conn):
    """Verkaufsjournal von Felix."""
    if not table_exists(conn, "verkauf"):
        return []
    lines = ["## Verkäufe"]

    # Umsatz gesamt
    total = query_one(conn, "SELECT SUM(gesamtpreis) as summe, COUNT(*) as anzahl FROM verkauf WHERE gesamtpreis IS NOT NULL")
    if total:
        lines.append(f"**Gesamt:** {total['anzahl']} Verkäufe | Umsatz: {fmt_currency(total['summe'])}")
        lines.append("")

    # Umsatz diesen Monat
    mtd = query_one(conn, """
        SELECT SUM(gesamtpreis) as summe, COUNT(*) as anzahl
        FROM verkauf
        WHERE strftime('%Y-%m', datum) = strftime('%Y-%m', 'now')
        AND gesamtpreis IS NOT NULL
    """)
    if mtd and mtd["anzahl"]:
        lines.append(f"**Diesen Monat:** {mtd['anzahl']} Verkäufe | {fmt_currency(mtd['summe'])}")
        lines.append("")

    # Letzte 5 Verkäufe
    recent = query_all(conn, "SELECT datum, produkt, gesamtpreis, kanal FROM verkauf ORDER BY datum DESC, id DESC LIMIT 5")
    if recent:
        lines.append("**Letzte Verkäufe:**")
        lines.append("| Datum | Produkt | Preis | Kanal |")
        lines.append("|-------|---------|-------|-------|")
        for r in recent:
            preis = f"€{r['gesamtpreis']:.2f}" if r["gesamtpreis"] else "-"
            lines.append(f"| {r['datum']} | {r['produkt']} | {preis} | {r['kanal'] or '-'} |")
    lines.append("")
    return lines


# ============================================================
# HAUPT-GENERATOR
# ============================================================

# Alle Sektions-Funktionen hier registrieren. Während der Installation
# kommen weitere dazu.
SECTIONS = [
    section_lager,
    section_buchhaltung,
    section_verkauf,
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
            cols = [r["name"] for r in conn.execute(f"PRAGMA table_info({name})").fetchall()]
            date_col = next((c for c in cols if c in ("date", "datum")), None)
            if date_col:
                row = conn.execute(f"SELECT MAX({date_col}) as d FROM {name}").fetchone()
                if row and row["d"]:
                    lines.append(f"| {name} | {row['d']} | verbunden |")
                else:
                    lines.append(f"| {name} | - | leer |")
            else:
                lines.append(f"| {name} | - | keine Datums-Spalte |")
        except Exception:
            lines.append(f"| {name} | - | Fehler |")

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

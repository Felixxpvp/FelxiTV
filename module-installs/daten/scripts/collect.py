"""
Daten: Sammel-Orchestrator

Findet und startet alle aktiven Sammler (collect_*.py im scripts-Ordner).
Nach der Sammlung wird die key-metrics.md neu erzeugt, damit /prime immer
frische Zahlen lädt.

Nutzung:
    python scripts/collect.py                          # Alle Sammler
    python scripts/collect.py --sources youtube,stripe  # Nur bestimmte
    python scripts/collect.py --date 2026-02-20         # Datum überschreiben
"""

import sys
import os
import argparse
import importlib.util
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def discover_collectors():
    """Alle collect_*.py Dateien im scripts-Ordner finden."""
    collectors = {}
    for filepath in sorted(SCRIPT_DIR.glob("collect_*.py")):
        # Den Orchestrator selber überspringen
        if filepath.name == "collect.py":
            continue
        # Name extrahieren: collect_youtube.py -> youtube
        name = filepath.stem.replace("collect_", "")
        collectors[name] = filepath
    return collectors


def import_collector(name, filepath):
    """Sammler-Modul dynamisch laden."""
    spec = importlib.util.spec_from_file_location(f"collect_{name}", str(filepath))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    parser = argparse.ArgumentParser(description="Daten aus allen Quellen sammeln")
    parser.add_argument(
        "--sources", type=str, default=None,
        help="Komma-Liste der Quellen (Standard: alle)"
    )
    parser.add_argument(
        "--date", type=str, default=None,
        help="Sammel-Datum überschreiben (YYYY-MM-DD, Standard: heute)"
    )
    args = parser.parse_args()

    today = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Verfügbare Sammler finden
    available = discover_collectors()
    if not available:
        print(f"[{timestamp}] Keine Sammler gefunden. Leg collect_*.py Dateien in scripts/ an.",
              file=sys.stderr)
        sys.exit(1)

    # Bestimmen, welche laufen sollen
    if args.sources:
        names = [s.strip() for s in args.sources.split(",")]
        unknown = [s for s in names if s not in available]
        if unknown:
            print(f"[{timestamp}] Unbekannte Quellen ignoriert: {', '.join(unknown)}",
                  file=sys.stderr)
        names = [s for s in names if s in available]
    else:
        names = list(available.keys())

    # Datenbank initialisieren
    sys.path.insert(0, str(SCRIPT_DIR))
    from db import init_db, log_collection

    conn = init_db()
    print(f"[{timestamp}] Sammlung gestartet, {len(names)} Quellen für Datum={today}",
          file=sys.stderr)

    results = []
    for name in names:
        filepath = available[name]
        print(f"  Sammle {name}...", file=sys.stderr, end="")

        try:
            mod = import_collector(name, filepath)
            result = mod.collect()
            status = result.get("status", "unknown")

            if status == "success":
                records = mod.write(conn, result, today)
                log_collection(conn, name, "success", records)
                print(f" OK ({records} Datensätze)", file=sys.stderr)
                results.append((name, "success", records))
            elif status == "skipped":
                reason = result.get("reason", "")
                log_collection(conn, name, "skipped", reason=reason)
                print(f" ÜBERSPRUNGEN ({reason})", file=sys.stderr)
                results.append((name, "skipped", 0))
            else:
                reason = result.get("reason", "")
                log_collection(conn, name, "error", reason=reason)
                print(f" FEHLER ({reason})", file=sys.stderr)
                results.append((name, "error", 0))

        except Exception as e:
            log_collection(conn, name, "exception", reason=str(e))
            print(f" EXCEPTION ({e})", file=sys.stderr)
            results.append((name, "exception", 0))

    conn.close()

    # Zusammenfassung
    successes = sum(1 for _, s, _ in results if s == "success")
    total_records = sum(r for _, _, r in results)
    skipped = sum(1 for _, s, _ in results if s == "skipped")
    errors = sum(1 for _, s, _ in results if s in ("error", "exception"))

    summary = (f"[{timestamp}] Fertig: {successes} erfolgreich, "
               f"{skipped} übersprungen, {errors} Fehler, {total_records} Datensätze gesamt")
    print(summary, file=sys.stderr)
    print(summary)

    # Nach der Sammlung: Kennzahlen neu erzeugen
    if successes > 0:
        try:
            from generate_metrics import main as regen
            regen()
            print(f"[{timestamp}] Kennzahlen neu erzeugt", file=sys.stderr)
        except Exception as e:
            print(f"[{timestamp}] Warnung: Kennzahlen-Regeneration fehlgeschlagen: {e}", file=sys.stderr)

    sys.exit(0 if successes > 0 else 1)


if __name__ == "__main__":
    main()

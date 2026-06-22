"""
Supabase-Setup: Bestehende Produktdaten einmalig hochladen.

Einmalig ausführen nachdem die Tabellen in Supabase angelegt sind:
  python scripts/setup_supabase.py
"""

import csv
import os
from pathlib import Path
from dotenv import load_dotenv

WORKSPACE = Path(__file__).resolve().parent.parent
load_dotenv(WORKSPACE / ".env")

from supabase import create_client


def main():
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")
    if not url or not key:
        print("FEHLER: SUPABASE_URL oder SUPABASE_KEY fehlt in .env")
        return

    client = create_client(url, key)

    # Produkte aus waren.csv hochladen
    waren_pfad = WORKSPACE / "waren.csv"
    if waren_pfad.exists():
        print("Lade Produkte hoch...")
        with open(waren_pfad, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            ok = 0
            for row in reader:
                preis = float(row["verkaufspreis"]) if row.get("verkaufspreis") else None
                try:
                    client.table("produkte").upsert({
                        "kategorie":     row["kategorie"],
                        "name":          row["produkt"],
                        "einheit":       row["einheit"],
                        "bestand":       float(row.get("bestand") or 0),
                        "mindestbestand": float(row.get("mindestbestand") or 0),
                        "preis":         preis,
                        "notiz":         row.get("notiz", "")
                    }, on_conflict="name").execute()
                    print(f"  ✅ {row['produkt']}")
                    ok += 1
                except Exception as e:
                    print(f"  FEHLER  {row['produkt']}: {e}")
        print(f"\n{ok} Produkte hochgeladen.")
    else:
        print("waren.csv nicht gefunden — übersprungen.")

    print("\nSetup abgeschlossen. Daten sind jetzt in Supabase.")
    print("Bot starten: python scripts/stimme.py")


if __name__ == "__main__":
    main()

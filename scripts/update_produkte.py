"""
Produktliste in Supabase aktualisieren.
Einmalig ausführen: python scripts/update_produkte.py
"""

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")
from supabase import create_client

client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

PRODUKTE = [
    # Met
    {"kategorie": "Met", "name": "Met 0.5L",             "einheit": "Flasche", "preis": 9.50,  "bestand": 40},
    {"kategorie": "Met", "name": "Met 0.35L",            "einheit": "Flasche", "preis": 10.00, "bestand": 0},
    {"kategorie": "Met", "name": "Met-Apfel 0.5L",       "einheit": "Flasche", "preis": 11.00, "bestand": 0},
    {"kategorie": "Met", "name": "Met-Apfel 0.35L",      "einheit": "Flasche", "preis": 10.50, "bestand": 0},
    {"kategorie": "Met", "name": "Met-Zimt 0.5L",        "einheit": "Flasche", "preis": 11.00, "bestand": 0},
    {"kategorie": "Met", "name": "Met-Zimt 0.35L",       "einheit": "Flasche", "preis": 10.50, "bestand": 0},
    {"kategorie": "Met", "name": "Met-Apfel-Zimt 0.5L",  "einheit": "Flasche", "preis": 11.00, "bestand": 0},
    {"kategorie": "Met", "name": "Met-Apfel-Zimt 0.35L", "einheit": "Flasche", "preis": 10.50, "bestand": 0},
    # Gemüse
    {"kategorie": "Gemüse", "name": "Salat",       "einheit": "Stück", "preis": None, "bestand": 0},
    {"kategorie": "Gemüse", "name": "Tomaten",     "einheit": "kg",    "preis": None, "bestand": 0},
    {"kategorie": "Gemüse", "name": "Radieschen",  "einheit": "Bund",  "preis": None, "bestand": 0},
    {"kategorie": "Gemüse", "name": "Kartoffeln",  "einheit": "kg",    "preis": None, "bestand": 0},
    {"kategorie": "Gemüse", "name": "Zwiebeln",    "einheit": "kg",    "preis": None, "bestand": 0},
    {"kategorie": "Gemüse", "name": "Knoblauch",   "einheit": "Stück", "preis": None, "bestand": 0},
    {"kategorie": "Gemüse", "name": "Rote Rüben",  "einheit": "kg",    "preis": None, "bestand": 0},
    {"kategorie": "Gemüse", "name": "Kohlrabi",    "einheit": "Stück", "preis": None, "bestand": 0},
    {"kategorie": "Gemüse", "name": "Rotkraut",    "einheit": "Stück", "preis": None, "bestand": 0},
    {"kategorie": "Gemüse", "name": "Weißkraut",   "einheit": "Stück", "preis": None, "bestand": 0},
    {"kategorie": "Gemüse", "name": "Zucchini",    "einheit": "kg",    "preis": None, "bestand": 0},
    # Obstbau
    {"kategorie": "Obstbau", "name": "Äpfel",      "einheit": "kg", "preis": None, "bestand": 0},
    {"kategorie": "Obstbau", "name": "Birnen",     "einheit": "kg", "preis": None, "bestand": 0},
    {"kategorie": "Obstbau", "name": "Kirschen",   "einheit": "kg", "preis": None, "bestand": 0},
    {"kategorie": "Obstbau", "name": "Erdbeeren",  "einheit": "kg", "preis": None, "bestand": 0},
    {"kategorie": "Obstbau", "name": "Himbeeren",  "einheit": "kg", "preis": None, "bestand": 0},
]

# Alte Produkte die nicht mehr im Sortiment sind
ZU_LOESCHEN = ["Met 0.75L", "Apfelsaft 0.5L", "Birnensaft 0.5L", "Gemischter Fruchtsaft 0.5L",
                "Wildschwein (Frischfleisch)", "Wildschwein (Vakuum)", "Reh (Frischfleisch)",
                "Reh (Vakuum)", "Paprika", "Gemüsekorb gemischt"]

print("Aktualisiere Produktliste...")

# Neue Produkte eintragen
ok = 0
for p in PRODUKTE:
    try:
        # Prüfe ob schon vorhanden (um Bestand nicht zu überschreiben)
        existing = client.table("produkte").select("bestand").eq("name", p["name"]).execute().data
        if existing:
            # Nur Preis und Kategorie aktualisieren, Bestand behalten
            client.table("produkte").update({
                "kategorie": p["kategorie"],
                "einheit":   p["einheit"],
                "preis":     p["preis"],
            }).eq("name", p["name"]).execute()
        else:
            client.table("produkte").insert(p).execute()
        print(f"  OK  {p['name']}")
        ok += 1
    except Exception as e:
        print(f"  FEHLER  {p['name']}: {e}")

# Alte entfernen
print("\nEntferne alte Produkte...")
for name in ZU_LOESCHEN:
    try:
        client.table("produkte").delete().eq("name", name).execute()
        print(f"  Entfernt: {name}")
    except Exception as e:
        print(f"  FEHLER beim Entfernen {name}: {e}")

print(f"\nFertig. {ok}/{len(PRODUKTE)} Produkte aktualisiert.")

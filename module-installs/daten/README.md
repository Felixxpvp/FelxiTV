# Daten — Das Gehirn, Teil 2

Dieses Modul verbindet dein CEO-GPT mit echten Zahlen aus deinen Excel-Dateien.

**Was es tut:**
- Legt `scripts/produktion.xlsx` an (Met, Gemüse, Obst, Jagd & Fleisch)
- Legt `scripts/finanzen.xlsx` an (Einnahmen und Ausgaben nach Sparte)
- Erstellt `scripts/update_daten.py` — liest die Excel-Dateien und aktualisiert `context/current-data.md`

**Wie du es nutzt:**
1. Trag deine echten Zahlen in die Excel-Dateien ein (in `scripts/`)
2. Ruf im CEO-GPT auf: `python scripts/update_daten.py`
3. Dein Mitarbeiter hat dann immer aktuelle Zahlen beim `/prime`

**Voraussetzungen:** Absicherung + Kontext müssen eingerichtet sein.

**Danach:** `/install module-installs/intelligenz`

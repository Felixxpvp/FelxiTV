# Prime

> Lies den Kontext und mach dich für die Sitzung bereit.

## Was du tust

1. Lies `CLAUDE.md` vollständig
2. Lies alle Dateien in `context/` durch
3. Lies `context/group/key-metrics.md` — aktuelle Geschäftszahlen (automatisch aus der Datenbank)
4. Lies `HISTORY.md` — CEO-GPT-Logbuch (was wurde gebaut, wann)
5. Lies `docs/_index.md` — Doku-Routing-Index (wo die Dokus liegen)
6. Wenn `context/import/` Dateien enthält, schau auch dort rein

**On-Demand** (nur laden wenn eine Aufgabe es braucht):
- `reference/data-access.md` — Tabellen-Schemas und SQL-Beispiele für direkte Datenbank-Abfragen

## Zusammenfassung an den Geschäftsführer

Wenn du fertig gelesen hast, fass kurz zusammen:

1. **Wer er ist und was sein Business macht.** Ein bis zwei Sätze. Zeig, dass du das Bild hast.
2. **Seine Rolle.** Wofür er verantwortlich ist und wo seine Zeit hingeht.
3. **Aktuelle Prioritäten.** Was diese Wochen oder dieses Quartal zählt.
4. **Daten-Stand.** Einnahmen, Ausgaben, Met-Produktion und Verkauf aus `key-metrics.md`. Wenn Daten älter als 2 Tage sind, darauf hinweisen.
5. **Verfügbare Befehle.** Welche Slash-Befehle in `.claude/commands/` liegen.
6. **Bereit.** Bestätige knapp, dass du im Bild bist und auf Anweisungen wartest.

Für tiefere Daten-Analysen: `data/data.db` kann direkt per SQL abgefragt werden. `reference/data-access.md` laden für Schemas und Beispiele.

## Verhalten

- Keine Fachsprache. Normales Deutsch.
- Knapp, nicht überfrachtet. Der Geschäftsführer will einen Überblick, kein Protokoll.
- Wenn `context/` noch leer oder dünn ist, sag das ehrlich. Empfiehl `/install module-installs/kontext`, damit das Gehirn deines Mitarbeiters einen echten Stand bekommt.
- Wenn etwas in den Kontext-Dateien widersprüchlich oder veraltet wirkt, weis darauf hin. Nicht überstimmen, sondern fragen.

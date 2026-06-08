# Integration: [Name]

> Ein Satz dazu, was diese Integration anbindet.

## Überblick

Welcher externe Dienst angebunden ist, welche Daten gesammelt werden, wie oft das läuft.

## Wichtige Dateien

| Datei | Zweck |
|---|---|
| `pfad/zum/collector` | Sammelt Daten von der API |
| `pfad/zum/writer` | Schreibt Daten in die Datenbank |

## Datentabellen

| Tabelle | Schlüssel-Spalten | Beschreibung |
|---|---|---|
| `example_daily` | date, metric_name, value | Tagesstands |

## Wie es läuft

1. Authentifizierung (API Key, OAuth oder ähnlich)
2. Welche Daten geholt werden
3. Wie sie transformiert werden
4. Wo sie landen

## Wichtige Abfragen

```sql
-- Die Kern-Abfrage für diese Daten
SELECT * FROM example_daily
WHERE date >= date('now', '-30 days')
ORDER BY date DESC;
```

## Konfiguration

| Variable | Zweck | Wo bekommt man die |
|---|---|---|
| `SERVICE_API_KEY` | API-Authentifizierung | https://example.com/settings/api |

## Stolpersteine

- Bekanntes Problem und wie man es behandelt
- Edge Case, auf den man achten muss
- Rate Limits oder Kontingent-Grenzen

## Historie

| Datum | Änderung |
|---|---|
| YYYY-MM-DD | Erste Doku |

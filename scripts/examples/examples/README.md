# Beispiel-Sammler

Diese Dateien sind Referenz-Implementierungen für gängige Datenquellen.
Während der Installation liest dein Mitarbeiter sie als Muster und macht eins von dreien:

1. **Direkt kopieren** nach `scripts/collect_NAME.py`, wenn die Quelle eins zu eins passt
2. **Anpassen** an dein konkretes Setup (eigene Spalten, andere Kennzahlen)
3. **Neu bauen** für Quellen, die hier nicht liegen, nach dem gleichen Muster

## Verfügbare Beispiele

| Datei | Quelle | Zugangsdaten | Was sie holt |
|-------|--------|--------------|--------------|
| `youtube.py` | YouTube Data API v3 | API-Key (gratis) | Channel-Stats, Video-Performance |
| `stripe.py` | Stripe API | API-Key (gratis) | Umsatz, MRR, Abos, Kündigungsrate |
| `google_analytics.py` | Google Analytics Data API | Service Account | Webseiten-Traffic, Quellen |
| `google_sheets.py` | Google Sheets API | Service Account | Beliebige Tabellen-Daten |
| `bitly.py` | Bitly API v4 | API-Key (gratis) | Link-Klicks, Content-Attribution |

## Das Sammler-Muster

Jeder Sammler stellt drei Sachen bereit:

```python
def collect():
    """Daten von der Schnittstelle holen. Gibt {source, status, data} zurück."""
    ...

def write(conn, result, date):
    """In die Datenbank schreiben. Legt Tabelle bei Bedarf an. Gibt Anzahl zurück."""
    ...

if __name__ == "__main__":
    """Schneller Test, lässt den Sammler einzeln laufen."""
    ...
```

Der Orchestrator (`collect.py`) findet jede `collect_*.py` Datei im scripts-Ordner
automatisch und startet sie. Eine neue Quelle dazunehmen heißt einfach, eine neue Datei
nach diesem Muster anzulegen.

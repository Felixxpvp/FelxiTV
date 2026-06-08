# Daten

> Dein Mitarbeiter sieht deine Zahlen. Eine lokale Datenbank, frisch jeden Morgen, ein Ort statt zehn Dashboards.

| Feld | Wert |
|---|---|
| Modul | `daten` |
| Version | v1 |
| Status | RELEASED |
| Released | 2026-02-27 |
| Voraussetzung | `kontext` installiert |
| Setup-Zeit | 30 bis 60 Minuten |
| Laufende Kosten | kostenlos |

## Was hier passiert

- **Geführter Workshop.** Dein Mitarbeiter geht mit dir durch, wo deine Zahlen heute liegen, und schlägt vor, was angebunden wird. Stripe, Excel-Dateien, Google Sheets, deine Webseite, YouTube, Social Media. Was du eben nutzt.
- **Eigene Anbindungen pro Quelle.** Pro Tool ein kleines Skript, das jeden Tag automatisch die frischen Zahlen zieht.
- **Eine lokale SQLite-Datenbank.** Alle Zahlen landen in einer Datei auf deinem Rechner. Nichts geht in die Cloud, alles bleibt bei dir.
- **Tagesstände.** Du baust dir mit der Zeit eine Historie auf. Diese Woche gegen letzte, dieser Monat gegen den davor.
- **Eine `key-metrics.md`-Datei**, die dein Mitarbeiter bei jeder Sitzung liest. Er kennt deine Zahlen, bevor du den ersten Satz tippst.
- **Automatischer Lauf.** Du legst fest wann das passieren soll, zum Beispiel jeden Morgen um 6 Uhr. Während du frühstückst, sind die Zahlen schon da.

## Was du brauchst

- Einen Computer (Mac oder Linux)
- Claude Code installiert
- `kontext` schon eingerichtet
- Zugang zu den Tools, die du anbinden willst (Stripe, Excel-Dateien, Google Sheets, deine Webseite, YouTube, was eben relevant ist)

## Installation

1. Der `daten` Ordner liegt schon in `module-installs/`
2. Führe `/install module-installs/daten` aus
3. Mach den Workshop mit deinem Mitarbeiter mit, fang mit deiner zentralsten Quelle an

**Geschätzte Setup-Zeit:** 30 bis 60 Minuten, je nachdem wie viele Quellen du anbindest

**Tipp:** Mach dir keinen Kopf. Fang mit EINER Quelle an, der zentralsten für dein Business. Weitere packst du später jederzeit dazu, das Ganze ist genau für diesen schrittweisen Aufbau gebaut.

## Kosten

Kostenlos. Alle hier genutzten Schnittstellen haben kostenlose Kontingente, die für eine tägliche Sammlung locker reichen.

## Was hier drin liegt

| Datei | Zweck |
|---|---|
| `INSTALL.md` | Geführter Workshop und Setup (liest dein Mitarbeiter) |
| `README.md` | Diese Datei, der Überblick für dich |
| `scripts/db.py` | Datenbank-Grundlage |
| `scripts/config.py` | Lädt deine API-Keys aus `.env` |
| `scripts/collect.py` | Orchestrator, findet alle Sammler automatisch |
| `scripts/generate_metrics.py` | Erzeugt die `key-metrics.md` aus der Datenbank |
| `scripts/collect_fx_rates.py` | Starter-Sammler ohne API-Key, beweist dass die Pipeline läuft |
| `scripts/examples/*.py` | Referenz-Sammler für YouTube, Stripe, Google Analytics, Google Sheets, Bitly |
| `scripts/requirements.txt` | Python-Pakete |
| `config/com.ceogpt.daten-collect.plist` | macOS-Zeitplan-Vorlage |

## Quellen, die du typischerweise anbindest

| Quelle | Was du danach im Blick hast |
|---|---|
| Stripe | Umsatz, MRR, Abos, Kündigungsrate |
| Excel-Dateien oder Google Sheets | P&L, Marketing-KPIs, eigene Listen |
| Deine Webseite | Sitzungen, Nutzer, Traffic-Quellen |
| YouTube | Abonnenten, Aufrufe, Video-Performance |
| Social Media | Reichweite, Follower, Engagement |
| Eigenes Tool | Alles mit API, dein Mitarbeiter baut den Sammler |

## Wie das mit dem Gehirn zusammenhängt

`kontext` hat deinem Mitarbeiter dein Business erklärt. Mit `daten` kommt der zweite Schritt: Er sieht jetzt auch deine Zahlen. Wenn du in der nächsten Sitzung `/prime` läufst, weiß er nicht nur was du machst, sondern auch wie das Business gerade läuft.

## Pro-Tipp

Lass es eine Woche laufen. Der Wert von Tagesständen kommt aus der Historie. Nach sieben Tagen siehst du erste Trends, nach 30 Tagen wird der Monatsvergleich richtig nützlich.

## Nach diesem Modul

Dein Mitarbeiter sieht deine Zahlen jetzt jeden Morgen. Im nächsten Schritt hört er bei deinen Meetings mit und liest deine Team-Chats mit `/install module-installs/intelligenz`, damit er alles nachschlagen kann.

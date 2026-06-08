# Absicherung

> Jede Änderung wird mitgeschrieben, in der Cloud gesichert und dokumentiert. Geht der Laptop kaputt, lädst du dir alles zurück und machst weiter.

| Feld | Wert |
|---|---|
| Modul | `absicherung` |
| Version | v1 |
| Status | RELEASED |
| Released | 2026-02-27 |
| Voraussetzung | keine (der erste Schritt) |
| Setup-Zeit | 20 bis 30 Minuten |
| Laufende Kosten | kostenlos |

## Was hier passiert

- **Automatische Sicherung im Hintergrund.** Jede Änderung an deinem CEO-GPT wird mitgeschrieben. Falscher Schritt? Du gehst zurück. Frage was war letzte Woche? Du schaust nach.
- **Backup im Internet.** Dein kompletter CEO-GPT liegt sicher bei GitHub. Laptop kaputt, gestohlen, im See? Du lädst dir alles auf das nächste Gerät und arbeitest weiter.
- **Ein `/commit` Befehl.** Speichert deine Arbeit, hält die Doku aktuell und schreibt das Logbuch fort, alles in einem Schritt. Den nutzt du am Ende jeder Session.
- **HISTORY.md als Logbuch.** Ein laufendes Protokoll von allem, was du gebaut hast. Dein CEO-GPT bekommt ein Gedächtnis.
- **`docs/` als Doku-Ordner.** Wenn dein Mitarbeiter Systeme baut, legt er passende technische Dokus an und pflegt sie. Künftige Sessions lesen nach, statt zu raten.
- **Schutz vor Leaks.** Eine `.gitignore` und das `.env` Muster sorgen dafür, dass deine API Keys nicht versehentlich im Netz landen.

## Was du brauchst

- Einen Computer (Mac, Linux, Windows)
- Claude Code installiert und laufend
- Einen GitHub Account (kostenlos, wir legen einen an, falls du keinen hast)

## Installation

1. Der `absicherung` Ordner liegt schon in `module-installs/`
2. Führe `/install module-installs/absicherung` aus
3. Folge der Anleitung, dein Mitarbeiter führt dich durch

**Geschätzte Setup-Zeit:** 20 bis 30 Minuten

## Kosten

Kostenlos. Git läuft lokal, private Repositories bei GitHub kosten nichts.

## Was hier drin liegt

| Datei | Zweck |
|---|---|
| `INSTALL.md` | Geführte Installation (liest dein Mitarbeiter) |
| `README.md` | Diese Datei, der Überblick für dich |
| `commands/commit.md` | Der `/commit` Befehl, speichert, dokumentiert und schreibt das Logbuch fort |
| `templates/history.md` | Vorlage für die HISTORY.md |
| `templates/docs-index.md` | Vorlage für den Doku-Index in `docs/_index.md` |
| `templates/doc-system-template.md` | Vorlage für System-Dokus |
| `templates/doc-integration-template.md` | Vorlage für Integrations-Dokus |
| `templates/gitignore` | Sichere Defaults für die `.gitignore` |
| `templates/env-example` | Vorlage für die `.env.example` |

## Pro-Tipp

Pack `/commit` am Ende jeder Session ans Ende deines Ablaufs. Drei Buchstaben, und deine Arbeit ist gespeichert, dokumentiert und in der Cloud. Geht der Laptop morgen kaputt, bist du in zehn Minuten auf einem neuen Gerät wieder am Start.

## Nach diesem Modul

Die Basis steht. Im nächsten Schritt baust du das Gehirn mit `/install module-installs/kontext`.

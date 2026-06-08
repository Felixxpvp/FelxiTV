# Plan

Erstellt einen detaillierten Plan für eine Änderung am CEO-GPT. Pläne sind durchdachte Dokumente, die Kontext, Begründung und Schritt-für-Schritt-Aufgaben festhalten, damit die Umsetzung sauber läuft.

## Variablen

anfrage: $ARGUMENTS (beschreib, was du planen willst: neuer Befehl, neuer Ablauf, struktureller Umbau, Vorlagen-Update, etc.)

---

## Anleitung

- **Wichtig:** Du erstellst einen PLAN, du setzt nichts um. Recherchier gründlich, denk tief, schreib dann ein durchdachtes Plan-Dokument.
- Nutz dein Köpfchen. Denk über die Anfrage, die CEO-GPT-Struktur und den besten Ansatz nach.
- Schau dir das CEO-GPT an, um bestehende Muster, Konventionen und Anknüpfungspunkte zu verstehen.
- Leg den Plan in `plans/` ab, mit Dateinamen `YYYY-MM-DD-{beschreibender-name}.md`
  - Heutiges Datum
  - `{beschreibender-name}` als kurzen kebab-case-Namen ersetzen (z.B. "wettbewerbsanalyse-befehl", "outputs-umstrukturieren")
- Füll jeden Abschnitt der Plan-Vorlage unten. Ersetz alle `<platzhalter>` mit konkretem, umsetzbarem Inhalt.
- Sei gründlich. Der Plan wird mit `/implement` ausgeführt und muss genug Detail haben, dass das ohne Rückfragen klappt.
- Halt dich an bestehende Muster. Schau dir ähnliche Dateien im CEO-GPT an, bevor du neue Strukturen vorschlägst.

---

## Recherche-Phase

Bevor du den Plan schreibst, schau dir an:

1. **Kern-Referenzen lesen:**
   - `CLAUDE.md`: CEO-GPT-Überblick
   - `context/`: Hintergrund zum Geschäftsführer und Business

2. **Relevante Bereiche durchgehen:**
   - Neuer Befehl? Lies bestehende Befehle in `.claude/commands/`
   - Outputs anpassen? Schau dir die `outputs/`-Struktur an
   - Vorlagen aktualisieren? Prüf `reference/` auf bestehende Muster
   - Skripte hinzufügen? Schau in `scripts/` für Konventionen

3. **Verbindungen verstehen:**
   - Wie hängt die Änderung mit bestehenden Abläufen zusammen?
   - Welche Dateien verweisen auf Bereiche, die geändert werden?
   - Welche Namenskonventionen gelten?

---

## Plan-Format

Schreib den Plan in genau dieser Struktur:

```markdown
# Plan: <beschreibender Titel>

**Erstellt:** <YYYY-MM-DD>
**Status:** Entwurf
**Anfrage:** <Ein-Satz-Zusammenfassung>

---

## Überblick

### Was dieser Plan erreicht

<2-3 Sätze, die das Endergebnis beschreiben und warum es zählt>

### Warum das zählt

<Verbind die Änderung mit den Zielen des Geschäfts. Welcher Wert kommt rein?>

---

## Aktueller Stand

### Bestehende relevante Struktur

<Dateien, Ordner oder Muster, die existieren und mit der Änderung zusammenhängen>

### Lücken oder Probleme, die der Plan löst

<Was fehlt, ist kaputt oder unrund?>

---

## Geplante Änderungen

### Zusammenfassung der Änderungen

<Bulletpoint-Liste auf hoher Ebene>

### Neue Dateien

| Pfad | Zweck |
|---|---|
| `pfad/zu/datei.md` | Beschreibung |

### Geänderte Dateien

| Pfad | Änderungen |
|---|---|
| `pfad/zu/datei.md` | Beschreibung |

### Gelöschte Dateien (falls vorhanden)

<Liste, mit Begründung>

---

## Design-Entscheidungen

### Wichtige Entscheidungen

1. **<Entscheidung>**: <Begründung>
2. **<Entscheidung>**: <Begründung>

### Verworfene Alternativen

<Welche anderen Wege wurden geprüft und warum verworfen?>

### Offene Fragen (falls vorhanden)

<Welche Entscheidungen brauchen noch Input vom Geschäftsführer?>

---

## Schritt-für-Schritt-Aufgaben

In dieser Reihenfolge ausführen.

### <Titel>

<Detaillierte Beschreibung>

**Aktionen:**
- <konkrete Aktion>
- <konkrete Aktion>

**Betroffene Dateien:**
- `pfad/zu/datei.md`

---

### <Titel>

<Detaillierte Beschreibung>

**Aktionen:**
- <konkrete Aktion>

**Betroffene Dateien:**
- `pfad/zu/datei.md`

---

<So viele Schritte wie nötig. Gründlich. Enthält:>
<- Neue Dateien anlegen (mit vollständiger Inhalts-Spezifikation)>
<- Bestehende Dateien ändern (mit Vorher/Nachher oder genauen Edits)>
<- Querverweise aktualisieren>
<- Test- und Prüf-Schritte>

---

## Verbindungen und Abhängigkeiten

### Dateien, die auf diesen Bereich verweisen

<Wer hängt mit dran?>

### Updates für Konsistenz

<Welche Doku, Verweise oder verwandte Dateien müssen mit?>

### Auswirkung auf bestehende Abläufe

<Wie verändert sich der Workflow für bestehende Befehle, Outputs oder Prozesse?>

---

## Prüf-Checkliste

So prüfst du, dass die Umsetzung sauber ist:

- [ ] <Prüf-Schritt, z.B. "Neuer Befehl läuft ohne Fehler">
- [ ] <Prüf-Schritt, z.B. "Output-Dateien am richtigen Platz">
- [ ] <Prüf-Schritt, z.B. "CLAUDE.md spiegelt die neue Struktur">
- [ ] <Prüf-Schritt, z.B. "Querverweise stimmen">

---

## Erfolgskriterien

Die Umsetzung ist fertig, wenn:

1. <konkretes, messbares Kriterium>
2. <konkretes, messbares Kriterium>
3. <konkretes, messbares Kriterium>

---

## Notizen

<Zusätzlicher Kontext, spätere Überlegungen oder verwandte Ideen>
```

---

## Qualitäts-Standards

- **Vollständig:** Jeder Abschnitt mit konkretem Inhalt, keine leeren Platzhalter
- **Umsetzbar:** Die Schritte sind so detailliert, dass `/implement` ohne Rückfragen ausführen kann
- **Konsistent:** Folgt bestehenden CEO-GPT-Mustern und Namenskonventionen
- **Klar:** Jemand, der das Projekt nicht kennt, könnte den Plan lesen und ausführen
- **Nachvollziehbar:** Änderungen sind mit Zielen und Begründung verbunden

---

## Bericht

Nachdem du den Plan geschrieben hast:

1. Knappe Zusammenfassung, was der Plan abdeckt
2. Offene Fragen, die noch Input brauchen, bevor umgesetzt werden kann
3. Vollständiger Pfad zur Plan-Datei: `plans/YYYY-MM-DD-{name}.md`
4. Hinweis an den Geschäftsführer, `/implement plans/YYYY-MM-DD-{name}.md` zu laufen, um auszuführen

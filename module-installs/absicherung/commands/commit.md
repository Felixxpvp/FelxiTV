# Commit

> Arbeit speichern, Doku aktualisieren, Logbuch fortschreiben, alles in einem Befehl.

## Variablen

message: $ARGUMENTS (optional, überschreibt die Commit-Message, oder leer lassen für eine automatisch generierte)

---

## Anleitung

Du committest Änderungen am CEO-GPT. Dieser Befehl macht drei Dinge:
1. Legt einen sauberen Git-Commit mit strukturierter Message an
2. Prüft, ob technische Dokus angelegt oder aktualisiert werden müssen
3. Aktualisiert HISTORY.md mit dem, was passiert ist

Geh genau so vor.

### Verstehen, was sich geändert hat

Lass `git diff HEAD` laufen, um alle Änderungen zu sehen (gestaged und nicht gestaged). Auch `git status` für untracked Dateien.

Schau dir die Änderungen an und versteh, was passiert ist. Fass es im Kopf zusammen, du brauchst das für die Commit-Message, den Doku-Check und das Logbuch.

### Änderungen stagen

Stage die relevanten Dateien. Bevorzug einzelne Dateien beim Namen statt `git add -A`, damit nicht versehentlich sensible Dateien mitcommittet werden.

**Niemals stagen:**
- `.env` oder andere Credential-Dateien
- `data/*.db` oder `data/*.db-*` (Datenbank-Dateien)
- `__pycache__/` oder `.venv/`
- Jede Datei, die in der gitignore stehen sollte

Im Zweifel frag den Member: "Ich stage gleich diese Dateien: {Liste}. Passt?"

### Commit-Message generieren

Wenn `$ARGUMENTS` gesetzt ist, nutz das als Commit-Message.

Wenn keine Message vorgegeben ist, generier eine in diesem Format:

```
<typ>: <beschreibung>
```

**Typen:**
- `feat`: Neues Feature, Befehl oder Capability
- `update`: Erweiterung eines bestehenden Features oder Content-Update
- `fix`: Bug-Fix oder Korrektur
- `data`: Daten-Sammlung, Backfill oder Schema-Änderung
- `context`: Strategie-, Projekt- oder Geschäfts-Kontext-Update
- `docs`: Doku-Änderungen
- `refactor`: Code umgestaltet, Verhalten unverändert
- `chore`: Pflege, Dependencies, Config

**Regeln:**
- Verben im Präsens (add, fix, update, NICHT added, fixed, updated)
- Erste Zeile maximal 50 Zeichen
- Kein Punkt am Ende
- Konkret benennen, was sich geändert hat

**Beispiele:**
- `feat: Daten-Pipeline für Stripe hinzugefügt`
- `update: Geschäfts-Strategie für Q2 umstrukturiert`
- `fix: Umsatz-Berechnung im Dashboard korrigiert`
- `docs: Daten-Pipeline System-Doku aktualisiert`

Wenn der Commit Änderungen über mehrere Bereiche umfasst, nimm den passendsten Typ und fass zusammen. Häng einen Body mit Bullet Points für Details an.

### Committen

Lass den Commit laufen:

```bash
git commit -m "$(cat <<'EOF'
<commit message hier>
EOF
)"
```

Lass `git status` danach laufen, um den Erfolg zu prüfen.

### Doku-Check

**Bei `fix`, `chore`, `refactor` und `docs` Commits diesen Schritt komplett überspringen.**

Für `feat` und `update` Commits, die System-Dateien anfassen (`scripts/`, `apps/`, `.claude/commands/`, `.claude/skills/`):

1. **Lies `docs/_index.md`**, um zu sehen, welche Systeme dokumentiert sind und welche nicht
2. **Beurteil die Änderungen:**
   - Wurde ein NEUES System angelegt, ohne Doku? Leg eine an.
   - Wurde ein bestehendes dokumentiertes System deutlich geändert? Aktualisier die Doku.
   - Nur kleine Anpassungen innerhalb eines Systems? Überspringen.
3. **Wenn du eine neue Doku anlegst:**
   - Nimm die Vorlage aus `docs/_templates/doc-system-template.md` oder `docs/_templates/doc-integration-template.md`
   - Ziel 60 bis 120 Zeilen, schlank genug zum Laden, detailliert genug für eine künftige Session
   - Trag sie in `docs/_index.md` ein mit Bedingung (wann diese Doku laden), Pfad und einer Zeile Zusammenfassung
4. **Wenn du eine bestehende Doku aktualisierst:**
   - Lies die aktuelle Doku
   - Aktualisier die geänderten Abschnitte
   - Trag einen datierten Eintrag in die History-Tabelle unten ein
5. **Wenn Dokus angelegt oder aktualisiert wurden,** stage und committ sie:
   ```
   docs: Doku für {Systemname} aktualisiert
   ```

Sag dem Member, was du gemacht hast: "Ich hab die Doku für {System} aktualisiert, weil {Grund}." oder "Keine Doku-Updates nötig, die Änderungen waren klein."

### HISTORY.md aktualisieren

**Bei `feat` und `update` Commits:**

Häng einen Eintrag an HISTORY.md unter dem heutigen Datum an. Wenn der heutige Abschnitt schon existiert, ergänze ihn. Wenn nicht, leg einen neuen Abschnitt oben an.

Format:
```markdown
## YYYY-MM-DD

### [Kurzer Titel]

- Was gemacht wurde (Bullet Points)
- Welche Dateien angefasst wurden
```

Halt es knapp, 2 bis 5 Bullet Points. Fokus auf WAS gebaut wurde und WARUM, nicht WIE.

Stage und committ:
```
docs: changelog aktualisiert
```

**Bei `fix`, `context`, `data` Commits:** HISTORY.md nur aktualisieren, wenn die Änderung relevant ist. Kleine Fixes brauchen keinen Logbuch-Eintrag.

**Bei `chore`, `refactor` Commits:** HISTORY.md überspringen.

### Push vorschlagen

Wenn alles committet ist, schlag den Push vor:

"Alles committet. Soll ich zu GitHub pushen? (Das sichert deine Arbeit in der Cloud.)"

Wenn ja:
```bash
git push
```

Wenn nein, alles gut, der Member kann später pushen.

### Bestätigen

Bericht:
- Welche Commit-Messages verwendet wurden
- Welche Dateien committet wurden
- Ob Dokus aktualisiert wurden (und welche)
- Ob HISTORY.md aktualisiert wurde
- Aktueller Branch und Push-Status

---

## Wichtige Regeln

- **Niemals Secrets committen**: Keine `.env`, keine Credentials, keine API Keys. Warn, wenn welche gestaged sind.
- **Niemals ohne Nachfrage pushen**: Frag immer, bevor du pushst. Der Member will vielleicht noch reviewen.
- **Niemals amenden**: Neue Commits anlegen, keine Amends, außer der Member fragt explizit danach.
- **Niemals forcen**: Kein `--force`, kein `--no-verify`, keine destruktiven Git-Operationen.
- **Vor dem Commit reviewen**: Zeig immer, was committet wird, und hol Bestätigung ein, wenn die Änderungen groß sind oder sensible Bereiche berühren.
- **Doku-Updates in eigenem Commit**: Halt den Haupt-Commit sauber. Doku kommt in einen Folge-Commit.

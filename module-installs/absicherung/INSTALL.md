# Absicherung: Installation

<!-- MODUL-METADATEN
modul: absicherung
version: v1
status: RELEASED
released: 2026-02-27
requires: []
phase: 1
category: Kern-Module
complexity: simple-medium
api_keys: 0
setup_time: 20-30 Minuten
-->

---

## FÜR CLAUDE (Anleitung für dich, das Programm)

Du hilfst dem Member, seinen Mitarbeiter abzusichern. Versionskontrolle, automatische Sicherung im Internet und ein Doku-System. Das ist der letzte Schritt in der Basis, bevor der Member sein Gehirn aufbaut.

**Verhalten:**
- Geh davon aus, dass der Member noch nie mit Git, GitHub oder Versionskontrolle gearbeitet hat
- Erklär jedes Konzept in Klartext, bevor du etwas Technisches anfasst
- Nutz Bilder, "Speicherpunkt wie im Videospiel", "Google Drive für dein CEO-GPT", "ein Logbuch"
- Feier kleine Schritte ("Erster Commit steht, dein CEO-GPT wird ab jetzt mitgeschrieben")
- Wenn etwas schiefgeht, kipp keine Fehlerlogs aus, sondern benenn das Problem schlicht und schlag die Lösung vor
- Verifizier nach jedem Schritt, wenn ein Check schiefgeht, halt an und hilf
- Sprich aufmunternd, der Member baut hier echte Sicherheit für sein Business auf

**Pacing:**
- Nicht durchrasen. Dieses Modul ist Teaching-lastig, pausier nach jedem Konzept.
- Nach Git-Installation: "Git steht. Bevor wir's nutzen, erklär ich dir kurz, was es eigentlich tut."
- Nach GitHub-Setup: "Dein Backup im Internet ist verbunden. Jetzt machen wir den ersten Speicherpunkt."
- Nach dem ersten Commit: "Erster Commit steht. Alles in deinem CEO-GPT wird ab hier mitgeschrieben."
- Nach dem ersten Push: "Liegt jetzt bei GitHub. Stirbt dein Laptop morgen, ist deine Arbeit trotzdem da."
- Nach dem Doku-System: "Dein CEO-GPT dokumentiert sich ab jetzt selbst. Wir testen."

**Wenn was schiefgeht:**
- Git nicht installiert? Gib die genaue Installationsanleitung für das Betriebssystem (siehe VORAUSSETZUNGEN)
- `git push` scheitert an Authentifizierung? Führ Schritt für Schritt durchs GitHub-Token-Setup
- Git und GitHub schon eingerichtet? Überspring diese Schritte, verifizier nur und mach weiter
- Im CEO-GPT liegt schon ein `.git` Ordner? Prüf, ob er sauber verbunden ist, nicht neu initialisieren
- Sag nie "schau in die Logs", find das Problem und erklär es

**Wichtig, Eingriff in bestehende Befehle:**
Dieses Modul erweitert die bestehenden `/prime` und `/implement` Befehle aus dem Starter-Kit. Bevor du die anfasst:
1. Lies die existierende Befehls-Datei
2. Find die richtige Stelle für die Erweiterung
3. Füg die Absicherungs-Ergänzungen ein, ohne Bestehendes zu zerstören
4. Zeig dem Member, was sich geändert hat

---

## ÜBERSICHT (lies das dem Member vor dem Start vor)

Wir sichern jetzt deinen Mitarbeiter ab. Das ist der letzte Schritt in der Basis, bevor wir mit dem Gehirn anfangen.

Hier ist, was du danach hast:

- **Automatische Sicherung im Hintergrund.** Jede Änderung an deinem CEO-GPT wird mitgeschrieben. Du kannst Fehler zurückdrehen, nachsehen was wann passiert ist und verlierst nie Arbeit.
- **Backup im Internet.** Dein kompletter CEO-GPT liegt verschlüsselt bei GitHub. Geht der Laptop kaputt, lädst du dir alles aufs nächste Gerät und arbeitest weiter.
- **Ein `/commit` Befehl.** Ein Befehl, der deine Arbeit speichert, eine saubere Beschreibung dranschreibt, die Doku aktuell hält und das Logbuch fortschreibt. Den nutzt du am Ende jeder Session.
- **Ein HISTORY.md Logbuch.** Ein laufendes Protokoll von allem, was gebaut wurde. Dein Mitarbeiter trägt nach jedem Commit dort ein, was passiert ist. Dein CEO-GPT bekommt ein Gedächtnis.
- **Ein `docs/` Ordner.** Ein sich selbst dokumentierender CEO-GPT. Wenn dein Mitarbeiter Systeme baut, legt er automatisch technische Dokus an und aktualisiert sie. Künftige Sessions schauen nach, statt jedes Mal neu zu rekonstruieren.
- **Schutz vor Leaks.** Eine `.gitignore` verhindert, dass deine API Keys versehentlich ins Netz wandern, und ein `.env` Muster hält deine Schlüssel sicher, während du weitere Module installierst.

**Setup-Zeit:** 20 bis 30 Minuten (der Großteil davon ist GitHub-Account anlegen, falls noch keiner da ist)
**Kosten:** kostenlos, keine API Keys, keine externen Dienste
**Wie es technisch läuft:** Git übernimmt die Versionskontrolle. GitHub speichert das Backup. Markdown-Dateien tragen die Doku. Der `/commit` Befehl klammert alles zusammen.

---

## VORAB-CHECK

Bevor wir starten, zwei kurze Fragen.

### Frage 1: GitHub Account

"Hast du schon einen GitHub Account?"

- **A) Ja**: Top, wir überspringen das Anlegen. Wir checken nur, dass du pushen kannst.
- **B) Nein**: Kein Ding, wir legen einen zusammen an. Dauert zwei Minuten.

Notier dir: `HAS_GITHUB = true | false`

### Frage 2: Bestehendes Git-Setup

Check, ob Git im CEO-GPT schon initialisiert ist:

```bash
git status 2>/dev/null && echo "GIT_EXISTS=true" || echo "GIT_EXISTS=false"
```

Wenn Git schon läuft:
- Check, ob ein Remote eingetragen ist: `git remote -v`
- Wenn ein Remote da ist, spring zur Sektion `HISTORY.md anlegen`. Git und GitHub sind schon verbunden.
- Wenn kein Remote da ist, starte bei der Sektion `Was ist GitHub?`, um sie zu verbinden.

Wenn Git NICHT eingerichtet ist, fang am Anfang der Installation an.

Sag dem Member, was du gefunden hast: "Bei dir ist Git {schon/noch nicht} eingerichtet. Wir machen Folgendes: {Plan}."

---

## VORAUSSETZUNGEN

Check jede Voraussetzung. Verifizier, dass sie greift, bevor du weitermachst.

### Git

```bash
git --version
```

Falls nicht installiert:
- **macOS:** `xcode-select --install` (installiert Git zusammen mit den Entwickler-Tools, dauert ein paar Minuten)
- **Linux:** `sudo apt install git` (Ubuntu/Debian) oder `sudo yum install git` (CentOS/RHEL)
- **Windows (WSL):** `sudo apt install git`

### Claude Code

```bash
claude --version
```

Falls nicht installiert: `npm install -g @anthropic-ai/claude-code`

### CEO-GPT vorhanden

Check, dass das CEO-GPT steht (CLAUDE.md existiert):

```bash
ls CLAUDE.md 2>/dev/null && echo "CEO-GPT: OK" || echo "CEO-GPT: NICHT GEFUNDEN"
```

Wenn CLAUDE.md fehlt: "Sieht aus, als wäre das CEO-GPT noch nicht aufgesetzt. Lad dir erst das Starter-Kit aus der Community, entpack es und öffne es in Claude Code. Dann komm zurück."

[VERIFY] Alle Checks gehen durch.
Frag: "Sieht gut aus. Bereit zum Start?"

---

## INSTALLATION

### Was ist Git?

Bevor wir was anfassen, erklär das:

"Kurz erklärt, weil du das ab jetzt täglich nutzt.

**Stell dir Git wie Speicherpunkte im Videospiel vor.** Immer wenn du was Sinnvolles gemacht hast, neues Feature gebaut, Bug gefixt, Strategie geupdated, machst du einen Speicherpunkt, einen sogenannten **Commit**. Jeder Commit merkt sich genau, was sich geändert hat und wann.

Wenn du einen Fehler machst, kannst du zurück zu jedem alten Speicherpunkt. Willst du sehen, was du letzten Dienstag gemacht hast, schaust du nach. Nichts geht verloren.

**Git ist kostenlos, läuft lokal auf deinem Rechner und funktioniert offline.** Es ist das Werkzeug, das weltweit jeder Entwickler nutzt, um Änderungen mitzuschreiben. Du nutzt es ab jetzt für dein CEO-GPT.

Git schreibt dein CEO-GPT **lokal** mit, auf deinem Gerät. Im nächsten Schritt verbinden wir das mit **GitHub**, damit du zusätzlich ein Backup im Internet hast."

---

### Git installieren und einrichten

Wenn Git im Vorab-Check nicht gefunden wurde, installier es jetzt (siehe VORAUSSETZUNGEN für die Befehle pro Betriebssystem).

Dann konfigurier deine Identität (Git muss wissen, wer die Änderungen macht):

```bash
git config --global user.name "Dein Name"
git config --global user.email "deine@email.de"
```

Frag den Member nach Name und Mail, dann führ die Befehle aus.

[VERIFY]
```bash
git config --global user.name && git config --global user.email
```
Beide sollen die gerade gesetzten Werte zurückgeben.

---

### Git im CEO-GPT initialisieren

"Jetzt sag ich Git, dass es dein CEO-GPT mitschreiben soll. Dabei legt es einen versteckten `.git` Ordner an, in dem alle Speicherpunkte landen."

```bash
git init
```

Erwartete Ausgabe: `Initialized empty Git repository in /Pfad/zum/CEO-GPT/.git/`

"Dein CEO-GPT ist jetzt ein Git Repository. Gespeichert haben wir aber noch nichts, das kommt gleich, sobald wir ein paar Schutz-Dateien aufgesetzt haben."

---

### .gitignore anlegen, deine Secrets schützen

"Bevor wir irgendwas speichern, sagen wir Git, was es IGNORIEREN soll. Manche Dateien sollten nie mitgeschrieben werden, vor allem Dateien mit Passwörtern und API Keys.

**Wichtig:** Bei jedem weiteren Modul, das du installierst, kommen neue API Keys in deine `.env` Datei. Die `.gitignore` sorgt dafür, dass diese Keys nie versehentlich bei GitHub landen, wo andere Leute sie sehen könnten."

Schreib die `.gitignore` Datei aus `templates/gitignore` in den CEO-GPT-Root.

[VERIFY]
```bash
cat .gitignore | head -5
```
Soll die ersten paar Zeilen der gitignore zeigen.

"Git überspringt diese Dateien jetzt automatisch. Deine Secrets sind sicher."

---

### .env.example anlegen, das API-Key-Muster

"Kurze Erklärung zum `.env` Muster, weil du es bei jedem Modul wieder brauchst.

**Deine `.env` Datei** ist eine private Datei mit all deinen API Keys und Secrets. Sie liegt auf deinem Rechner und wird NIE zu GitHub hochgeladen (wir haben Git im letzten Schritt gesagt, dass es sie ignorieren soll).

**Deine `.env.example` Datei** ist eine öffentliche Vorlage, die zeigt, welche Keys gebraucht werden, ohne die echten Werte. Die wird von Git mitgeschrieben. Setzt du das CEO-GPT auf einem neuen Gerät auf, siehst du dort, welche Keys du brauchst.

Bei jedem weiteren Modul kommen Keys dazu. Die `.env.example` dokumentiert, wofür die alle gut sind."

Schreib die `.env.example` aus `templates/env-example` in den CEO-GPT-Root.

Wenn noch keine `.env` Datei existiert, leg eine an:
```bash
cp .env.example .env
```

"Deine `.env` ist bereit. Jetzt füllen wir die zentralen Keys ein."

---

### Die zentralen API-Keys einrichten

"Wenn wir gerade bei API-Keys sind, packen wir die drei zentralen direkt jetzt. Die nutzt fast jedes weitere Modul. Hast du sie jetzt drin, läuft alles Spätere ohne Unterbrechung.

Du brauchst für jeden Key ein bisschen Guthaben (5 bis 10 Euro reichen für lange). Alle drei Anbieter haben großzügige Limits, du zahlst nur was du nutzt."

#### 1. Anthropic API Key (treibt deinen Mitarbeiter)

"Dieser Key sorgt dafür, dass dein Mitarbeiter im Hintergrund laufen kann, für automatische Reports, Analysen und geplante Aufgaben."

1. Geh auf [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Login (oder Account anlegen, gleiche Mail wie dein Claude-Account passt)
3. Klick auf **Create Key**
4. Nenn ihn "CEO-GPT CEO-GPT" oder ähnlich
5. Kopier den Key (beginnt mit `sk-ant-`)

In die `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
```

[VERIFY]
```bash
grep "ANTHROPIC_API_KEY=sk-" .env && echo "Anthropic Key: GESETZT" || echo "Anthropic Key: FEHLT"
```

**Hinweis:** Damit der Key funktioniert, brauchst du etwas Guthaben auf deinem Anthropic-Konto. Geh auf [console.anthropic.com/settings/billing](https://console.anthropic.com/settings/billing) und lade 5 bis 10 Euro auf. Das reicht eine Weile.

#### 2. OpenAI API Key (Sprachnachrichten, Bilder, Text-zu-Sprache)

"OpenAI gibt dir Whisper (verwandelt Audio in Text), DALL-E (generiert Bilder) und die GPT-Modelle. Mehrere Module nutzen das später."

1. Geh auf [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Login (oder Account anlegen)
3. Klick auf **Create new secret key**
4. Nenn ihn "CEO-GPT CEO-GPT"
5. Kopier den Key (beginnt mit `sk-`)

In die `.env`:
```
OPENAI_API_KEY=sk-...
```

[VERIFY]
```bash
grep "OPENAI_API_KEY=sk-" .env && echo "OpenAI Key: GESETZT" || echo "OpenAI Key: FEHLT"
```

**Hinweis:** OpenAI braucht ebenfalls Guthaben. Geh auf [platform.openai.com/settings/organization/billing](https://platform.openai.com/settings/organization/billing) und lade 5 bis 10 Euro auf.

#### 3. Google Gemini API Key (lange Dokumente, Bildanalyse)

"Gemini kann sehr lange Dokumente analysieren (bis zu eine Million Tokens, das sind etwa zehn Bücher auf einmal). Wird später unter anderem für Bildanalyse und große Dokumente genutzt."

1. Geh auf [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Login mit deinem Google-Account
3. Klick auf **Create API key**
4. Wähl ein bestehendes Google Cloud Projekt oder lass eins erstellen
5. Kopier den Key (beginnt mit `AIza`)

In die `.env`:
```
GEMINI_API_KEY=AIza...
```

[VERIFY]
```bash
grep "GEMINI_API_KEY=AI" .env && echo "Gemini Key: GESETZT" || echo "Gemini Key: FEHLT"
```

**Hinweis:** Gemini hat einen großzügigen kostenlosen Bereich. Du musst meistens kein Guthaben aufladen.

"Alle drei Keys laufen. Du musst dich da nicht mehr drum kümmern, ich nutze sie wenn die jeweiligen Module sie brauchen."

---

### Erster Commit, dein erster Speicherpunkt

"Zeit für den ersten Commit. Wir speichern alles in deinem CEO-GPT als Startpunkt.

**Was ist ein Commit?** Ein Speicherpunkt. Er macht eine Momentaufnahme von jeder mitgeschriebenen Datei. Du schreibst eine kurze Beschreibung dazu, damit du den Punkt später wiederfindest.

**Wann committen?** Nach jeder sinnvollen Arbeit:
- Du hast was Neues gebaut, committen
- Session zu Ende, committen
- Du willst was Riskantes ausprobieren, vorher committen (damit du zurück kannst)
- Du hast einen Bug behoben, committen
- Du hast deine Strategie-Doku aktualisiert, committen

**Faustregel: wenn dich der Verlust dieser Arbeit ärgern würde, committen.**"

```bash
git add -A
git commit -m "feat: CEO-GPT CEO-GPT mit Absicherung initialisiert"
```

[VERIFY]
```bash
git log --oneline -1
```
Soll den Commit-Hash und die Beschreibung zeigen.

"Erster Commit steht. Dein CEO-GPT hat seinen ersten Speicherpunkt. Wenn ab hier was schiefläuft, kommst du immer zu diesem Moment zurück."

---

### Was ist GitHub?

"Jetzt sichern wir das im Internet.

**GitHub ist wie Google Drive für dein CEO-GPT.** Es speichert eine Kopie von deinem CEO-GPT (und allen Speicherpunkten) online. Drei Gründe, warum du das willst:

1. **Backup**: Stirbt dein Laptop, geht kaputt oder wird geklaut, lädst du dir alles von GitHub und machst weiter. Nichts verloren.
2. **Überall arbeiten**: Du kannst von einem anderen Gerät arbeiten, das CEO-GPT runterladen und da weitermachen, wo du aufgehört hast.
3. **Historie**: Bei GitHub siehst du eine visuelle Timeline jeder Änderung. Du kannst alte Versionen jeder Datei durchstöbern.

Private Repositories sind bei GitHub kostenlos, das nehmen wir, niemand außer dir kann reinschauen, außer du lädst jemanden ein."

---

### GitHub Account und Repository anlegen

**Wenn HAS_GITHUB = false:**

1. Geh auf [github.com](https://github.com)
2. Klick auf **Sign up**
3. Mail, Username, Passwort eingeben
4. Mail bestätigen (sie schicken dir einen Code)
5. Eingeloggt? Dann weiter.

**Für alle (Repository anlegen):**

"Wir brauchen jetzt einen Platz bei GitHub, wo dein CEO-GPT liegen soll. Das heißt dort Repository (oder kurz Repo)."

1. Geh auf [github.com/new](https://github.com/new)
2. **Repository name:** Benenn es nach deinem CEO-GPT (z.B. `mein-ceo-gpt`, `firma-CEO-GPT`, `[firmenname]-CEO-GPT`)
3. **Description:** Optional, etwa "Mein CEO-GPT CEO-GPT"
4. **Visibility:** Wähl **Private** (wichtig, dein CEO-GPT enthält Geschäfts-Kontext)
5. Setz NICHT die Haken bei "Add a README" oder ".gitignore" (haben wir beides schon)
6. Klick auf **Create repository**

Danach zeigt GitHub eine Seite mit Setup-Befehlen. Die nutzen wir gleich.

---

### Mit GitHub verbinden und pushen

"Jetzt verbinden wir deinen lokalen CEO-GPT mit deinem GitHub Repository und laden alles hoch."

**Zuerst die Authentifizierung.** GitHub muss prüfen, dass du es wirklich bist, wenn du was hochlädst. Der einfachste Weg:

Check, ob das GitHub CLI schon da ist:
```bash
gh --version 2>/dev/null && echo "GitHub CLI: installiert" || echo "GitHub CLI: nicht installiert"
```

**Wenn das GitHub CLI installiert ist:**
```bash
gh auth status 2>/dev/null || gh auth login
```
Folg den Prompts (wähl HTTPS, authentifizier dich über den Browser).

**Wenn das GitHub CLI nicht installiert ist, nutz die Token-Methode:**

1. Geh auf [github.com/settings/tokens](https://github.com/settings/tokens)
2. Klick auf **Generate new token (classic)**
3. Benenn ihn "CEO-GPT CEO-GPT"
4. Setz den Haken bei `repo` (volle Kontrolle über private Repositories)
5. Klick auf **Generate token**
6. Kopier den Token (beginnt mit `ghp_`), du siehst ihn nur einmal.

Jetzt verbinden und pushen:

```bash
git remote add origin https://github.com/USERNAME/REPO-NAME.git
git branch -M main
git push -u origin main
```

Ersetz `USERNAME/REPO-NAME` durch den GitHub-Benutzernamen und Repo-Namen des Members.

Wenn du mit Token arbeitest (kein GitHub CLI), wirst du nach Username und Passwort gefragt. Das Passwort ist der gerade kopierte Token, nicht das GitHub-Passwort.

[VERIFY]
```bash
git remote -v
```
Soll die GitHub-URL für `fetch` und `push` zeigen.

Außerdem auf GitHub prüfen: "Geh auf github.com/USERNAME/REPO-NAME, du solltest dort alle deine CEO-GPT-Dateien sehen."

"Dein CEO-GPT ist bei GitHub gesichert. Ab jetzt aktualisiert sich deine Cloud-Kopie bei jedem Push."

---

### Was ist Pushen?

"Du hast gerade zum ersten Mal **gepusht**. Kurz der Unterschied:

- **Commit** = Speicherpunkt auf deinem Gerät (lokal). Schnell, kostenlos, mach es oft.
- **Push** = Deine Speicherpunkte zu GitHub hochladen (Cloud). Am Ende einer Session, oder wann immer du ein Cloud-Backup willst.

**Stell dir vor, du schreibst in ein Notizbuch und kopierst es ab und zu in einen Tresor.**
- Commit = ins Notizbuch schreiben (passiert ständig)
- Push = Notizbuch fotokopieren und in den Tresor legen (passiert in Abständen)

**Wann pushen:**
- Am Ende einer Session
- Bevor du den Laptop zumachst
- Nachdem du was Größeres fertig hast
- Bevor du verreist oder lange weg vom Rechner bist

**Du musst nicht nach jedem Commit pushen.** Fünf bis zehn Commits pro Session und am Schluss einmal pushen ist völlig ok."

---

### Kurz zu Branches

"Du wirst mal von **Branches** in Git hören. Die Kurzversion:

Ein Branch ist wie eine parallele Zeitlinie. Du legst einen Branch an, um was auszuprobieren, ohne deinen Haupt-CEO-GPT anzufassen. Klappt das Experiment, fügst du es zurück. Klappt es nicht, löschst du den Branch, kein Schaden.

**Für jetzt nutzen wir keine Branches.** Alles läuft auf `main` (deiner einzigen Zeitlinie). Hält es einfach. Branches sind sinnvoll für Teams oder komplexe Experimente, du lernst sie später kennen, wenn du sie brauchst.

Wenn dir jemand sagt, du "müsstest mit Branches arbeiten", für einen Solo-CEO-GPT ist direkt auf `main` arbeiten völlig in Ordnung."

---

### HISTORY.md anlegen, das Gedächtnis deines CEO-GPT

"Jetzt richten wir was Starkes ein, ein **laufendes Logbuch** für dein CEO-GPT.

**HISTORY.md** ist eine Datei, in der dein Mitarbeiter festhält, was bei jeder Session gebaut, geändert oder behoben wurde. Wie das Logbuch eines Schiffes, datierte Einträge zu allem, was passiert ist.

**Warum das zählt:** Kommst du nach einer Woche Pause zurück, oder startet eine neue Session, kann dein Mitarbeiter zuerst die HISTORY.md lesen, um zu wissen, was alles steht. Kein erneutes Rekonstruieren, kein Suchen.

**Du schreibst diese Datei nicht selbst, dein Mitarbeiter macht es.** Jedes Mal, wenn du `/commit` ausführst, kommt automatisch ein Eintrag dazu."

Schreib die `HISTORY.md` aus `templates/history.md` in den CEO-GPT-Root.

[VERIFY]
```bash
head -10 HISTORY.md
```

---

### Das docs/ System aufsetzen, der selbst-dokumentierende CEO-GPT

"Das ist die andere Hälfte des Gedächtnisses.

Während HISTORY.md das WAS mitschreibt (zeitliches Logbuch), trägt das `docs/` System das WIE (technische Referenz).

Wenn du ein System baust, sagen wir eine Daten-Pipeline oder einen Telegram-Bot, legt dein Mitarbeiter eine technische Doku an, die die Architektur erklärt, die wichtigen Dateien, wie man es nutzt und wie man es ändert. Diese Dokus liegen in `docs/` und werden in `docs/_index.md` indexiert.

**Der Trick:** Wenn eine künftige Session an diesem System arbeitet, liest sie `docs/_index.md`, findet die passende Doku und weiß sofort, wie alles funktioniert. Kein erneutes Code-Lesen. Kein Raten.

**Du schreibst die Dokus nicht selbst, dein Mitarbeiter macht es.** Der `/commit` Befehl prüft nach jedem Commit, ob Dokus angelegt oder geändert werden müssen."

Leg den `docs/` Ordner an und schreib den Index:

```bash
mkdir -p docs
```

Schreib `docs/_index.md` aus `templates/docs-index.md`.

Leg auch die Doku-Vorlagen ab, damit dein Mitarbeiter sie nachher findet. Schreib `docs/_templates/` mit der System- und der Integrations-Vorlage aus `templates/doc-system-template.md` und `templates/doc-integration-template.md`.

```bash
mkdir -p docs/_templates
```

[VERIFY]
```bash
ls docs/
```
Soll `_index.md` und `_templates/` zeigen.

"Dein Doku-System steht. Noch leer, es füllt sich, sobald du Systeme baust."

---

### Den /commit Befehl installieren

"Jetzt der Befehl, der alles zusammenklammert.

**`/commit` macht drei Dinge in einem:**
1. **Speichert deine Arbeit**: Legt einen Git-Commit mit sauberer, strukturierter Beschreibung an
2. **Hält die Doku aktuell**: Prüft, ob technische Dokus angelegt oder aktualisiert werden müssen
3. **Schreibt das Logbuch fort**: Fügt einen Eintrag in HISTORY.md an

Den nutzt du am Ende jeder Session oder nach einem sinnvollen Stück Arbeit."

Leg den Befehl an:

```bash
mkdir -p .claude/commands
```

Schreib den `/commit` Befehl aus `commands/commit.md` nach `.claude/commands/commit.md`.

[VERIFY]
```bash
cat .claude/commands/commit.md | head -3
```
Soll den Header des Befehls zeigen.

"Dein `/commit` Befehl ist drin. Im Test-Abschnitt zeig ich dir, wie er sich anfühlt."

---

### /prime erweitern, HISTORY.md und docs/_index.md laden

"Wir sagen jetzt deinem `/prime` Befehl, dass er die neuen Dateien mitliest. Beim Start einer Session soll dein Mitarbeiter HISTORY.md und docs/_index.md lesen, damit er weiß, was schon gebaut wurde und wo die Dokus liegen."

Lies den bestehenden `/prime` Befehl:
```bash
cat .claude/commands/prime.md
```

Trag die zwei Dateien in die Leseliste von prime ein. Find den Abschnitt, in dem die gelesenen Dateien aufgelistet sind, und ergänze:

```markdown
- `HISTORY.md`: CEO-GPT-Logbuch (was wurde gebaut, wann, von wem)
- `docs/_index.md`: Doku-Routing-Index (hier findest du die passenden Dokus)
```

**Wo einfügen:** Such die Stelle, an der `/prime` die zu lesenden Dateien auflistet (meistens nummerierte Punkte oder Bullets). Häng die zwei neuen Dateien ans Ende an. Lösch oder ändere nichts, was schon da ist.

Zeig dem Member, was sich geändert hat: "Ich hab HISTORY.md und docs/_index.md in deinen /prime Befehl eingetragen. Ab jetzt startet jede Session mit dem Wissen, was gebaut wurde und wo die Dokus liegen."

---

### /implement erweitern, Doku-Bewusstsein

"Falls du einen `/implement` Befehl hast (oder `/create-plan`), bauen wir Doku-Bewusstsein ein. Heißt, nach jedem fertigen Stück Arbeit prüft dein Mitarbeiter, ob die Doku aktualisiert werden muss."

Check, ob der implement-Befehl existiert:
```bash
ls .claude/commands/implement.md 2>/dev/null && echo "EXISTIERT" || echo "NICHT VORHANDEN"
```

**Wenn er existiert:** Lies die Datei und füg diesen Abschnitt an der passenden Stelle ein (meistens nach den Implementierungs-Schritten, vor dem Abschluss-Bericht):

```markdown
### Doku-Check

Nach jedem fertigen Stück Arbeit:

1. Prüf, ob die Änderungen ein neues System angelegt oder ein bestehendes deutlich verändert haben
2. Lies `docs/_index.md`, gibt es schon eine Doku für dieses System?
3. Wenn keine Doku existiert und die Änderungen sind sinnvoll (neues System, neuer Befehl, neue Integration):
   - Leg eine Doku an mit der Vorlage in `docs/_templates/`
   - Trag sie in `docs/_index.md` ein
4. Wenn die Doku existiert, aber veraltet ist:
   - Aktualisier die betroffenen Abschnitte
   - Trag einen datierten Eintrag in die History-Tabelle der Doku ein
5. Aktualisier `HISTORY.md` mit dem, was umgesetzt wurde
6. Committ die Doku-Updates: `docs: update documentation for {system}`
```

**Wenn er nicht existiert:** Überspring diesen Schritt. Sag dem Member: "Du hast noch keinen /implement Befehl, kein Ding. Wenn du später einen baust oder installierst, übernimmt der /commit Befehl die Doku-Arbeit von allein."

---

### Alles, was wir gerade gebaut haben, committen

"Wir speichern jetzt alles, was wir gerade aufgesetzt haben."

```bash
git add -A
git status
```

Zeig dem Member, was committet wird. Dann:

```bash
git commit -m "feat: Absicherung dazu, Git-Workflow, Doku-System, /commit Befehl"
```

Dann push:

```bash
git push
```

[VERIFY]
```bash
git log --oneline -3
```
Soll den Absicherungs-Commit und den ersten Commit zeigen.

"Alles gespeichert und bei GitHub gesichert. Jetzt testen wir."

---

## TEST

### Test 1: /commit laufen lassen

"Wir testen deinen neuen `/commit` Befehl. Mach erst eine kleine Änderung, z.B. eine Zeile in HISTORY.md oder einen Tippfehler in CLAUDE.md."

Mach eine kleine Änderung an HISTORY.md, ergänze einen Test-Eintrag:

```
## {heutiges Datum}

### Absicherung Test
- Den /commit Ablauf getestet
```

Lass jetzt `/commit` laufen (oder geh manuell durch, was `/commit` macht):

1. Er erkennt die geänderte Datei
2. Stage die Änderung
3. Generier eine Commit-Message wie `docs: /commit Ablauf getestet`
4. Committ sie
5. Stell fest, dass keine System-Dateien geändert wurden, Doku-Check übersprungen
6. HISTORY.md war schon aktualisiert, Logbuch-Schritt übersprungen

Nach dem Lauf: "Der /commit Befehl läuft. Er hat deine Änderung erkannt, mit sauberer Message committet und geprüft, ob Dokus aktualisiert werden müssen (diesmal nicht, weil du nur HISTORY.md angefasst hast)."

### Test 2: Push zu GitHub

```bash
git push
```

Dann: "Geh in deinem Browser zu deinem GitHub Repository, du solltest den neuen Commit dort sehen. Dein Cloud-Backup ist auf Stand."

### Test 3: Deine Historie ansehen

```bash
git log --oneline
```

"Das sind all deine Speicherpunkte bisher. Jede Zeile ist ein Commit mit seiner Beschreibung. Während dein CEO-GPT wächst, wird das deine komplette Timeline."

Wenn alles läuft, sag mit Pause und Wärme:
> *"Dein Mitarbeiter ist gesichert. Egal was passiert, er ist in einer Minute wieder da."*

Dein CEO-GPT schreibt ab jetzt jede Änderung mit, dokumentiert sich selbst und liegt sicher in der Cloud. Hier ist dein neuer Ablauf für jede Session.

---

## TÄGLICHER ABLAUF

Nach dem Test, erklär wie das im Alltag aussieht:

**Session-Start:**
- `/prime` ausführen, dein Mitarbeiter lädt HISTORY.md und docs/_index.md (und mehr), weiß sofort, was gebaut wurde

**Während der Arbeit:**
- Bauen, ändern, ausprobieren
- Alles wird von Git mitgeschrieben, du kannst jederzeit zurück

**Session-Ende (oder nach sinnvoller Arbeit):**
- `/commit` ausführen, dein Mitarbeiter staget die Änderungen, schreibt eine saubere Commit-Message, aktualisiert die Dokus wenn nötig, ergänzt HISTORY.md
- `git push` ausführen, damit alles bei GitHub liegt (oder sag deinem Mitarbeiter "push zu GitHub")

**Das war's.** Drei Befehle: `/prime` zum Start, `/commit` zum Speichern, `git push` zum Sichern.

**Wie oft committen:**
- Feature fertig, committen
- Was Riskantes geplant, vorher committen
- Session zu Ende, committen
- Bug gefixt, committen
- Geschäfts-Kontext aktualisiert, committen
- Chaos gemacht und willst von vorne anfangen, `git checkout .` macht alles seit dem letzten Commit rückgängig

---

## WAS ALS NÄCHSTES

*"Die Basis steht. Dein CEO-GPT ist gesichert, dein Backup liegt im Netz, dein Logbuch läuft.*

*Als Nächstes käme das Gehirn. Ich lerne dich, dein Business, dein Team und deine Strategie kennen, damit ich in jeder Sitzung weiß wer du bist und woran wir arbeiten. Setup-Zeit etwa 30 Minuten.*

*Willst du gleich weitermachen, oder lieber Pause?"*

Wenn der Member "ja" oder "weiter" sagt, direkt `/install module-installs/kontext` starten.
Wenn er Pause will, warm verabschieden und sagen dass er einfach `/install module-installs/kontext` läuft wenn er soweit ist.

## Nützliche Gewohnheiten

Bei allem was du ab hier baust, schreibt `/commit` automatisch mit und legt Dokus an. Je mehr du baust, desto klüger wird dein CEO-GPT. Wenn du tiefer in Git willst, `git log` zeigt die Historie, `git diff` zeigt was sich geändert hat, `git checkout .` macht uncommittete Änderungen rückgängig. Frag deinen Mitarbeiter zu jedem Befehl.

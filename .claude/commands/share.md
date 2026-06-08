# Share

> Packt ein System oder eine Funktion aus deinem CEO-GPT zum Weitergeben. Du tauchst erst tief rein, dann produzierst du ein eigenständiges, einsteigerfreundliches Paket mit geführtem Installer, den jeder nutzen kann.

## Variablen

ziel: $ARGUMENTS (beschreib das System oder Feature, z.B. "die Daten-Pipeline", "der Kunden-Onboarding-Flow", "der Wachstums-Hebel")

---

## Phase 1: RECHERCHE: System vollständig verstehen

**Ziel:** Jedes Stück des Systems erfassen, bevor du ein Wort schreibst.

**Aktionen:**

1. Parse die Ziel-Beschreibung aus den Argumenten
2. Durchsuch das CEO-GPT komplett nach allem, was zum System gehört:
   - Skripte und Code: die eigentliche Umsetzung
   - Doku: alle technischen Beschreibungen
   - Befehle (`.claude/commands/`): beteiligte Slash-Befehle
   - Fähigkeiten (`.claude/skills/`): eingebundene Skills
   - Konfiguration (`.env`, `.env.example`): nötige API-Keys und Dienste
   - Datenbank-Schemas: beteiligte Tabellen
   - Zeitpläne (cron, launchd): Automatisierungs-Zeitpläne
   - Abhängigkeiten (`requirements.txt`, `package.json`, Imports im Code)
3. Lies jede relevante Datei. Versteh Eingaben, Verarbeitung, Ausgaben, externe Abhängigkeiten, was geschäfts-spezifisch ist und was wiederverwendbar
4. Bau eine **Komponenten-Karte**: jede Datei, jeder externe Dienst, jeder API-Key, jeder Zeitplan

**Präsentation:**

```
System: {name}
Komponenten:
  [x] {Datei oder Modul 1}: {was es tut}
  [x] {Datei oder Modul 2}: {was es tut}
  ...
Externe Dienste: {Liste, mit Hinweis ob API-Key nötig}
API-Keys nötig: {Anzahl und Liste}
Datenbank-Tabellen: {Liste oder "keine"}
Automatisierung: {cron, launchd, manuell, keine}
Komplexität: Einfach (1-3 Dateien) / Mittel (4-10) / Komplex (10+)
```

**STOPP und warte auf Bestätigung.** "Das habe ich gefunden. Übersehe ich was?"

---

## Phase 2: ZUSCHNITT: Festlegen, was reinkommt

**Ziel:** Bestimmen, was rein soll und an wen das geht. Halt es knapp, zwei bis drei Fragen reichen.

**Aktionen:**

1. Zeig die Komponenten-Liste aus der Recherche als Checkliste. Markier empfohlene Komponenten mit `[x]` und optionale mit `[ ]`:

   ```
   Dieses System hat folgende Komponenten:
   [x] {Kern-Komponente}: {Beschreibung}
   [x] {Pflicht-Komponente}: {Beschreibung}
   [ ] {Optional: Erweitertes Feature}: {Beschreibung}
   [ ] {Optional: Zeitplan}: {Beschreibung}

   Was kommt rein? Alles markierte, oder anpassen?
   ```

2. Frag, wohin das geht:

   ```
   Wohin geht das?
   A) Team (intern): für Teammitglieder oder Mitstreiter
   B) Community: für eine Gruppe, ein Forum, einen Community-Channel
   C) Kunden: für Kunden oder Partner
   D) Öffentlich: zum freien Teilen (Blog, YouTube, Social Media)
   ```

3. Nur wenn es echte optionale Features gibt, frag:
   ```
   Optionale Features: [{Liste}]. Reinpacken oder weglassen?
   ```

**Festhalten:** Ziel, Komponenten, optionale Features.

**STOPP und warte auf Antworten, bevor du weitermachst.**

---

## Phase 3: RAHMEN: Nutzen festlegen

**Ziel:** Klären, warum jemand das will und wie es positioniert wird.

**Aktionen:**

1. Definier das **Problem**, das dieses System löst, in normalem Deutsch, aus Sicht des Empfängers
2. Definier den **konkreten Nutzen**. Was kriegt der Empfänger, wie verändert sich sein Arbeitstag?
3. Identifizier den **Wow-Faktor**, also was daran beeindruckend ist
4. Identifizier **zu beachten**: Kosten, Komplexität, Voraussetzungen, Pflege

**Präsentation:**

- "So würde ich das positionieren: [Problem → Lösung → Nutzen]. Trifft das, oder anpassen?"

**STOPP und warte auf Input, bevor du schreibst.**

---

## Phase 4: SCHREIBEN: Paket bauen

**Ziel:** Das vollständige, weitergebbare Paket als einsteigerfreundliche Anleitung mit geführtem Installer schreiben.

Ausgabe in `shares/{name}/` mit folgender Struktur:

```
shares/{name}/
├── INSTALL.md              # DIE ZENTRALE DATEI: Anleitung FÜR den Mitarbeiter beim Empfänger
├── README.md               # Menschen-Überblick: was es tut, was du brauchst
├── scripts/
│   ├── requirements.txt    # Python-Abhängigkeiten
│   ├── .env.example        # Vorlage für API-Keys mit Kommentaren
│   └── *.py                # Skripte (in sich abgeschlossen)
├── templates/              # Optional: Vorlagen, die der Empfänger anpasst
│   └── *.md
└── config/                 # Optional: Zeitplan-Konfigs (launchd plist, systemd, cron)
    └── *.plist / *.service
```

**`INSTALL.md` muss diese Abschnitte enthalten:**

1. **FÜR CLAUDE** Verhaltens-Abschnitt, der dem Mitarbeiter beim Empfänger sagt, wie er führen soll:
   - Geh von nicht-technisch aus, außer der Empfänger sagt etwas anderes
   - Erklär jeden Schritt in normalem Deutsch BEVOR du ihn machst
   - Feier kleine Schritte ("API-Key passt, sauber, das war das härteste Stück.")
   - Wenn etwas schiefgeht, erklär schlicht und schlag den Fix vor. Nie Error-Logs dumpen.
   - Überspring keine Prüf-Schritte
   - Tempo halten: nach Meilensteinen pausieren

2. **ÜBERBLICK**: 2-3 Absätze in normalem Deutsch, die abdecken was es tut, warum es nützt, was am Ende dasteht, Setup-Zeit und laufende Kosten

3. **ZUSCHNITT**: EMPFOHLEN (sinnvolle Voreinstellungen, schnellster Weg) vs. ANGEPASST (jede Option durchgehen). Frag, welchen Weg.

4. **VORAUSSETZUNGEN**: Jeden Punkt mit Prüf-Befehl. Anleitung zum Installieren, falls etwas fehlt.

5. **API-KEYS**: Schritt für Schritt pro Key, mit genauer URL, genauen Klicks, Prüf-Befehl. Einer nach dem anderen.

6. **INSTALLATION**: Kleine, nummerierte Schritte. Alle zwei bis drei Schritte einen `[PRÜFEN]`-Block. Bei komplexen Setups in Phasen gliedern:
   - Phase 1: Grundlage (Ordner, env, Abhängigkeiten)
   - Phase 2: Kern (Hauptskripte)
   - Phase 3: Extras (Zeitplan, Integrationen)

7. **TEST**: Kurzer Test plus voller Test mit erwarteter Ausgabe in normalem Deutsch.

8. **WAS ALS NÄCHSTES**: Naheliegende nächste Schritte, Anpassungs-Ideen, verwandte Systeme.

**`README.md` knapp und scanbar:**

- Was es tut (3 Punkte)
- Was du brauchst (Konten, Tools)
- Wie installieren ("Gib diesen Ordner an Claude Code und sag, er soll INSTALL.md lesen und das einrichten")
- Laufende Kosten
- Datei-Liste

### Code-Extraktions-Regeln

Wenn du Code aus dem CEO-GPT ziehst:

1. **In sich abgeschlossen**: Jede Datei läuft ohne CEO-GPT-spezifische Imports. Hilfsfunktionen reinhängen.
2. **Keine sensiblen Daten**: Geschäftszahlen, Umsätze, Kundennamen, interne Strategie, sensibles IP raus.
3. **Keine festen Pfade**: Relative Pfade nutzen oder `Path(__file__).resolve().parent`.
4. **Vereinfacht**: Features raus, die nicht zum geteilten System gehören.
5. **Lauffähig**: Wenn der Empfänger der Anleitung folgt, muss es laufen.
6. **Kommentiert**: Kurze Kommentare wo die Logik nicht offensichtlich ist. Normales Deutsch.
7. **Einzeln testbar**: Jedes Skript hat `if __name__ == "__main__":` mit Grundtest.
8. **Hilfreiche Fehlermeldungen**: Fehler schlagen Fix vor, statt nur Versagen zu melden.

---

## Phase 5: PRÜFEN: Durchgang als Empfänger

**Ziel:** Jedes Stolperstein finden, der einen Erstnutzer aufhalten würde.

**Aktionen:**

1. **Gedanklicher Durchgang**: Lauf das Paket durch, als wärst du der Empfänger:
   - Würde jemand, der Claude Code gerade frisch installiert hat, das schaffen?
   - Ist jeder API-Key-Schritt spezifisch genug? (Nicht "hol deinen Stripe-Key" sondern "geh auf stripe.com/developers, klick API Keys, kopier den Secret Key der mit sk_live anfängt")
   - Setzen Schritte Wissen voraus, das fehlt?
   - Fehlen Voraussetzungen? (Python-Version, pip, npm, Betriebssystem-Tools)

2. **Abhängigkeits-Check**: Jeder Import in Skripten hat eine Zeile in `requirements.txt`

3. **Pfad-Check**: Keine festen absoluten Pfade, keine CEO-GPT-spezifischen Imports

4. **Vollständigkeit**: Jede in der Anleitung referenzierte Datei liegt wirklich im Paket

5. **Probleme fixen**: Nicht nur notieren. Vor der Übergabe fixen.

**Präsentation:**

- "Ich bin das als neuer Nutzer durchgegangen. {N} Probleme gefunden und gefixt: {kurze Liste}. Das Paket ist bereit."

**STOPP und zeig das fertige Paket zur Abnahme.**

---

## Phase 6: ÜBERGABE: Speichern und Übergeben

**Ziel:** Fertigstellen, speichern, übergeben.

**Aktionen:**

1. **Paket speichern** in `shares/{name}/`

2. **ZIP erstellen:**

   ```bash
   cd shares && zip -r {name}.zip {name}/
   ```

3. **Zusammenfassung zeigen:**

   ```
   Paket: {name}
   Dateien: {Anzahl}
   Externe Dienste: {Liste}
   API-Keys nötig: {Anzahl}
   Setup-Zeit: {Schätzung}
   Laufende Kosten: {Schätzung}
   Einschränkungen: {falls vorhanden}
   Ort: shares/{name}/
   ```

4. **Frag:** "Willst du noch was anpassen, oder ist das fertig zum Weitergeben?"

---

## Kritische Regeln

- **Erst recherchieren, dann schreiben**: Niemals anfangen zu schreiben, bevor du den relevanten Code wirklich verstanden hast. Halbverstandene Systeme produzieren kaputte Pakete.
- **Zuschnitt vor dem Schreiben**: Niemals anfangen, bevor das Ziel bestätigt ist. Das spart sinnlose Arbeit.
- **In sich abgeschlossen ist Pflicht**: Das Paket muss allein laufen. Kein "hol dir das auch noch aus dem anderen Repo." Alles drin.
- **Sensible Daten raus**: Geschäftszahlen, Umsatz, Kundeninfos, interne Strategie. Nichts davon ins Paket. Nur System-Architektur und Code.
- **`INSTALL.md` ist das Produkt**: Die Anleitung zählt mehr als der Code. Perfektes Skript mit verwirrender Anleitung scheitert. Einfaches Skript mit klarer Anleitung gewinnt.
- **Als Anfänger prüfen**: Phase 5 immer machen. Wenn ein Schritt einen Erstnutzer verwirren würde, fix das vor der Übergabe.
- **Ehrlich bei Kosten und Komplexität**: Verkauf den Setup nicht unter Wert. Wenn fünf API-Keys und ein Server nötig sind, sag das gleich.
- **Claude-Code-freundlich**: Setup-Schritte sind klein und einzeln testbar. Der Mitarbeiter kann sie Schritt für Schritt ausführen.

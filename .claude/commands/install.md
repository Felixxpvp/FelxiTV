# Install

> Richtet eine neue Fähigkeit in diesem CEO-GPT ein. Zeig auf einen Ordner in `module-installs/`, und du führst den Geschäftsführer geführt durch das Setup.

## Variablen

modul_pfad: $ARGUMENTS (Pfad zum Ordner, z.B. `module-installs/kontext`)

---

## Anleitung

Du richtest eine neue **Fähigkeit** im CEO-GPT ein. Jede Fähigkeit ist ein in sich abgeschlossenes Paket, das dem Mitarbeiter etwas Neues hinzufügt. Fähigkeiten werden eine nach der anderen eingerichtet.

### Was so ein Ordner enthält

Jeder Fähigkeits-Ordner enthält:

- **INSTALL.md**: Die zentrale Datei. Eine Anleitung, die direkt FÜR DICH (den Mitarbeiter) geschrieben ist. Sie führt dich Schritt für Schritt durch das Setup, geführt mit dem Geschäftsführer.
- **README.md**: Eine Übersicht für Menschen, was die Fähigkeit tut.
- **scripts/**: Optional. Python-Skripte, die zur Fähigkeit gehören.
- **templates/**: Optional. Vorlagen-Dateien, die in das CEO-GPT kopiert werden.
- **config/**: Optional. Konfigurations- oder Zeitplan-Dateien.
- **reference/**: Optional. Begleit-Dokumentation.

### Wie du eine Einrichtung durchführst

1. **Lies die `INSTALL.md`** aus dem übergebenen Pfad (z.B. `module-installs/kontext/INSTALL.md`)
2. **Folg jeder Anweisung in der `INSTALL.md` exakt**, das ist dein Drehbuch für die ganze Einrichtung
3. Die `INSTALL.md` hat einen eigenen Abschnitt "FÜR CLAUDE" mit Verhaltensregeln, halt dich daran

### Kritische Regeln

**Über den Geschäftsführer:**

- Geh davon aus, dass er **nicht-technisch** ist und Claude Code zum ersten Mal nutzt, außer er sagt etwas anderes
- Er ist Geschäftsführer oder Unternehmer. Klug, aber kein Entwickler.
- Das hier ist möglicherweise eines der ersten Dinge, die er in Claude Code überhaupt baut.
- Sei geduldig, ermutigend, klar. Keine Fachsprache. Keine Annahmen, was er schon weiß.

**Über den Einrichtungs-Ablauf:**

- Das ist eine **geführte, interaktive Sitzung**, kein stilles Skript-Abarbeiten
- Erklär in normalem Deutsch, was du gleich tust, BEVOR du es tust
- Pausier nach Meilensteinen. Lass den Geschäftsführer aufnehmen, was gerade passiert ist.
- Wenn etwas schiefgeht, kipp keinen Error-Log raus. Erklär das Problem schlicht und fix es.
- Feier kleine Schritte ("Sauber, das läuft. Ein Stück näher dran.")

**Über das Anpassen:**

- Jedes CEO-GPT ist anders. Die `INSTALL.md` gibt den Standardweg vor, du **passt dich der konkreten Situation an**.
- Wenn etwas schon existiert, was die Fähigkeit anlegen würde, schreib nichts drüber, sondern frag.
- Wenn die CEO-GPT-Struktur abweicht, passt du die Fähigkeit an die Struktur an, nicht umgekehrt.
- Wenn die Fähigkeit andere Fähigkeiten voraussetzt, die noch nicht eingerichtet sind, sag das klar, blockier aber nicht. Empfehl, was als Nächstes dran wäre.

**Über die `.env`-Datei:**

- API-Keys kommen in die `.env`-Datei im CEO-GPT-Root
- Wenn eine Fähigkeit einen API-Key braucht, führ den Geschäftsführer Schritt für Schritt durch das Holen (genaue URL, genaue Klickpfade)
- Prüf immer, dass Keys funktionieren, bevor du weitergehst
- Zeig vollständige API-Keys niemals zurück, nachdem sie gesetzt wurden

### Ausführung

Jetzt lies die `INSTALL.md` am übergebenen Pfad und start die Einrichtung.

```
Read: {modul_pfad}/INSTALL.md
```

Folg ihr von oben nach unten. Die `INSTALL.md` ist dein vollständiger Leitfaden.

# Implement

Führt einen Plan aus, den `/create-plan` erstellt hat. Lies den Plan gründlich, arbeite jeden Schritt in Reihenfolge ab und berichte am Ende, was getan wurde.

## Variablen

plan_pfad: $ARGUMENTS (Pfad zur Plan-Datei, z.B. `plans/2026-05-11-wettbewerbsanalyse.md`)

---

## Anleitung

### Phase 1: Plan verstehen

1. **Lies die Plan-Datei vollständig.** Nicht überfliegen. Jeden Abschnitt verstehen.
2. **Voraussetzungen prüfen:**
   - Gibt es offene Fragen, die zuerst beantwortet werden müssen?
   - Hängt etwas an externen Ressourcen oder Entscheidungen des Geschäftsführers?
   - Wenn Blocker existieren, stopp und frag, bevor du weitermachst.
3. **Bestätige, dass der Plan startklar ist:**
   - Status sollte "Entwurf" oder "Bereit" sein
   - Alle Abschnitte sollten ausgefüllt sein (keine Platzhalter mehr)

---

### Phase 2: Plan ausführen

1. **Folg den Schritt-für-Schritt-Aufgaben in genau der Reihenfolge.**
   - Jeden Schritt voll abschließen, bevor du zum nächsten gehst
   - Wenn ein Schritt eine Datei anlegen will, schreib die volle Datei. Keine Stümpfe.
   - Wenn ein Schritt eine Datei ändert, lies sie zuerst, dann mach die Änderung präzise.

2. **Für jeden Schritt:**
   - Lies die betroffenen Dateien
   - Setz die Änderung um
   - Prüf, dass die Änderung stimmt, bevor du weitermachst

3. **Probleme ruhig anfassen:**
   - Wenn ein Schritt nicht wie geschrieben funktioniert, halt das fest und pass an, wenn die Absicht klar ist
   - Wenn du unsicher bist, frag den Geschäftsführer, statt zu raten
   - Dokumentier jede Abweichung vom Plan

---

### Phase 3: Prüfen

1. **Geh die Prüf-Checkliste aus dem Plan durch**
   - Hak jeden Punkt ab
   - Notier, was nicht klappt

2. **Prüf die Erfolgskriterien**
   - Bestätige jeden Punkt
   - Notier Lücken

3. **Querverweise und Konsistenz prüfen:**
   - Sind neue Dateien dort verlinkt, wo sie sein sollten?
   - Ist `CLAUDE.md` aktualisiert, wenn sich die CEO-GPT-Struktur geändert hat?
   - Folgen Namen den Konventionen?

---

### Phase 4: Plan-Status aktualisieren

Nach der Umsetzung pflegst du die Plan-Datei nach:

1. Ändere `**Status:** Entwurf` auf `**Status:** Umgesetzt`
2. Füg am Ende einen Abschnitt "Umsetzungs-Notizen" hinzu:

```markdown
---

## Umsetzungs-Notizen

**Umgesetzt:** <YYYY-MM-DD>

### Zusammenfassung

<Knappe Beschreibung, was getan wurde>

### Abweichungen vom Plan

<Was wurde während der Umsetzung geändert? Oder "Keine">

### Aufgetretene Probleme

<Welche Probleme kamen, wie wurden sie gelöst? Oder "Keine">
```

---

## Qualitäts-Standards

- **Gründlich:** Jeder Schritt im Plan wird ausgeführt, nichts übersprungen
- **Präzise:** Änderungen entsprechen dem, was der Plan vorgibt
- **Vollständig:** Dateien sind voll geschrieben, keine Stümpfe
- **Konsistent:** Alle Querverweise und Doku-Stellen sind aktualisiert
- **Nachvollziehbar:** Abweichungen sind dokumentiert

---

## Bericht

Nach der Umsetzung:

1. **Zusammenfassung:** Bulletpoint-Liste, was getan wurde
2. **Geänderte Dateien:** Alle angelegten, geänderten oder gelöschten Dateien
3. **Prüf-Ergebnisse:** Status jedes Checklisten-Punktes
4. **Abweichungen:** Was vom ursprünglichen Plan abweicht
5. **Nächste Schritte:** Was noch zu tun ist (falls vorhanden)

Format:

```
## Umsetzung fertig

### Zusammenfassung
- <Was wurde getan>
- <Was wurde getan>

### Geänderte Dateien
**Angelegt:**
- `pfad/zur/neuen-datei.md`

**Geändert:**
- `pfad/zur/geänderten-datei.md`

**Gelöscht:**
- (keine)

### Prüf-Ergebnis
- [x] <Bestanden>
- [x] <Bestanden>

### Abweichungen vom Plan
<Keine, oder Liste>

### Plan-Status
`plans/YYYY-MM-DD-{name}.md` Status auf "Umgesetzt" gesetzt
```

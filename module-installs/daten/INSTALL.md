# Daten: Installation

<!-- MODUL-METADATEN
modul: daten
version: v1
status: RELEASED
released: 2026-02-27
requires: [kontext]
phase: 2
category: Kern-Module
complexity: complex
api_keys: 1-7 (je nach Quellen)
setup_time: 30-60 Minuten
-->

---

## FÜR CLAUDE (Anleitung für dich, das Programm)

Du hilfst dem Member, das **Gehirn** seines Mitarbeiters mit Zahlen auszustatten. Das ist der zweite Schritt im CEO-GPT. Sein Geschäfts-Kontext steht schon, jetzt kommen die Zahlen dazu.

**Wir gehen das im Workshop durch, Schritt für Schritt.** Du baust nicht stumpf Dateien ab. Du gehst mit dem Member durch eine Erkundungsphase. Du lernst sein Business kennen, kartierst seine Datenquellen und baust eine Pipeline, die genau auf sein Setup zugeschnitten ist.

**Verhalten:**
- Geh davon aus, dass der Member nicht technisch ist, außer er sagt etwas anderes
- Erklär in Klartext, was du als Nächstes machst, bevor du es machst
- Feier kleine Erfolge ("API-Key sitzt, das war der schwierigste Teil")
- Wenn was fehlschlägt, kein Log-Dump. Erklär das Problem in einem Satz und schlag die Lösung vor
- Überspring keine Prüfungen, wenn ein Check fehlschlägt, hilf beim Fixen statt weiterzumachen
- Sprich aufmunternd, der Member baut hier was Echtes

**Pacing:**
- Nicht durchrasen. Nach Meilensteinen kurz halten.
- Nach dem Workshop: "Gut, dein Daten-Bild steht. Wir können bauen."
- Nach der Basis-Pipeline: "Die Pipeline läuft. Jetzt klemmen wir deine echten Quellen an."
- Nach jeder Quelle: "Sitzt. Lass mich dir kurz zeigen, was jetzt in der Datenbank steht."
- Nach der Vollpipeline: "Deine Zahlen-Basis läuft. Schau, was du gerade gebaut hast."

**Workshop (Phase 1):**
- Lies zuerst die Kontext-Dateien des Members (`context/business-info.md`, `context/strategy.md`, `context/current-data.md`), damit du sein Business verstehst
- Wenn der Kontext noch nicht da ist, frag 3 bis 4 Sachen: Was macht dein Business? Wie kommen Kunden zu dir? Welche Tools nutzt du jeden Tag? Wo kommt dein Umsatz her?
- Auf Basis dessen schlag DU Datenquellen vor, warte nicht, bis der Member sie nennt
- Stell den Plan vor, bevor du baust. Hol dir ein "passt", bevor du Dateien schreibst.

**Eigene Sammler bauen:**
- Beispiel-Sammler liegen in `scripts/examples/`. Lies sie als MUSTER, nicht zum stumpfen Kopieren.
- Pass jeden Sammler an das Setup des Members an (Spalten, Kennzahlen, Tabellen)
- Für Quellen, die nicht in `examples/` liegen, such die API-Doku im Web und bau einen eigenen Sammler nach dem gleichen Muster: `collect() -> dict`, `write(conn, result, date) -> int`
- Jeder Sammler muss fehlende Zugangsdaten sauber abfangen (`status="skipped"`) und darf die Pipeline nie killen

**Fehler abfangen:**
- Wenn die Python-Version zu alt ist, gib genaue Upgrade-Schritte für sein Betriebssystem
- Wenn ein API-Key ungültig ist, führ ihn Schritt für Schritt durch das Holen eines neuen
- Wenn `pip install` scheitert, probier (1) pip upgraden, (2) Build-Tools installieren, (3) gezielten Fix
- Wenn ein Befehl scheitert, erklär in einem Satz, was schief ging, dann gib den Fix
- Nie "schau in die Logs" sagen. Find das Problem und erklär es.

**Schlüssel-Konzepte, die du durchgehend einstreust:**
- **Tagesstand-Logik:** Die meisten APIs liefern aktuelle Gesamtwerte, keine historischen Veränderungen. Wir nehmen Tagesstände und rechnen Veränderungen aus dem Vergleich. Deshalb zählt der tägliche Lauf.
- **Monat-bis-heute:** Die nützlichste Geschäfts-Kennzahl. "Läuft dieser Monat besser als der letzte?" `key-metrics.md` beantwortet das.
- **Pipeline kippt nie ganz:** Fehlen Zugangsdaten für eine Quelle, wird genau die übersprungen, der Rest läuft weiter.
- **Alles bleibt lokal:** Die Datenbank lebt als SQLite-Datei auf dem Rechner des Members. Nichts geht in eine fremde Cloud. Sag das früh, das beruhigt.

---

## ÜBERSICHT (lies das dem Member vor dem Start vor)

Jetzt bauen wir den zweiten Bereich vom Gehirn, nämlich Daten.

Deine Geschäftszahlen liegen heute auf einem Dutzend Plattformen verstreut. Stripe für Umsatz, deine Webseite über Google Analytics, eine Excel-Tabelle für die Marge, YouTube und Instagram für Reichweite. Jedes Mal, wenn du wissen willst, wo du stehst, öffnest du fünf Dashboards und stückelst dir das Bild von Hand zusammen.

Damit ist Schluss. Wir bauen alle deine Zahlen in eine einzige Datenbank auf deinem eigenen Rechner. Ein kleines Skript läuft jeden Morgen, holt die frischen Zahlen aus jeder angebundenen Quelle und schreibt einen Tagesstand. Mit der Zeit baust du dir eine Historie auf, die genau zeigt, wie dein Business sich entwickelt. Woche gegen Woche, Monat gegen Monat.

Dein Mitarbeiter liest diese Zahlen. Wenn du eine neue Sitzung startest und `/prime` läufst, lädt er deine frischen Werte mit. Umsatz, Traffic, Abonnenten, Kündigungsrate. Er kennt deine Lage, bevor du den ersten Satz tippst.

**Was du am Ende hast:**
- Eine lokale SQLite-Datenbank mit deinen Tagesständen
- Automatische Sammler für jede deiner Quellen (eine bis sieben, je nach Tools)
- Eine `key-metrics.md`-Datei, die sich nach jeder Sammlung aktualisiert, geladen über `/prime`
- Ein täglicher Lauf, der alles automatisch macht, während du schläfst

**Setup-Zeit:** 30 bis 60 Minuten, je nachdem wie viele Quellen du anbindest
**Laufende Kosten:** kostenlos. Alle hier genutzten Schnittstellen haben kostenlose Kontingente, die für eine tägliche Sammlung reichen.
**Wo das lebt:** Alles auf deinem Rechner. Die Datenbank ist eine Datei in deinem CEO-GPT, keine Cloud und kein Account, auch kein Tracker.

---

## PHASE 1: WORKSHOP

> Die Kern-Phase. Wir klären, was gebaut wird, bevor wir bauen.

### Das Business verstehen

Erst mal will ich verstehen, wie dein Business tickt.

Lies die existierenden Kontext-Dateien:
- `context/business-info.md` (was das Business macht)
- `context/strategy.md` (Prioritäten und Ziele)
- `context/personal-info.md` (Rolle und Verantwortung)
- `context/current-data.md` (manuell gepflegte Lage)

Wenn diese Dateien fehlen oder der Kontext noch nicht steht, frag:

1. **Was macht dein Business?** (Agentur, Creator, SaaS, Coaching, E-Commerce, Beratung)
2. **Wie kommen Kunden zu dir?** (YouTube, Social Media, Anzeigen, Empfehlungen, Kaltakquise)
3. **Welche Tools nutzt du im Alltag?** (Stripe, Excel-Dateien, Google Sheets, deine Webseite, eigene Datenbanken)
4. **Wo kommt dein Umsatz her?** (Abos, Einmalverkäufe, Retainer, Kurse, Beratung)

### Den Kunden-Weg durchgehen

Geh den Kunden-Weg Stufe für Stufe durch. Für jede Stufe klären, WO die Zahlen heute liegen.

**Oben im Kunden-Weg, wie kommen Leute auf dich aufmerksam?**
- Inhalte: YouTube, Instagram, TikTok, Blog, Podcast
- Anzeigen: Google Ads, Meta Ads, LinkedIn Ads
- Outreach: Kaltakquise, LinkedIn-DMs, Empfehlungsnetz

**Mitte im Kunden-Weg, wie engagieren sie sich?**
- Webseiten-Besuche (Google Analytics)
- Community-Beitritte (Skool, Discord, Circle)
- Lead-Magneten und Newsletter-Anmeldungen
- Link-Klicks (Bitly, UTM)

**Unten im Kunden-Weg, wie wird gekauft?**
- Buchungen (Calendly)
- Bewerbungen und Formulare (Typeform, Google Forms)
- Demo-Termine, DMs, Angebote

**Umsatz, wo kommt das Geld an?**
- Zahlungsabwicklung (Stripe, PayPal, Rechnungen)
- Abo-Verwaltung (Stripe, Chargebee)
- Finanzübersicht (P&L in Excel oder Google Sheets)

### Datenquellen vorschlagen

Auf Basis dessen was du im Workshop gehört hast, schlägst du dem Member eine Liste vor. Ordne sie nach Stufe im Kunden-Weg.

Beispiel-Output:
```
Basierend auf deinem Business würde ich dir das anschließen:

INHALTE & TRAFFIC
[ ] YouTube: Channel-Stats, Video-Performance (gratis API-Key)
[ ] Google Analytics 4: Webseiten-Traffic und Quellen (Service Account)

UMSATZ
[ ] Stripe: Umsatz, Abos, MRR (gratis API-Key)
[ ] P&L-Tabelle in Google Sheets: Monatszahlen (gleicher Service Account wie Google Analytics)

MARKETING
[ ] Bitly: Link-Klicks aus deinem Content (gratis API-Key)

Macht 5 Quellen, gesamt etwa 40 Minuten Setup.
```

Frag: **"Hab ich was übersehen? Andere Tools, wo deine Geschäftszahlen liegen?"**

Pass die Liste an die Antwort an.

### Anbindungen planen

Für jede ausgewählte Quelle kurz erklären:
- Welche Zugangsdaten du brauchst (API-Key, OAuth, Service Account)
- Welche Zahlen du danach im Blick hast
- Etwa wie lange das Anbinden dauert (rund 5 bis 10 Minuten pro Quelle)

Wo Quellen sich Zugangsdaten teilen, gleich sagen (Google Analytics und Google Sheets teilen den gleichen Service Account).

Gib die Gesamtzeit an.

Frag: **"So sieht der Plan aus. Sollen wir loslegen?"**

[VERIFY] Der Member hat bestätigt, welche Quellen angebunden werden, und ist bereit.

---

## PHASE 2: BASIS

### Voraussetzungen

#### Python 3.10 oder neuer
```bash
python3 --version
```
Erwartet: `Python 3.10.x` oder höher.

Falls nicht installiert oder zu alt:
- **macOS:** `brew install python@3.12` (Homebrew vorher installieren falls nötig: https://brew.sh)
- **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install python3.12 python3.12-venv`
- **Linux (Fedora):** `sudo dnf install python3.12`

#### Claude Code CLI
```bash
claude --version
```
Falls nicht installiert:
```bash
npm install -g @anthropic-ai/claude-code
```
Wenn npm fehlt, erst Node.js installieren: https://nodejs.org

[VERIFY] Beide Befehle zeigen Versionsnummern ohne Fehler.
Frag: "Alles steht. Sollen wir die Basis bauen?"

---

### CEO-GPT-Struktur anlegen

Wenn der Member schon ein CEO-GPT hat (aus `kontext`), den nutzen. Sonst anlegen.

```bash
mkdir -p scripts/examples data context/group credentials config
```

Das legt an:
- `scripts/`: hier wohnen alle Sammler
- `scripts/examples/`: Referenz-Sammler für gängige Quellen
- `data/`: hier landet die SQLite-Datenbank
- `context/group/`: hier wird die `key-metrics.md` erzeugt
- `credentials/`: für Google-Service-Account-JSON-Dateien (gitignored)
- `config/`: für den Zeitplan

Wenn es eine `.gitignore` gibt, sicherstellen, dass das drin steht:
```
.env
credentials/
data/*.db
```

[VERIFY]
```bash
ls -la scripts/ data/ context/group/ credentials/
```
Alle Ordner sind da.

---

### Python-Umgebung einrichten

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Leg `scripts/requirements.txt` an:
```
python-dotenv>=1.0.0
requests>=2.31.0
```

Basis-Pakete installieren:
```bash
pip install -r scripts/requirements.txt
```

[VERIFY]
```bash
.venv/bin/python -c "from dotenv import load_dotenv; import requests; print('Basis-Pakete OK')"
```
Erwartet: `Basis-Pakete OK`

---

### Datenbank anlegen

Leg `scripts/db.py` an. Das ist das Herz, die Datei verwaltet deine SQLite-Datenbank, legt Tabellen an und liefert Abfrage-Helfer.

Nimm den Code aus `scripts/db.py`. Die Logik bleibt wie sie ist, nur die Pfade greifen automatisch auf den aktuellen CEO-GPT zu.

[VERIFY]
```bash
cd /pfad/zum/workspace && .venv/bin/python scripts/db.py
```
Erwartet: `Datenbank initialisiert: .../data/data.db` mit Größenanzeige und leerer Tabellen-Liste.

---

### Konfigurations-Loader installieren

Leg `scripts/config.py` an. Liest API-Keys aus deiner `.env`, damit die Sammler sie nutzen können.

Code aus `scripts/config.py` übernehmen.

---

### Orchestrator installieren

Leg `scripts/collect.py` an. Das ist die Datei, die du läufst, wenn du Daten aus ALLEN Quellen sammeln willst. Sie findet automatisch jede `collect_*.py` im Skript-Ordner und startet sie.

Code aus `scripts/collect.py` übernehmen.

---

### Kennzahlen-Generator installieren

Leg `scripts/generate_metrics.py` an. Diese Datei liest die Datenbank und erzeugt eine lesbare `key-metrics.md`, die dein `/prime`-Befehl bei jeder Sitzung lädt.

Code aus `scripts/generate_metrics.py` übernehmen.

---

### Starter-Sammler installieren

Leg `scripts/collect_fx_rates.py` an. Das ist der Sammler ohne Zugangsdaten. Er beweist, dass die Pipeline läuft, indem er Wechselkurse von der Frankfurter-API holt.

Code aus `scripts/collect_fx_rates.py` übernehmen.

---

### Pipeline testen

Moment der Wahrheit. Wir lassen die ganze Sammel-Pipeline einmal durchlaufen.

```bash
cd /pfad/zum/workspace && .venv/bin/python scripts/collect.py --sources fx_rates
```

[VERIFY] Erwartete Ausgabe (auf stderr):
```
  Sammle fx_rates... OK (7 Datensätze)
[...] Fertig: 1 erfolgreich, 0 übersprungen, 0 Fehler, 7 Datensätze gesamt
```

Datenbank prüfen:
```bash
.venv/bin/python scripts/db.py
```

[VERIFY] Erwartet: Die Datenbank zeigt `fx_rates` in der Tabellen-Liste.

Kennzahlen erzeugen:
```bash
.venv/bin/python scripts/generate_metrics.py
```

[VERIFY] Erwartet: `Kennzahlen geschrieben nach: .../context/group/key-metrics.md`

Lies die Datei und zeig sie dem Member. Er sollte eine Wechselkurs-Tabelle mit aktuellen Kursen sehen und einen Frische-Block, der zeigt `fx_rates | heutiges Datum | verbunden`.

**Meilenstein:** "Deine Pipeline läuft. Der schwerste Teil ist durch. Datenbank, Sammler und Generator funktionieren alle. Ab hier klemmen wir nur noch deine echten Quellen ran. Eine nach der anderen. Bereit?"

---

## PHASE 3: QUELLEN ANBINDEN

> Mach nur die Abschnitte, die der Member in Phase 1 ausgewählt hat. Den Rest überspringen.
> Jeder Abschnitt ist eigenständig, Reihenfolge egal.
> Nach jeder Quelle einmal die Sammlung testen, bevor die nächste drankommt.

---

### `.env` anlegen

Bevor du irgendeine Quelle anbindest, leg die `.env` im CEO-GPT-Root an. Wir tragen pro Quelle dort die Zugangsdaten ein.

```bash
cp scripts/.env.example .env 2>/dev/null || touch .env
```

Wenn die Vorlage fehlt, leg `.env` mit diesem Start-Inhalt an:
```
# Daten: Umgebungsvariablen
# Pro Quelle tragen wir hier ein, wenn wir sie einrichten.
# Leere Werte werden übersprungen, du musst nur ausfüllen, was du nutzt.
```

---

### QUELLE: Stripe

> Überspringen, wenn der Member Stripe in Phase 1 nicht ausgewählt hat.

**Was du danach im Blick hast:** Tagesstände von MRR, aktiven Abos, neuen Abos, Kündigungen, Kündigungsrate und Monat-bis-heute-Umsatz. Mehrere Stripe-Konten gehen.

**Was du brauchst:**
- Einen Stripe API-Key (eingeschränkt, nur lesend)

**Zusätzliche Pakete:**
```bash
.venv/bin/pip install stripe
```

#### Stripe API-Key holen

1. https://dashboard.stripe.com/apikeys öffnen
2. Unter "Standard keys" siehst du "Secret key", "Reveal test key" zeigt das Format
3. Für Live-Daten brauchst du den **Live**-Secret-Key. Besser noch, leg einen **eingeschränkten Key** an.
   - "+ Create restricted key" klicken
   - Namen geben, z.B. "Daten Read Only"
   - ALLE Rechte auf **Read** setzen (nicht Write)
   - Notwendige Read-Rechte: Charges, Customers, Subscriptions, Balance
   - "Create key" klicken
   - Key kopieren (beginnt mit `rk_live_...`)

In `.env` speichern:
```
STRIPE_API_KEY_MAIN=rk_live_dein_key
```

**Mehrere Stripe-Konten:** Wenn du mehr als ein Stripe-Konto hast, leg pro Konto eine Zeile an:
```
STRIPE_API_KEY_AGENTUR=rk_live_...
STRIPE_API_KEY_SAAS=rk_live_...
```
Der Sammler findet automatisch jeden `STRIPE_API_KEY_*` und sammelt von allen.

[VERIFY]
```bash
.venv/bin/python -c "
import os; from dotenv import load_dotenv; load_dotenv()
import stripe
keys = {k: v for k, v in os.environ.items() if k.startswith('STRIPE_API_KEY_') and v.strip()}
for name, key in keys.items():
    stripe.api_key = key
    try:
        acct = stripe.Account.retrieve()
        print(f'{name}: verbunden ({acct.get(\"business_profile\", {}).get(\"name\", \"OK\")})')
    except Exception as e:
        print(f'{name}: FEHLER: {e}')
"
```
Erwartet: Jedes Konto zeigt "verbunden" mit dem Geschäftsnamen.

#### Stripe-Sammler installieren

Lies das Beispiel in `scripts/examples/stripe.py` und kopier es nach `scripts/collect_stripe.py`.

Anpassen, wenn nötig:
- Bei einzelner Währung notieren. Bei mehreren Währungen erkennt der Sammler die Standardwährung pro Konto automatisch.
- Der Sammler trackt von Haus aus MRR, Umsatz-MTD, aktive/neue/gekündigte Abos und Kündigungsrate.

[VERIFY]
```bash
cd /pfad/zum/workspace && .venv/bin/python scripts/collect_stripe.py
```
Erwartet: Zeigt MRR, Umsatz-MTD, aktive Abos je Konto.

Dann durch die Pipeline:
```bash
.venv/bin/python scripts/collect.py --sources stripe
```
Erwartet: `Sammle stripe... OK (X Datensätze)`

**"Stripe sitzt. Umsatz, MRR und Abo-Zahlen werden ab jetzt täglich getrackt."**

---

### QUELLE: Excel oder Google Sheets

> Überspringen, wenn keine Tabelle angebunden werden soll.

**Was du danach im Blick hast:** Beliebige Daten aus deiner Tabelle in der Datenbank. Typische Fälle: P&L, Marketing-KPIs, Kundenliste, Outreach-Stand, Projekt-Tracking.

**Wenn du eine lokale Excel-Datei hast:** Am einfachsten ist es, die Datei nach Google Sheets hochzuladen oder regelmäßig dorthin zu syncen. Wir bauen die Anbindung über Google Sheets, weil eine echte Schnittstelle existiert. Wenn du strikt bei Excel bleiben willst, sag Bescheid, dann bauen wir einen Sammler, der eine lokale `.xlsx` direkt liest.

**Was du brauchst:**
- Google Service Account (siehe nächster Abschnitt, falls noch nicht eingerichtet)
- Deine Google-Sheet-ID (aus der URL)

---

### Google Service Account (geteiltes Setup)

> Brauchst du, wenn du Google Analytics, Google Sheets oder beides nutzt.
> Nur einmal machen, der gleiche Service Account funktioniert für alle Google-Quellen.

**Was das ist:** Ein Google Service Account ist wie ein Roboter-Nutzer, der deine Google-Daten lesen darf. Er wird von Google Analytics und Google Sheets gleichermaßen genutzt.

1. https://console.cloud.google.com aufrufen
2. Falls noch kein Projekt da, eins anlegen (oder das von YouTube weiternutzen)
3. Linke Leiste: **IAM & Admin** > **Service Accounts**
4. **"+ CREATE SERVICE ACCOUNT"** klicken
5. Name: `daten-reader` (oder beliebig)
6. Beschreibung: "Lese-Zugriff für Daten-Sammlung"
7. **"Create and Continue"** klicken
8. Rolle kannst du überspringen, wir geben Zugriff später pro Dienst
9. **"Done"** klicken
10. Den neuen Service Account in der Liste anklicken, dann auf die E-Mail
11. Tab **"Keys"** öffnen
12. **"Add Key"** > **"Create new key"**
13. **JSON** wählen, **"Create"** klicken
14. Eine JSON-Datei wird runtergeladen. Das sind deine Zugangsdaten.

JSON-Datei verschieben:
```bash
cp ~/Downloads/dein-projekt-name-*.json credentials/google-service-account.json
```

In `.env`:
```
GOOGLE_SERVICE_ACCOUNT_JSON=./credentials/google-service-account.json
```

**Wichtig:** Notier dir die E-Mail-Adresse des Service Accounts (sieht aus wie `daten-reader@dein-projekt.iam.gserviceaccount.com`). Mit dieser Adresse teilst du gleich deine Sheets und Google-Analytics-Properties.

APIs aktivieren, je nach Quelle:
- **Google Sheets:** https://console.cloud.google.com/apis/library/sheets.googleapis.com: "Enable"
- **Google Analytics:** https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com: "Enable"
- **YouTube:** https://console.cloud.google.com/apis/library/youtube.googleapis.com: "Enable"

[VERIFY]
```bash
.venv/bin/python -c "
import json; from pathlib import Path
p = Path('credentials/google-service-account.json')
if p.exists():
    data = json.loads(p.read_text())
    print(f'Service Account: {data.get(\"client_email\", \"unbekannt\")}')
    print(f'Projekt: {data.get(\"project_id\", \"unbekannt\")}')
    print('Zugangsdaten gültig.')
else:
    print('FEHLER: credentials/google-service-account.json nicht gefunden')
"
```
Erwartet: Service-Account-E-Mail und Projektname werden gezeigt.

---

### QUELLE: Google Analytics 4 (deine Webseite)

> Überspringen, wenn Google Analytics nicht ausgewählt.
> Voraussetzung: Google Service Account oben eingerichtet.

**Was du danach im Blick hast:** Webseiten-Tagesstände. Sitzungen, Nutzer, neue Nutzer, Seitenaufrufe, Absprungrate, Engagement-Rate, dazu Aufschlüsselung der Traffic-Quellen.

**Zusätzliche Pakete:**
```bash
.venv/bin/pip install google-analytics-data google-auth
```

#### Google Analytics Property-ID holen

1. https://analytics.google.com öffnen
2. Zahnrad-Icon unten links (Admin)
3. In Spalte "Property" auf **"Property Settings"**
4. Property-ID steht oben, eine Zahl wie `123456789`

In `.env`:
```
GA4_PROPERTY_ID=deine_property_id
```

#### Service Account Zugriff geben

1. In Google Analytics Admin (Zahnrad)
2. Spalte "Property" → **"Property Access Management"**
3. Oben rechts **"+"** → **"Add users"**
4. E-Mail deines Service Accounts eingeben
5. Rolle **"Viewer"** (nur lesen reicht)
6. **"Add"**

[VERIFY] siehe Code-Beispiel im englischen Original, übersetz die Ausgabe-Meldung in: `Google Analytics verbunden! Sitzungen gestern: ...`

#### Google-Analytics-Sammler installieren

Lies `scripts/examples/google_analytics.py`, kopier es nach `scripts/collect_google_analytics.py`.

Standardmäßig werden Sitzungen, Nutzer, Seitenaufrufe, Absprungrate, Engagement-Rate und Top-Traffic-Quellen geholt. Wenn der Member zusätzliche Kennzahlen will (Conversions, Events), in die Metrik-Liste eintragen.

[VERIFY]
```bash
.venv/bin/python scripts/collect_google_analytics.py
.venv/bin/python scripts/collect.py --sources google_analytics
```

**"Google Analytics sitzt. Du trackst ab jetzt Webseiten-Traffic, Nutzer-Engagement und Quellen."**

---

### QUELLE: Google Sheets (P&L, KPIs, Listen)

> Überspringen, wenn keine Tabelle angebunden wird.
> Voraussetzung: Google Service Account eingerichtet.

#### Sheet-ID holen

Aus der URL: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`. Die ID ist alles zwischen `/d/` und `/edit`.

In `.env`:
```
GOOGLE_SHEET_ID=deine_sheet_id
GOOGLE_SHEET_TAB=Tabelle1
```

#### Sheet mit dem Service Account teilen

1. Google Sheet öffnen
2. "Freigeben" oben rechts
3. Service-Account-E-Mail einfügen
4. Rolle **"Betrachter"**
5. "Personen benachrichtigen" rausnehmen, ist eh ein Roboter
6. "Senden"

[VERIFY] siehe Code im englischen Original, deutsche Ausgabe: `Sheet verbunden, Tabs: ...`

#### Sheets-Sammler installieren

Lies `scripts/examples/google_sheets.py`. Kopier es passend zum Inhalt der Tabelle:
- P&L → `scripts/collect_pnl.py`
- Marketing-KPIs → `scripts/collect_marketing.py`
- Generisch → `scripts/collect_sheets.py`

**Wichtig:** Das Beispiel ist ein generischer Tabellen-Leser. Während des Setups passt du es an:
- Tabellen-Namen sinnvoll setzen (nicht das generische `sheet_*`)
- Spalten-Typen sauber definieren (Zahlen, Datum, Währung, nicht alles TEXT)
- Primary Key bestimmen
- Sonder-Formate parsen (Währungssymbole, Prozentzeichen, Datumsformat)

Frag den Member: **"Was steht in dieser Tabelle drin?"** Dann pass die `write()`-Funktion entsprechend an.

[VERIFY]
```bash
.venv/bin/python scripts/collect_sheets.py
.venv/bin/python scripts/collect.py --sources sheets
```

**"Deine Tabelle sitzt. Die Datenbank hat ab jetzt einen Tagesstand deiner Sheet-Daten."**

---

### QUELLE: YouTube

> Überspringen, wenn YouTube nicht ausgewählt.

**Was du danach im Blick hast:** Channel-Tagesstände (Abonnenten, Gesamtaufrufe, Video-Anzahl) plus Performance jedes Videos der letzten 30 Tage (Aufrufe, Likes, Kommentare).

**Was du brauchst:**
- YouTube API-Key (gratis, 3 Minuten)
- Deine YouTube-Channel-ID

**Zusätzliche Pakete:**
```bash
.venv/bin/pip install google-api-python-client google-auth
```

#### YouTube API-Key holen

1. https://console.cloud.google.com/apis/credentials öffnen
2. Falls noch kein Google-Cloud-Projekt, "Create Project" klicken, Name vergeben
3. Im Projekt "+ CREATE CREDENTIALS"
4. "API key" wählen
5. Key kopieren (Format: `AIzaSy...`)
6. "Close" klicken
7. YouTube Data API aktivieren: https://console.cloud.google.com/apis/library/youtube.googleapis.com → "Enable"

In `.env`:
```
YOUTUBE_API_KEY=dein_key
```

#### Channel-ID holen

1. https://www.youtube.com, eingeloggt
2. Profilbild oben rechts > "Mein Kanal"
3. URL anschauen: `youtube.com/channel/UCxxxxxxx` oder `youtube.com/@handle`
4. Bei Handle: https://www.youtube.com/account_advanced → Channel-ID (beginnt mit `UC`)

In `.env`:
```
YOUTUBE_CHANNEL_ID=deine_channel_id
```

#### YouTube-Sammler installieren

Lies `scripts/examples/youtube.py`, kopier es nach `scripts/collect_youtube.py`.

[VERIFY]
```bash
.venv/bin/python scripts/collect_youtube.py
.venv/bin/python scripts/collect.py --sources youtube
```

**"YouTube sitzt. Du trackst ab jetzt Abonnenten, Aufrufe und Video-Performance täglich."**

---

### QUELLE: Bitly (Link-Klicks)

> Überspringen, wenn nicht ausgewählt.

**Was du danach im Blick hast:** Tägliche Klick-Zahlen aller Bitly-Links, welche Links klicken, 1-Tages- und 30-Tages-Klicks, mit Tags zur Kategorisierung.

#### Access Token holen

1. https://app.bitly.com/settings/api/ öffnen
2. Unter "Access token" dein Bitly-Passwort eingeben
3. "Generate token" klicken
4. Token kopieren

In `.env`:
```
BITLY_ACCESS_TOKEN=dein_token
```

[VERIFY]
```bash
.venv/bin/python scripts/collect_bitly.py
.venv/bin/python scripts/collect.py --sources bitly
```

**"Bitly sitzt. Link-Klicks gehören ab jetzt zum täglichen Lauf."**

---

### QUELLE: Beliebige andere API (Custom)

> Für alles, was nicht in den Beispielen liegt.
> Typische Fälle: Calendly, HubSpot, Notion, Airtable, ConvertKit, Meta Ads, Google Ads, Shopify, Gumroad, Paddle, Lemlist, Instantly, Pipedrive.

**Wenn der Member eine Quelle hat, die nicht im Beispiel-Ordner liegt:**

1. Frag, welches Tool oder welche Plattform es ist
2. Such die API-Doku im Web
3. Bau einen eigenen Sammler nach dem Standard-Muster

**Das Muster für eigene Sammler** (gleiche Struktur wie der Stripe-Sammler):
- Modul-Docstring mit Quelle, Anforderungen, erzeugter Tabelle
- `load_dotenv` aus dem CEO-GPT-Root
- `collect()` Funktion, gibt `{source, status, data}` zurück, bei fehlendem Key `status="skipped"`, bei Fehler `status="error"`
- `write(conn, result, date)` legt Tabelle an, schreibt Datensätze, gibt Anzahl zurück
- `if __name__ == "__main__"` als Stand-alone-Test

**Schritte für einen eigenen Sammler:**
1. API-Doku der Plattform suchen
2. Authentifizierungs-Methode erkennen (API-Key, OAuth-Token)
3. Endpunkte finden, die die gewünschten Kennzahlen liefern
4. `collect()` schreiben, die diese Endpunkte aufruft
5. Tabelle entwerfen (Spalten, Primary Key)
6. `write()` schreiben, die die Daten speichert
7. Als `scripts/collect_{quelle}.py` speichern
8. Zugangsdaten in `.env` eintragen
9. Testen: `.venv/bin/python scripts/collect.py --sources {quelle}`

[VERIFY] Nach dem Bau jedes eigenen Sammlers:
```bash
.venv/bin/python scripts/collect_{quelle}.py
.venv/bin/python scripts/collect.py --sources {quelle}
```

---

## PHASE 4: KENNZAHLEN-DATEI BAUEN

> Wenn alle Sammler stehen, schneiden wir die `key-metrics.md` zu.

### Section-Funktionen ergänzen

Öffne `scripts/generate_metrics.py` und füg für jede angebundene Quelle eine Funktion hinzu. Pro Quelle eine Funktion im CUSTOMIZATION-Block. Pattern wie bei `section_fx_rates`.

Beispiel für Stripe:
```python
def section_stripe(conn):
    """Umsatz und Abo-Kennzahlen."""
    if not table_exists(conn, "stripe_daily"):
        return []
    lines = ["## Umsatz"]
    rows = query_all(conn, "SELECT * FROM stripe_daily WHERE date = (SELECT MAX(date) FROM stripe_daily)")
    if rows:
        lines.append(f"| Konto | MRR | Umsatz MTD | Aktive Abos | Kündigungsrate | Stand |")
        lines.append(f"|-------|-----|------------|-------------|----------------|-------|")
        for row in rows:
            lines.append(f"| {row['account']} | {fmt_currency(row['mrr'])} ({row['currency']}) | {fmt_currency(row['revenue_mtd'])} | {row['active_subscriptions']} | {fmt_pct(row['churn_rate'])} | {row['date']} |")
    lines.append("")
    return lines
```

### In SECTIONS registrieren

```python
SECTIONS = [
    section_fx_rates,
    section_stripe,
    section_google_analytics,
    section_youtube,
    # eigene Sections hier dazu
]
```

### Erzeugen und anschauen

```bash
.venv/bin/python scripts/generate_metrics.py
```

[VERIFY] Lies die erzeugte `context/group/key-metrics.md` und zeig sie dem Member. Sie sollte enthalten:
- Eine Section pro angebundene Quelle mit aktuellen Zahlen
- Eine Frische-Tabelle mit allen Tabellen und ihrem letzten Datensatz

Frag: **"Das sieht dein Mitarbeiter jede Sitzung. Deckt das die Zahlen ab, die du brauchst? Was fehlt, was soll anders?"**

Iterier, wenn nötig.

### Daten-Zugriffs-Referenz anlegen

"Du hast jetzt eine Datenbank voller Geschäftszahlen. Damit dein Mitarbeiter sie auch wirklich nutzen kann, braucht er einen Lageplan. Welche Tabellen gibt es, welche Spalten stecken drin, wie schreibt man die Abfragen. Den bauen wir jetzt."

Leg `reference/data-access.md` an. Eine lebende Doku, die deinem Mitarbeiter zeigt, wie er die Datenbank abfragt. Erzeug die Datei auf Basis dessen, was tatsächlich angebunden wurde.

**Pflicht-Abschnitte:**

1. **SQLite-Datenbank**: Ort (`data/data.db`), wie verbinden (Python-sqlite3-Beispiel mit `sqlite3.connect("data/data.db")`), Hinweis dass dein Mitarbeiter direkt SQL laufen lassen kann.
2. **Angebundene Quellen**: Tabelle: Quelle, Tabelle(n), Sammel-Skript, was sie trackt.
3. **Tabellen-Aufbau**: Pro Tabelle Spaltenname, Typ, Klartext-Beschreibung. Holst du aus `PRAGMA table_info(TABELLE)` und deinem Wissen aus dem Aufbau.
4. **Häufige Abfragen**: 5 bis 10 nützliche SQL-Beispiele. Mindestens: neuester Tagesstand pro Quelle, Trend der letzten 30 Tage, Monatsvergleich. Quellenübergreifende Joins sind besonders wertvoll (z.B. Webseiten-Traffic gegen Umsatz).
5. **Daten-Sammlung**: Wie man manuell sammelt (`python scripts/collect.py`), wie man einzelne Quellen läuft, wo die Logs liegen.

**Wie du das baust:**

1. Verbinde dich zur Datenbank, liste alle Tabellen: `SELECT name FROM sqlite_master WHERE type='table'`
2. Pro Tabelle Schema holen: `PRAGMA table_info(TABELLE)`
3. Pro Tabelle eine Section mit Spalten-Beschreibungen schreiben
4. Beispiel-Abfragen schneidern, passend zu den echten Quellen des Members
5. Hinweise zu Kennzahl-Typen einbauen wo relevant (Tagesstand, kumuliert, Periodensumme)

**Qualitätsmaßstab:** Eine spätere Sitzung soll die Datei lesen und sofort sinnvolle Abfragen laufen lassen können, ohne in den Quellcode zu schauen.

[VERIFY] Lies `reference/data-access.md` und prüfe, dass alle Tabellen mit Aufbau und Beispiel-Abfragen drin sind.

---

### In /prime und CLAUDE.md einbauen

"Hier kommts drauf an. Wir machen deinen Mitarbeiter daten-fit. Jede Sitzung weiß er deine Zahlen UND weiß, dass er eine ganze Datenbank abfragen kann."

**5a. /prime-Befehl aktualisieren**

Lies den existierenden Prime-Befehl (`.claude/commands/prime.md`). Mach diese drei Änderungen:

1. **key-metrics.md in die Leseliste.** Wo Dateien aufgelistet sind (nummeriert oder als Bullets unter "Read"), trag `context/group/key-metrics.md` ein, beschrieben als "Aktuelle Geschäftszahlen (automatisch aus der Datenbank)".

2. **data-access.md als On-Demand-Doku.** Wenn der Prime-Befehl einen "On-Demand"-Abschnitt hat, füg `reference/data-access.md` dazu, beschrieben als "Volle Tabellen-Schemas, SQL-Beispiele, Sammler-Details". Wenn es keinen On-Demand-Abschnitt gibt, leg einen an. Diese Dateien werden NICHT bei jedem /prime geladen, sondern nur wenn eine Aufgabe sie braucht.

3. **Summary-Abschnitt anpassen.** Wenn der /prime-Befehl einen "Summary"- oder "After reading"-Abschnitt hat, ergänz: **Daten-Stand**: Frische-Tabelle in key-metrics.md prüfen. Alles über 2 Tage alt markieren. Hinweis, dass live-SQL gegen `data/data.db` möglich ist.

Das sagt deinem Mitarbeiter zwei Dinge: (a) Er soll die Zahlen aus der Kennzahlen-Datei aktiv erwähnen, und (b) er hat direkten Datenbank-Zugriff für tiefere Analyse.

**Umgang mit current-data.md:**

`kontext` hat `context/current-data.md` für manuell gepflegte Kennzahlen und Lage angelegt. `daten` ersetzt den Kennzahlen-Teil automatisch. Lies die Datei und entscheide:

- **Wenn da manuell eingetragene Zahlen drin sind** (Umsatz, Abos, Traffic), die sind jetzt in `key-metrics.md`. Die Zahlen-Sections aus `current-data.md` raus.
- **Wenn da qualitative Notizen drin sind** (laufende Projekte, Blocker, Team-Notizen, strategische Beobachtungen), die bleiben. Wenn es hilft, Datei umbenennen, etwa `context/current-notes.md`.
- **Wenn da fast nur Zahlen drin sind**, kann sie komplett raus. Erklär dem Member: "Daten macht das jetzt automatisch. `key-metrics.md` aktualisiert sich jeden Morgen mit frischen Zahlen aus der Datenbank, du musst nichts mehr manuell pflegen."

**5b. CLAUDE.md aktualisieren**

Lies `CLAUDE.md` und mach folgende Anpassungen:

1. **CEO-GPT-Struktur-Abschnitt**: folgende Einträge an passender Stelle eintragen:
   - `data/` mit `data.db`: "SQLite-Datenbank, alle Kennzahlen, Tagesstände"
   - `context/group/key-metrics.md`: "Aktuelle Kennzahlen, automatisch aus der Datenbank"
   - `reference/data-access.md`: "Tabellen-Aufbau, SQL-Beispiele, Sammler-Details"
   - Unter `scripts/`: `db.py` (Datenbank), `config.py` (Env-Loader), `collect.py` (Orchestrator), `collect_*.py` (Sammler), `generate_metrics.py` (Generator)

2. **Commands**: `/update-data` eintragen, läuft `python scripts/collect.py`, holt frische Zahlen, regeneriert `key-metrics.md`. Hinweis, dass der tägliche Lauf das eh macht.

3. **Session-Workflow**: Hinweis, dass `/prime` aktuelle Kennzahlen aus der Datenbank lädt, und dass dein Mitarbeiter für tiefere Analyse direkt `data/data.db` abfragen kann (`reference/data-access.md` laden für Schemas und Beispiele).

4. **Daten-Abschnitt einfügen.** Erklärt späteren Sitzungen:
   - Alle Kennzahlen werden täglich nach `data/data.db` (SQLite) gesammelt
   - `key-metrics.md` wird automatisch erzeugt und über `/prime` geladen
   - Für direkte Abfragen `reference/data-access.md` laden, da stehen alle Schemas und Beispiel-Queries
   - Dein Mitarbeiter kann SQL direkt über Python ausführen: `sqlite3.connect("data/data.db")`

[VERIFY] Lies den aktualisierten /prime-Befehl und CLAUDE.md. Sicherstellen:
- /prime liest key-metrics.md
- /prime erwähnt Datenbank-Zugriff im Summary
- /prime listet data-access.md als On-Demand
- CLAUDE.md hat data/, Scripts und Hinweise zur Daten-Nutzung

**Meilenstein:** "Dein CEO-GPT ist jetzt daten-fit. Jede Sitzung startet mit frischen Zahlen, und dein Mitarbeiter weiß, dass er eine ganze Datenbank zur Verfügung hat. Lass mal `/prime` laufen, du siehst, dass deine echten Geschäftszahlen direkt mitgemeldet werden."

---

## PHASE 5: AUTOMATISIEREN

> Wir richten den täglichen Lauf ein, damit du nichts mehr manuell anstoßen musst.

**Wann soll das laufen?** Frag den Member. Klassisch ist früh morgens, zum Beispiel um 6 Uhr, dann sind die Zahlen da, bevor du am Schreibtisch sitzt. Manche bevorzugen Mitternacht, andere kurz vor Arbeitsbeginn. Egal welche Zeit, wichtig ist nur, dass der Rechner zu dem Zeitpunkt läuft.

### Variante A: macOS (launchd)

Leg `config/com.ceogpt.daten-collect.plist` an, mit den echten Pfaden des Members.

Die Vorlage liegt im `config/`-Ordner. Ersetz `WORKSPACE_PATH` mit dem absoluten Pfad zum CEO-GPT, und passe Hour/Minute auf die gewünschte Uhrzeit an.

Installieren:
```bash
cp config/com.ceogpt.daten-collect.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.ceogpt.daten-collect.plist
```

Testen:
```bash
launchctl start com.ceogpt.daten-collect
```

[VERIFY]
```bash
cat data/collect.log
```
Erwartet: Sammel-Output mit Erfolg, Übersprungen, Fehler pro Quelle.

Stoppen:
```bash
launchctl unload ~/Library/LaunchAgents/com.ceogpt.daten-collect.plist
```

### Variante B: Linux (cron)

```bash
crontab -e
```

Diese Zeile dazu (Pfad anpassen, Uhrzeit wählen):
```
0 6 * * * cd /pfad/zum/workspace && .venv/bin/python scripts/collect.py >> data/collect.log 2>&1
```

[VERIFY]
```bash
crontab -l | grep collect
```

---

### Wichtige Hinweise zur Planung

- **Der Rechner muss zur geplanten Zeit laufen.** Schläft er, läuft der Job beim nächsten Wachwerden (launchd) oder wird übersprungen (cron).
- **Bei Laptops (macOS):** Systemeinstellungen > Energie > "Automatischen Ruhezustand bei ausgeschaltetem Display verhindern" aktivieren, oder über Nacht ans Ladekabel.
- **Logs liegen in** `data/collect.log`.
- **Uhrzeit ändern** über die plist (Hour/Minute) oder den Cron-Ausdruck.

**Meilenstein:** "Automatik steht. Deine Pipeline läuft ab jetzt jeden Morgen, zieht frische Zahlen aus jeder Quelle und baut deine Kennzahlen-Datei neu. Bis du am Schreibtisch sitzt, weiß dein Mitarbeiter schon, wie das Business steht."

---

## PHASE 6: KOMPLETT-TEST

Lass die volle Pipeline einmal komplett durchlaufen:

```bash
.venv/bin/python scripts/collect.py
```

[VERIFY] Erwartet: Alle angebundenen Quellen "OK", übersprungene Quellen "SKIPPED", Zusammenfassung mit Gesamtzahl der Datensätze.

Dann die Kennzahlen prüfen:
```bash
.venv/bin/python scripts/generate_metrics.py
```

Zeig die fertige `context/group/key-metrics.md`.

**Schluss-Feier:** Sag mit Pause und Wärme:
> *"Dein Mitarbeiter sieht deine Zahlen jetzt jeden Morgen. Frag ihn, was du wissen willst."*

Was du gerade gebaut hast:
- Eine lokale SQLite-Datenbank in `data/data.db` mit Tagesständen
- {N} Sammler für deine echten Quellen
- Eine `key-metrics.md`, die sich jeden Morgen aktualisiert
- Einen automatischen Lauf, der alles macht, während du schläfst

Wenn du `/prime` läufst, lädt dein Mitarbeiter die aktuellen Werte und kann Fragen wie "Wie laufen wir diesen Monat gegen den letzten?" mit echten Zahlen beantworten.

---

## WAS ALS NÄCHSTES

*"Deine Zahlen sind drin. Jeden Morgen kommen sie frisch ins CEO-GPT.*

*Als Nächstes kommt die Intelligenz. Ich höre bei deinen Meetings mit und lese deine Team-Chats, damit ich auch die Sachen mitbekomme die nicht in Zahlen stehen. Setup-Zeit etwa 20 bis 30 Minuten.*

*Willst du gleich weitermachen, oder lieber Pause?"*

Wenn der Member "ja" oder "weiter" sagt, direkt `/install module-installs/intelligenz` starten.
Wenn er Pause will, warm verabschieden und sagen dass er einfach `/install module-installs/intelligenz` läuft wenn er soweit ist.

## Nützliche Gewohnheiten

Tagesstände zeigen ihren Wert erst, wenn Historie da ist. Nach sieben Tagen siehst du Trends, nach dreißig wird der Monatsvergleich aussagekräftig. Wenn dein Business wächst oder du neue Tools nutzt, leg einfach eine neue `collect_*.py` an. Der Orchestrator findet sie automatisch. Und ab jetzt kannst du deinen Mitarbeiter Sachen fragen wie "Wie läuft der Umsatz diesen Monat?" oder "Welche YouTube-Videos liefen letzte Woche am besten?". Für tiefere Analyse fragt er die Datenbank direkt ab.

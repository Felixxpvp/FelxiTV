"""
Stimme: Telegram-Bot für Felix' CEO-GPT

24/7 erreichbar über Telegram. Verbunden mit Supabase-Datenbank und Claude.
Kann Bestände abfragen, Verkäufe verbuchen und Kassenbuch führen.

Starten: python scripts/stimme.py
"""

import os
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv

WORKSPACE = Path(__file__).resolve().parent.parent
load_dotenv(WORKSPACE / ".env")

import anthropic
from supabase import create_client, Client
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


# ─── Konfiguration ────────────────────────────────────────────────────────────

BOT_TOKEN     = os.getenv("TELEGRAM_BOT_TOKEN", "")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SUPABASE_URL  = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY  = os.getenv("SUPABASE_KEY", "")
ALLOWED_CHAT  = os.getenv("TELEGRAM_CHAT_ID", "")

MODEL      = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024


# ─── Supabase ────────────────────────────────────────────────────────────────

def sb() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# ─── Tools für Claude ────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "produkte_abfragen",
        "description": "Aktuellen Bestand aller Verkaufsprodukte abfragen (Met, Säfte, Fleisch, Gemüse)",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "verkauf_verbuchen",
        "description": "Einen Verkauf eintragen. Reduziert automatisch den Produktbestand und schreibt ins Kassenbuch.",
        "input_schema": {
            "type": "object",
            "properties": {
                "produkt": {"type": "string", "description": "Name des verkauften Produkts"},
                "menge":   {"type": "number", "description": "Verkaufte Menge"},
                "preis":   {"type": "number", "description": "Gesamterlös in Euro"},
                "kanal":   {"type": "string", "description": "Direktverkauf, Online oder Markt"},
                "datum":   {"type": "string", "description": "YYYY-MM-DD, leer = heute"}
            },
            "required": ["produkt", "preis"]
        }
    },
    {
        "name": "ausgabe_eintragen",
        "description": "Eine Ausgabe ins Kassenbuch eintragen",
        "input_schema": {
            "type": "object",
            "properties": {
                "betrag":       {"type": "number", "description": "Betrag in Euro"},
                "kategorie":    {"type": "string", "description": "z.B. Saatgut, Jagd, Imkerei, Verpackung, Sonstiges"},
                "beschreibung": {"type": "string", "description": "Was wurde gekauft oder bezahlt"},
                "datum":        {"type": "string", "description": "YYYY-MM-DD, leer = heute"}
            },
            "required": ["betrag", "kategorie"]
        }
    },
    {
        "name": "kassenbuch_abfragen",
        "description": "Kassenstand, Einnahmen und Ausgaben abfragen",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "bestand_korrigieren",
        "description": "Bestand eines Produkts manuell setzen, z.B. nach Produktion oder Inventur",
        "input_schema": {
            "type": "object",
            "properties": {
                "produkt": {"type": "string", "description": "Name des Produkts"},
                "bestand": {"type": "number", "description": "Neuer Bestand"}
            },
            "required": ["produkt", "bestand"]
        }
    }
]


def fuehre_tool_aus(name: str, inp: dict) -> str:
    client = sb()
    today  = date.today().isoformat()

    try:
        if name == "produkte_abfragen":
            rows = client.table("produkte").select("*").order("kategorie").execute().data
            if not rows:
                return "Keine Produkte angelegt."
            lines = []
            kat = None
            for r in rows:
                if r["kategorie"] != kat:
                    kat = r["kategorie"]
                    lines.append(f"\n{kat}:")
                bestand = r.get("bestand") or 0
                einheit = r.get("einheit", "")
                preis   = f" | {r['preis']:.2f} €" if r.get("preis") else ""
                minb    = r.get("mindestbestand") or 0
                warn    = " ⚠️ LEER" if bestand == 0 else (" ⚠️ KNAPP" if bestand <= minb else "")
                lines.append(f"  {r['name']}: {bestand} {einheit}{preis}{warn}")
            return "\n".join(lines).strip()

        elif name == "verkauf_verbuchen":
            produkt = inp["produkt"]
            menge   = inp.get("menge", 1)
            preis   = inp["preis"]
            kanal   = inp.get("kanal", "Direktverkauf")
            datum   = inp.get("datum") or today

            client.table("verkauf").insert({
                "datum": datum, "produkt": produkt,
                "menge": menge, "preis": preis, "kanal": kanal
            }).execute()

            # Bestand reduzieren
            row = client.table("produkte").select("bestand").eq("name", produkt).execute().data
            neuer_bestand = None
            if row:
                neuer_bestand = max(0, (row[0].get("bestand") or 0) - menge)
                client.table("produkte").update({
                    "bestand": neuer_bestand,
                    "aktualisiert_am": datetime.utcnow().isoformat()
                }).eq("name", produkt).execute()

            # Einnahme ins Kassenbuch
            client.table("buchhaltung").insert({
                "datum": datum, "typ": "Einnahme",
                "kategorie": f"{produkt.split()[0]}-Verkauf",
                "betrag": preis,
                "beschreibung": f"{menge}x {produkt} ({kanal})"
            }).execute()

            rest = f" | Restbestand: {neuer_bestand}" if neuer_bestand is not None else ""
            return f"✅ {menge}x {produkt} für {preis:.2f} € eingetragen{rest}"

        elif name == "ausgabe_eintragen":
            client.table("buchhaltung").insert({
                "datum":        inp.get("datum") or today,
                "typ":          "Ausgabe",
                "kategorie":    inp["kategorie"],
                "betrag":       inp["betrag"],
                "beschreibung": inp.get("beschreibung", "")
            }).execute()
            return f"✅ {inp['betrag']:.2f} € für {inp['kategorie']} eingetragen"

        elif name == "kassenbuch_abfragen":
            rows = client.table("buchhaltung").select("*").order("datum", desc=True).limit(100).execute().data
            if not rows:
                return "Kassenbuch ist leer."
            einnahmen = sum(r["betrag"] for r in rows if r["typ"] == "Einnahme")
            ausgaben  = sum(r["betrag"] for r in rows if r["typ"] == "Ausgabe")
            saldo     = einnahmen - ausgaben
            lines = [
                f"Einnahmen: {einnahmen:.2f} €",
                f"Ausgaben:  {ausgaben:.2f} €",
                f"Saldo:     {saldo:+.2f} €",
                "",
                "Letzte Buchungen:"
            ]
            for r in rows[:5]:
                sign = "+" if r["typ"] == "Einnahme" else "-"
                lines.append(f"  {r['datum']}  {sign}{r['betrag']:.2f} €  {r['kategorie']}")
            return "\n".join(lines)

        elif name == "bestand_korrigieren":
            produkt = inp["produkt"]
            bestand = inp["bestand"]
            existing = client.table("produkte").select("id").eq("name", produkt).execute().data
            if existing:
                client.table("produkte").update({
                    "bestand": bestand,
                    "aktualisiert_am": datetime.utcnow().isoformat()
                }).eq("name", produkt).execute()
                return f"✅ {produkt}: Bestand auf {bestand} gesetzt"
            else:
                return f"⚠️ '{produkt}' nicht gefunden. Frag mich nach den verfügbaren Produkten."

        return f"Unbekanntes Tool: {name}"

    except Exception as e:
        return f"⚠️ Datenbankfehler: {str(e)[:300]}"


# ─── Kontext ─────────────────────────────────────────────────────────────────

def lade_kontext() -> str:
    teile = []
    for pfad, label in [
        ("context/business-info.md", "BUSINESS"),
        ("context/strategy.md",      "STRATEGIE"),
    ]:
        datei = WORKSPACE / pfad
        if datei.exists():
            inhalt = datei.read_text(encoding="utf-8", errors="ignore").strip()
            if inhalt:
                teile.append(f"=== {label} ===\n{inhalt}")

    return f"""Du bist der persönliche Mitarbeiter von Felix — Landwirt, Jäger, Einzelunternehmer.

{chr(10).join(teile)}

Du hast Zugriff auf die echte Datenbank mit Beständen, Verkäufen und Kassenbuch.

VERHALTEN:
- Kurz und direkt auf Deutsch antworten
- Bei Bestandsfragen immer Tool benutzen — nie aus dem Kopf antworten
- Wenn Felix sagt er hat etwas verkauft → verkauf_verbuchen aufrufen
- Wenn Felix sagt er hat etwas ausgegeben → ausgabe_eintragen aufrufen
- Zahlen immer mit 2 Dezimalstellen und € Zeichen
- Kein unnötiges Briefing"""


# ─── Claude mit Tool-Schleife ────────────────────────────────────────────────

def frage_claude(nachricht: str, verlauf: list) -> str:
    client   = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    messages = verlauf[-8:] + [{"role": "user", "content": nachricht}]

    try:
        response = client.messages.create(
            model=MODEL, max_tokens=MAX_TOKENS,
            system=lade_kontext(), tools=TOOLS, messages=messages
        )

        while response.stop_reason == "tool_use":
            tool_uses = [b for b in response.content if b.type == "tool_use"]
            results   = [
                {
                    "type":        "tool_result",
                    "tool_use_id": t.id,
                    "content":     fuehre_tool_aus(t.name, t.input)
                }
                for t in tool_uses
            ]
            messages = messages + [
                {"role": "assistant", "content": response.content},
                {"role": "user",      "content": results}
            ]
            response = client.messages.create(
                model=MODEL, max_tokens=MAX_TOKENS,
                system=lade_kontext(), tools=TOOLS, messages=messages
            )

        texts = [b for b in response.content if hasattr(b, "text")]
        return texts[0].text if texts else "Kein Ergebnis."

    except anthropic.AuthenticationError:
        return "⚠️ API-Key ungültig."
    except Exception as e:
        return f"⚠️ Fehler: {str(e)[:200]}"


# ─── Gesprächs-Speicher ───────────────────────────────────────────────────────

gespraeche: dict[int, list] = {}


# ─── Telegram Handler ────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not os.getenv("TELEGRAM_CHAT_ID"):
        env  = WORKSPACE / ".env"
        text = env.read_text(encoding="utf-8")
        env.write_text(text.replace("TELEGRAM_CHAT_ID=", f"TELEGRAM_CHAT_ID={chat_id}"), encoding="utf-8")
        os.environ["TELEGRAM_CHAT_ID"] = str(chat_id)

    await update.message.reply_text(
        "Mitarbeiter bereit.\n\n"
        "Beispiele:\n"
        "• Wie viel Met hab ich noch?\n"
        "• 5 Flaschen Met verkauft, 47,50 €\n"
        "• 45 € Saatgut ausgegeben\n"
        "• Kassenstand?\n"
        "• Was ist heute meine Priorität?\n\n"
        "/status — Überblick\n"
        "/neu — Gespräch zurücksetzen"
    )


async def cmd_neu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gespraeche[update.effective_chat.id] = []
    await update.message.reply_text("Gespräch zurückgesetzt.")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    antwort = frage_claude(
        "Kurzer Überblick: Kassenstand, welche Produkte sind vorrätig oder leer, nächste Priorität.",
        []
    )
    await update.message.reply_text(antwort)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    erlaubt = os.getenv("TELEGRAM_CHAT_ID", "")
    if erlaubt and str(chat_id) != erlaubt:
        await update.message.reply_text("Kein Zugriff.")
        return

    nachricht = (update.message.text or "").strip()
    if not nachricht:
        return

    verlauf = gespraeche.get(chat_id, [])
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    antwort = frage_claude(nachricht, verlauf)

    verlauf.append({"role": "user",      "content": nachricht})
    verlauf.append({"role": "assistant", "content": antwort})
    gespraeche[chat_id] = verlauf[-16:]

    await update.message.reply_text(antwort)


# ─── Start ───────────────────────────────────────────────────────────────────

def main():
    fehlend = [k for k, v in {
        "TELEGRAM_BOT_TOKEN": BOT_TOKEN,
        "ANTHROPIC_API_KEY":  ANTHROPIC_KEY,
        "SUPABASE_URL":       SUPABASE_URL,
        "SUPABASE_KEY":       SUPABASE_KEY,
    }.items() if not v]

    if fehlend:
        for k in fehlend:
            print(f"FEHLER: {k} fehlt in .env")
        return

    print("Mitarbeiter startet (Supabase-Anbindung aktiv)...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",  cmd_start))
    app.add_handler(CommandHandler("neu",    cmd_neu))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

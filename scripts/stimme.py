"""
Stimme: Telegram-Bot für Felix' CEO-GPT

Dieser Bot läuft auf deinem Rechner und verbindet dein Handy
mit deinem Mitarbeiter. Schick ihm Text oder Sprachnachrichten,
er antwortet mit dem vollen Business-Kontext.

Starten: python scripts/stimme.py
Stoppen: Ctrl+C im Terminal, oder Fenster schließen
"""

import asyncio
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

WORKSPACE = Path(__file__).resolve().parent.parent
load_dotenv(WORKSPACE / ".env")

import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


# ─── Konfiguration ───────────────────────────────────────────────────────────

BOT_TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN", "")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ALLOWED_CHAT = os.getenv("TELEGRAM_CHAT_ID", "")  # Leer = alle akzeptieren (wird beim ersten Start gesetzt)

# claude-haiku-4-5: schnell und günstig für tägliche Bot-Nutzung
MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024


# ─── Kontext laden ───────────────────────────────────────────────────────────

def lade_kontext() -> str:
    """Liest die CEO-GPT Kontext-Dateien und baut den System-Prompt."""
    teile = []

    dateien = [
        ("context/business-info.md",   "BUSINESS"),
        ("context/personal-info.md",   "PERSON"),
        ("context/strategy.md",        "STRATEGIE"),
        ("context/current-data.md",    "AKTUELLE LAGE"),
        ("context/group/key-metrics.md", "KENNZAHLEN"),
    ]

    for pfad, label in dateien:
        datei = WORKSPACE / pfad
        if datei.exists():
            inhalt = datei.read_text(encoding="utf-8", errors="ignore").strip()
            if inhalt:
                teile.append(f"=== {label} ===\n{inhalt}")

    kontext = "\n\n".join(teile) if teile else "Noch kein Kontext vorhanden."

    return f"""Du bist der persönliche Mitarbeiter von Felix. Du kennst sein Business in der Tiefe.

{kontext}

VERHALTEN:
- Antworte auf Deutsch, kurz und klar
- Du kennst Felix und sein Business — kein Briefing nötig
- Bei Zahlen-Fragen: schau in die Kennzahlen
- Bei Strategie-Fragen: schau in Strategie und Business-Info
- Sei direkt und praktisch, keine langen Einleitungen
- Wenn du etwas nicht weißt, sag es kurz
"""


# ─── Sprachnotiz transkribieren ───────────────────────────────────────────────

async def transkribiere(datei_pfad: str) -> str | None:
    """Versucht eine Audiodatei zu transkribieren. Gibt None zurück wenn nicht möglich."""
    try:
        import whisper  # type: ignore
        model = whisper.load_model("tiny")
        result = model.transcribe(datei_pfad, language="de")
        return result["text"].strip()
    except ImportError:
        pass

    try:
        import speech_recognition as sr  # type: ignore
        r = sr.Recognizer()
        with sr.AudioFile(datei_pfad) as source:
            audio = r.record(source)
        return r.recognize_google(audio, language="de-DE")
    except Exception:
        pass

    return None


# ─── Claude aufrufen ─────────────────────────────────────────────────────────

def frage_claude(nachricht: str, verlauf: list) -> str:
    """Schickt eine Nachricht an Claude und gibt die Antwort zurück."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

    messages = verlauf[-10:] + [{"role": "user", "content": nachricht}]

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=lade_kontext(),
            messages=messages,
        )
        return response.content[0].text
    except anthropic.AuthenticationError:
        return "⚠️ API-Key ungültig. Prüf den ANTHROPIC_API_KEY in der .env-Datei."
    except Exception as e:
        return f"⚠️ Fehler: {str(e)[:200]}"


# ─── Gesprächs-Speicher ───────────────────────────────────────────────────────

gespraeche: dict[int, list] = {}


# ─── Handler ─────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Beim ersten Start: Chat-ID in .env speichern
    if not ALLOWED_CHAT:
        env_pfad = WORKSPACE / ".env"
        inhalt = env_pfad.read_text(encoding="utf-8")
        inhalt = inhalt.replace("TELEGRAM_CHAT_ID=", f"TELEGRAM_CHAT_ID={chat_id}")
        env_pfad.write_text(inhalt, encoding="utf-8")
        os.environ["TELEGRAM_CHAT_ID"] = str(chat_id)

    await update.message.reply_text(
        "Mitarbeiter bereit.\n\n"
        "Schick mir Text oder eine Sprachnachricht — ich antworte mit dem vollen Business-Kontext.\n\n"
        "/neu — Gespräch zurücksetzen\n"
        "/status — aktueller Stand"
    )


async def cmd_neu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    gespraeche[chat_id] = []
    await update.message.reply_text("Gespräch zurückgesetzt.")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    antwort = frage_claude(
        "Gib mir in 3-4 Sätzen den aktuellen Stand: Business, Zahlen, Prioritäten.",
        []
    )
    await update.message.reply_text(antwort)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Zugriff prüfen
    erlaubt = os.getenv("TELEGRAM_CHAT_ID", "")
    if erlaubt and str(chat_id) != erlaubt:
        await update.message.reply_text("Kein Zugriff.")
        return

    nachricht = update.message.text or ""
    if not nachricht.strip():
        return

    verlauf = gespraeche.get(chat_id, [])

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    antwort = frage_claude(nachricht, verlauf)

    verlauf.append({"role": "user", "content": nachricht})
    verlauf.append({"role": "assistant", "content": antwort})
    gespraeche[chat_id] = verlauf[-20:]

    await update.message.reply_text(antwort)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    erlaubt = os.getenv("TELEGRAM_CHAT_ID", "")
    if erlaubt and str(chat_id) != erlaubt:
        return

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    # Audiodatei herunterladen
    voice = update.message.voice
    datei = await context.bot.get_file(voice.file_id)

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        tmp_pfad = tmp.name

    await datei.download_to_drive(tmp_pfad)

    # Transkribieren
    text = await transkribiere(tmp_pfad)
    Path(tmp_pfad).unlink(missing_ok=True)

    if not text:
        await update.message.reply_text(
            "Sprachnachrichten werden erst unterstützt wenn ffmpeg installiert ist.\n"
            "Schreib die Nachricht kurz als Text, ich antworte sofort."
        )
        return

    # Antworten
    verlauf = gespraeche.get(chat_id, [])
    antwort = frage_claude(text, verlauf)

    verlauf.append({"role": "user", "content": f"[Sprachnachricht]: {text}"})
    verlauf.append({"role": "assistant", "content": antwort})
    gespraeche[chat_id] = verlauf[-20:]

    await update.message.reply_text(f"_{text}_\n\n{antwort}", parse_mode="Markdown")


# ─── Start ────────────────────────────────────────────────────────────────────

def main():
    if not BOT_TOKEN:
        print("FEHLER: TELEGRAM_BOT_TOKEN fehlt in .env")
        return
    if not ANTHROPIC_KEY:
        print("FEHLER: ANTHROPIC_API_KEY fehlt in .env")
        return

    print("Mitarbeiter startet...")
    print(f"Bot läuft. Öffne Telegram und schreib deinen Bot an.")
    print("Stoppen: Ctrl+C")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("neu",   cmd_neu))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    app.run_polling()


if __name__ == "__main__":
    main()

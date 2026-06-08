"""
Daten: Konfigurations-Loader

Liest Zugangsdaten aus der .env im Workspace-Root.
Stellt Helfer für API-Keys und Google-Zugangsdaten bereit.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env aus dem Workspace-Root laden (eine Ebene über scripts/)
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = WORKSPACE_ROOT / ".env"

load_dotenv(ENV_PATH)


def get_env(key, required=True):
    """
    Umgebungsvariable holen. Gibt None zurück, wenn nicht gesetzt.
    Aufrufer fangen fehlende Zugangsdaten sauber ab (Sammler wird übersprungen).
    """
    value = os.getenv(key, "").strip()
    if not value:
        return None
    return value


def get_google_credentials_path():
    """
    Pfad zur Google-Service-Account-JSON-Datei holen.
    Löst relative Pfade gegen den Workspace-Root auf.
    """
    path = get_env("GOOGLE_SERVICE_ACCOUNT_JSON")
    if path is None:
        return None
    full_path = Path(path)
    if not full_path.is_absolute():
        full_path = WORKSPACE_ROOT / path
    if not full_path.exists():
        return None
    return str(full_path)

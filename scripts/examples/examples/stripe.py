"""
Daten: Stripe-Umsatz-Sammler (Beispiel)

Holt Umsatz, Abo- und Kündigungs-Kennzahlen aus Stripe.
Mehrere Konten gehen, leg pro Konto STRIPE_API_KEY_DEINNAME=sk_live_... in der .env an.

Diese Datei nach scripts/collect_stripe.py kopieren, um sie zu aktivieren.

Voraussetzungen:
    Mindestens ein STRIPE_API_KEY_* in der .env
    Keys holen unter: dashboard.stripe.com/apikeys (eingeschränkt, nur lesend)

Erzeugte Tabelle: stripe_daily
Zusätzliches pip: stripe
"""

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

try:
    import stripe
except ImportError:
    raise ImportError(
        "Paket 'stripe' fehlt, installier es mit: pip install stripe"
    )


def _collect_account(api_key, account_name):
    """Daten von einem einzelnen Stripe-Konto holen."""
    stripe.api_key = api_key

    # Währung des Kontos erkennen
    try:
        account = stripe.Account.retrieve()
        currency = (account.get("default_currency") or "usd").upper()
    except Exception:
        currency = "USD"

    # Grenzen des aktuellen Monats
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_start_ts = int(month_start.timestamp())

    # Aktive Abos plus MRR-Berechnung
    active_subs = 0
    mrr = 0.0
    subs_iter = stripe.Subscription.list(status="active", limit=100)
    for sub in subs_iter.auto_paging_iter():
        active_subs += 1
        for item in sub.get("items", {}).get("data", []):
            amount = item.get("price", {}).get("unit_amount", 0) or 0
            interval = item.get("price", {}).get("recurring", {}).get("interval", "month")
            qty = item.get("quantity", 1) or 1
            monthly = amount * qty / 100
            if interval == "year":
                monthly /= 12
            elif interval == "week":
                monthly *= 4.33
            mrr += monthly

    # Neue Abos in diesem Monat
    new_subs = 0
    for _ in stripe.Subscription.list(
        created={"gte": month_start_ts}, limit=100
    ).auto_paging_iter():
        new_subs += 1

    # Umsatz in diesem Monat (erfolgreiche Zahlungen)
    revenue_mtd = 0.0
    for charge in stripe.Charge.list(
        created={"gte": month_start_ts}, limit=100
    ).auto_paging_iter():
        if charge.status == "succeeded":
            revenue_mtd += (charge.amount or 0) / 100

    # In diesem Monat gekündigt
    canceled = 0
    for sub in stripe.Subscription.list(
        status="canceled", limit=100
    ).auto_paging_iter():
        if sub.canceled_at and sub.canceled_at >= month_start_ts:
            canceled += 1

    churn_rate = (canceled / active_subs * 100) if active_subs > 0 else 0.0

    return {
        "account": account_name,
        "currency": currency,
        "mrr": round(mrr, 2),
        "active_subscriptions": active_subs,
        "new_subscriptions": new_subs,
        "canceled": canceled,
        "revenue_mtd": round(revenue_mtd, 2),
        "churn_rate": round(churn_rate, 2),
    }


def collect():
    """Stripe-Daten von allen konfigurierten Konten holen."""
    # Alle STRIPE_API_KEY_* Variablen in der .env finden
    accounts = {}
    for key, value in os.environ.items():
        if key.startswith("STRIPE_API_KEY_") and value.strip():
            name = key.replace("STRIPE_API_KEY_", "").lower()
            accounts[name] = value.strip()

    if not accounts:
        return {
            "source": "stripe", "status": "skipped",
            "reason": "Keine STRIPE_API_KEY_* in .env gefunden. "
                      "Trag STRIPE_API_KEY_MAIN=sk_live_... ein "
                      "(Keys gibt es unter dashboard.stripe.com/apikeys)"
        }

    results = {}
    errors = []
    for name, api_key in accounts.items():
        try:
            results[name] = _collect_account(api_key, name)
        except Exception as e:
            errors.append(f"{name}: {e}")

    if not results:
        return {
            "source": "stripe", "status": "error",
            "reason": "; ".join(errors)
        }

    return {
        "source": "stripe",
        "status": "success",
        "data": {"accounts": results, "errors": errors}
    }


def write(conn, result, date):
    """Stripe-Daten in die Datenbank schreiben. Gibt Anzahl der Datensätze zurück."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stripe_daily (
            date TEXT NOT NULL,
            account TEXT NOT NULL,
            currency TEXT,
            mrr REAL,
            revenue_mtd REAL,
            active_subscriptions INTEGER,
            new_subscriptions INTEGER,
            canceled INTEGER,
            churn_rate REAL,
            collected_at TEXT,
            PRIMARY KEY (date, account)
        )
    """)

    if result.get("status") != "success":
        conn.commit()
        return 0

    collected_at = datetime.now(timezone.utc).isoformat()
    records = 0

    for name, data in result["data"]["accounts"].items():
        conn.execute(
            "INSERT OR REPLACE INTO stripe_daily "
            "(date, account, currency, mrr, revenue_mtd, active_subscriptions, "
            "new_subscriptions, canceled, churn_rate, collected_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (date, name, data["currency"], data["mrr"], data["revenue_mtd"],
             data["active_subscriptions"], data["new_subscriptions"],
             data["canceled"], data["churn_rate"], collected_at)
        )
        records += 1

    conn.commit()
    return records


if __name__ == "__main__":
    result = collect()
    if result["status"] == "success":
        for name, data in result["data"]["accounts"].items():
            print(f"\n{data['account']} ({data['currency']}):")
            print(f"  MRR: {data['mrr']:,.2f}")
            print(f"  Umsatz MTD: {data['revenue_mtd']:,.2f}")
            print(f"  Aktive Abos: {data['active_subscriptions']}")
            print(f"  Neu: {data['new_subscriptions']}, Gekündigt: {data['canceled']}")
    else:
        print(f"{result['status']}: {result.get('reason', '')}")

# fx_rates.py — v1.0.0
# FX rates collector via Open Exchange Rates API.
# Good first collector to test — shows the pattern with minimal setup.

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import OPEN_EXCHANGE_RATES_APP_ID, DB_PATH
from db import get_conn

import requests

CURRENCIES = ["AUD", "CAD", "EUR", "GBP", "JPY", "NZD", "SGD"]


def collect():
    today = date.today().isoformat()

    if OPEN_EXCHANGE_RATES_APP_ID:
        url = f"https://openexchangerates.org/api/latest.json?app_id={OPEN_EXCHANGE_RATES_APP_ID}&base=USD"
    else:
        # Free endpoint (limited currencies, no key needed)
        url = "https://open.er-api.com/v6/latest/USD"

    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        print(f"FX Rates: API error {resp.status_code}")
        return

    data = resp.json()
    rates = data.get("rates", {})

    conn = get_conn(DB_PATH)
    c = conn.cursor()
    saved = 0

    for currency in CURRENCIES:
        if currency in rates:
            c.execute("""
                INSERT OR REPLACE INTO fx_rates (date, currency, rate_from_usd)
                VALUES (?, ?, ?)
            """, (today, currency, rates[currency]))
            saved += 1

    conn.commit()
    conn.close()
    print(f"FX Rates: {saved} currencies saved for {today}")


if __name__ == "__main__":
    collect()

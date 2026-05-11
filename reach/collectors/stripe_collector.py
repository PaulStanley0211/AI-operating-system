# stripe_collector.py — v1.0.0
# Stripe metrics collector: MRR, ARR, active subscribers, new/churned customers.
# Uses a restricted API key with read-only access.

import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import STRIPE_SECRET_KEY, DB_PATH
from db import get_conn

import stripe as stripe_lib


def collect():
    if not STRIPE_SECRET_KEY:
        print("Stripe: skipping — STRIPE_SECRET_KEY not set")
        return

    stripe_lib.api_key = STRIPE_SECRET_KEY
    today = date.today().isoformat()

    # Active subscriptions → MRR
    subscriptions = stripe_lib.Subscription.list(status="active", limit=100)
    active_count = 0
    mrr_cents = 0

    for sub in subscriptions.auto_paging_iter():
        active_count += 1
        for item in sub["items"]["data"]:
            plan = item.get("price") or item.get("plan", {})
            amount = plan.get("unit_amount", 0) or 0
            interval = plan.get("interval", "month")
            # Normalize to monthly
            if interval == "year":
                amount = amount // 12
            elif interval == "week":
                amount = amount * 4
            mrr_cents += amount

    arr_cents = mrr_cents * 12

    # New customers (last 30 days)
    cutoff = int((datetime.now() - timedelta(days=30)).timestamp())
    new_customers = stripe_lib.Customer.list(created={"gte": cutoff}, limit=100)
    new_count = len(list(new_customers.auto_paging_iter()))

    # Churned (canceled in last 30 days — approximation)
    canceled = stripe_lib.Subscription.list(
        status="canceled",
        created={"gte": cutoff},
        limit=100
    )
    churned_count = len(list(canceled.auto_paging_iter()))

    conn = get_conn(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO stripe_daily
        (date, mrr_cents, arr_cents, active_subscribers, new_customers, churned_customers)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (today, mrr_cents, arr_cents, active_count, new_count, churned_count))
    conn.commit()
    conn.close()

    print(f"Stripe: MRR ${mrr_cents/100:,.2f} | {active_count} subscribers | {new_count} new | {churned_count} churned")


if __name__ == "__main__":
    collect()

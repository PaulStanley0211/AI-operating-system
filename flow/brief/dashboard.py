# dashboard.py — v1.0.0
# Generates a chart image of the primary metric over the last 30 days.
# Dark theme, clean formatting, 800x400 PNG.

import os
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = Path(__file__).parent.parent.parent
DB_PATH = ROOT / "reach" / "data" / "data.db"
OUTPUT_PATH = Path(__file__).parent / "dashboard.png"

DASHBOARD_METRIC = os.getenv("DASHBOARD_METRIC", "youtube_subscribers")

METRIC_CONFIG = {
    "youtube_subscribers": {
        "table": "youtube_daily",
        "column": "subscribers",
        "label": "Subscribers",
        "color": "#FF4444",
    },
    "youtube_views_30d": {
        "table": "youtube_daily",
        "column": "views_30d",
        "label": "Views (30d)",
        "color": "#4488FF",
    },
    "stripe_mrr": {
        "table": "stripe_daily",
        "column": "mrr_cents",
        "label": "MRR ($)",
        "color": "#44FF88",
        "divisor": 100,
    },
}


def generate():
    if not DB_PATH.exists():
        print("Dashboard: no data.db found — skipping chart generation")
        return None

    config = METRIC_CONFIG.get(DASHBOARD_METRIC, METRIC_CONFIG["youtube_subscribers"])
    table = config["table"]
    column = config["column"]

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    # Check table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    if not c.fetchone():
        print(f"Dashboard: table '{table}' not found — skipping")
        conn.close()
        return None

    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    c.execute(f"SELECT date, {column} FROM {table} WHERE date >= ? ORDER BY date", (cutoff,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("Dashboard: no data for chart — skipping")
        return None

    divisor = config.get("divisor", 1)
    dates = [datetime.strptime(r[0][:10], "%Y-%m-%d") for r in rows]
    values = [r[1] / divisor if r[1] else 0 for r in rows]

    # Dark theme chart
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor("#1a1a1a")
    ax.set_facecolor("#1a1a1a")

    ax.plot(dates, values, color=config["color"], linewidth=2.5, marker="o", markersize=4)
    ax.fill_between(dates, values, alpha=0.15, color=config["color"])

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=30, ha="right", fontsize=9, color="#aaaaaa")
    plt.yticks(fontsize=9, color="#aaaaaa")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#333333")
    ax.spines["bottom"].set_color("#333333")
    ax.tick_params(colors="#aaaaaa")
    ax.grid(True, alpha=0.1, color="#444444")

    latest = values[-1] if values else 0
    label_text = f"{config['label']}: {latest:,.0f}"
    ax.set_title(label_text, fontsize=14, color="white", pad=15, fontweight="bold")

    today_str = date.today().strftime("%B %d, %Y")
    fig.text(0.99, 0.01, today_str, ha="right", va="bottom", fontsize=8, color="#666666")

    plt.tight_layout()
    plt.savefig(str(OUTPUT_PATH), dpi=150, bbox_inches="tight", facecolor="#1a1a1a")
    plt.close()

    print(f"Dashboard: chart saved to {OUTPUT_PATH}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    generate()

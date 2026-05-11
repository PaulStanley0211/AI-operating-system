# generate_metrics.py — v1.0.0
# Queries data.db and writes a fresh reach/metrics.md.
# Run after each collection run, or on demand.

import sqlite3
from datetime import date, datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "data.db"
INTEL_DB_PATH = Path(__file__).parent / "data" / "intel.db"
OUTPUT_PATH = Path(__file__).parent / "metrics.md"


def get_conn(path):
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def freshness_flag(date_str: str) -> str:
    if not date_str:
        return "⚠️ No data"
    try:
        d = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
        delta = (date.today() - d).days
        if delta == 0:
            return "✅ Today"
        elif delta == 1:
            return "✅ Yesterday"
        elif delta <= 3:
            return f"⚠️ {delta} days ago"
        else:
            return f"🔴 {delta} days ago — stale"
    except Exception:
        return "⚠️ Unknown"


def build_metrics() -> str:
    lines = [
        "# Key Metrics",
        "",
        f"> Auto-generated from database. Last updated: {date.today().isoformat()}",
        f"> Source: `reach/data/data.db` | Regenerate: `python reach/generate_metrics.py`",
        "",
    ]

    if not DB_PATH.exists():
        lines.append("*No data.db found. Install the Intelligence Node to connect data sources.*")
        return "\n".join(lines)

    conn = get_conn(DB_PATH)
    c = conn.cursor()

    # Check which tables exist
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {r[0] for r in c.fetchall()}

    freshness_rows = []

    # YouTube
    if "youtube_daily" in tables:
        c.execute("SELECT * FROM youtube_daily ORDER BY date DESC LIMIT 1")
        row = c.fetchone()
        if row:
            lines += [
                "## YouTube",
                "| Metric | Value | As Of |",
                "|--------|-------|-------|",
                f"| Subscribers | {row['subscribers']:,} | {row['date']} |",
                f"| Total Views | {row['total_views']:,} | {row['date']} |",
                f"| Views (30d) | {row['views_30d']:,} | {row['date']} |",
                "",
            ]
            freshness_rows.append(("youtube_daily", row["date"]))

    if "youtube_videos" in tables:
        c.execute("""
            SELECT title, views, likes FROM youtube_videos
            WHERE date >= date('now', '-30 days')
            ORDER BY views DESC LIMIT 5
        """)
        videos = c.fetchall()
        if videos:
            lines.append("**Top Videos (last 30 days):**")
            lines.append("| Title | Views | Likes |")
            lines.append("|-------|-------|-------|")
            for v in videos:
                title = v["title"][:50] + "..." if len(v["title"]) > 50 else v["title"]
                lines.append(f"| {title} | {v['views']:,} | {v['likes']:,} |")
            lines.append("")

    # Stripe
    if "stripe_daily" in tables:
        c.execute("SELECT * FROM stripe_daily ORDER BY date DESC LIMIT 1")
        row = c.fetchone()
        if row:
            lines += [
                "## Revenue (Stripe)",
                "| Metric | Value | As Of |",
                "|--------|-------|-------|",
                f"| MRR | ${row['mrr_cents']/100:,.2f} | {row['date']} |",
                f"| ARR | ${row['arr_cents']/100:,.2f} | {row['date']} |",
                f"| Active Subscribers | {row['active_subscribers']:,} | {row['date']} |",
                "",
            ]
            freshness_rows.append(("stripe_daily", row["date"]))

    # FX Rates
    if "fx_rates" in tables:
        c.execute("SELECT currency, rate_from_usd, date FROM fx_rates ORDER BY date DESC, currency")
        rows = c.fetchall()
        if rows:
            latest_date = rows[0]["date"]
            lines += ["## Exchange Rates", "| Currency | Rate (from USD) | As Of |", "|----------|----------------|-------|"]
            for r in rows:
                if r["date"] == latest_date:
                    lines.append(f"| {r['currency']} | {r['rate_from_usd']:.4f} | {r['date']} |")
            lines.append("")
            freshness_rows.append(("fx_rates", latest_date))

    conn.close()

    # Freshness summary
    lines += ["## Data Freshness", "| Source | Latest Record | Status |", "|--------|---------------|--------|"]
    for source, latest in freshness_rows:
        lines.append(f"| {source} | {latest} | {freshness_flag(latest)} |")
    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    content = build_metrics()
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Metrics written to {OUTPUT_PATH}")

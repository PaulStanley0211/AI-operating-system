# refresh_dashboard.py — v1.0.0
# Reads all GTD files and regenerates flow/gtd/dashboard.md.
# Run after any GTD update: python flow/refresh_dashboard.py

from datetime import datetime
from pathlib import Path

GTD_DIR = Path(__file__).parent / "gtd"
DASHBOARD_PATH = GTD_DIR / "dashboard.md"


def count_items(filepath: Path) -> int:
    """Count non-empty, non-header lines in a markdown file."""
    if not filepath.exists():
        return 0
    lines = filepath.read_text(encoding="utf-8").splitlines()
    return sum(1 for line in lines if line.strip() and not line.startswith("#") and not line.startswith(">"))


def get_top_items(filepath: Path, tag: str = None, limit: int = 3) -> list[str]:
    """Get first N action items, optionally filtered by context tag."""
    if not filepath.exists():
        return []
    lines = filepath.read_text(encoding="utf-8").splitlines()
    items = []
    in_section = tag is None

    for line in lines:
        if tag and line.strip() == f"## {tag}":
            in_section = True
            continue
        if tag and in_section and line.startswith("## "):
            break
        if in_section and line.strip().startswith("- [ ]"):
            items.append(line.strip()[6:].strip())
            if len(items) >= limit:
                break
    return items


def get_waiting_overdue(filepath: Path) -> list[str]:
    """Find waiting-for items that appear overdue (date in past)."""
    if not filepath.exists():
        return []

    today = datetime.now().date()
    overdue = []
    lines = filepath.read_text(encoding="utf-8").splitlines()

    for line in lines:
        if "|" in line and "---" not in line and "Expected By" not in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 4:
                try:
                    due = datetime.strptime(parts[3][:10], "%Y-%m-%d").date()
                    if due < today:
                        overdue.append(f"{parts[0]} (due {parts[3][:10]})")
                except Exception:
                    pass
    return overdue


def build_dashboard() -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    inbox_count = count_items(GTD_DIR / "inbox.md")
    project_lines = (GTD_DIR / "projects.md").read_text(encoding="utf-8") if (GTD_DIR / "projects.md").exists() else ""
    project_count = project_lines.count("### ")
    next_action_count = count_items(GTD_DIR / "next-actions.md")
    waiting_count = count_items(GTD_DIR / "waiting-for.md")

    top_me = get_top_items(GTD_DIR / "next-actions.md", "## @me")
    top_claude = get_top_items(GTD_DIR / "next-actions.md", "## @claude")
    overdue = get_waiting_overdue(GTD_DIR / "waiting-for.md")

    lines = [
        "# GTD Dashboard",
        f"\n> Last refreshed: {now}",
        "\n## Status",
        "| List | Count |",
        "|------|-------|",
        f"| Inbox (unprocessed) | {inbox_count} |",
        f"| Active projects | {project_count} |",
        f"| Next actions | {next_action_count} |",
        f"| Waiting for | {waiting_count} |",
    ]

    if top_me:
        lines += ["\n## Top Next Actions (@me)"]
        for item in top_me:
            lines.append(f"- [ ] {item}")

    if top_claude:
        lines += ["\n## For Claude (@claude)"]
        for item in top_claude:
            lines.append(f"- [ ] {item}")

    if overdue:
        lines += ["\n## ⚠️ Waiting For — Overdue"]
        for item in overdue:
            lines.append(f"- {item}")

    return "\n".join(lines)


if __name__ == "__main__":
    content = build_dashboard()
    DASHBOARD_PATH.write_text(content, encoding="utf-8")
    print(f"Dashboard refreshed: {DASHBOARD_PATH}")

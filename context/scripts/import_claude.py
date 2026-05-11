# import_claude.py — v1.0.0
# Imports Claude conversation export into context/references/conversations/claude/
# Usage: python context/scripts/import_claude.py path/to/conversations.json

import sys
import json
import re
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "references" / "conversations" / "claude"
MIN_CHARS = 500  # Skip very short conversations


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:60]


def main():
    if len(sys.argv) < 2:
        print("Usage: python context/scripts/import_claude.py path/to/conversations.json")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        conversations = json.load(f)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    saved = 0
    skipped = 0

    for convo in conversations:
        name = convo.get("name") or convo.get("title") or "Untitled"
        created = convo.get("created_at", "")
        if created:
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                date_str = dt.strftime("%Y-%m-%d")
            except Exception:
                date_str = "unknown"
        else:
            date_str = "unknown"

        messages = convo.get("chat_messages") or convo.get("messages") or []
        lines = []
        for msg in messages:
            role = msg.get("sender") or msg.get("role") or "unknown"
            content = msg.get("text") or msg.get("content") or ""
            if isinstance(content, list):
                content = " ".join(
                    c.get("text", "") if isinstance(c, dict) else str(c)
                    for c in content
                )
            if content:
                lines.append(f"**{role.upper()}:** {content}")

        full_text = "\n\n".join(lines)
        if len(full_text) < MIN_CHARS:
            skipped += 1
            continue

        filename = f"{date_str}_{slugify(name)}.md"
        output_file = OUTPUT_DIR / filename
        output_file.write_text(
            f"# {name}\n\n*Imported from Claude export — {date_str}*\n\n---\n\n{full_text}",
            encoding="utf-8"
        )
        saved += 1

    print(f"Imported {saved} conversations to {OUTPUT_DIR}")
    print(f"Skipped {skipped} (too short)")


if __name__ == "__main__":
    main()

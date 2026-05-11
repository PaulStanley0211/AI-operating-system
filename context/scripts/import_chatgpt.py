# import_chatgpt.py — v1.0.0
# Imports ChatGPT conversation export into context/references/conversations/chatgpt/
# Usage: python context/scripts/import_chatgpt.py path/to/conversations.json

import sys
import json
import re
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "references" / "conversations" / "chatgpt"
MIN_CHARS = 500


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:60]


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)
        return " ".join(parts)
    if isinstance(content, dict):
        return content.get("text", "") or content.get("parts", [""])[0] if isinstance(content.get("parts"), list) else ""
    return ""


def main():
    if len(sys.argv) < 2:
        print("Usage: python context/scripts/import_chatgpt.py path/to/conversations.json")
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
        title = convo.get("title") or "Untitled"
        created_ts = convo.get("create_time")
        date_str = datetime.fromtimestamp(created_ts).strftime("%Y-%m-%d") if created_ts else "unknown"

        mapping = convo.get("mapping") or {}
        messages = []
        for node in mapping.values():
            msg = node.get("message")
            if not msg:
                continue
            role = msg.get("author", {}).get("role", "unknown")
            if role in ("system",):
                continue
            content = extract_text(msg.get("content") or "")
            if content:
                messages.append((msg.get("create_time") or 0, role, content))

        messages.sort(key=lambda x: x[0])
        lines = [f"**{role.upper()}:** {text}" for _, role, text in messages]
        full_text = "\n\n".join(lines)

        if len(full_text) < MIN_CHARS:
            skipped += 1
            continue

        filename = f"{date_str}_{slugify(title)}.md"
        output_file = OUTPUT_DIR / filename
        output_file.write_text(
            f"# {title}\n\n*Imported from ChatGPT export — {date_str}*\n\n---\n\n{full_text}",
            encoding="utf-8"
        )
        saved += 1

    print(f"Imported {saved} conversations to {OUTPUT_DIR}")
    print(f"Skipped {skipped} (too short)")


if __name__ == "__main__":
    main()

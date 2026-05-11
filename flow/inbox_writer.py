# inbox_writer.py — v1.0.0
# Appends an item to flow/gtd/inbox.md programmatically.
# Used by the Telegram bot /capture command.
# Usage: python flow/inbox_writer.py "item to capture"

import sys
from datetime import datetime
from pathlib import Path

INBOX_PATH = Path(__file__).parent / "gtd" / "inbox.md"


def append_to_inbox(item: str) -> None:
    if not INBOX_PATH.exists():
        INBOX_PATH.parent.mkdir(parents=True, exist_ok=True)
        INBOX_PATH.write_text("# Inbox\n\n", encoding="utf-8")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"- {item} _(captured {timestamp})_\n"

    with open(INBOX_PATH, "a", encoding="utf-8") as f:
        f.write(line)

    print(f"Captured: {item}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python flow/inbox_writer.py \"item to capture\"")
        sys.exit(1)

    item = " ".join(sys.argv[1:])
    append_to_inbox(item)

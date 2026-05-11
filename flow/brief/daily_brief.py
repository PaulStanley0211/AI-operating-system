# daily_brief.py — v1.0.0
# Orchestrator: runs the full Coffee Debrief pipeline.
# prompt → generate → dashboard → deliver → archive
# Schedule this to run at 7:00 AM daily.

import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

BRIEF_PRESET = os.getenv("BRIEF_PRESET", "founder")
BRIEFS_DIR = ROOT / "tuning" / "briefs"


def main():
    print(f"=== Coffee Debrief — {date.today().isoformat()} ===")

    # Step 1: Assemble prompt
    print("Step 1: Assembling prompt...")
    from prompt import build_prompt
    system_prompt, user_prompt = build_prompt(BRIEF_PRESET)

    # Step 2: Generate brief
    print("Step 2: Generating brief...")
    from generate import generate
    brief_text = generate(system_prompt, user_prompt)

    # Step 3: Generate dashboard chart
    print("Step 3: Generating dashboard chart...")
    from dashboard import generate as generate_chart
    chart_path = generate_chart()

    # Step 4: Deliver to Telegram
    print("Step 4: Delivering to Telegram...")
    from deliver import deliver
    deliver(brief_text, chart_path)

    # Step 5: Archive the brief
    print("Step 5: Archiving brief...")
    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    brief_file = BRIEFS_DIR / f"{date.today().isoformat()}.md"
    brief_file.write_text(
        f"# Daily Brief — {date.today().strftime('%B %d, %Y')}\n\n{brief_text}",
        encoding="utf-8"
    )
    print(f"Brief archived to {brief_file}")

    print("=== Done ===")


if __name__ == "__main__":
    main()

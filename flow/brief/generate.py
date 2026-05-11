# generate.py — v1.0.0
# Calls Gemini or Claude to generate the daily brief from the assembled prompt.

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

BRIEF_LLM = os.getenv("BRIEF_LLM", "gemini")
BRIEF_PRESET = os.getenv("BRIEF_PRESET", "founder")


def generate_with_gemini(system_prompt: str, user_prompt: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_prompt,
    )
    response = model.generate_content(user_prompt)
    return response.text


def generate_with_claude(system_prompt: str, user_prompt: str) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text


def generate(system_prompt: str, user_prompt: str) -> str:
    if BRIEF_LLM == "claude":
        print("Generating brief with Claude...")
        return generate_with_claude(system_prompt, user_prompt)
    else:
        print("Generating brief with Gemini...")
        return generate_with_gemini(system_prompt, user_prompt)


if __name__ == "__main__":
    from prompt import build_prompt
    sys_p, usr_p = build_prompt(BRIEF_PRESET)
    brief = generate(sys_p, usr_p)
    print(brief)

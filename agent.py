"""
agent.py — Runs a single browser‑use skill.

Reads a markdown skill file, injects the expected JSON schema, hands the
task to browser‑use + Google Gemini (free tier), then extracts and validates
the returned JSON.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import traceback
from pathlib import Path

from browser_use import Agent
from browser_use.browser.session import BrowserSession
from browser_use.llm.google.chat import ChatGoogle

from validator import SkillResult, validate_skill_result, get_supplier_schema_json

# Retry settings for transient errors
MAX_RETRIES = 3
INITIAL_BACKOFF_SECS = 30


def _extract_json(text: str) -> dict:
    """Best‑effort extraction of a JSON object from free‑form LLM text."""
    if not text:
        raise ValueError("Empty text — nothing to extract.")

    # 1. Direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Fenced code block
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # 3. Largest { … } blob
    m = re.search(r"(\{[\s\S]*\})", text)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    raise ValueError("Could not extract valid JSON from agent output.")


def _build_task_prompt(skill_text: str) -> str:
    """Combine skill instructions with the expected output schema."""
    return (
        "You are an autonomous research agent. Your job is to execute the "
        "skill defined below using the browser.\n\n"
        "## SKILL INSTRUCTIONS\n\n"
        f"{skill_text}\n\n"
        "## REQUIRED OUTPUT SCHEMA\n\n"
        "After completing your research, you MUST return a single JSON object "
        "(no other text) that conforms to this Pydantic‑derived JSON Schema:\n\n"
        f"```json\n{get_supplier_schema_json()}\n```\n\n"
        "Rules:\n"
        "- Only include data you actually found. Never fabricate.\n"
        "- If a field is optional and you didn't find it, omit it or use null.\n"
        "- Return ONLY the JSON object, nothing else.\n"
    )


async def run_skill(
    skill_path: str | Path,
    *,
    model: str = "gemini-2.0-flash",
    headless: bool = False,
) -> SkillResult | None:
    """Execute one skill file and return validated results (or None on failure).

    Retries up to MAX_RETRIES times on transient errors with exponential
    backoff so a single failure doesn't kill a multi‑skill run.
    """

    skill_path = Path(skill_path)
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill not found: {skill_path}")

    skill_text = skill_path.read_text(encoding="utf-8")
    task_prompt = _build_task_prompt(skill_text)

    # Use browser‑use's built‑in Google Gemini wrapper (FREE tier)
    # gemini-2.0-flash has higher free‑tier RPM (15) than 2.5-flash (10)
    # ChatGoogle already includes retry logic for 429s with exponential backoff
    llm = ChatGoogle(
        model=model,
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.0,
        max_retries=8,
        retry_base_delay=5.0,
        retry_max_delay=120.0,
    )

    # Configure browser session:
    #   - keep default extensions ENABLED — the "I don't care about cookies"
    #     extension auto‑dismisses cookie banners that block page interaction
    #   - add wait_between_actions to pace LLM calls within free‑tier RPM
    browser_session = BrowserSession(
        headless=headless,
        enable_default_extensions=True,
        wait_between_actions=3.0,
    )

    print(f"\n{'='*60}")
    print(f"  Running skill: {skill_path.name}")
    print(f"  Model: {model} (Google Gemini — free tier)")
    print(f"{'='*60}\n")

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            agent = Agent(
                task=task_prompt,
                llm=llm,
                browser_session=browser_session,
            )
            history = await agent.run()

            # browser‑use returns an AgentHistoryList; pull the final answer
            if hasattr(history, "final_result"):
                raw_text = history.final_result()
            elif isinstance(history, str):
                raw_text = history
            else:
                raw_text = str(history)

            if not raw_text:
                print(f"⚠️  Skill {skill_path.name} returned empty output.")
                return None

            data = _extract_json(raw_text)
            result = validate_skill_result(data)
            print(f"✅  {skill_path.name} → {len(result.suppliers)} suppliers validated")
            return result

        except Exception as exc:
            last_error = exc
            exc_str = str(exc).lower()

            # Check for transient / rate‑limit errors
            is_retriable = any(
                kw in exc_str
                for kw in ("rate_limit", "ratelimit", "429", "quota", "too many requests", "503", "overloaded")
            )
            if is_retriable and attempt < MAX_RETRIES:
                wait = INITIAL_BACKOFF_SECS * (2 ** (attempt - 1))
                print(
                    f"⏳  Transient error on attempt {attempt}/{MAX_RETRIES}. "
                    f"Waiting {wait}s before retry…"
                )
                await asyncio.sleep(wait)
                continue

            # Non‑retriable or final attempt
            print(f"❌  Skill {skill_path.name} failed (attempt {attempt}/{MAX_RETRIES}):")
            traceback.print_exc()
            return None

    # Should not reach here, but just in case
    print(f"❌  Skill {skill_path.name} exhausted all retries.")
    if last_error:
        traceback.print_exception(type(last_error), last_error, last_error.__traceback__)
    return None

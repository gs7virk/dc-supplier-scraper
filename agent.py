"""
agent.py — Runs a single browser‑use skill.

Reads a markdown skill file, injects the expected JSON schema, hands the
task to browser‑use + xAI Grok, then extracts and validates
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
from browser_use.llm.openai.chat import ChatOpenAI

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
        "- When typing a search query into a search engine (such as Google or DuckDuckGo), ALWAYS submit the query by pressing the 'Enter' key. Do NOT try to click a magnifying glass or search button, as this can cause browser automation to hang.\n"
        "- Only include data you actually found. Never fabricate.\n"
        "- If a field is optional and you didn't find it, omit it or use null.\n"
        "- Return ONLY the JSON object, nothing else.\n"
    )


async def run_skill(
    skill_path: str | Path,
    *,
    model: str = "grok-3-mini-fast",
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

    # Use xAI Grok via the OpenAI-compatible API
    llm = ChatOpenAI(
        model=model,
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
        temperature=0.0,
        max_retries=8,
        frequency_penalty=None,
    )

    print(f"\n{'='*60}")
    print(f"  Running skill: {skill_path.name}")
    print(f"  Model: {model}")
    print(f"{'='*60}\n")

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        # Configure browser session:
        #   - keep default extensions ENABLED — the "I don't care about cookies"
        #     extension auto‑dismisses cookie banners that block page interaction
        #   - add wait_between_actions to pace LLM calls within free‑tier RPM
        browser_session = BrowserSession(
            headless=headless,
            enable_default_extensions=True,
            wait_between_actions=1.0,
            cross_origin_iframes=False,
            max_iframe_depth=1,
        )
        try:
            agent = Agent(
                task=task_prompt,
                llm=llm,
                browser_session=browser_session,
            )
            # Restrict max_steps to 20 to avoid runaway costs & stuck loops
            history = await agent.run(max_steps=20)

            # Print token usage summary
            if hasattr(history, "usage") and history.usage:
                usage = history.usage
                print(f"\n📊  Token Usage for {skill_path.name}:")
                print(f"    • Prompt Tokens:      {usage.total_prompt_tokens}")
                print(f"    • Completion Tokens:  {usage.total_completion_tokens}")
                print(f"    • Total Tokens:       {usage.total_tokens}")
                if usage.total_cost > 0:
                    print(f"    • Estimated Cost:     ${usage.total_cost:.5f}")
                print()

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
        finally:
            try:
                await browser_session.kill()
            except Exception:
                pass

    # Should not reach here, but just in case
    print(f"❌  Skill {skill_path.name} exhausted all retries.")
    if last_error:
        traceback.print_exception(type(last_error), last_error, last_error.__traceback__)
    return None

"""
main.py — DC Supplier Lead‑Generation Agent Orchestrator

Discovers all skill markdown files under ./skills/, runs each one
sequentially via browser‑use, validates every result, de‑duplicates
suppliers, and writes a final aggregated report to ./output/.

Usage:
    python main.py                        # run ALL skills
    python main.py --skill epc            # run only skills whose filename contains "epc"
    python main.py --headless             # run browser in headless mode
    python main.py --model gemini-2.0-flash  # use a different model
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from agent import run_skill
from validator import AggregatedReport, Supplier

load_dotenv()

SKILLS_DIR = Path("skills")
OUTPUT_DIR = Path("output")


def discover_skills(filter_term: str | None = None) -> list[Path]:
    """Return sorted list of .md skill files, optionally filtered."""
    if not SKILLS_DIR.exists():
        print(f"❌  Skills directory not found: {SKILLS_DIR}")
        sys.exit(1)

    skills = sorted(SKILLS_DIR.glob("*.md"))
    if filter_term:
        skills = [s for s in skills if filter_term.lower() in s.stem.lower()]

    if not skills:
        print("❌  No matching skill files found.")
        sys.exit(1)

    return skills


def deduplicate(suppliers: list[Supplier]) -> list[Supplier]:
    """Remove duplicate suppliers by normalised website domain."""
    seen: dict[str, Supplier] = {}
    for s in suppliers:
        domain = (
            s.website.lower()
            .replace("https://", "")
            .replace("http://", "")
            .replace("www.", "")
            .rstrip("/")
        )
        if domain not in seen:
            seen[domain] = s
    return list(seen.values())


async def main(args: argparse.Namespace) -> None:
    # ── Pre‑flight checks ──────────────────────────────────────────────
    if not os.getenv("GEMINI_API_KEY"):
        print("❌  GEMINI_API_KEY not set. Copy .env.example → .env and add your key.")
        print("   Get a free key at: https://aistudio.google.com/apikey")
        sys.exit(1)

    skills = discover_skills(args.skill)
    print(f"\n🔍  Found {len(skills)} skill(s) to run:")
    for s in skills:
        print(f"    • {s.name}")
    print()

    # ── Run skills sequentially ─────────────────────────────────────────
    all_suppliers: list[Supplier] = []
    skills_completed: list[str] = []

    for skill_path in skills:
        result = await run_skill(
            skill_path,
            model=args.model,
            headless=args.headless,
        )
        if result:
            all_suppliers.extend(result.suppliers)
            skills_completed.append(result.skill)

    # ── De‑duplicate & build report ─────────────────────────────────────
    unique = deduplicate(all_suppliers)
    report = AggregatedReport(
        total_leads=len(unique),
        skills_run=skills_completed,
        suppliers=unique,
    )

    # ── Write output ────────────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    json_path = OUTPUT_DIR / f"leads_{ts}.json"
    json_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")

    # Also write a human‑readable summary
    summary_path = OUTPUT_DIR / f"leads_{ts}_summary.txt"
    lines = [
        f"DC Supplier Lead‑Generation Report",
        f"Generated: {ts}",
        f"Skills run: {', '.join(skills_completed)}",
        f"Total unique leads: {report.total_leads}",
        "",
        "=" * 70,
    ]
    for i, s in enumerate(unique, 1):
        lines.append(f"\n#{i}  {s.company_name}")
        lines.append(f"     Website:     {s.website}")
        lines.append(f"     HQ:          {s.headquarters or 'N/A'}")
        lines.append(f"     Categories:  {', '.join(s.categories)}")
        lines.append(f"     Services:    {', '.join(s.services)}")
        lines.append(f"     Retrofit:    {'Yes' if s.retrofit_capable else 'No'}")
        lines.append(f"     Summary:     {s.summary}")
        if s.contact_email:
            lines.append(f"     Email:       {s.contact_email}")
        if s.contact_phone:
            lines.append(f"     Phone:       {s.contact_phone}")
        if s.notable_clients_or_projects:
            lines.append(f"     Clients:     {', '.join(s.notable_clients_or_projects)}")
        if s.source_url:
            lines.append(f"     Source:      {s.source_url}")

    summary_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  ✅  DONE — {report.total_leads} unique leads found")
    print(f"  📄  JSON  → {json_path}")
    print(f"  📝  Text  → {summary_path}")
    print(f"{'='*60}\n")


# ── CLI ─────────────────────────────────────────────────────────────────────

def cli() -> None:
    parser = argparse.ArgumentParser(
        description="DC Supplier Lead‑Generation Agent"
    )
    parser.add_argument(
        "--skill",
        type=str,
        default=None,
        help="Run only skills whose filename contains this term (e.g. 'epc')",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-2.0-flash",
        help="Gemini model to use (default: gemini-2.5-flash)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode (no visible window)",
    )
    args = parser.parse_args()
    asyncio.run(main(args))


if __name__ == "__main__":
    cli()

# DC Supplier Scraper — Lead‑Generation Agent

An autonomous **browser‑use** agent that searches the web for companies that can help **build, maintain, or retrofit data centers**. It reads task instructions from dedicated **skill files** (Markdown), opens a real browser to research each category of supplier, validates every result through **Pydantic**, and writes a de‑duplicated report to disk.

## How It Works

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐     ┌─────────────┐
│  Skill .md   │ ──▶ │  browser‑use +   │ ──▶ │  Pydantic    │ ──▶ │  output/    │
│  (task def)  │     │  xAI Grok agent  │     │  Validator   │     │  JSON + TXT │
└──────────────┘     └──────────────────┘     └──────────────┘     └─────────────┘
```

1. **`main.py`** discovers all `.md` files in `skills/` and runs them one by one.
2. **`agent.py`** reads the skill, injects the expected JSON schema, and hands it to a `browser-use` Agent backed by xAI Grok.
3. The agent opens a Chrome browser, searches the web, visits company pages, and returns structured JSON.
4. **`validator.py`** validates the JSON against strict Pydantic models (`Supplier`, `SkillResult`).
5. Results are de‑duplicated and written to `output/` as timestamped JSON + a human‑readable summary.

## Skills (Markdown Task Files)

Each file in `skills/` is a self‑contained research brief:

| Skill File | What It Finds |
|---|---|
| `search_epc_contractors.md` | EPC firms & general contractors that build/retrofit DCs |
| `search_cooling_hvac.md` | HVAC, precision cooling, liquid/immersion cooling suppliers |
| `search_electrical_power.md` | UPS, generators, PDU, switchgear, battery storage vendors |
| `search_raw_materials.md` | Raised flooring, containment, fire suppression, modular/prefab |
| `search_network_connectivity.md` | Fiber optics, structured cabling, server racks/cabinets |
| `search_india_datacenters.md` | Upcoming & planned data centers in India (new builds, expansions) |

You can add your own skill by dropping a new `.md` file into `skills/`.

## Quickstart

```bash
# 1. Clone & enter the repo
cd dc-supplier-scraper

# 2. Create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers (one‑time)
playwright install chromium

# 5. Set your xAI API key
cp .env.example .env
# edit .env and add your real key (get one at https://console.x.ai)

# 6. Run all skills
python main.py

# Or run a single category
python main.py --skill epc
python main.py --skill india

# Headless mode (no visible browser window)
python main.py --headless

# Use a different Grok model
python main.py --model grok-3
```

## Output

After a run you'll find timestamped files in `output/`:

- **`leads_<timestamp>.json`** — machine‑readable, validated supplier data
- **`leads_<timestamp>_summary.txt`** — human‑readable one‑pager

## Project Structure

```
dc-supplier-scraper/
├── main.py                 # Orchestrator — discovers skills, runs agent, writes output
├── agent.py                # Single‑skill runner (browser‑use + xAI Grok)
├── validator.py            # Pydantic models & validation helpers
├── requirements.txt
├── .env.example
├── skills/
│   ├── search_epc_contractors.md
│   ├── search_cooling_hvac.md
│   ├── search_electrical_power.md
│   ├── search_raw_materials.md
│   ├── search_network_connectivity.md
│   └── search_india_datacenters.md
└── output/                 # Generated at runtime
```

## Notes

- **Respect robots.txt & ToS** — the agent visits public pages just like a human would.
- **Model** — defaults to `grok-3-mini-fast` (cheapest). Use `--model grok-3` for the most capable model.
- **Adding skills** — just drop a new `.md` file into `skills/` following the same template. The agent will pick it up automatically.

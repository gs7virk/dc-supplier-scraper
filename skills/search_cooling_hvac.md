# Skill: Find Cooling & HVAC Suppliers for Data Centers

You are searching for companies that manufacture or supply **cooling systems, HVAC equipment, and thermal management solutions** purpose-built for data center environments.

## Search Strategy

1. Go to **https://duckduckgo.com**
2. Run the following searches one by one. For each search, visit the **top 3–5 organic results** (skip ads):
   - `"data center" cooling system supplier`
   - `"data center" HVAC manufacturer`
   - `"precision cooling" "data center" company`
   - `"liquid cooling" "data center" supplier`
3. For each company website you visit:
   - Navigate to their **Products**, **Solutions**, or **Data Center** page.
   - Confirm they supply cooling or HVAC specifically for data centers (not residential/commercial HVAC only).
   - Look for product lines: CRAC/CRAH units, in-row cooling, rear-door heat exchangers, liquid cooling, chillers, free cooling, immersion cooling.

## Data to Extract (per company)

| Field | What to capture |
|---|---|
| **company_name** | Official company name |
| **website** | Homepage URL |
| **headquarters** | City, State/Country of their HQ |
| **summary** | 1–2 sentence description of their data center cooling offerings |
| **categories** | Pick from: `HVAC`, `Precision Cooling`, `Liquid Cooling`, `Immersion Cooling`, `Chillers`, `Free Cooling` |
| **services** | List of specific products/services |
| **retrofit_capable** | `true` if they can retrofit cooling into existing facilities |
| **notable_clients_or_projects** | Any named clients or project case studies |
| **contact_email** | Email address if publicly listed |
| **contact_phone** | Phone number if publicly listed |
| **source_url** | The specific page URL where you found this info |

## Output Format

Return the results as a JSON object:
```json
{
  "skill": "cooling_hvac",
  "suppliers": [ { ... }, { ... } ]
}
```

Aim for **at least 5 unique companies**. Do not fabricate data — only include what you actually find on the page.

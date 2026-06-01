# Skill: Find Upcoming & Planned Data Centers in India

You are searching for **new data centers that are being planned, announced, or are under construction in India**. Focus on recent news, press releases, and industry reports from 2024–2026.

## Search Strategy

1. Go to **https://duckduckgo.com**
2. Run the following searches one by one. For each search, visit the **top 3–5 organic results** (skip ads and social media posts):
   - `new data center India 2025 2026 planned under construction`
   - `India data center expansion hyperscale upcoming announcement`
   - `"data center" India site:economictimes.indiatimes.com OR site:livemint.com OR site:datacenterdynamics.com`
   - `Adani OR NTT OR Yotta OR STT OR CtrlS OR Nxtra "data center" India new`
3. For each result page you visit:
   - Look for **specific project announcements**: location (city/state), capacity (MW or sqft), developer/operator name, expected completion date
   - Prioritize **news articles, press releases, and industry reports** over generic company pages
   - Cross-reference the same project across multiple sources if possible

## Data to Extract (per planned data center project)

| Field | What to capture |
|---|---|
| **company_name** | The developer or operator building the data center (e.g. Adani Group, Yotta Infrastructure, NTT DATA) |
| **website** | Company homepage URL |
| **headquarters** | Company HQ city/country |
| **summary** | Description of the planned project — include: **location** (city, state), **capacity** (MW or sqft), **investment amount** if mentioned, **expected completion year**, and current status (planned/under construction/announced) |
| **categories** | Pick from: `Hyperscale`, `Colocation`, `Edge`, `Enterprise`, `Cloud`, `AI/ML` |
| **services** | Planned services (e.g. "colocation", "cloud hosting", "AI compute", "managed hosting") |
| **retrofit_capable** | `false` (these are new builds) |
| **notable_clients_or_projects** | The specific project name and its India location (e.g. "Chennai Data Center Park - 200 MW", "Noida Campus Phase 2") |
| **contact_email** | Contact email if publicly listed (or null) |
| **contact_phone** | Contact phone if publicly listed (or null) |
| **source_url** | The news article or page URL where you found this information |

## Output Format

Return the results as a JSON object:
```json
{
  "skill": "india_datacenters",
  "suppliers": [ { ... }, { ... } ]
}
```

Aim for **at least 5 unique projects or companies**. Focus on:
- Tier 1 cities: Mumbai, Chennai, Hyderabad, Pune, Delhi-NCR, Bengaluru
- Emerging locations: Kolkata, Kochi, Lucknow, Vizag, Jaipur

Only include data you actually found in the search results. Never fabricate information.

# Skill: Find Network & Connectivity Infrastructure Suppliers for Data Centers

You are searching for companies that supply **network cabling, fiber optics, rack/cabinet systems, and connectivity infrastructure** used inside data centers.

## Search Strategy

1. Go to **https://duckduckgo.com**
2. Run the following searches one by one. For each search, visit the **top 3–5 organic results** (skip ads):
   - `"data center" network cabling supplier`
   - `"data center" server rack cabinet manufacturer`
   - `"data center" fiber optic infrastructure supplier`
   - `"data center" structured cabling company`
3. For each company website you visit:
   - Navigate to their **Products**, **Solutions**, or **Data Center** page.
   - Confirm they supply network/connectivity infrastructure for data centers.
   - Look for: fiber optic cables, copper cabling, patch panels, server racks/cabinets, cable management, PDUs within racks, KVM switches, cable trays.

## Data to Extract (per company)

| Field | What to capture |
|---|---|
| **company_name** | Official company name |
| **website** | Homepage URL |
| **headquarters** | City, State/Country of their HQ |
| **summary** | 1–2 sentence description of their data center networking offerings |
| **categories** | Pick from: `Fiber Optics`, `Structured Cabling`, `Server Racks/Cabinets`, `Cable Management`, `Patch Panels`, `Network Hardware` |
| **services** | List of specific products/services |
| **retrofit_capable** | `true` if they mention cabling upgrades or retrofit installations |
| **notable_clients_or_projects** | Any named clients or project case studies |
| **contact_email** | Email address if publicly listed |
| **contact_phone** | Phone number if publicly listed |
| **source_url** | The specific page URL where you found this info |

## Output Format

Return the results as a JSON object:
```json
{
  "skill": "network_connectivity",
  "suppliers": [ { ... }, { ... } ]
}
```

Aim for **at least 5 unique companies**. Do not fabricate data — only include what you actually find on the page.

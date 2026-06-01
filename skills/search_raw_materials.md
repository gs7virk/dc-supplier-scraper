# Skill: Find Raw Material & Structural Suppliers for Data Centers

You are searching for companies that supply **raw materials and structural components** needed to physically construct data center buildings — steel, concrete, raised flooring, containment systems, fire suppression, and modular/prefab structures.

## Search Strategy

1. Go to **https://duckduckgo.com**
2. Run the following searches one by one. For each search, visit the **top 3–5 organic results** (skip ads):
   - `"data center" raised floor supplier manufacturer`
   - `"data center" modular building supplier prefab`
   - `"data center" fire suppression system supplier`
   - `"data center" containment system hot aisle cold aisle`
3. For each company website you visit:
   - Navigate to their **Products**, **Solutions**, or relevant page.
   - Confirm they supply physical materials or structural systems for data center construction.
   - Look for: raised floor tiles/pedestals, hot/cold aisle containment panels, fire suppression (FM-200, Novec, inert gas), modular DC pods, structural steel framing, concrete solutions.

## Data to Extract (per company)

| Field | What to capture |
|---|---|
| **company_name** | Official company name |
| **website** | Homepage URL |
| **headquarters** | City, State/Country of their HQ |
| **summary** | 1–2 sentence description of their data center material offerings |
| **categories** | Pick from: `Raised Flooring`, `Containment`, `Fire Suppression`, `Modular/Prefab`, `Structural Steel`, `Concrete`, `Cabling Infrastructure` |
| **services** | List of specific products/services |
| **retrofit_capable** | `true` if they can retrofit materials into existing facilities |
| **notable_clients_or_projects** | Any named clients or project case studies |
| **contact_email** | Email address if publicly listed |
| **contact_phone** | Phone number if publicly listed |
| **source_url** | The specific page URL where you found this info |

## Output Format

Return the results as a JSON object:
```json
{
  "skill": "raw_materials",
  "suppliers": [ { ... }, { ... } ]
}
```

Aim for **at least 5 unique companies**. Do not fabricate data — only include what you actually find on the page.

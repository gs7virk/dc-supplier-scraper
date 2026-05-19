# Skill: Find Electrical & Power Infrastructure Suppliers for Data Centers

You are searching for companies that manufacture or supply **electrical power infrastructure** for data centers — including UPS systems, generators, PDUs, switchgear, transformers, and busway/busbar systems.

## Search Strategy

1. Go to **https://www.google.com**
2. Run the following searches one by one. For each search, visit the **top 3–5 organic results** (skip ads):
   - `"data center" power infrastructure supplier`
   - `"data center" UPS manufacturer`
   - `"data center" generator supplier`
   - `"data center" electrical switchgear PDU supplier`
3. For each company website you visit:
   - Navigate to their **Products**, **Solutions**, or **Data Center** page.
   - Confirm they supply power/electrical equipment specifically suitable for data centers.
   - Look for product lines: UPS, diesel/gas generators, static transfer switches, PDUs, RPPs, busway, transformers, switchgear, battery storage.

## Data to Extract (per company)

| Field | What to capture |
|---|---|
| **company_name** | Official company name |
| **website** | Homepage URL |
| **headquarters** | City, State/Country of their HQ |
| **summary** | 1–2 sentence description of their data center power offerings |
| **categories** | Pick from: `UPS`, `Generators`, `PDU`, `Switchgear`, `Transformers`, `Busway`, `Battery Storage`, `Full Electrical` |
| **services** | List of specific products/services |
| **retrofit_capable** | `true` if they mention upgrading/retrofitting existing power infrastructure |
| **notable_clients_or_projects** | Any named clients or project case studies |
| **contact_email** | Email address if publicly listed |
| **contact_phone** | Phone number if publicly listed |
| **source_url** | The specific page URL where you found this info |

## Output Format

Return the results as a JSON object:
```json
{
  "skill": "electrical_power",
  "suppliers": [ { ... }, { ... } ]
}
```

Aim for **at least 5 unique companies**. Do not fabricate data — only include what you actually find on the page.

# Skill: Find EPC & General Contractors for Data Centers

You are searching for companies that build new data centers or retrofit existing ones.

## Steps

1. Go to **https://duckduckgo.com**
2. Search for: `top data center EPC construction companies`
3. Look at the **top 5 organic results** (skip ads and LinkedIn).
4. Click on result pages that look like industry listings or company websites.
5. For each company you find, extract their name, website URL, a brief description of their data center services, and whether they do retrofitting.
6. If you see a cookie banner, click "Accept" or dismiss it, then continue.
7. Try to find **at least 3 companies** from the search results.

## Data to Extract (per company)

For each company, extract:
- **company_name**: Official company name
- **website**: Their homepage URL
- **headquarters**: City/Country if visible
- **summary**: 1-2 sentences about their data center work
- **categories**: Pick from: `EPC`, `General Contractor`, `Design-Build`, `Civil/Structural`
- **services**: List of services (e.g. "full turnkey DC build", "site preparation")
- **retrofit_capable**: true/false — do they mention retrofitting or upgrading?
- **notable_clients_or_projects**: Any named clients (or null)
- **contact_email**: Email if visible (or null)
- **contact_phone**: Phone if visible (or null)
- **source_url**: The page URL where you found the info

## Output

Return a JSON object like:
```json
{
  "skill": "epc_contractors",
  "suppliers": [ { ... }, { ... } ]
}
```

Only include data you actually found. Never make anything up.

# Skill: campaign-anomaly-digest

**Purpose:** a short morning note telling the team which campaigns need attention today.

## Inputs
- Facts from `python tools/campaign_anomalies.py <daily_metrics.csv>`

## Steps
1. Read the facts JSON; it already contains every number you may use
2. Write a headline line: date, total spend and conversions yesterday, number of flagged campaigns
3. For each anomaly, write one bullet: campaign, what moved, by how much against its typical day, and the most likely first check (for example, bid changes for a cost per click spike, tracking or landing page changes for a conversion drop)
4. If nothing is flagged, say so in one line

## Output
`digest.md`, under 150 words.

## Checks before handing on
Run `python tools/verify_numbers.py digest.md facts.json`. If any number is untraceable, rewrite the digest. Never round or estimate numbers that are not in the facts.

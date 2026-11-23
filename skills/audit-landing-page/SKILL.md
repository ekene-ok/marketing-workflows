# Skill: audit-landing-page

**Purpose:** check a landing page against the ad that sends traffic to it, and list fixes in priority order.

## Inputs
- A landing page in `inputs/landing_page_*.md`
- The campaign brief (its `Promise:` line is what the ad promised)
- Facts from `python tools/audit_page.py <page> <brief>`

## Steps
1. Run `tools/audit_page.py` and read the JSON facts
2. Check each threshold: message match (at least 50% of promise terms above the fold), one call to action, 5 or fewer form fields, reading grade 9 or lower, no banned words, an approved proof point present
3. For each failed check, write the problem, why it costs conversions, and a specific fix (rewrite the headline, cut named fields, and so on)
4. Order fixes by expected impact: message match and form friction first, then CTA focus, then proof, then copy polish

## Output
`landing_page_audit.md`: a scorecard table (check, result, threshold, pass or fail), then prioritised fixes with suggested rewrites.

## Rules
- Every number in the audit must come from the facts JSON
- Suggested rewrites must pass `brand_voice.md`

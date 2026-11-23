# Skill: score-ad-variants

**Purpose:** score variants against the rubric so a human reviews a short, ranked list.

## Inputs
- `variants.json` (all variants must pass `tools/check_copy.py` first)
- `context/ad_rubric.md`, `context/icp.md`, `context/brand_voice.md`

## Steps
1. Score every variant 1 to 5 on each rubric criterion, with a one-sentence reason per score
2. Total the scores (out of 25)
3. Mark variants scoring under 18 as "Do not ship"
4. Recommend the top 3 for testing, choosing different angles where possible so the test teaches something

## Output
`scores.md`: one table of all variants (id, five scores, total, verdict) and a short "Recommended for testing" section explaining the pick.

## Rules
- Be strict: a 5 should be rare
- The scores are advice for a human reviewer, who makes the final call

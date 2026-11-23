# Skill: check-brand-and-compliance

**Purpose:** a final read for the things a script cannot judge, after the hard checks pass.

## Inputs
- Any copy file that has passed `tools/check_copy.py`
- `context/brand_voice.md`, `context/compliance_rules.md`

## Steps
1. Confirm the hard checks passed (attach the output)
2. Read each piece for tone: plain-spoken, practical, calm. Flag anything that sounds like pressure or hype
3. Check every claim is supported by an approved proof point
4. Check the security and AI wording rules are met in spirit, not just in words

## Output
`review_notes.md`: one line per item, "OK" or a specific issue with a suggested fix. Anything flagged goes to a human before launch.

# Skill: write-ad-variants

**Purpose:** turn angles into ad copy for a given format, ready for checking.

## Inputs
- `angles.md` from `generate-angles`
- The ad format named in the brief (`paid_search` or `linkedin`)
- `context/brand_voice.md`, `context/compliance_rules.md`, `context/messaging.md`

## Steps
1. For each angle, write **2 variants** in the requested format
2. Respect the character limits in `compliance_rules.md` for every field
3. Use the call to action that matches the funnel stage in `messaging.md`
4. Use only approved numbers from `company.md`

## Output
`variants.json`: a list of objects
```json
{"id": "A1-v1", "angle": 1, "format": "linkedin", "fields": {"intro": "...", "headline": "..."}}
```

## Checks before handing on
Run `python tools/check_copy.py <variants.json>`. Rewrite any variant that fails, and record what changed in the run notes.

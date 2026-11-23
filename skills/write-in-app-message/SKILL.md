# Skill: write-in-app-message

**Purpose:** turn a product release note into short in-app messages for different customer segments.

## Inputs
- A release note in `inputs/release_note_*.md`
- `context/company.md`, `context/icp.md`, `context/brand_voice.md`, `context/compliance_rules.md`

## Steps
1. Identify who benefits from the release and why, in customer language
2. Write one message per segment named in the release note (for example, customers without the add-on vs current add-on users)
3. Each message has a `title`, `body` and `button`, within the in-app limits
4. Lead with the outcome for the firm; mention the feature second

## Output
`in_app_messages.json` in the same format as `variants.json`, with `"format": "in_app"`, plus a `segment` field.

## Checks before handing on
Run `python tools/check_copy.py <in_app_messages.json>` and fix any failure.

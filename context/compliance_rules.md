# Compliance and copy rules (machine-checked)

These are enforced by `tools/check_copy.py`. Skills must also follow them when writing.

## Length limits
| Format | Field | Max characters |
|---|---|---|
| Paid search | Headline | 30 |
| Paid search | Description | 90 |
| LinkedIn ad | Intro text | 150 |
| LinkedIn ad | Headline | 70 |
| In-app message | Title | 50 |
| In-app message | Body | 160 |
| In-app message | Button | 25 |

## Banned words and phrases
revolutionary, game-changing, game changer, seamless, best-in-class, cutting-edge, supercharge, unlock, guaranteed, risk-free, act now, last chance

## Numbers
Any number in customer-facing copy must appear in the approved proof points in `company.md` or be a product price. Other numbers fail the check.

## Required wording
- Any copy mentioning security must name "SOC 2 Type II" exactly
- Any copy mentioning AI must describe it as "AI-assisted" (never "fully automated" or "AI does it for you"), because staff still review extracted data

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
Any number in customer-facing copy must match an approved proof point, price or offer term in `company.md`, `messaging.md` or the run's brief, together with the word that gives it meaning. "4 days faster" is approved, so "4 days" passes but "4 hours" fails; "92% of support tickets" is approved, so "92% of firms" fails. Numbers written in words (ten, twice, half, thousands) also fail: use an approved proof point instead.

## Required wording
- Any copy mentioning security must name "SOC 2 Type II" exactly
- Any copy mentioning AI must describe it as "AI-assisted" (never "fully automated" or "AI does it for you"), because staff still review extracted data

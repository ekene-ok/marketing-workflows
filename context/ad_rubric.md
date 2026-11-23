# Ad scoring rubric

Each variant is scored 1 to 5 on five criteria. Total out of 25. Variants below 18 are not shipped.

| Criterion | 5 means | 1 means |
|---|---|---|
| ICP fit | Speaks to one ICP pain in the customer's own words | Generic; could be for any software |
| Clarity | One idea, understood in under 3 seconds | Several ideas, or confusing |
| Proof | Uses an approved proof point or a concrete, checkable detail | Vague claims with no support |
| Brand voice | Fully follows `brand_voice.md` | Breaks a "Do not" rule |
| Call to action | Clear next step matching the funnel stage | No CTA, or a CTA that does not fit the stage |

Scoring rules:
- A variant that fails any hard check in `tools/check_copy.py` (length limits, banned words, unapproved numbers) scores 0 on Brand voice and Proof automatically
- Explain every score in one sentence so a human can disagree with it

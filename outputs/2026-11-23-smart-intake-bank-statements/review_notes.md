# Brand and compliance review: Smart Intake bank statement messages

Hard checks: all four messages passed (`check_results.txt`).

| ID | Segment | Result | Notes |
|---|---|---|---|
| S1-v1 | Core customers without Smart Intake | OK | Leads with the outcome and states the AI is assisted and reviewed by staff, matching the release note |
| S1-v2 | Core customers without Smart Intake | OK | "Less typing" is a fair outcome claim with no number attached |
| S2-v1 | Current Smart Intake users | OK | Describes exactly what the release note says |
| S2-v2 | Current Smart Intake users | Flag | "Confirm, edit or reject each line" goes beyond the release note, which only mentions confirming. Check with product that edit and reject exist before launch |

**Recommendation:** run S1-v1 against S1-v2 as an A/B test for the trial offer, and launch S2-v1 to current users (use S2-v2 only once product confirms the edit and reject options).

**Human review gate:** product marketing approves the copy and sets the audience rules for each segment in the in-app messaging tool.

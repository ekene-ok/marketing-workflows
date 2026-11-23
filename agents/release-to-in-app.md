# Agent: release-to-in-app

**Goal:** turn a product release into checked in-app messages for each customer segment.

| Step | Skill or tool | Output |
|---|---|---|
| 1 | `skills/write-in-app-message` | `in_app_messages.json` |
| 2 | `tools/check_copy.py` (fix and re-run until all pass) | check results |
| 3 | `skills/check-brand-and-compliance` | `review_notes.md` |
| 4 | `tools/log_run.py` | entry in `outputs/run_log.md` |

**Human review gate:** product marketing approves before messages go live, and sets the audience rules in the in-app tool.

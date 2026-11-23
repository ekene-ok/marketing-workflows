# Agent: morning-campaign-digest

**Goal:** a daily note that surfaces campaigns behaving unusually, so the team checks them before spending more.

| Step | Skill or tool | Output |
|---|---|---|
| 1 | `tools/campaign_anomalies.py <daily_metrics.csv>` | `facts.json` |
| 2 | `skills/campaign-anomaly-digest` | `digest.md` |
| 3 | `tools/verify_numbers.py digest.md facts.json` | check result |
| 4 | `tools/log_run.py` | entry in `outputs/run_log.md` |

**Human review gate:** the campaign owner investigates flagged campaigns; the digest never changes budgets itself.

# Agent: landing-page-audit

**Goal:** make sure the page delivers on what the ad promised, before money is spent sending traffic to it.

| Step | Skill or tool | Output |
|---|---|---|
| 1 | `tools/audit_page.py <page> <brief>` | `page_facts.json` |
| 2 | `skills/audit-landing-page` | `landing_page_audit.md` |
| 3 | `tools/verify_numbers.py landing_page_audit.md page_facts.json --with-approved` | check result |
| 4 | `tools/log_run.py` | entry in `outputs/run_log.md` |

**Human review gate:** the page owner decides which fixes to make.

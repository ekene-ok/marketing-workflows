# Run log

| Date | Agent | Inputs | Outputs | Checks | Notes |
|---|---|---|---|---|---|
| 2026-11-23 | ad-variant-pipeline | brief_client_portal_tax_season.md | outputs/2026-11-23-client-portal-tax-season/ | Round 1: 8 of 10 passed; round 2: 10 of 10 passed | 2 variants rewritten (invented number and banned word; exclamation mark and missing SOC 2 wording). Top 3 sent for approval |
| 2026-11-23 | landing-page-audit | landing_page_client_portal.md + brief | outputs/2026-11-23-landing-page-audit/ | Number verification passed (second attempt) | Page failed all six checks; fixes ranked for the page owner |
| 2026-11-23 | release-to-in-app | release_note_smart_intake.md | outputs/2026-11-23-smart-intake-bank-statements/ | 4 of 4 passed | One message flagged for product to confirm a feature claim |
| 2026-11-23 | morning-campaign-digest | campaign_daily_metrics.csv | outputs/2026-11-23-morning-digest/ | Number verification passed (second attempt, after adding the flagged count to the facts) | 2 campaigns flagged; no budget changes made by the agent |

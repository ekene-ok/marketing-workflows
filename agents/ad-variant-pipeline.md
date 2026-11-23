# Agent: ad-variant-pipeline

**Goal:** from a campaign brief to a short, ranked list of ad variants a human can approve.

| Step | Skill or tool | Output |
|---|---|---|
| 1 | `skills/generate-angles` | `angles.md` |
| 2 | `skills/write-ad-variants` | `variants.json` |
| 3 | `tools/check_copy.py` (rewrite failures in step 2, then re-run) | check results |
| 4 | `skills/score-ad-variants` | `scores.md` |
| 5 | `skills/check-brand-and-compliance` on the top 3 | `review_notes.md` |
| 6 | `tools/log_run.py` | entry in `outputs/run_log.md` |

**Human review gate:** a marketer approves the final variants before anything launches.
Write all outputs to `outputs/<date>-<campaign>/`.

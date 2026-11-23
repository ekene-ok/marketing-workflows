# AGENTS.md: start here

This file orients any AI coding assistant (or a new teammate) working in this repo. Read it first, then the files it points to.

## What this repo is
A library of reusable marketing workflows for **Tallyroot**, a fictional practice management software company for small accounting firms. Business knowledge lives in `/context`, single-task prompts live in `/skills`, and `/agents` chain skills into repeatable pipelines. Python checks in `/tools` enforce the rules a model can get wrong.

## Layout
| Folder | Contents | Rule |
|---|---|---|
| `context/` | Company, ICP, messaging, brand voice, ad rubric, compliance rules | The source of truth. Read before writing anything customer-facing |
| `skills/` | One folder per task, each with a `SKILL.md` (purpose, inputs, steps, output, checks) | Skills do one thing and state their inputs and outputs |
| `agents/` | Ordered lists of skills and tools | Agents contain no prompts of their own, so skills stay reusable |
| `tools/` | Deterministic checks (copy rules, page audit, anomaly facts, number verification, run log) | Always run the checks a skill or agent names |
| `inputs/` | Briefs, pages, release notes, metrics | Never edit inputs during a run |
| `outputs/` | One folder per run, plus `run_log.md` | Every run is logged |

## Conventions
- Use only proof points and numbers from `context/company.md`. If a claim needs a number that is not there, write `[PROOF POINT NEEDED]`
- Follow `context/brand_voice.md` in all copy (no hype words, no dashes, no exclamation marks in headlines)
- Every run ends at a **human review gate**. Nothing launches without approval
- Change a skill on a branch, run it on the same inputs, compare results, then merge

## How to run an agent
Ask your assistant: "Run `agents/ad-variant-pipeline.md` on `inputs/brief_client_portal_tax_season.md`." It should follow the steps in order, run each named tool, and write outputs to `outputs/<date>-<name>/`.

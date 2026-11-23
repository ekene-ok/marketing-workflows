"""Append a line to outputs/run_log.md so every run is traceable.

Usage: python tools/log_run.py <agent> <inputs> <outputs folder> <checks result> [notes]
"""
import sys
from datetime import date
from pathlib import Path

LOG = Path(__file__).resolve().parents[1] / "outputs" / "run_log.md"
if not LOG.exists():
    LOG.write_text("# Run log\n\n| Date | Agent | Inputs | Outputs | Checks | Notes |\n|---|---|---|---|---|---|\n")
agent, inputs, outputs, checks = sys.argv[1:5]
notes = sys.argv[5] if len(sys.argv) > 5 else ""
with LOG.open("a") as f:
    f.write(f"| {date.today():%Y-%m-%d} | {agent} | {inputs} | {outputs} | {checks} | {notes} |\n")
print(f"Logged run of {agent}")

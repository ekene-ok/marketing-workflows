"""Guardrail for AI-written summaries: every number in the text must exist in the facts file.

Usage: python tools/verify_numbers.py outputs/digest.md outputs/facts.json [--with-approved]
--with-approved also allows the approved proof-point numbers from context/company.md
(use it when the text suggests customer-facing rewrites).
Numbers are compared after removing thousands separators; a number also passes if it is a
rounded form (0 or 1 decimal places) of a fact value.
"""
import json
import re
import sys


def fact_numbers(obj, acc):
    if isinstance(obj, dict):
        for v in obj.values():
            fact_numbers(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            fact_numbers(v, acc)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        for d in (0, 1, 2):
            acc.add(f"{abs(obj):.{d}f}")
    elif isinstance(obj, str):
        acc.update(n.replace(",", "") for n in re.findall(r"\d+(?:[.,]\d+)?", obj))
    return acc


LIST_NUMBER = re.compile(r"^\s*(?:\*\*)?\d+\.\s", re.M)  # "1. " or "**1. " at line start


def verify(text, facts, extra=()):
    allowed = fact_numbers(facts, set()) | set(extra)
    text = LIST_NUMBER.sub("", text)  # list numbering is formatting, not a claim
    found = [n.replace(",", "") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text)]
    return [n for n in found if n not in allowed]


if __name__ == "__main__":
    text = open(sys.argv[1]).read()
    facts = json.load(open(sys.argv[2]))
    extra = ()
    if "--with-approved" in sys.argv:
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from tools.common import approved_numbers
        extra = approved_numbers()
    unknown = verify(text, facts, extra)
    print("PASS: every number traces to the facts file" if not unknown else f"FAIL: untraceable numbers {unknown}")
    sys.exit(0 if not unknown else 1)

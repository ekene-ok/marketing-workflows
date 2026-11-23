"""Hard checks on customer-facing copy (ads and in-app messages).

Input: a JSON file with a list of variants, each {"id", "format", "fields": {field: text}}.
Checks: character limits, banned words, unapproved numbers, dashes, exclamation marks in
headlines/titles, and required wording for security and AI claims.
Usage: python tools/check_copy.py path/to/variants.json
"""
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import BANNED, LIMITS, numbers_in, approved_numbers


def check_variant(v: dict, allowed: set[str]) -> list[str]:
    problems = []
    fmt = v["format"]
    all_text = " ".join(v["fields"].values())
    low = all_text.lower()
    for field, text in v["fields"].items():
        limit = LIMITS.get((fmt, field))
        if limit and len(text) > limit:
            problems.append(f"{field} is {len(text)} characters (limit {limit})")
        if field in ("headline", "title") and "!" in text:
            problems.append(f"{field} uses an exclamation mark")
    for w in BANNED:
        if re.search(rf"\b{re.escape(w)}\b", low):
            problems.append(f"banned word: '{w}'")
    for n in numbers_in(all_text):
        if n not in allowed:
            problems.append(f"unapproved number: {n}")
    if "\u2014" in all_text or "\u2013" in all_text:
        problems.append("contains an em or en dash")
    if re.search(r"\bsecur(e|ity)\b", low) and "SOC 2 Type II" not in all_text:
        problems.append("mentions security without 'SOC 2 Type II'")
    if re.search(r"\bai\b", low) and "AI-assisted" not in all_text:
        problems.append("mentions AI without 'AI-assisted'")
    if re.search(r"fully automated|ai does it for you", low):
        problems.append("overstates automation")
    return problems


def check_file(path: str) -> list[dict]:
    variants = json.loads(Path(path).read_text())
    allowed = approved_numbers()
    return [{"id": v["id"], "passed": not (p := check_variant(v, allowed)), "problems": p} for v in variants]


if __name__ == "__main__":
    results = check_file(sys.argv[1])
    for r in results:
        print(f"{r['id']}: {'PASS' if r['passed'] else 'FAIL'}" + ("" if r["passed"] else f"  {'; '.join(r['problems'])}"))
    sys.exit(0 if all(r["passed"] for r in results) else 1)

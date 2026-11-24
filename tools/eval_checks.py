"""How much can the copy checks be trusted? Seed known problems into copy that already passed and count what gets caught.

Builds test cases from the 14 approved variants in the example runs:
- clean copy, which should pass
- eight kinds of rule break the checks are built for, each seeded into every variant
- three kinds of problem the checks are not built for (claims that need a person to judge)
Writes outputs/check_evaluation/results.csv and summary.csv.
Usage: python tools/eval_checks.py --label before   (the original number check)
       python tools/eval_checks.py --label after    (the current checker)
"""
import copy
import csv
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.check_copy import check_variant
from tools.common import LIMITS, ROOT, approved_claims, approved_numbers, numbers_in

BASES = [ROOT / "outputs/2026-11-23-client-portal-tax-season/variants.json",
         ROOT / "outputs/2026-11-23-smart-intake-bank-statements/in_app_messages.json"]
OUT = ROOT / "outputs/check_evaluation"


def main_field(v):
    return "intro" if v["format"] == "linkedin" else "body"


def head_field(v):
    return "headline" if v["format"] == "linkedin" else "title"


def add(v, text, field=None):
    f = field or main_field(v)
    v["fields"][f] = v["fields"][f].rstrip() + " " + text
    return v


def strip_required(v):
    for f, t in v["fields"].items():
        v["fields"][f] = t.replace(" SOC 2 Type II certified.", "").replace(", and Tallyroot is SOC 2 Type II certified", "") \
            .replace(" Tallyroot is SOC 2 Type II certified.", "").replace("AI-assisted, and", "Your")
    return v


def too_long(v, i):
    f = main_field(v)
    limit = LIMITS[(v["format"], f)]
    while len(v["fields"][f]) <= limit:
        v["fields"][f] += " Your clients will thank you for it."
    return v


BANNED_CYCLE = ["seamless", "revolutionary", "game-changing", "best-in-class", "cutting-edge", "supercharge",
                "unlock", "guaranteed", "risk-free", "act now", "last chance", "game changer"]
INVENTED = ["Save 10 hours a week.", "Used by 500 firms.", "3x faster than email.", "Cut admin by 70%.",
            "Rated 4.8 by accountants.", "Set up in 15 minutes."]
REUSED = ["Cut admin time by 50%.", "Save 4 hours a week.", "Trusted by 92% of firms.", "Set up in 30 minutes.",
          "Join 310 firms already using it.", "Now $18 less per month."]
WORDS = ["Save ten hours a week.", "Twice as fast as email.", "Cut admin time in half.", "Trusted by thousands of firms.",
         "Set up in fifteen minutes.", "Three times faster than email."]
# Written after the fix to the number check, to test it on phrasings it was not tuned on
FRESH_REUSED = ["Save $12 a month on every seat.", "Built for firms of 50 or more.", "Answers in 4 minutes, not days.",
                "92% faster document collection.", "Ready in 2 days.", "Get set up 4 days sooner."]
FRESH_WORDS = ["One in three firms switched last year.", "Dozens of firms switched this season.",
               "Seven days a week support.", "Collect documents in half the time.",
               "Hundreds of firms rely on it.", "Cut follow-ups by a third."]
SUPERLATIVE = ["The easiest portal your clients will ever use.", "Faster than any other practice software.",
               "The only portal built for accountants."]
PROMISE = ["Never chase a missing document again.", "Your team will never miss a deadline.", "No more errors, ever."]

# A case only counts as caught when it is flagged for the problem that was seeded, not for a side effect
# such as going over the length limit.
REASON = {"too_long": "characters", "banned_word": "banned word", "invented_number": "number",
          "dash": "dash", "exclamation": "exclamation", "security_wording": "SOC 2", "ai_wording": "AI-assisted",
          "overstated_automation": "overstates", "approved_number_new_claim": "number", "number_in_words": "number", "fresh_reused_number": "number", "fresh_number_in_words": "number",
          "superlative": "claim", "absolute_promise": "claim"}

CASES = {
    # (group, should the checks catch it?, mutation)
    "clean": ("Clean copy", False, lambda v, i: v),
    "too_long": ("Built to catch", True, too_long),
    "banned_word": ("Built to catch", True, lambda v, i: add(v, f"A {BANNED_CYCLE[i % 12]} way to work.")),
    "invented_number": ("Built to catch", True, lambda v, i: add(v, INVENTED[i % 6])),
    "dash": ("Built to catch", True, lambda v, i: add(v, "\u2014 built for busy season.")),
    "exclamation": ("Built to catch", True, lambda v, i: add(v, "today!", head_field(v))),
    "security_wording": ("Built to catch", True, lambda v, i: add(strip_required(v), "Your files stay secure.")),
    "ai_wording": ("Built to catch", True, lambda v, i: add(strip_required(v), "Powered by AI.")),
    "overstated_automation": ("Built to catch", True, lambda v, i: add(v, "Fully automated.")),
    "approved_number_new_claim": ("Gaps found", True, lambda v, i: add(v, REUSED[i % 6])),
    "number_in_words": ("Gaps found", True, lambda v, i: add(v, WORDS[i % 6])),
    "fresh_reused_number": ("Fresh phrasings", True, lambda v, i: add(v, FRESH_REUSED[i % 6])),
    "fresh_number_in_words": ("Fresh phrasings", True, lambda v, i: add(v, FRESH_WORDS[i % 6])),
    "superlative": ("Needs a person", False, lambda v, i: add(v, SUPERLATIVE[i % 3])),
    "absolute_promise": ("Needs a person", False, lambda v, i: add(v, PROMISE[i % 3])),
}


def legacy_check(v, _allowed):
    """The original checker, which approved numbers on their own, kept so the before and after can be rerun."""
    keep = [p for p in check_variant(v, approved_claims())
            if not p.startswith("unapproved number") and not p.startswith("number written in words")]
    old = approved_numbers()
    return keep + [f"unapproved number: {n}" for n in numbers_in(" ".join(v["fields"].values())) if n not in old]


def run(label):
    checker = legacy_check if label == "before" else check_variant
    bases = [v for p in BASES for v in json.loads(p.read_text())]
    allowed = approved_claims()
    rows = []
    for case, (group, _, mutate) in CASES.items():
        for i, base in enumerate(bases):
            v = mutate(copy.deepcopy(base), i)
            problems = checker(v, allowed)
            key = REASON.get(case)
            caught = any(key in p for p in problems) if key else bool(problems)
            rows.append({"label": label, "case": case, "group": group, "variant": base["id"],
                         "flagged": caught, "problems": "; ".join(problems)})
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"results_{label}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    summary = []
    for case, (group, _, _) in CASES.items():
        r = [x for x in rows if x["case"] == case]
        summary.append({"label": label, "group": group, "case": case, "cases": len(r),
                        "flagged": sum(x["flagged"] for x in r)})
    with open(OUT / f"summary_{label}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=summary[0].keys())
        w.writeheader()
        w.writerows(summary)
    for s in summary:
        print(f"{s['case']:<28}{s['group']:<16}{s['flagged']:>3} of {s['cases']}")


if __name__ == "__main__":
    run(sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--label" else "current")

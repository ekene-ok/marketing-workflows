"""Measurable landing page checks against the campaign brief.

Input: a landing page in a simple markdown format (see inputs/landing_page_*.md):
  # Headline, a "Subheadline:" line, body text, "CTA:" lines, and "Form fields:" list.
And the brief, whose "Promise:" line states what the ad promised.
Output: JSON facts the audit skill must base its findings on.
Usage: python tools/audit_page.py inputs/landing_page.md inputs/brief.md
"""
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.common import BANNED

STOP = set("a an the and or for to of in on with your you our we is are be it this that at by from as get".split())


def words(t):
    return [w for w in re.findall(r"[a-z']+", t.lower()) if w not in STOP and len(w) > 2]


def syllables(word):
    groups = re.findall(r"[aeiouy]+", word.lower())
    n = len(groups) - (1 if word.lower().endswith("e") and len(groups) > 1 else 0)
    return max(1, n)


def reading_grade(text):
    sents = max(1, len(re.findall(r"[.!?]+", text)))
    ws = re.findall(r"[A-Za-z']+", text)
    if not ws:
        return 0.0
    syl = sum(syllables(w) for w in ws)
    return round(0.39 * len(ws) / sents + 11.8 * syl / len(ws) - 15.59, 1)  # Flesch-Kincaid grade


def audit(page_path, brief_path):
    page = Path(page_path).read_text()
    brief = Path(brief_path).read_text()
    headline = re.search(r"^# (.+)$", page, re.M).group(1).strip()
    sub = (re.search(r"^Subheadline:\s*(.+)$", page, re.M) or [None, ""])[1]
    ctas = re.findall(r"^CTA:\s*(.+)$", page, re.M)
    fields = re.findall(r"^- field:\s*(.+)$", page, re.M)
    body = "\n".join(l for l in page.splitlines()
                     if l and not l.startswith(("#", "CTA:", "- field:", "Subheadline:", "Form fields:")))
    promise = re.search(r"^Promise:\s*(.+)$", brief, re.M).group(1)
    promise_terms = set(words(promise))
    above_fold = set(words(headline + " " + sub))
    overlap = sorted(promise_terms & above_fold)
    low = page.lower()
    return {
        "headline": headline,
        "ad_promise": promise,
        "promise_terms_found_above_fold": overlap,
        "message_match_share": round(len(overlap) / max(1, len(promise_terms)), 2),
        "distinct_ctas": len(set(c.strip().lower() for c in ctas)),
        "cta_labels": ctas,
        "form_fields": len(fields),
        "form_field_names": fields,
        "reading_grade_level": reading_grade(body),
        "body_word_count": len(re.findall(r"[A-Za-z']+", body)),
        "banned_words_found": [w for w in BANNED if re.search(rf"\b{re.escape(w)}\b", low)],
        "has_approved_proof_point": "4 days faster" in page or "SOC 2 Type II" in page,
        "thresholds": {"message_match_share_min": 0.5, "distinct_ctas_max": 1, "form_fields_max": 5,
                       "reading_grade_level_max": 9},
    }


if __name__ == "__main__":
    print(json.dumps(audit(sys.argv[1], sys.argv[2]), indent=2))

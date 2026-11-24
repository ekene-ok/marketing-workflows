"""Shared helpers: repo paths, approved numbers and claims, and number extraction."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CONTEXT = ROOT / "context"
NUMBER = re.compile(r"\d+(?:[.,]\d+)?")
BANNED = ["revolutionary", "game-changing", "game changer", "seamless", "best-in-class", "cutting-edge",
          "supercharge", "unlock", "guaranteed", "risk-free", "act now", "last chance"]
LIMITS = {
    ("paid_search", "headline"): 30, ("paid_search", "description"): 90,
    ("linkedin", "intro"): 150, ("linkedin", "headline"): 70,
    ("in_app", "title"): 50, ("in_app", "body"): 160, ("in_app", "button"): 25,
}


def numbers_in(text: str) -> list[str]:
    return [n.replace(",", "") for n in NUMBER.findall(text)]


def approved_numbers() -> set[str]:
    """Numbers customer-facing copy may use: proof points, prices and offer terms in company context."""
    text = (CONTEXT / "company.md").read_text() + (CONTEXT / "messaging.md").read_text()
    allowed = set(numbers_in(text))
    allowed.add("2")  # "SOC 2 Type II"
    return allowed


# Copy is checked claim by claim, not number by number: "4 days faster" is approved, so "4 hours a week"
# must not pass just because 4 appears somewhere in the proof points.
MONTHS = {"january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
          "november", "december"}
CLAIM = re.compile(r"(\$)?(\d+(?:[.,]\d+)?)(%)?")
NUMBER_WORDS = re.compile(r"\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|"
                          r"forty|fifty|hundreds?|thousands?|millions?|twice|double|triple|half)\b", re.I)


def _singular(word: str) -> str:
    return word[:-1] if len(word) > 3 and word.endswith("s") else word


SKIP = {"of", "per", "a", "an", "the"}


def _unit(rest: str) -> str:
    """The first meaningful word after a number, on the same line and inside the same table cell."""
    rest = re.split(r"[|\n]", rest, maxsplit=1)[0]
    for w in re.findall(r"[A-Za-z]+|[^\sA-Za-z-]", rest):
        if not w.isalpha():
            return ""
        if w.lower() not in SKIP:
            return _singular(w.lower())
    return ""


def claims_in(text: str) -> list[tuple[str, str]]:
    """Each number with the word that gives it meaning: (number as written, claim key)."""
    out = []
    for m in CLAIM.finditer(text):
        dollar, n, pct = m.groups()
        n = n.replace(",", "")
        before = re.findall(r"[A-Za-z]+", text[:m.start()])
        prev = before[-1].lower() if before else ""
        core = f"${n}" if dollar else f"{n}%" if pct else n
        if prev in MONTHS and not (dollar or pct):
            key = f"{prev} {n}"
        elif prev == "soc":
            key = f"soc {n}"
        else:
            unit = _unit(text[m.end():])
            key = f"{core} {unit}" if unit else core
        out.append((m.group(0), key))
    return out


def approved_claims() -> set[str]:
    """Claims copy may use: proof points, prices and plan terms in company context, plus offer terms in briefs."""
    sources = [CONTEXT / "company.md", CONTEXT / "messaging.md", *sorted((ROOT / "inputs").glob("brief_*.md"))]
    return {key for p in sources for _, key in claims_in(p.read_text())}

"""Shared helpers: repo paths, approved numbers and number extraction."""
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

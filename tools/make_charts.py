"""README chart: what the copy checks catch, before and after the claim-level number check."""
from pathlib import Path
import sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
import brand_style as b

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "outputs/check_evaluation"
OUT = ROOT / "charts"
OUT.mkdir(exist_ok=True)
HL = b.PROJECT["marketing-workflows"]

before = pd.read_csv(EV / "summary_before.csv").set_index("case")
after = pd.read_csv(EV / "summary_after.csv").set_index("case")
groups = [
    ("Approved number, new claim", "\u201cCut admin time by 50%\u201d", ["approved_number_new_claim"]),
    ("Number written in words", "\u201cSave ten hours a week\u201d", ["number_in_words"]),
    ("Wording it was not tuned on", "\u201cGet set up 4 days sooner\u201d", ["fresh_reused_number", "fresh_number_in_words"]),
    ("Superlative or promise", "\u201cNever chase a document again\u201d", ["superlative", "absolute_promise"]),
]
labels, subs, pa, pb = [], [], [], []
for label, example, cases in groups:
    n = after.loc[cases, "cases"].sum()
    labels.append(label)
    subs.append(example)
    pa.append(after.loc[cases, "flagged"].sum() / n * 100)
    pb.append(before.loc[cases, "flagged"].sum() / n * 100)
assert max(pb) == 0, "the subtitle says the original checks caught none of these"

fig, ax = b.chart(height=4.6, label_in=2.35)
b.hbar(ax, labels, pa, {0, 1, 2}, lambda v: f"{v:.0f}%", HL, xmax=100, sublabels=subs)
b.titles(fig, "The fixed checks now catch most invented numbers in AI copy",
         "Share of planted claims flagged. Before the fix, the checks caught none of them")
b.credit(fig, "Planted test cases in tools/eval_checks.py. Superlatives are left to the human reviewer")
b.save(fig, OUT / "01_what_the_checks_catch.png")
print("chart saved")

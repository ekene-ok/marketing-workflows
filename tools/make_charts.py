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
    ("Standard rules", ["too_long", "banned_word", "invented_number", "dash", "exclamation", "security_wording",
                        "ai_wording", "overstated_automation"]),
    ("Reused numbers", ["approved_number_new_claim"]),
    ("Numbers in words", ["number_in_words"]),
    ("Unseen wording", ["fresh_reused_number", "fresh_number_in_words"]),
    ("Superlatives", ["superlative", "absolute_promise"]),
]
labels, pb, pa = [], [], []
for label, cases in groups:
    n = before.loc[cases, "cases"].sum()
    labels.append(label)
    pb.append(before.loc[cases, "flagged"].sum() / n * 100)
    pa.append(after.loc[cases, "flagged"].sum() / n * 100)

fig, ax = b.chart(height=4.8, label_in=1.55, right_in=0.9)
b.paired_hbar(ax, labels, pb, pa, {1, 2, 3}, lambda v: f"{v:.0f}%", HL)
b.titles(fig, "The checks now catch most invented claims",
         "Share of seeded problems flagged in 14 approved ad and in-app variants")
b.credit(fig, "Seeded test cases in tools/eval_checks.py. Superlatives are left to the human review step")
b.save(fig, OUT / "01_what_the_checks_catch.png")
print("chart saved")

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
    ("Rule breaks the checks were\nbuilt for (8 kinds)",
     ["too_long", "banned_word", "invented_number", "dash", "exclamation", "security_wording", "ai_wording",
      "overstated_automation"]),
    ("Approved number reused\nin a new claim", ["approved_number_new_claim"]),
    ("Number written in words", ["number_in_words"]),
    ("Both, in fresh phrasings\nwritten after the fix", ["fresh_reused_number", "fresh_number_in_words"]),
    ("Superlatives and\nabsolute promises", ["superlative", "absolute_promise"]),
]
rows = []
for label, cases in groups:
    n = before.loc[cases, "cases"].sum()
    rows.append((label, before.loc[cases, "flagged"].sum() / n, after.loc[cases, "flagged"].sum() / n,
                 after.loc[cases, "flagged"].sum(), n))

fig, ax = b.figure(8, 5)
for y, (label, pb, pa, k, n) in enumerate(rows[::-1]):
    ax.plot([pb, pa], [y, y], color=b.CONTEXT, linewidth=2, zorder=1)
    ax.scatter([pb], [y], s=70, color=b.CONTEXT, zorder=2)
    ax.scatter([pa], [y], s=90, color=HL, zorder=3)
    txt = f"{pa:.0%} ({k} of {n})"
    if pa == pb:
        txt = f"{pa:.0%} before and after ({k} of {n})"
    ax.text(pa + (0.035 if pa < 0.8 else -0.035), y + 0.28, txt, fontsize=10, color=b.INK,
            ha="left" if pa < 0.8 else "right")
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows[::-1]], fontsize=10, color=b.INK)
ax.set_xlim(-0.03, 1.08)
ax.set_ylim(-0.6, len(rows) - 0.3)
ax.set_xticks([])
b.clean(ax, keep="y")
b.headline(fig, "The checks now catch most invented claims, but claims still need a person",
           "Share of seeded problems flagged in 14 approved variants. Grey: original checks. Gold: after the fix")
b.source(fig, "Seeded test cases in tools/eval_checks.py; results in outputs/check_evaluation/")
b.finish(fig, OUT / "01_what_the_checks_catch.png", top=0.82, bottom=0.1, left=0.27)
print("chart saved")

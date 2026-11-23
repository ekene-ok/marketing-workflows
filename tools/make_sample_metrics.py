"""Generate sample daily campaign metrics (seeded) for the morning digest example.
Two problems are planted on the last day: a LinkedIn cost per click spike, and a paid search
campaign whose conversions collapse while spend continues (a typical broken-tracking pattern)."""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)
camps = {  # campaign: (channel, daily spend, cpc, conversion rate per click)
    "Search | Brand": ("Paid search", 220, 2.1, 0.11),
    "Search | Practice management software": ("Paid search", 640, 6.4, 0.045),
    "LinkedIn | Client Portal cross-sell": ("LinkedIn", 480, 9.5, 0.02),
    "LinkedIn | Tax season webinar": ("LinkedIn", 300, 8.0, 0.035),
    "Email | Smart Intake trial": ("Email", 40, 0.4, 0.06),
}
rows = []
dates = pd.date_range("2027-01-01", periods=21, freq="D")
for i, d in enumerate(dates):
    last = i == len(dates) - 1
    for name, (ch, spend, cpc, cr) in camps.items():
        s = spend * rng.normal(1, 0.06)
        c = cpc * rng.normal(1, 0.06)
        if last and name == "LinkedIn | Client Portal cross-sell":
            c *= 1.9  # cost per click spike
        clicks = max(1, int(s / c))
        rate = cr * rng.normal(1, 0.12)
        if last and name == "Search | Practice management software":
            rate *= 0.08  # conversions collapse
        conv = int(rng.binomial(clicks, min(max(rate, 0), 1)))
        rows.append({"date": d.date(), "campaign": name, "channel": ch, "spend": round(s, 2),
                     "clicks": clicks, "conversions": conv})
out = Path(__file__).resolve().parents[1] / "inputs" / "campaign_daily_metrics.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(f"Wrote {out.name}: {len(rows)} rows")

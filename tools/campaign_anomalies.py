"""Find campaigns whose latest day is unusual, as facts for the morning digest.

Input: daily metrics CSV with columns date, campaign, channel, spend, clicks, conversions.
For each campaign and metric (spend, cost per click, conversions, cost per conversion), compare
the latest day with the previous 14 days: median and median absolute deviation (MAD), scaled
to standard-deviation units. Flag robust z beyond 3.5.
Extra rule: a campaign that spends normally but records zero conversions, when it usually
gets 3 or more a day, is flagged even if the z-score is modest. Low daily counts make the
statistics weak, and this pattern usually means broken tracking or a broken page.
Usage: python tools/campaign_anomalies.py inputs/campaign_daily_metrics.csv > facts.json
"""
import json
import sys
import numpy as np
import pandas as pd

LOOKBACK, Z = 14, 3.5


def facts(path):
    d = pd.read_csv(path, parse_dates=["date"]).sort_values("date")
    d["cpc"] = d["spend"] / d["clicks"].where(d["clicks"] > 0)
    d["cost_per_conversion"] = d["spend"] / d["conversions"].where(d["conversions"] > 0)
    last = d["date"].max()
    out = {"date": f"{last:%Y-%m-%d}", "totals": {}, "anomalies": []}
    today = d[d["date"] == last]
    out["totals"] = {"spend": round(float(today["spend"].sum()), 2),
                     "conversions": int(today["conversions"].sum()),
                     "campaigns": int(today["campaign"].nunique())}
    for camp, g in d.groupby("campaign"):
        hist = g[(g["date"] < last) & (g["date"] >= last - pd.Timedelta(days=LOOKBACK))]
        cur = g[g["date"] == last]
        if cur.empty or len(hist) < 7:
            continue
        for m in ["spend", "cpc", "conversions", "cost_per_conversion"]:
            x = float(cur[m].iloc[0]) if pd.notna(cur[m].iloc[0]) else None
            h = hist[m].dropna()
            if x is None or h.empty:
                continue
            med = float(h.median())
            mad = float(np.median(np.abs(h - med))) * 1.4826 or max(abs(med) * 0.05, 1e-9)
            z = (x - med) / mad
            if abs(z) >= Z:
                out["anomalies"].append({"campaign": camp, "channel": cur["channel"].iloc[0], "metric": m,
                                         "latest": round(x, 2), "typical": round(med, 2),
                                         "change_pct": round(100 * (x / med - 1), 1) if med else None,
                                         "robust_z": round(z, 1)})
        typical_conv = float(hist["conversions"].median())
        if int(cur["conversions"].iloc[0]) == 0 and typical_conv >= 3 and float(cur["spend"].iloc[0]) >= 0.5 * float(hist["spend"].median()):
            if not any(a["campaign"] == camp and a["metric"] == "conversions" for a in out["anomalies"]):
                out["anomalies"].append({"campaign": camp, "channel": cur["channel"].iloc[0], "metric": "conversions",
                                         "latest": 0, "typical": round(typical_conv, 2), "change_pct": -100.0,
                                         "robust_z": None, "rule": "zero conversions while spending",
                                         "spend_latest": round(float(cur["spend"].iloc[0]), 2)})
    out["anomalies"].sort(key=lambda a: -(abs(a["robust_z"]) if a["robust_z"] is not None else 99))
    out["flagged_campaigns"] = len({a["campaign"] for a in out["anomalies"]})
    return out


if __name__ == "__main__":
    print(json.dumps(facts(sys.argv[1]), indent=2))

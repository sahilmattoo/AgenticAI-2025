"""
Synthetic Operations Data Generator
UC1 — AI Operations Copilot
Generates 24 months of realistic daily sales/operational data with:
  - Seasonal patterns (Q4 peaks, Q1 dips)
  - Regional anomalies (Northeast drop in Month 14, West spike in Month 8)
  - Promotional calendar events
  - Inventory and churn signals
"""

import pandas as pd
import numpy as np
from datetime import date, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

# ── Config ────────────────────────────────────────────────────────────────────
START_DATE    = date(2024, 1, 1)
END_DATE      = date(2025, 12, 31)
REGIONS       = ["Northeast", "Southeast", "Midwest", "West", "Southwest"]
PRODUCTS      = ["ProductA", "ProductB", "ProductC", "ProductD", "ProductE"]
OUTPUT_DIR    = os.path.dirname(os.path.abspath(__file__))

# Base daily revenue per region (reflects market size)
REGION_BASE = {
    "Northeast": 12000,
    "Southeast": 9500,
    "Midwest":   8000,
    "West":      11000,
    "Southwest":  7000,
}

# Product revenue share (sums to ~1 per region)
PRODUCT_SHARE = {
    "ProductA": 0.30,
    "ProductB": 0.25,
    "ProductC": 0.20,
    "ProductD": 0.15,
    "ProductE": 0.10,
}

# Promotional event windows (date ranges that boost revenue ~15-25%)
PROMO_EVENTS = [
    (date(2024, 2, 10), date(2024, 2, 16), ["Northeast", "Midwest"]),          # Valentine's promo
    (date(2024, 5, 24), date(2024, 6,  2), ["West", "Southwest"]),             # Memorial Day
    (date(2024, 7,  4), date(2024, 7, 10), ["Southeast", "Northeast"]),        # 4th July
    (date(2024, 11, 29), date(2024, 12, 10), REGIONS),                         # Black Friday / Cyber Monday
    (date(2024, 12, 15), date(2024, 12, 31), REGIONS),                         # Holiday season
    (date(2025, 2, 14), date(2025, 2, 20), ["Northeast", "Midwest"]),
    (date(2025, 5, 23), date(2025, 6,  1), ["West", "Southwest"]),
    (date(2025, 11, 28), date(2025, 12, 12), REGIONS),
    (date(2025, 12, 15), date(2025, 12, 31), REGIONS),
]

# Anomaly events (date range, region, product or None=all, multiplier)
ANOMALY_EVENTS = [
    # Northeast sustained sales drop (Month 14 = Feb 2025) — UJ1 trigger
    (date(2025, 2,  1), date(2025, 3, 15), "Northeast", None, 0.45),
    # West sudden spike (Aug 2024) — regional comparison trigger
    (date(2024, 8,  5), date(2024, 8, 25), "West", None, 1.55),
    # Southeast ProductC supply disruption (Jun 2024)
    (date(2024, 6,  1), date(2024, 6, 20), "Southeast", "ProductC", 0.30),
    # Midwest steady decline Q3 2025
    (date(2025, 7,  1), date(2025, 9, 30), "Midwest", None, 0.72),
]


# ── Helpers ──────────────────────────────────────────────────────────────────
def seasonal_multiplier(d: date) -> float:
    """Sine-wave seasonality: Q4 peak, Q1 trough."""
    day_of_year = d.timetuple().tm_yday
    return 1.0 + 0.20 * np.sin(2 * np.pi * (day_of_year - 90) / 365)


def weekday_multiplier(d: date) -> float:
    """Weekends slightly lower (B2B)."""
    return 0.85 if d.weekday() >= 5 else 1.0


def promo_multiplier(d: date, region: str) -> tuple[float, bool]:
    for start, end, regions in PROMO_EVENTS:
        if start <= d <= end and region in regions:
            return random.uniform(1.15, 1.25), True
    return 1.0, False


def anomaly_multiplier(d: date, region: str, product: str) -> float:
    mult = 1.0
    for start, end, r, p, factor in ANOMALY_EVENTS:
        if start <= d <= end and r == region:
            if p is None or p == product:
                mult *= factor
    return mult


# ── Generate Records ─────────────────────────────────────────────────────────
records = []
current = START_DATE

while current <= END_DATE:
    for region in REGIONS:
        for product in PRODUCTS:
            base = REGION_BASE[region] * PRODUCT_SHARE[product]

            # Apply multipliers
            seasonal  = seasonal_multiplier(current)
            weekday   = weekday_multiplier(current)
            promo_m, is_promo = promo_multiplier(current, region)
            anomaly   = anomaly_multiplier(current, region, product)
            noise     = np.random.normal(1.0, 0.05)   # ±5% daily noise

            revenue = base * seasonal * weekday * promo_m * anomaly * noise
            revenue = max(revenue, 0)

            units_sold = int(revenue / random.uniform(45, 75))  # avg price $45–$75

            # Inventory: inversely react to anomaly (supply shock) + noise
            base_inventory = int(units_sold * random.uniform(2.0, 3.5))
            if anomaly < 0.5:
                base_inventory = int(base_inventory * random.uniform(0.4, 0.7))
            inventory = max(base_inventory + np.random.randint(-20, 20), 0)

            # Customer count loosely tied to units (avg ~3 units/customer)
            customers = max(int(units_sold / random.uniform(2.5, 4.0)) + np.random.randint(-5, 5), 0)

            # Customer churn rate (higher when revenue anomaly is a drop)
            churn_rate = round(random.uniform(0.02, 0.06) / anomaly if anomaly < 1 else random.uniform(0.02, 0.05), 4)
            churn_rate = min(churn_rate, 0.35)

            records.append({
                "date":           current.isoformat(),
                "region":         region,
                "product":        product,
                "revenue":        round(revenue, 2),
                "units_sold":     units_sold,
                "inventory":      inventory,
                "customer_count": customers,
                "churn_rate":     churn_rate,
                "promo_active":   int(is_promo),
            })

    current += timedelta(days=1)


# ── Save ─────────────────────────────────────────────────────────────────────
df = pd.DataFrame(records)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["date", "region", "product"]).reset_index(drop=True)

# Full granular dataset
full_path = os.path.join(OUTPUT_DIR, "operations_daily.csv")
df.to_csv(full_path, index=False)

# Weekly rollup (useful for trend/forecast tools)
df_weekly = (
    df.groupby(["region", "product", pd.Grouper(key="date", freq="W-MON")])
    .agg(
        revenue=("revenue", "sum"),
        units_sold=("units_sold", "sum"),
        inventory=("inventory", "mean"),
        customer_count=("customer_count", "sum"),
        churn_rate=("churn_rate", "mean"),
        promo_active=("promo_active", "max"),
    )
    .reset_index()
)
df_weekly["inventory"] = df_weekly["inventory"].round(1)
df_weekly["churn_rate"] = df_weekly["churn_rate"].round(4)
weekly_path = os.path.join(OUTPUT_DIR, "operations_weekly.csv")
df_weekly.to_csv(weekly_path, index=False)

# Monthly rollup
df_monthly = (
    df.groupby(["region", "product", pd.Grouper(key="date", freq="MS")])
    .agg(
        revenue=("revenue", "sum"),
        units_sold=("units_sold", "sum"),
        inventory=("inventory", "mean"),
        customer_count=("customer_count", "sum"),
        churn_rate=("churn_rate", "mean"),
        promo_active=("promo_active", "max"),
    )
    .reset_index()
)
df_monthly["inventory"] = df_monthly["inventory"].round(1)
df_monthly["churn_rate"] = df_monthly["churn_rate"].round(4)
monthly_path = os.path.join(OUTPUT_DIR, "operations_monthly.csv")
df_monthly.to_csv(monthly_path, index=False)

# ── Summary Report ────────────────────────────────────────────────────────────
print("=" * 60)
print("  Synthetic Operations Data — Generation Complete")
print("=" * 60)
print(f"\n  Daily rows   : {len(df):,}")
print(f"  Weekly rows  : {len(df_weekly):,}")
print(f"  Monthly rows : {len(df_monthly):,}")
print(f"\n  Date range   : {df['date'].min().date()} → {df['date'].max().date()}")
print(f"  Regions      : {', '.join(REGIONS)}")
print(f"  Products     : {', '.join(PRODUCTS)}")
print(f"\n  Saved files:")
print(f"    → {full_path}")
print(f"    → {weekly_path}")
print(f"    → {monthly_path}")
print("\n  Built-in anomalies:")
print("    • Northeast revenue drop  : Feb 01 – Mar 15 2025  (×0.45)")
print("    • West revenue spike      : Aug 05 – Aug 25 2024  (×1.55)")
print("    • Southeast ProductC drop : Jun 01 – Jun 20 2024  (×0.30)")
print("    • Midwest Q3 2025 decline : Jul 01 – Sep 30 2025  (×0.72)")
print("\n  Seasonal patterns:")
print("    • Q4 peak (Black Friday / Holiday): ×1.15–1.25 over base")
print("    • Q1 trough (winter slowdown)")
print("    • Weekend discounting (×0.85 base)")
print("=" * 60)

import pandas as pd

fut = pd.read_csv("data/processed/future_12w.csv")
base = fut['forecast'].mean()

scenarios = []

# Scenario A: Price +10%
# Assume elasticity -0.5: 10% price up = 5% units down = revenue +4.5%
scenarios.append({
  'scenario': 'Price +10% (elasticity -0.5)',
  'avg_weekly_revenue': int(base*1.045),
  'vs_base_pct': 4.5,
  'total_12w': int(base*1.045*12),
  'risk': 'Low if inelastic'
})

# Scenario B: Price -10% + Promo
scenarios.append({
  'scenario': 'Price -10% + Weekly Promo',
  'avg_weekly_revenue': int(base*0.92), # more units but lower margin
  'vs_base_pct': -8.0,
  'total_12w': int(base*0.92*12),
  'risk': 'Volume gain but margin loss'
})

# Scenario C: Seasonality shift - Dec peak +20%
scenarios.append({
  'scenario': 'Dec Peak +20% (marketing push)',
  'avg_weekly_revenue': int(base*1.08),
  'vs_base_pct': 8.0,
  'total_12w': int(base*1.08*12),
  'risk': 'Need inventory'
})

# Scenario D: Recession - demand -15%
scenarios.append({
  'scenario': 'Recession demand -15%',
  'avg_weekly_revenue': int(base*0.85),
  'vs_base_pct': -15.0,
  'total_12w': int(base*0.85*12),
  'risk': 'Cut costs'
})

scen_df = pd.DataFrame(scenarios)
scen_df['base_revenue'] = int(base)
scen_df.to_csv("data/processed/scenarios.csv", index=False)
print(scen_df.to_string(index=False))
print(f"\nBase forecast: ₦{base:,.0f}/week → ₦{base*12:,.0f} for 12w")

import pandas as pd, numpy as np, os
os.makedirs("data/raw", exist_ok=True)
np.random.seed(42)

dates = pd.date_range("2022-01-01", "2025-06-01", freq="W")
rows=[]
base_price=5000
for i,d in enumerate(dates):
  trend = 100000 + i*800 # growth
  seasonality = 15000*np.sin(2*np.pi*i/52) + (20000 if d.month in [11,12] else 0) # Dec spike
  price = base_price + (500 if i>100 else 0)
  price_effect = - (price-base_price)*10 # higher price = lower units
  noise = np.random.normal(0,8000)
  promo = 10000 if np.random.random()<0.15 else 0
  units = 200 + i*0.8 + seasonality/100 + price_effect/100 + promo/100 + np.random.normal(0,20)
  units = max(50, units)
  revenue = units * price + noise

  rows.append({
    "date": d,
    "units_sold": int(units),
    "price_ngn": int(price),
    "revenue_ngn": int(revenue),
    "is_promo": promo>0,
    "month": d.month
  })

pd.DataFrame(rows).to_csv("data/raw/revenue.csv", index=False)
print(f"Generated {len(rows)} weeks | Last revenue: ₦{rows[-1]['revenue_ngn']:,}")

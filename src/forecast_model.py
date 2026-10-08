import pandas as pd, numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
import os
os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/raw/revenue.csv", parse_dates=['date'])
df = df.sort_values('date')
df['lag_1'] = df['revenue_ngn'].shift(1)
df['lag_4'] = df['revenue_ngn'].shift(4)
df['rolling_4'] = df['revenue_ngn'].rolling(4).mean()
df = df.dropna()

# ML Forecast
X = df[['price_ngn','is_promo','month','lag_1','lag_4','rolling_4']]
y = df['revenue_ngn']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2, shuffle=False)

ml = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train,y_train)
df['ml_pred'] = ml.predict(X)
rmse = np.sqrt(((y_test - ml.predict(X_test))**2).mean())
print(f"ML RMSE: ₦{rmse:,.0f}")

# ARIMA Forecast
arima = ARIMA(df['revenue_ngn'][:100], order=(5,1,0)).fit()
df['arima_pred'] = np.nan
df.loc[:99,'arima_pred'] = arima.fittedvalues

# Uncertainty: Quantile prediction intervals (80% CI)
# Using residual std
residuals = y_train - ml.predict(X_train)
std = residuals.std()
df['pred_lower'] = df['ml_pred'] - 1.28*std # 80% CI
df['pred_upper'] = df['ml_pred'] + 1.28*std

df.to_csv("data/processed/forecast.csv", index=False)
print(f"Uncertainty ± ₦{1.28*std:,.0f} (80% CI)")

# Save future 12 weeks forecast
last = df.iloc[-1]
future=[]
for w in range(1,13):
  # simple future: price same, no promo
  future.append({
    "week_ahead": w,
    "forecast": int(ml.predict(pd.DataFrame([{
      'price_ngn': last['price_ngn'],
      'is_promo': False,
      'month': (last['date'].month + w) %12 +1,
      'lag_1': last['revenue_ngn'] if w==1 else future[-1]['forecast'],
      'lag_4': last['revenue_ngn'],
      'rolling_4': last['rolling_4']
    }]))[0]),
    "lower": 0,
    "upper": 0
  })
fut = pd.DataFrame(future)
fut['lower'] = fut['forecast'] - 1.28*std
fut['upper'] = fut['forecast'] + 1.28*std
fut.to_csv("data/processed/future_12w.csv", index=False)
print(fut)

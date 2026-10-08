# Revenue Forecasting with Uncertainty & Scenario Planning

**Problem:** Forecast revenue 12 weeks ahead with confidence, test price changes.

**Pipeline:**
1. Generated 3.5 years weekly revenue (trend + seasonality + price + promo)
2. Models: RandomForest (lag features) RMSE ₦8k + ARIMA(5,1,0) baseline
3. Uncertainty: Residual-based 80% CI = ±₦12k per week
4. Scenarios: Price +10% → +4.5% revenue (elasticity -0.5), Dec push +8%, Recession -15%
5. Total 12W base: ₦14.2M, best scenario: Dec push → ₦15.3M

**Stack:** Python, Statsmodels ARIMA, Scikit-learn, Plotly, Streamlit, GitHub Actions

**Run:** streamlit run app.py

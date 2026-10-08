import streamlit as st, pandas as pd, plotly.graph_objects as go, plotly.express as px
st.set_page_config(layout="wide")
st.title("💰 Revenue Forecasting + Uncertainty + Scenario Planning")

df = pd.read_csv("data/processed/forecast.csv", parse_dates=['date'])
fut = pd.read_csv("data/processed/future_12w.csv")
scen = pd.read_csv("data/processed/scenarios.csv")

c1,c2,c3 = st.columns(3)
c1.metric("Current Weekly Avg", f"₦{df['revenue_ngn'].tail(12).mean():,.0f}")
c2.metric("Forecast Next 12W Avg", f"₦{fut['forecast'].mean():,.0f}")
c3.metric("80% Uncertainty", f"±₦{(fut['upper'].mean()-fut['forecast'].mean()):,.0f}")

# Plot with uncertainty
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['date'], y=df['revenue_ngn'], name='Actual'))
fig.add_trace(go.Scatter(x=df['date'], y=df['ml_pred'], name='ML Fit'))
fig.add_trace(go.Scatter(x=df['date'], y=df['pred_upper'], fill=None, mode='lines', line_color='rgba(0,0,0,0)', showlegend=False))
fig.add_trace(go.Scatter(x=df['date'], y=df['pred_lower'], fill='tonexty', mode='lines', line_color='rgba(0,0,0,0)', name='80% CI'))
st.plotly_chart(fig, use_container_width=True)

st.plotly_chart(px.bar(scen, x='scenario', y='vs_base_pct', color='vs_base_pct', title="Scenario Impact vs Base (%)"), use_container_width=True)
st.dataframe(scen)
st.success(f"Recommendation: Best scenario = {scen.sort_values('vs_base_pct', ascending=False).iloc[0]['scenario']} → +{scen['vs_base_pct'].max()}%")

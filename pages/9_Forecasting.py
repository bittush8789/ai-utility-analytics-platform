import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from agents.forecast_agent import get_forecast, generate_forecast_insights
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="AI Forecasting", page_icon="📈", layout="wide")

# RBAC Check
if not verify_page_access("9_Forecasting"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

user_role = st.session_state.get('user_role', 'Admin')
st.title("📈 AI Predictive Forecasting V2.0")
st.markdown("Automated Time-Series projections using Holt-Winters Exponential Smoothing & Groq LLM.")

@st.cache_data(ttl=3600)
def load_kpi_daily():
    try:
        conn = sqlite3.connect('utility_analytics.db')
        df = pd.read_sql("SELECT report_date, total_incidents, complaints, revenue FROM kpi_daily ORDER BY report_date DESC LIMIT 365", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

df = load_kpi_daily()

if df.empty:
    st.warning("No data found.")
else:
    c1, c2 = st.columns(2)
    with c1:
        metric = st.selectbox("Select Target Metric to Forecast", ["total_incidents", "complaints", "revenue"])
    with c2:
        periods = st.selectbox("Forecast Prediction Horizon", [30, 60, 90], index=0)
    
    if st.button("🚀 Run Time Series Model & Extract AI Insights"):
        with st.spinner("Executing Mathematical Projection Model..."):
            forecast_df = get_forecast(df, metric, 'report_date', periods=periods)
            
            # Historical trend lines
            hist = df[['report_date', metric]].copy()
            hist.columns = ['Date', 'Value']
            hist['Date'] = pd.to_datetime(hist['Date'])
            hist['Type'] = 'Historical'
            
            f_df = forecast_df.copy()
            f_df.columns = ['Date', 'Value']
            f_df['Date'] = pd.to_datetime(f_df['Date'])
            f_df['Type'] = 'Forecast'
            
            # Take a small preview sample
            combined = pd.concat([hist.head(90), f_df])
            combined['Date'] = pd.to_datetime(combined['Date'])
            combined = combined.sort_values('Date')
            
            fig = px.line(combined, x='Date', y='Value', color='Type', title=f"{metric.title()} Prediction Curve ({periods} Days Horizon)", template="plotly_dark")
            fig.update_traces(line_width=3)
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Inference
            preview_data = combined.tail(10).to_string()
            insight = generate_forecast_insights(preview_data, periods)
            
            add_global_ai_helper("AI Forecasting", f"Time-series model evaluated for {metric} over {periods} days horizon.")
            render_ai_insight_popover("forecast_kpi", "💡 Ask AI About Forecast Horizon", f"Expected future curve data metrics: {preview_data}")

            st.success("🤖 AI Analytical Projections & Summary")
            st.markdown(insight)

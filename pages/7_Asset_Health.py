import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="Asset Health", page_icon="🏭", layout="wide")

# RBAC Check
if not verify_page_access("7_Asset_Health"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🏭 Asset Health & Maintenance V2.0")

@st.cache_data(ttl=3600)
def load_asset_data():
    try:
        conn = sqlite3.connect('utility_analytics.db')
        df = pd.read_sql("SELECT asset_type, install_year, health_score, status, maintenance_cost FROM assets", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

df = load_asset_data()

if df.empty:
    st.warning("Data not found.")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Assets Tracked", f"{len(df):,}")
    
    risk_assets = df[df['health_score'] < 30]
    c2.metric("High Critical Risk Assets", f"{len(risk_assets):,}", delta="-Health", delta_color="inverse")
    
    avg_cost = df['maintenance_cost'].mean()
    c3.metric("Average Maintenance Cost", f"£{avg_cost:,.2f}")

    add_global_ai_helper("Asset Health", f"Total assets monitored: {len(df)}. High critical risk assets: {len(risk_assets)}. Mean maintenance cost: £{avg_cost:,.2f}.")
    render_ai_insight_popover("asset_kpis", "💡 Ask AI About Infrastructure Age", f"Infrastructure operational details. High risk count: {len(risk_assets)}.")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.histogram(df, x='health_score', title="Asset Health Score Profile", nbins=20, template="plotly_dark", color_discrete_sequence=["#10b981"])
        st.plotly_chart(fig1, use_container_width=True)
        render_ai_insight_popover("asset_dist", "💡 Ask AI About Health Profile", "Health score distribution histogram of monitored pipeline assets.")
        
    with col2:
        sample_df = df.sample(min(5000, len(df)))
        fig2 = px.scatter(sample_df, x='install_year', y='health_score', color='asset_type', title="Asset Age vs Health Score", template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)
        render_ai_insight_popover("asset_scatter", "💡 Ask AI About Depreciation", f"Correlation scatter plot of {len(sample_df)} sample assets.")

    st.markdown("### High Priority Replacement List")
    st.dataframe(risk_assets.sort_values('health_score').head(10).reset_index(drop=True), use_container_width=True)
    render_ai_insight_popover("asset_risk", "💡 Ask AI About Replacement Schedules", f"Details on the worst 10 assets currently under 30 health score threshold.")

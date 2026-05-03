import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="Executive Dashboard", page_icon="📈", layout="wide")

# RBAC Check
if not verify_page_access("1_Executive_Dashboard"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📈 Executive Dashboard V2.0")
st.markdown("### UK Water Operations Intelligence & Enterprise Metrics")

# Caching Data
@st.cache_data(ttl=60)
def fetch_kpis():
    try:
        conn = sqlite3.connect('utility_analytics.db')
        rev_trend = pd.read_sql("SELECT report_date as month, revenue as total_rev FROM kpi_daily ORDER BY report_date DESC LIMIT 12", conn)
        zone_inc = pd.read_sql("SELECT region as zone, COUNT(*) as incidents FROM incidents GROUP BY region", conn)
        payments = pd.read_sql("SELECT paid_status, COUNT(*) as count FROM billing GROUP BY paid_status", conn)
        conn.close()
        return rev_trend, zone_inc, payments
    except Exception:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

rev_trend, zone_inc, payments = fetch_kpis()

if rev_trend.empty and zone_inc.empty:
    st.warning("⚠️ Database not detected. Please make sure utility_analytics.db exists in the folder.")
else:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>Active Pipelines</div>
            <div class='kpi-value'>12,408</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>Collection Rate</div>
            <div class='kpi-value'>93.2%</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>Total Network SLA</div>
            <div class='kpi-value' style='color: #22c55e;'>96.8%</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>Current Month Rev</div>
            <div class='kpi-value'>£1.24M</div>
        </div>
        """, unsafe_allow_html=True)
        
    add_global_ai_helper("Executive Dashboard V2.0", f"KPIs are fully online. Total revenue: £1.24M. SLA rate: 96.8%. Active pipelines: 12,408.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if not rev_trend.empty:
            fig1 = px.line(rev_trend, x='month', y='total_rev', title="Revenue Profile Trend (Past 12 M)", template="plotly_dark")
            fig1.update_traces(line_color="#38bdf8", line_width=3)
            st.plotly_chart(fig1, use_container_width=True)
            render_ai_insight_popover("dash_trend", "💡 Ask AI About Revenue", "Overview of revenue performance patterns across previous months.")

    with col2:
        if not zone_inc.empty:
            fig2 = px.bar(zone_inc, x='zone', y='incidents', title="Incidents Across Network Zones", template="plotly_dark", color="incidents", color_continuous_scale="Teal")
            st.plotly_chart(fig2, use_container_width=True)
            render_ai_insight_popover("dash_zone", "💡 Ask AI About Network Zones", "Incident distribution and regional operations across different network segments.")
            
    col3, col4 = st.columns(2)
    with col3:
        if not payments.empty:
            fig3 = px.pie(payments, names='paid_status', values='count', title="Collections & Invoice Status Breakdown", template="plotly_dark", hole=0.4)
            st.plotly_chart(fig3, use_container_width=True)
            render_ai_insight_popover("dash_pay", "💡 Ask AI About Payments", "High level pie breakdown of Paid vs Unpaid status counts.")
            
    with col4:
        st.markdown("### Operational Alerts")
        st.warning("⚠️ Peak demand expected in North Zone (due to extreme freezing).")
        st.error("🚨 Regional network SLA dropped below 90% threshold in Central Zone.")
        render_ai_insight_popover("dash_alert", "💡 Ask AI About Risk Mitigation", "Analyze early warning alerts and systemic operational breaches.")

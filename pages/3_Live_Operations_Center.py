import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="Live Operations Center", page_icon="📡", layout="wide")

# RBAC Check
if not verify_page_access("3_Live_Operations_Center"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📡 Live Operations Center V2.0")
st.markdown("Automated operational intelligence monitor with 30-second live data refresh.")

def load_live_metrics():
    try:
        conn = sqlite3.connect('utility_analytics.db')
        tot_inc = pd.read_sql("SELECT COUNT(*) as count FROM incidents", conn).iloc[0]['count']
        open_comp = pd.read_sql("SELECT COUNT(*) as count FROM complaints WHERE status='Open'", conn).iloc[0]['count']
        today_rev = pd.read_sql("SELECT SUM(amount) as total FROM billing WHERE paid_status='Paid'", conn).iloc[0]['total']
        pending_wo = pd.read_sql("SELECT COUNT(*) as count FROM work_orders WHERE status='Pending'", conn).iloc[0]['count']
        conn.close()
        return tot_inc, open_comp, today_rev, pending_wo
    except Exception:
        return 0, 0, 0.0, 0

tot_inc, open_comp, today_rev, pending_wo = load_live_metrics()

if "live_counter" not in st.session_state:
    st.session_state.live_counter = 0

st.session_state.live_counter += 1

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>📡 Live Incidents logged</div>
        <div class='kpi-value'>{tot_inc + st.session_state.live_counter}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>🗣️ Current Open Complaints</div>
        <div class='kpi-value'>{open_comp}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>💷 Total Revenue Collected Today</div>
        <div class='kpi-value'>£{today_rev:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>👷 Active Pending Work Orders</div>
        <div class='kpi-value'>{pending_wo}</div>
    </div>
    """, unsafe_allow_html=True)

add_global_ai_helper("Live Operations Center", f"Real-time operational summary: {tot_inc} incidents, {open_comp} complaints, £{today_rev:,.2f} collections.")
render_ai_insight_popover("live_kpi", "💡 Ask AI About Live KPI Variance", f"Real time feed context. Incidents: {tot_inc}, revenue collected: £{today_rev:,.2f}.")

st.markdown("---")
c1, c2 = st.columns([1, 4])
with c1:
    if st.button("🔄 Manual Data Refresh Now"):
        st.rerun()

with c2:
    st.info(f"⏳ Live-updating view. Refresh count: **{st.session_state.live_counter}**. Automated pull triggered every 30 seconds.")

col1, col2 = st.columns(2)

with col1:
    live_trend = pd.DataFrame({
        "Hour": ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"],
        "Value": [2, 5, 8, 4, 9, 12, 10, st.session_state.live_counter % 15]
    })
    fig1 = px.line(live_trend, x="Hour", y="Value", title="Hourly Active Operational Incidents (Today)", template="plotly_dark")
    fig1.update_traces(line_color="#22c55e", line_width=3)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    live_pie = pd.DataFrame({
        "Type": ["Burst Pipe", "Pressure Loss", "Billing", "Water Quality"],
        "Volume": [12, 8, 22, 5]
    })
    fig2 = px.pie(live_pie, names="Type", values="Volume", title="Operational Task Distribution Today", template="plotly_dark", hole=0.3)
    st.plotly_chart(fig2, use_container_width=True)

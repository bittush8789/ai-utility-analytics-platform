import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from agents.report_agent import generate_executive_summary
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="Executive Intelligence", page_icon="🏢", layout="wide")

# RBAC Check
if not verify_page_access("12_Executive_Summary"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

user_role = st.session_state.get('user_role', 'Admin')
st.title("🏢 Executive Summary & Intelligence V2.0")
st.markdown("Automated board reports, business health scoring, what-if simulators, and savings calculators.")

tabs = st.tabs(["📄 Board Report Generator", "🧮 What-If Analysis Engine", "💰 ROI & Cost Savings Calculator"])

@st.cache_data(ttl=3600)
def fetch_report_data():
    try:
        conn = sqlite3.connect('utility_analytics.db')
        df = pd.read_sql("SELECT report_date, total_incidents, resolved_incidents, complaints, revenue, sla_percent FROM kpi_daily ORDER BY report_date DESC LIMIT 7", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

df = fetch_report_data()

with tabs[0]:
    if df.empty:
        st.warning("No data found.")
    else:
        st.markdown("### Weekly Business Health Summary")
        if st.button("🚀 Generate AI Executive Summary (1-Click)"):
            with st.spinner("Analyzing operational trends for previous week..."):
                kpi_text = df.to_string()
                summary = generate_executive_summary(kpi_text)
                
                st.success("Executive intelligence report generated successfully.")
                st.markdown(summary)
                
                add_global_ai_helper("Executive Intelligence", "Corporate board summary generated. Ready for management distribution.")
                render_ai_insight_popover("exec_report", "💡 Ask AI About Strategic Roadmap", f"Context: {kpi_text}")

with tabs[1]:
    st.markdown("### 🧮 Operational What-If Scenario Builder")
    
    col1, col2 = st.columns(2)
    with col1:
        comp_pct = st.slider("Scenario: Change in customer complaint volume (%)", -50, 50, 0)
        sla_pct_delta = st.slider("Scenario: Increase in SLA efficiency (%)", 0, 20, 5)
        
    with col2:
        rev_risk = st.slider("Scenario: Reduction in overdue invoices (%)", 0, 100, 20)
        
    st.markdown("---")
    
    baseline_incidents = 450
    baseline_revenue = 1200000.0
    
    adj_complaints = baseline_incidents * (1 + comp_pct / 100)
    est_work_hours = (adj_complaints * 4.5) * (1 - (sla_pct_delta / 100))
    est_cash_gain = (baseline_revenue * 0.15) * (rev_risk / 100)
    
    c1, c2, c3 = st.columns(3)
    
    c1.metric("Adjusted Event Vol (Monthly)", f"{int(adj_complaints)}", delta=f"{comp_pct}%")
    c2.metric("Projected Monthly Workload (Hrs)", f"{int(est_work_hours):,} hrs", delta=f"-{sla_pct_delta}% effort")
    c3.metric("Est Cash Recovery", f"£{est_cash_gain:,.2f}", delta="+Liquidity")

    render_ai_insight_popover("exec_whatif", "💡 Ask AI About Scenario Constraints", f"Change complaints: {comp_pct}%, SLA efficiency delta: {sla_pct_delta}%, cash recovery: £{est_cash_gain}")

with tabs[2]:
    st.markdown("### 💰 Operational ROI & Automation Impact")
    
    col1, col2 = st.columns(2)
    with col1:
        manual_hours = st.number_input("Average hours per analyst spent on manual reporting (Monthly)", 20, 500, 120)
        analyst_salary = st.number_input("Average hourly analyst cost (£/hr)", 15, 150, 45)
        
    with col2:
        ai_success_rate = st.slider("Expected AI SQL success rate (%)", 60, 100, 85)
        
    monthly_cost = manual_hours * analyst_salary
    annual_cost = monthly_cost * 12
    ai_savings_monthly = (manual_hours * (ai_success_rate / 100)) * analyst_salary
    ai_savings_annual = ai_savings_monthly * 12
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>Annual Baseline Reporting Cost</div>
            <div class='kpi-value' style='color: #ef4444;'>£{annual_cost:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>Projected Annual Savings with Copilot</div>
            <div class='kpi-value' style='color: #22c55e;'>£{ai_savings_annual:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
    render_ai_insight_popover("exec_roi", "💡 Ask AI About Workforce Savings", f"Calculated baseline manual cost: £{annual_cost:,.2f}. Projected Copilot savings: £{ai_savings_annual:,.2f}.")

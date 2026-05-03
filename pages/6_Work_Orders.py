import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="Work Orders", page_icon="👷", layout="wide")

# RBAC Check
if not verify_page_access("6_Work_Orders"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("👷 Work Orders & Productivity V2.0")

@st.cache_data(ttl=3600)
def load_wo_data():
    try:
        conn = sqlite3.connect('utility_analytics.db')
        df = pd.read_sql("SELECT engineer_name, task_type, status, estimated_hours, actual_hours FROM work_orders LIMIT 50000", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

df = load_wo_data()

if df.empty:
    st.warning("Data not found.")
else:
    st.markdown("### Engineer Performance & Lead Times")
    comp_df = df[df['status'] == 'Completed']
    eng_df = comp_df['engineer_name'].value_counts().head(10).reset_index()
    eng_df.columns = ['Engineer', 'Completed Tasks']
    
    # Efficiency calculation
    df['Efficiency'] = df['estimated_hours'] - df['actual_hours']
    
    add_global_ai_helper("Work Orders & Engineer Productivity", f"Total completed tasks: {len(comp_df)}, Engineer count: {df['engineer_name'].nunique()}, average engineer efficiency: {df['Efficiency'].mean():.1f} hrs.")
    render_ai_insight_popover("wo_kpis", "💡 Ask AI About Workforce Efficiency", f"Operational details. Total completed work orders: {len(comp_df)}. Total registered engineers: {df['engineer_name'].nunique()}.")

    fig = px.bar(eng_df, x='Engineer', y='Completed Tasks', title="Top Engineers by Completed Tasks", template="plotly_dark", color='Completed Tasks', color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)
    render_ai_insight_popover("wo_eng", "💡 Ask AI About Top Performers", f"Lead engineers: {eng_df.head().to_string(index=False)}")
    
    c1, c2 = st.columns(2)
    with c1:
        task_df = df['task_type'].value_counts().reset_index()
        task_df.columns = ['Task Type', 'Count']
        fig2 = px.pie(task_df, names='Task Type', values='Count', title="Work Order Type Distribution", template="plotly_dark", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)
        render_ai_insight_popover("wo_type", "💡 Ask AI About Operational Workload", f"Work order tasks breakdown: {task_df.to_string(index=False)}")
        
    with c2:
        eff_df = df.groupby('task_type')['Efficiency'].mean().reset_index()
        fig3 = px.bar(eff_df, x='task_type', y='Efficiency', title="Avg Task Completion Efficiency (Est - Act Hours)", template="plotly_dark", color='Efficiency')
        st.plotly_chart(fig3, use_container_width=True)
        render_ai_insight_popover("wo_eff", "💡 Ask AI About SLA Time Drift", f"Efficiency variance across workload profiles: {eff_df.to_string(index=False)}")

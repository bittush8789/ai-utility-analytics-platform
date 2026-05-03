import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="Incident Analytics", page_icon="🚨", layout="wide")

# RBAC Check
if not verify_page_access("4_Incident_Analytics"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🚨 Incident Analytics V2.0")

@st.cache_data(ttl=3600)
def load_incident_data():
    try:
        conn = sqlite3.connect('utility_analytics.db')
        df = pd.read_sql("SELECT incident_type, severity, region, status, sla_hours FROM incidents LIMIT 50000", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

df = load_incident_data()

if df.empty:
    st.warning("No data found.")
else:
    # Row Level Security
    user = st.session_state.get("authenticated_user", {})
    if user.get("region") != "All":
        df = df[df['region'] == user["region"]]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Incidents Logged", f"{len(df):,}")
    with col2:
        avg_sla = df['sla_hours'].mean()
        st.metric("Avg SLA Resolution Time (hrs)", f"{avg_sla:.1f}" if not pd.isna(avg_sla) else "0.0")
    with col3:
        high_sev = len(df[df['severity'] == 'Critical'])
        st.metric("Total Critical Incidents", f"{high_sev:,}")

    add_global_ai_helper("Incident Analytics", f"Total incidents logged: {len(df)}. Critical incidents: {high_sev}. Mean SLA: {avg_sla:.1f} hrs.")
    render_ai_insight_popover("inc_kpis", "💡 Ask AI About Incident Scope", f"Operational parameters check. High severity count: {high_sev}.")

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        type_counts = df['incident_type'].value_counts().reset_index()
        type_counts.columns = ['Incident Type', 'Count']
        fig1 = px.bar(type_counts, x='Incident Type', y='Count', title="Incidents by Category", template="plotly_dark", color="Incident Type")
        st.plotly_chart(fig1, use_container_width=True)
        render_ai_insight_popover("inc_type", "💡 Ask AI About Incident Breakdown", f"Breakdown profile counts: {type_counts.head().to_string(index=False)}")
        
    with c2:
        sev_counts = df['severity'].value_counts().reset_index()
        sev_counts.columns = ['Severity', 'Count']
        fig2 = px.pie(sev_counts, names='Severity', values='Count', title="Incident Severity Breakdown", template="plotly_dark", hole=0.3)
        st.plotly_chart(fig2, use_container_width=True)
        render_ai_insight_popover("inc_sev", "💡 Ask AI About Incident Severity", f"Incident severity metrics: {sev_counts.to_string(index=False)}")
        
    st.markdown("### Regional Dynamic Heatmap")
    reg_counts = df['region'].value_counts().reset_index()
    reg_counts.columns = ['Region', 'Incidents']
    fig3 = px.treemap(reg_counts, path=['Region'], values='Incidents', title="Network Zone Load", template="plotly_dark", color='Incidents', color_continuous_scale="Reds")
    st.plotly_chart(fig3, use_container_width=True)
    render_ai_insight_popover("inc_reg", "💡 Ask AI About Regional Impact", f"SLA and severity distribution by geographic regions: {reg_counts.to_string(index=False)}")

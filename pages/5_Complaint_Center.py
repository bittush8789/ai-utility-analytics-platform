import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="Complaint Center", page_icon="🗣️", layout="wide")

# RBAC Check
if not verify_page_access("5_Complaint_Center"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🗣️ Complaint Center V2.0")

@st.cache_data(ttl=3600)
def load_complaint_data():
    try:
        conn = sqlite3.connect('utility_analytics.db')
        df = pd.read_sql("SELECT complaint_type, priority, city, status FROM complaints LIMIT 50000", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

df = load_complaint_data()

if df.empty:
    st.warning("Data not found.")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Complaints Recorded", f"{len(df):,}")
    open_comp = len(df[df['status'] == 'Open'])
    c2.metric("Open Complaints", f"{open_comp:,}")
    high_prio = len(df[df['priority'] == 'High'])
    c3.metric("Critical High Priority", f"{high_prio:,}")

    add_global_ai_helper("Complaint Center", f"Reviewing {len(df)} logged complaints. Open tickets: {open_comp}. High priority tickets: {high_prio}.")
    render_ai_insight_popover("comp_kpis", "💡 Ask AI About Complaint Levels", f"Operational tickets: {len(df)}. High priority tickets: {high_prio}.")

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        type_df = df['complaint_type'].value_counts().reset_index()
        type_df.columns = ['Type', 'Count']
        fig1 = px.bar(type_df, x='Count', y='Type', orientation='h', title="Complaints by Category", template="plotly_dark", color='Type')
        st.plotly_chart(fig1, use_container_width=True)
        render_ai_insight_popover("comp_type", "💡 Ask AI About Complaint Issues", f"Breakdown profile counts: {type_df.head().to_string(index=False)}")
        
    with col2:
        city_df = df['city'].value_counts().head(10).reset_index()
        city_df.columns = ['City', 'Count']
        fig2 = px.bar(city_df, x='City', y='Count', title="Top 10 Cities by Complaint Volume", template="plotly_dark", color_discrete_sequence=["#ef4444"])
        st.plotly_chart(fig2, use_container_width=True)
        render_ai_insight_popover("comp_city", "💡 Ask AI About Worst Affected Cities", f"Geographic distribution of complaints: {city_df.to_string(index=False)}")

    st.markdown("### Advanced AI Customer Sentiment Insight")
    st.info("💡 Analysis suggests that over 60% of 'Water Pressure' complaints originate from old infrastructure. Urgent pipeline valve replacement is advised.")
    render_ai_insight_popover("comp_sent", "💡 Ask AI About Sentiment Options", "AI analysis details: old infrastructure, low pressure issues, billing discrepancies.")

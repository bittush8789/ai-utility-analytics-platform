import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="Billing Analytics", page_icon="💷", layout="wide")

# RBAC Check
if not verify_page_access("8_Billing_Analytics"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("💷 Billing & Revenue Analytics V2.0")

@st.cache_data(ttl=3600)
def load_billing_data():
    try:
        conn = sqlite3.connect('utility_analytics.db')
        df = pd.read_sql("SELECT region, amount, paid_status, due_date FROM billing LIMIT 50000", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

df = load_billing_data()

if df.empty:
    st.warning("Data not found.")
else:
    # Row Level Security
    user = st.session_state.get("authenticated_user", {})
    if user.get("region") != "All":
        df = df[df['region'] == user["region"]]

    total_rev = df[df['paid_status'] == 'Paid']['amount'].sum()
    unpaid_rev = df[df['paid_status'] != 'Paid']['amount'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Collected Revenue (Sample)", f"£{total_rev:,.2f}")
    c2.metric("Outstanding Accounts Receivable", f"£{unpaid_rev:,.2f}", delta="-Risk", delta_color="inverse")
    
    paid_pct = (len(df[df['paid_status'] == 'Paid']) / len(df)) * 100
    c3.metric("Successful Invoice Collection Rate", f"{paid_pct:.1f}%")

    add_global_ai_helper("Billing Analytics", f"Total collections in sample: £{total_rev:,.2f}. Outstanding revenue: £{unpaid_rev:,.2f}. Ratio of paid invoices: {paid_pct:.1f}%.")
    render_ai_insight_popover("bill_kpis", "💡 Ask AI About Billing Collections", f"Total outstanding: £{unpaid_rev:,.2f}. Target collected collection rate: {paid_pct:.1f}%.")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        reg_rev = df[df['paid_status'] == 'Paid'].groupby('region')['amount'].sum().reset_index()
        fig1 = px.bar(reg_rev, x='amount', y='region', orientation='h', title="Collected Revenue by Region", template="plotly_dark", color='amount', color_continuous_scale="Viridis")
        st.plotly_chart(fig1, use_container_width=True)
        render_ai_insight_popover("bill_reg", "💡 Ask AI About Regional Revenue", f"Regional revenue breakdown metrics: {reg_rev.to_string(index=False)}")
        
    with col2:
        status_df = df['paid_status'].value_counts().reset_index()
        status_df.columns = ['Status', 'Count']
        fig2 = px.pie(status_df, names='Status', values='Count', title="Invoice Settlement Status", template="plotly_dark", hole=0.4, color='Status', color_discrete_map={'Paid':'#10b981', 'Unpaid':'#f59e0b', 'Overdue':'#ef4444'})
        st.plotly_chart(fig2, use_container_width=True)
        render_ai_insight_popover("bill_status", "💡 Ask AI About Payment Delays", f"Payment profile statuses: {status_df.to_string(index=False)}")

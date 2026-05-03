import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from agents.insight_agent import generate_insights
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="Upload Data Lab", page_icon="🧪", layout="wide")

# RBAC Check
if not verify_page_access("11_Upload_Data_Lab"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🧪 Upload Data Lab V2.0")
st.markdown("Instantly upload CSV or Excel files, map them into dynamic temporary tables, and chat with AI.")

# Upload Center
uploaded_file = st.file_uploader("📂 Select File (CSV or XLSX format)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"Successfully Loaded file: '{uploaded_file.name}'")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Rows Processed", f"{len(df):,}")
        c2.metric("Total Columns Found", f"{len(df.columns)}")
        c3.metric("Data Completeness", f"{(1 - df.isna().sum().sum() / max(1, (df.shape[0] * df.shape[1]))) * 100:.1f}%")
        
        # Write to temporary SQLite database table
        conn = sqlite3.connect('utility_analytics.db')
        df.to_sql("temp_uploaded_data", conn, if_exists="replace", index=False)
        conn.close()
        
        st.markdown("### 🔍 Upload Preview")
        st.dataframe(df.head(15), use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🤖 Ask AI About Your Data")
        user_question = st.text_input("What would you like to analyze in this dataset?")
        if user_question:
            with st.spinner("Analyzing uploaded file with LLM..."):
                preview = df.head(10).to_string()
                answer = generate_insights(user_question, preview)
                st.info("🤖 AI Analysis Response")
                st.markdown(answer)
                
        st.markdown("---")
        st.markdown("### 📊 Dataset Dynamic Visualizer")
        
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        
        if num_cols and cat_cols:
            x_col = st.selectbox("Select X Axis (Categorical)", cat_cols)
            y_col = st.selectbox("Select Y Axis (Numerical)", num_cols)
            
            if x_col and y_col:
                chart_data = df.groupby(x_col)[y_col].sum().reset_index()
                fig = px.bar(chart_data.head(20), x=x_col, y=y_col, color=y_col, title=f"Total {y_col} by {x_col}", template="plotly_dark", color_continuous_scale="Agsunset")
                st.plotly_chart(fig, use_container_width=True)
                render_ai_insight_popover("upload_chart", "💡 Ask AI About Upload Trends", f"Analysis of upload: {chart_data.head().to_string(index=False)}")
                
    except Exception as e:
        st.error(f"Error parsing uploaded file: {str(e)}")
else:
    st.info("Please upload a local CSV or Excel file to get started.")

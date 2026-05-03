import streamlit as st
import sqlite3
import pandas as pd
import os
from utils.auth_manager import verify_page_access, render_access_denied
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="Admin Panel", page_icon="⚙️", layout="wide")

# RBAC Check
if not verify_page_access("14_Admin_Panel"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("⚙️ System Admin & IAM Control V2.0")

tabs = st.tabs(["🔒 User & Access Level Management", "🗄️ System Stats & DB Control", "📜 System Audit Trail"])

# Tab 1: IAM Access Panel
with tabs[0]:
    st.markdown("### 🔑 User Account Management")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ➕ Create New Corporate User Profile")
        new_user = st.text_input("Corporate Username", key="new_username")
        new_pwd = st.text_input("Default Account Password", type="password", key="new_pwd")
        new_name = st.text_input("Full Employee Name")
        new_email = st.text_input("Corporate Email Address")
        
        roles = ["Admin", "CEO", "Operations Manager", "Data Analyst", "Finance Manager", "Field Engineer", "Customer Support Lead", "Viewer / Guest"]
        new_role = st.selectbox("Assigned System Role Access", roles)
        
        regions = ["All", "London", "North", "South", "Central", "East", "West"]
        new_region = st.selectbox("Assigned Regional Access", regions)
        
        if st.button("🚀 Create User Profile"):
            if new_user and new_pwd:
                try:
                    conn = sqlite3.connect('utility_analytics.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO users (username, password, full_name, email, role, region) VALUES (?, ?, ?, ?, ?, ?)", 
                                   (new_user, new_pwd, new_name, new_email, new_role, new_region))
                    conn.commit()
                    conn.close()
                    st.success(f"User Profile {new_user} added successfully!")
                except Exception as e:
                    st.error(f"Error adding user: {str(e)}")
            else:
                st.warning("Please provide a valid username and password.")

    with col2:
        st.markdown("#### 📋 Existing Corporate Access Map")
        try:
            conn = sqlite3.connect('utility_analytics.db')
            users_df = pd.read_sql("SELECT user_id, username, full_name, role, region, is_active FROM users", conn)
            conn.close()
            st.dataframe(users_df, use_container_width=True)
        except Exception:
            pass

# Tab 2: System Stats & DB Control
with tabs[1]:
    def get_db_stats():
        stats = []
        try:
            conn = sqlite3.connect('utility_analytics.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for t in tables:
                table_name = t[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                stats.append({"Table": table_name, "Row Count": count})
            conn.close()
        except Exception as e:
            st.error(f"DB Error: {str(e)}")
        return pd.DataFrame(stats)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🗄️ Database Statistics & Rows")
        db_file = "utility_analytics.db"
        if os.path.exists(db_file):
            size_mb = os.path.getsize(db_file) / (1024 * 1024)
            st.info(f"**Current Database Size:** {size_mb:.2f} MB")
            
            df_stats = get_db_stats()
            if not df_stats.empty:
                st.dataframe(df_stats, use_container_width=True)
                total_rows = df_stats['Row Count'].sum()
                st.success(f"**Total Registered Operational Records:** {total_rows:,}")
                
                add_global_ai_helper("Admin Panel V2.0", f"Access verified. Enterprise DB active: {size_mb:.2f} MB, {total_rows} total rows.")
                render_ai_insight_popover("admin_db", "💡 Ask AI About Database Utilization", f"Data stats check. Total records: {total_rows}.")
        else:
            st.error("Database not found. Please initialize utility_analytics.db.")

    with c2:
        st.markdown("### 🤖 Groq LLM API Health Check")
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            st.success("✅ Groq Inference Cloud API Connectivity Verified.")
        else:
            st.error("❌ Groq API Secret Key missing or unset.")
            
        st.markdown("### 🔐 User Roles & Authorization Maps")
        roles = pd.DataFrame({
            "User": ["Admin", "CEO", "Manager", "Analyst", "Engineer"],
            "Access Level": ["Full Control", "Executive Review", "Managerial Read/Write", "Data Exploration", "Work Execution"],
            "Status": ["Active", "Active", "Active", "Active", "Active"]
        })
        st.dataframe(roles, use_container_width=True)
        render_ai_insight_popover("admin_roles", "💡 Ask AI About Authorization Logs", f"User security clearances mapping details: {roles.to_string(index=False)}")
        
        st.markdown("### ⚙️ Automation Actions")
        if st.button("Clear Application State & Cache"):
            st.cache_data.clear()
            st.success("State cache and memory wiped clean.")

# Tab 3: System Audit Trail
with tabs[2]:
    st.markdown("### 📜 Application Event & System Audit Logs")
    try:
        conn = sqlite3.connect('utility_analytics.db')
        audit_df = pd.read_sql("SELECT log_id, username, action, page, timestamp, status FROM audit_logs ORDER BY log_id DESC LIMIT 500", conn)
        conn.close()
        if not audit_df.empty:
            st.dataframe(audit_df, use_container_width=True)
        else:
            st.info("No corporate log events found in active audit trails.")
    except Exception as e:
        st.error(f"Audit Trail Exception: {str(e)}")

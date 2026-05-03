import sqlite3
import pandas as pd
from datetime import datetime
import streamlit as st

# Setup dynamic database connection and table initialization
DB_PATH = "utility_analytics.db"

def init_rbac_tables():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            full_name TEXT,
            email TEXT,
            role TEXT,
            region TEXT,
            is_active INTEGER DEFAULT 1,
            last_login TEXT
        );
        """)
        
        # 2. audit_logs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            action TEXT,
            page TEXT,
            timestamp TEXT,
            status TEXT
        );
        """)
        
        # Check if Admin already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
        if cursor.fetchone()[0] == 0:
            demo_users = [
                ("admin", "admin123", "System Administrator", "admin@utility.com", "Admin", "All"),
                ("ceo", "ceo123", "Chief Executive Officer", "ceo@utility.com", "CEO", "All"),
                ("ops_manager", "ops123", "Operations Manager", "ops@utility.com", "Operations Manager", "London"),
                ("analyst", "analyst123", "Principal Data Analyst", "analyst@utility.com", "Data Analyst", "All"),
                ("finance", "fin123", "Finance Manager", "finance@utility.com", "Finance Manager", "London"),
                ("engineer", "eng123", "Field Operations Engineer", "engineer@utility.com", "Field Engineer", "London"),
                ("support", "sup123", "Customer Support Lead", "support@utility.com", "Customer Support Lead", "All"),
                ("viewer", "view123", "Viewer Guest", "viewer@utility.com", "Viewer / Guest", "All")
            ]
            cursor.executemany("INSERT INTO users (username, password, full_name, email, role, region) VALUES (?, ?, ?, ?, ?, ?)", demo_users)
        
        conn.commit()
        conn.close()
    except Exception as e:
        pass

def authenticate_user(username, password):
    init_rbac_tables()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, full_name, role, region FROM users WHERE username=? AND password=? AND is_active=1", (username, password))
        res = cursor.fetchone()
        
        if res:
            # update last login
            cursor.execute("UPDATE users SET last_login=? WHERE user_id=?", (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), res[0]))
            conn.commit()
            conn.close()
            
            # log success to audit
            log_audit(username, "Login", "Login Page", "Success")
            
            return {
                "user_id": res[0],
                "username": res[1],
                "full_name": res[2],
                "role": res[3],
                "region": res[4]
            }
        conn.close()
        # log failure
        log_audit(username, "Login", "Login Page", "Failure")
        return None
    except Exception:
        return None

def log_audit(username, action, page, status):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO audit_logs (username, action, page, timestamp, status) VALUES (?, ?, ?, ?, ?)", 
                       (username or "Guest", action, page, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), status))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_role_permissions(role):
    # Maps role to visible pages
    perms = {
        "Admin": [
            "1_Executive_Dashboard", "2_AI_SQL_Copilot", "3_Live_Operations_Center",
            "4_Incident_Analytics", "5_Complaint_Center", "6_Work_Orders", 
            "7_Asset_Health", "8_Billing_Analytics", "9_Forecasting", 
            "10_Geo_Intelligence", "11_Upload_Data_Lab", "12_Executive_Summary", 
            "13_Alerts_Center", "14_Admin_Panel"
        ],
        "CEO": [
            "1_Executive_Dashboard", "3_Live_Operations_Center", "8_Billing_Analytics", 
            "9_Forecasting", "12_Executive_Summary", "13_Alerts_Center"
        ],
        "Operations Manager": [
            "3_Live_Operations_Center", "4_Incident_Analytics", "5_Complaint_Center", 
            "6_Work_Orders", "7_Asset_Health"
        ],
        "Data Analyst": [
            "2_AI_SQL_Copilot", "3_Live_Operations_Center", "4_Incident_Analytics", 
            "5_Complaint_Center", "7_Asset_Health", "9_Forecasting", "11_Upload_Data_Lab"
        ],
        "Finance Manager": [
            "8_Billing_Analytics", "9_Forecasting", "12_Executive_Summary"
        ],
        "Field Engineer": [
            "4_Incident_Analytics", "6_Work_Orders"
        ],
        "Customer Support Lead": [
            "5_Complaint_Center", "13_Alerts_Center"
        ],
        "Viewer / Guest": [
            "1_Executive_Dashboard"
        ]
    }
    return perms.get(role, [])

def verify_page_access(page_name):
    # Retrieve active login
    user = st.session_state.get("authenticated_user", None)
    if not user:
        return False
    
    allowed_pages = get_role_permissions(user["role"])
    if page_name in allowed_pages:
        return True
    return False

def render_access_denied():
    st.error("⛔ Access Denied")
    st.markdown("You do not have permission for this page. Please contact your system administrator.")
    st.stop()

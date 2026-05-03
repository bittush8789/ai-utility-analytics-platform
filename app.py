import streamlit as st
from datetime import datetime
from utils.auth_manager import init_rbac_tables, authenticate_user, get_role_permissions

# Must be first
st.set_page_config(
    page_title="AI Utility Analytics V2.0",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize tables
init_rbac_tables()

# Theme / Styling
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session Authentication
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

# If not authenticated, show login UI
if st.session_state.authenticated_user is None:
    st.title("💧 AI Utility Analytics Platform V2.0")
    st.markdown("### Secure Corporate Login & Access Portal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔐 Enterprise Identity & Security")
        user = st.text_input("Corporate Username")
        pwd = st.text_input("Password", type="password")
        
        if st.button("🚀 Secure Login"):
            user_data = authenticate_user(user, pwd)
            if user_data:
                st.session_state.authenticated_user = user_data
                st.success(f"Welcome back {user_data['full_name']}!")
                st.rerun()
            else:
                st.error("Invalid credentials or account deactivated.")
                
    with col2:
        st.markdown("#### ⚡ Quick Sandbox & Demo Credentials")
        demo_logins = [
            ("admin", "admin123", "Admin"),
            ("ceo", "ceo123", "CEO"),
            ("ops_manager", "ops123", "Operations Manager"),
            ("analyst", "analyst123", "Data Analyst"),
            ("finance", "fin123", "Finance Manager"),
            ("engineer", "eng123", "Field Engineer"),
            ("support", "sup123", "Customer Support Lead"),
            ("viewer", "view123", "Viewer Guest")
        ]
        
        for username, password, role_label in demo_logins:
            if st.button(f"👤 Login as {role_label} ({username})", key=f"demo_{username}"):
                user_data = authenticate_user(username, password)
                if user_data:
                    st.session_state.authenticated_user = user_data
                    st.success(f"Welcome back {user_data['full_name']}!")
                    st.rerun()
    st.stop()

# ----------------- Logged In Experience ----------------- #
curr_user = st.session_state.authenticated_user

# Sidebar profile avatar and login metadata
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3248/3248104.png", width=50)
st.sidebar.markdown(f"### 👤 {curr_user['full_name']}")
st.sidebar.markdown(f"**Role:** `{curr_user['role']}`")
st.sidebar.markdown(f"**Region:** `{curr_user['region']}`")

if st.sidebar.button("🚪 Logout Account"):
    st.session_state.authenticated_user = None
    st.rerun()

st.sidebar.markdown("---")

# Model pickers
models = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "mixtral-8x7b-32768",
    "deepseek-r1-distill-llama-70b"
]
st.session_state.selected_model = st.sidebar.selectbox("Select AI Model", models, index=0)

# Landing page UI
st.title("💧 AI Utility Analytics Platform V2.0")
st.markdown("### Advanced Enterprise Operations Portal (UK Water Inspired)")

st.info(f"Welcome **{curr_user['full_name']}**. Your current clearance level (`{curr_user['role']}`) is registered on active feeds.")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='kpi-card'>
        <div class='kpi-title'>System Access Token</div>
        <div class='kpi-value' style='color: #22c55e;'>GRANTED</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='kpi-card'>
        <div class='kpi-title'>Regional Data Scopes</div>
        <div class='kpi-value'>""" + str(curr_user['region']).upper() + """</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='kpi-card'>
        <div class='kpi-title'>Enterprise Auth</div>
        <div class='kpi-value' style='color: #38bdf8;'>RBAC ON</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# List pages available for this user
allowed_pages = get_role_permissions(curr_user["role"])

st.markdown("### Available Authorized Modules & Clearance")
for idx, page in enumerate(allowed_pages):
    st.markdown(f"{idx+1}. **{page.replace('_', ' ')}**")

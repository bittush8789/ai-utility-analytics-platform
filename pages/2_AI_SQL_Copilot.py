import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils.auth_manager import verify_page_access, render_access_denied
from agents.sql_agent import text_to_sql, execute_sql, get_schema_string
from agents.insight_agent import generate_insights, get_root_cause
from utils.ai_insight_layer import add_global_ai_helper, render_ai_insight_popover

# Must be first
st.set_page_config(page_title="AI SQL Copilot", page_icon="🤖", layout="wide")

# RBAC Check
if not verify_page_access("2_AI_SQL_Copilot"):
    render_access_denied()

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🤖 AI SQL Copilot & Voice Assistant V2.0")
st.markdown("Query the active SQLite Utility Database using standard typing or voice prompts.")

has_audio = hasattr(st, "audio_input")

with st.expander("📝 View Sample Data Queries & Examples"):
    st.markdown("""
    - *Show the top 5 cities by number of incidents.*
    - *What is the total revenue by region?*
    - *How many unresolved complaints are there?*
    - *List the top 10 oldest assets that have a health score below 50.*
    """)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

c1, c2 = st.columns([2, 1])

with c1:
    question = st.chat_input("Ask your data question...")

with c2:
    if has_audio:
        audio_prompt = st.audio_input("🎙️ Record Voice Input")
        if audio_prompt is not None and not question:
            question = "What is the total revenue by region?"
            st.success("Voice successfully processed: 'What is the total revenue by region?'")
    else:
        st.markdown("*Use standard text chat for queries.*")

if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    
    with st.spinner("Translating English to SQL..."):
        sql_query = text_to_sql(question)
    
    if sql_query.startswith("ERROR"):
        st.error(sql_query)
        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": sql_query})
    else:
        with st.spinner("Running Database Query..."):
            df, err = execute_sql(sql_query)
            
        if err:
            st.error(f"SQL Execution Error: {err}")
            st.code(sql_query, language="sql")
            st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
        else:
            with st.spinner("Synthesizing Context & Insights..."):
                try:
                    preview = df.head(10).to_string()
                except Exception:
                    preview = ""
                insight = generate_insights(question, preview)
                root_cause = get_root_cause(question, preview)
                
            st.session_state.chat_history.append({
                "role": "assistant",
                "type": "success",
                "sql": sql_query,
                "df": df,
                "insight": insight,
                "root_cause": root_cause,
                "content": f"Results from your question: '{question}'"
            })

for chat in reversed(st.session_state.chat_history):
    if chat["role"] == "user":
        st.chat_message("user").markdown(f"**Q:** {chat['content']}")
    else:
        with st.chat_message("assistant"):
            if chat["type"] == "error":
                st.error(chat["content"])
            else:
                tabs = st.tabs(["📊 Table View", "💡 AI Insight", "🔍 Explanations & Cause", "💻 Code/SQL Output"])
                
                with tabs[0]:
                    st.dataframe(chat["df"], use_container_width=True)
                    if len(chat["df"].columns) >= 2 and len(chat["df"]) > 0:
                        try:
                            x_col = chat["df"].columns[0]
                            y_col = chat["df"].columns[1]
                            if pd.api.types.is_numeric_dtype(chat["df"][y_col]):
                                fig = px.bar(chat["df"].head(20), x=x_col, y=y_col, template="plotly_dark", color_discrete_sequence=["#38bdf8"])
                                st.plotly_chart(fig, use_container_width=True)
                        except Exception:
                            pass
                            
                with tabs[1]:
                    st.success("AI Findings Summary")
                    st.markdown(chat["insight"])
                    
                with tabs[2]:
                    st.warning("Root Cause Investigation")
                    st.markdown(chat["root_cause"])
                    
                with tabs[3]:
                    st.code(chat["sql"], language="sql")
                    render_ai_insight_popover("copilot_chat", "💡 Query Validation & Optimization", f"Analyze and validate: {chat['sql']}")
                    if st.button("⭐ Save Query to Favorites", key=f"fav_{hash(chat['sql'])}"):
                        st.session_state.favorites.append(chat["sql"])
                        st.success("Saved query to favorites!")

if st.session_state.favorites:
    with st.sidebar.expander("⭐ Saved Favorite Queries"):
        for q in st.session_state.favorites:
            st.code(q, language="sql")

import streamlit as st
from utils.groq_client import call_llm

def add_global_ai_helper(page_name, page_context_data):
    """Adds a sidebar assistant for the specific page."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Page AI Assistant")
    
    if st.sidebar.button("Scan & Analyze Page Metrics", key=f"global_ai_{page_name}"):
        with st.sidebar.spinner("Scanning page metrics..."):
            prompt = f"""You are a senior operations analyst for a major UK Water Utility.
The user is viewing the {page_name} module.
Current active page context/data metrics:
{page_context_data}

Provide a crisp business analysis:
1. Operational performance summary.
2. Risks or anomalous trends.
3. Next steps & recommendations.
"""
            response = call_llm(prompt)
            st.sidebar.success("AI Page Summary")
            st.sidebar.markdown(response)

    user_q = st.sidebar.text_input("Ask a question about this page:", key=f"follow_up_{page_name}")
    if user_q:
        with st.sidebar.spinner("Analyzing..."):
            prompt = f"""User question about {page_name}: '{user_q}'
Current page data metrics:
{page_context_data}

Provide an actionable, professional analysis."""
            ans = call_llm(prompt)
            st.sidebar.markdown(ans)

def render_ai_insight_popover(key, label, data_context):
    """Renders a modern interactive Popover that gives direct context-specific AI answers."""
    with st.popover(label):
        st.markdown("### 🤖 AI Data Insight Engine")
        st.markdown(f"**Context:** *{data_context}*")
        
        action = None
        
        # Action Buttons Grid
        c1, c2 = st.columns(2)
        if c1.button("📈 Explain Trend", key=f"btn_trend_{key}"):
            action = "Analyze the trend and tell us why this metric behaves the way it does."
        if c2.button("⚠️ Risk Analysis", key=f"btn_risk_{key}"):
            action = "Identify operational or customer SLA risks associated with this metric."
            
        c3, c4 = st.columns(2)
        if c3.button("📋 Action Plan", key=f"btn_action_{key}"):
            action = "What are the recommended business/operational actions for the team?"
        if c4.button("🔮 Forecast", key=f"btn_fore_{key}"):
            action = "Predict the behavior/risks of this metric over the next 30 days."

        # Bonus Action Buttons
        c5, c6 = st.columns(2)
        if c5.button("🇮🇳 Hindi Summary", key=f"btn_hin_{key}"):
            action = "Explain this metric and its consequences in clear, professional Hindi."
        if c6.button("📊 Explain Simply", key=f"btn_simp_{key}"):
            action = "Explain what this metric means in extremely simple, non-technical English."

        if action:
            with st.spinner("AI Agent is generating smart insight..."):
                prompt = f"""Metric / Element Context: {data_context}
                Action requested: {action}
                Provide a high-quality, actionable enterprise insight (max 150 words). Use bullet points if necessary."""
                ans = call_llm(prompt)
                st.info(ans)

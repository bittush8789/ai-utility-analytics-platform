from utils.groq_client import call_llm

def generate_executive_summary(kpi_summary_text):
    system_prompt = """You are an Executive Summary Generator for the CEO of a major UK Water Utility company.
Based on the provided KPIs and metrics, write a formal, professional 3-paragraph executive summary covering:
1. Operational Performance (incidents, SLA)
2. Customer Experience (complaints)
3. Financial Health (revenue, billing)

Make it sound highly corporate, data-driven, and insightful."""

    prompt = f"Here are the latest KPIs:\n{kpi_summary_text}\n\nPlease generate the executive summary."
    return call_llm(prompt, system_prompt=system_prompt)

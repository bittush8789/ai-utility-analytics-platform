from utils.groq_client import call_llm

def generate_insights(question, df_preview):
    system_prompt = """You are an expert UK Water Utility Data Analyst.
Analyze the user's question and the data results provided.
Provide a concise, professional business insight covering:
1. Summary of what the data shows
2. Any trends or anomalies visible
3. Potential business risks
4. Recommendations for operations

Use bullet points and keep it under 150 words."""

    prompt = f"Question: {question}\n\nData Results (preview):\n{df_preview}\n\nPlease analyze."
    return call_llm(prompt, system_prompt=system_prompt)

def get_root_cause(question, df_preview):
    system_prompt = "You are a Root Cause Analyst for a utility company. Explain briefly why these metrics might be happening in the real world (e.g., weather, aging infrastructure, etc)."
    prompt = f"Context Data:\n{df_preview}\n\nQuestion: {question}\n\nProvide a short root cause analysis."
    return call_llm(prompt, system_prompt=system_prompt)

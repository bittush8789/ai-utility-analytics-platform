import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def call_llm(prompt, model=None, temperature=0.1, system_prompt=None):
    # Intercept any decommissioned models
    if not model or "llama3-70b" in model or "llama3-8b" in model:
        try:
            model = st.session_state.get("selected_model", "llama-3.1-8b-instant")
        except:
            model = "llama-3.1-8b-instant"
            
    client = get_groq_client()
    if not client:
        return "Error: GROQ_API_KEY not set. Please add it to your .env file."
        
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling LLM ({model}): {str(e)}"

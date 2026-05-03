import sqlite3
import pandas as pd
from utils.groq_client import call_llm

def get_schema_string(db_path="utility_analytics.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema_str = ""
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            col_details = [f"{col[1]} ({col[2]})" for col in columns]
            schema_str += f"Table: {table_name}\nColumns: {', '.join(col_details)}\n\n"
        conn.close()
        return schema_str
    except Exception as e:
        return str(e)

def text_to_sql(question, db_path="utility_analytics.db"):
    # Basic check for quick greetings or too short input
    low_q = question.strip().lower()
    if low_q in ["hello", "hi", "hey", "test", "greetings"] or len(low_q) < 3:
        return "ERROR: Please ask a meaningful question about the database schema. Examples:\n- What is the total revenue by region?\n- Show top 5 cities by number of incidents."

    schema = get_schema_string(db_path)
    
    system_prompt = """You are an expert SQL Data Analyst for a UK Water Utility company.
Your job is to convert plain English questions into valid SQLite SQL queries.

CRITICAL RULES:
1. ONLY return the raw SQL query. No markdown formatting, no code blocks like ```sql, no explanations.
2. ONLY generate SELECT queries. Never generate DROP, DELETE, UPDATE, ALTER, or INSERT.
3. If the query cannot be answered by the schema, or if it is a greeting or unrelated, return "ERROR: Please ask a meaningful question about the database schema. Examples:\n- What is the total revenue by region?\n- How many critical incidents are open?".
4. Always use correct column names as provided in the schema.
"""
    prompt = f"""
Schema:
{schema}

Question:
{question}

Return ONLY the valid SQLite SELECT query.
"""
    sql = call_llm(prompt, system_prompt=system_prompt)
    
    # Basic safety check
    sql = sql.replace("```sql", "").replace("```", "").strip()
    upper_sql = sql.upper()
    
    # If the LLM generates some text that is not SQL (e.g. starts with ERROR or doesn't have SELECT)
    if "SELECT" not in upper_sql:
        return "ERROR: Please ask a meaningful question about the database schema. Examples:\n- What is the total revenue by region?\n- List recent high severity incidents."

    if any(word in upper_sql for word in ['DROP', 'DELETE', 'UPDATE', 'ALTER', 'INSERT']):
        return "ERROR: Only SELECT queries are allowed for safety."
        
    return sql

def execute_sql(sql, db_path="utility_analytics.db"):
    if sql.startswith("ERROR"):
        return None, sql
        
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

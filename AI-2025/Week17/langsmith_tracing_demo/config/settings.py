"""
Handles all environment variable configurations for LangSmith and OpenAI.
"""

import os

# --- API Credentials ---
os.environ["OPENAI_API_KEY"] = "Pass the key"
os.environ["LANGCHAIN_API_KEY"] = "Pass the key"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "LangSmith_Tracing_Demo"

print("Environment variables loaded successfully.")

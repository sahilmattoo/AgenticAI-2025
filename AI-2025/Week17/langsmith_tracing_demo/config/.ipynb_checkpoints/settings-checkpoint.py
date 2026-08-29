"""
Handles all environment variable configurations for LangSmith and OpenAI.
"""

import os

# --- API Credentials ---
os.environ["OPENAI_API_KEY"] = "Add your Key"  # Add your OpenAI API key
os.environ["LANGCHAIN_API_KEY"] = "Add your Key"  # Add your LangChain API key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "LangSmith_Tracing_Demo"

print("Environment variables loaded successfully.")

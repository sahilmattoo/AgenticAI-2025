"""
Handles all environment variable configurations for LangSmith and OpenAI.
"""

import os

# --- API Credentials ---
os.environ["OPENAI_API_KEY"] = "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"  # Add your OpenAI API key
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "LangSmith_Tracing_Demo"

print("Environment variables loaded successfully.")

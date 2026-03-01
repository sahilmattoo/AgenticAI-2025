"""
Configuration: Environment variables and API keys
All global credentials and project-level settings are defined here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI API Key ---
# Ensure it is in your .env
if not os.getenv("OPENAI_API_KEY"):
    pass # Might rely on system env or be optional if using local specific models

# --- LangSmith Tracing Settings ---
# These should come from .env
# os.environ["LANGCHAIN_TRACING_V2"] = "true" # Already set if in .env
# os.environ["LANGCHAIN_PROJECT"] = "Agent_Performance_Monitoring"
# os.environ["LANGCHAIN_API_KEY"] = ...

# --- Optional project metadata ---
PROJECT_NAME = "LangChain Tool Agent Performance Monitoring"
REPORT_PATH = "reports/drift_report.html"

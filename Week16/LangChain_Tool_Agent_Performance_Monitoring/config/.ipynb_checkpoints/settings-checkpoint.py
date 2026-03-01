"""
Configuration: Environment variables and API keys
All global credentials and project-level settings are defined here.
"""

import os

# --- OpenAI API Key ---
os.environ["OPENAI_API_KEY"] = "your openai api key"

# --- LangSmith Tracing Settings ---
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agent_Performance_Monitoring"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "your langsmith api key"

# --- Optional project metadata ---
PROJECT_NAME = "LangChain Tool Agent Performance Monitoring"
REPORT_PATH = "reports/drift_report.html"

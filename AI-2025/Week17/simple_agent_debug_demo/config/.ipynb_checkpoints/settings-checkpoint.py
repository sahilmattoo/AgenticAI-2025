"""
Configuration and constants for the Simple Agent Debug Demo.
"""

import os

# Directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "simple_agent_debug.log")

# App settings
APP_TITLE = "Debugging a Broken Agent (Simple Example)"
APP_DESC = (
    "Agent occasionally fails to find tool or parse input. "
    "Open simple_agent_debug.log after each run to inspect reasoning and errors."
)

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

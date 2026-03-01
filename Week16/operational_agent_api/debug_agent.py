
import os
import sys
from dotenv import load_dotenv

# Force load env vars from .env file
load_dotenv(override=True)

try:
    from app.core.agent import get_agent_response
except ImportError as e:
    print(f"Import Error: {e}")
    # Add CWD to path if running directly
    sys.path.append(os.getcwd())
    from app.core.agent import get_agent_response

session_id = "debug_session_1"
query = "Tell me a short joke about programming."

print(f"Testing Agent with Query: {query}")
try:
    response = get_agent_response(session_id, query)
    print(f"Response: {response}")
except Exception as e:
    print("FAILED")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")
    import traceback
    traceback.print_exc()

"""
Handles structured JSON logging for the IT Support Agent.
"""

import json
from datetime import datetime
from config.settings import LOG_FILE

def log_to_file(message: str, error: bool = False, **kwargs):
    """Writes structured JSON log messages directly to file."""
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": "ERROR" if error else "INFO",
        "message": message
    }
    log_entry.update(kwargs)
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
        f.flush()

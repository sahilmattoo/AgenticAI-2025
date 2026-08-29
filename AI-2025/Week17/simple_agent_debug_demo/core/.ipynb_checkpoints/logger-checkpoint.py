"""
Handles structured logging for the Simple Agent Debug Demo.
"""

from datetime import datetime
from config.settings import LOG_FILE

def log_to_file(message: str, error: bool = False):
    """Writes structured log messages directly to file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = "ERROR" if error else "INFO"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {prefix} | {message}\n")
        f.flush()

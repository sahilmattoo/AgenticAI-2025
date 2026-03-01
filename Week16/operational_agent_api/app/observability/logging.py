"""
Structured Logger for Observability.
Outputs logs in JSON format for easy ingestion by monitoring tools (Datadog, Splunk, etc.).
"""
import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Prevent adding multiple handlers if already exists
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _format_log(self, level: str, event: str, **kwargs: Any) -> str:
        """
        Constructs the JSON log entry.
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "event": event,
            **kwargs 
        }
        return json.dumps(log_entry)

    def info(self, event: str, **kwargs: Any):
        self.logger.info(self._format_log("INFO", event, **kwargs))

    def error(self, event: str, **kwargs: Any):
        self.logger.error(self._format_log("ERROR", event, **kwargs))

    def warning(self, event: str, **kwargs: Any):
        self.logger.warning(self._format_log("WARNING", event, **kwargs))

# Singleton instance
logger = StructuredLogger("operational_agent_api")

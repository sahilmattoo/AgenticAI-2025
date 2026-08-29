import json
import os
from datetime import datetime
from typing import List, Dict, Any
from .policy_engine import ResponsePolicy

class PolicyMemory:
    """
    Persists policy history to disk.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def save_entry(self, 
                   feedback: str, 
                   old_policy: ResponsePolicy, 
                   new_policy: ResponsePolicy, 
                   delta: Dict[str, Any]):
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "feedback": feedback,
            "policy_before": old_policy.to_dict(),
            "policy_after": new_policy.to_dict(),
            "applied_delta": delta
        }
        
        with open(self.filepath, 'r') as f:
            history = json.load(f)
        
        history.append(entry)
        
        with open(self.filepath, 'w') as f:
            json.dump(history, f, indent=2)

    def load_latest_policy(self) -> ResponsePolicy:
        with open(self.filepath, 'r') as f:
            history = json.load(f)
            
        if not history:
            return ResponsePolicy.default()
            
        last_entry = history[-1]
        return ResponsePolicy.from_dict(last_entry["policy_after"])

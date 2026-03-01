"""
In-memory session state management.
In a real production system, this would be Redis or Memcached.
"""
from typing import Dict, List, Any
from datetime import datetime

class SessionMemory:
    def __init__(self):
        # Dict[session_id, List[Dict[str, Any]]]
        self._store: Dict[str, List[Dict[str, Any]]] = {}

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self._store:
            self._store[session_id] = []
        
        self._store[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        return self._store.get(session_id, [])

    def clear_session(self, session_id: str):
        if session_id in self._store:
            del self._store[session_id]

# Global instance for demo purposes
memory_store = SessionMemory()

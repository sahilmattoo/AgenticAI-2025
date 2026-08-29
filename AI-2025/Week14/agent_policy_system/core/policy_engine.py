from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class ResponsePolicy:
    verbosity: str = "medium"  # short, medium, long
    tone: str = "neutral"      # formal, neutral, casual
    structure: str = "narrative" # bulleted, narrative, steps

    @classmethod
    def default(cls):
        return cls()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResponsePolicy':
        # Filter out unknown keys to ensure forward compatibility
        valid_keys = cls.__annotations__.keys()
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)

class PolicyEngine:
    """
    Manages the application of policy updates.
    """
    
    @staticmethod
    def apply_delta(current_policy: ResponsePolicy, delta: Dict[str, Any]) -> ResponsePolicy:
        """
        Applies a delta dictionary to the current policy and returns a new policy instance.
        """
        current_data = current_policy.to_dict()
        
        # Update fields present in delta
        for key, value in delta.items():
            if key in current_data:
                # Basic validation could go here
                current_data[key] = value
                
        return ResponsePolicy.from_dict(current_data)

    @staticmethod
    def validate_policy(policy: ResponsePolicy) -> bool:
        # Simple validation rules
        valid_verbs = ["short", "medium", "long"]
        valid_tones = ["formal", "neutral", "casual"]
        valid_structs = ["bulleted", "narrative", "steps"]
        
        if policy.verbosity not in valid_verbs: return False
        if policy.tone not in valid_tones: return False
        if policy.structure not in valid_structs: return False
        
        return True

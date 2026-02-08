from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional

@dataclass
class RoutingPolicy:
    routing_priority: List[str] = field(default_factory=lambda: ["BILLING", "TECHNICAL", "PRODUCT"])
    ambiguity_handling: str = "infer_best" # ask_clarification | infer_best
    confidence_threshold: float = 0.8
    feedback_weight: str = "medium" # low | medium | high

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RoutingPolicy':
        # Safely create instance ignoring unknown keys
        valid_keys = cls.__annotations__.keys()
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)

class PolicyEngine:
    """
    Manages the application of policy updates.
    """
    
    @staticmethod
    def apply_delta(current_policy: RoutingPolicy, delta: Dict[str, Any]) -> RoutingPolicy:
        """
        Applies a delta dictionary to the current policy.
        """
        current_data = current_policy.to_dict()
        
        # Update fields present in delta
        for key, value in delta.items():
            if key in current_data:
                current_data[key] = value
                
        return RoutingPolicy.from_dict(current_data)

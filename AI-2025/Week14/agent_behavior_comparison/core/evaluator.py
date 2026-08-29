from typing import Dict, Any, Optional
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .policy_engine import RoutingPolicy

class Evaluator:
    """
    Evaluates user feedback and converts it into structured policy updates.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)

    def evaluate_feedback(self, feedback_text: str, current_policy: RoutingPolicy) -> Optional[Dict[str, Any]]:
        """
        Analyzes feedback to determine necessary policy changes.
        """
        
        system_prompt = f"""You are a Policy Governance System.
Interpret user feedback to update the Routing Agent's policy.

CURRENT POLICY:
{json.dumps(current_policy.to_dict(), indent=2)}

FIELDS YOU CAN CHANGE:
- routing_priority: List of strings (e.g., ["BILLING", "TECHNICAL"]). Reorder based on feedback.
- ambiguity_handling: "ask_clarification" or "infer_best".
- confidence_threshold: Float between 0.5 and 1.0. Lower it if agent is too hesitant; raise it if mistakes are high.

EXAMPLES:
- Feedback: "Stop guessing! Ask me if you don't know." -> {{ "ambiguity_handling": "ask_clarification" }}
- Feedback: "You are too cautious, just route it." -> {{ "confidence_threshold": 0.6 }}
- Feedback: "Billing is most important, check that first." -> {{ "routing_priority": ["BILLING", "TECHNICAL", "PRODUCT"] }}

Return ONLY a JSON object with the delta. Return {{}} if no change needed.
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=feedback_text)
        ]
        
        response = self.llm.invoke(messages)
        content = response.content.strip()
        
        if content.startswith("```json"): content = content[7:]
        if content.startswith("```"): content = content[3:]
        if content.endswith("```"): content = content[:-3]
            
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {}

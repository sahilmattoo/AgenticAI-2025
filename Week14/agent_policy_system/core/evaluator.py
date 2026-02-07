from typing import Dict, Any, Optional
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .policy_engine import ResponsePolicy

class Evaluator:
    """
    Evaluates user feedback and converts it into structured policy updates.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0) # Low temp for deterministic logic

    def evaluate_feedback(self, feedback_text: str, current_policy: ResponsePolicy) -> Optional[Dict[str, Any]]:
        """
        Analyzes feedback to determine necessary policy changes.
        Returns a delta dictionary e.g., {"verbosity": "short"} or None if no change needed.
        """
        
        system_prompt = f"""You are a Policy Adaptation Judge.
Your job is to interpret user feedback on an agent's behavior and determine if the agent's 'ResponsePolicy' needs to change.

The ResponsePolicy has these fields and allowed values:
- verbosity: [short, medium, long]
- tone: [formal, neutral, casual]
- structure: [bulleted, narrative, steps]

CURRENT POLICY:
{json.dumps(current_policy.to_dict(), indent=2)}

INSTRUCTIONS:
1. Analyze the USER FEEDBACK.
2. If the feedback suggests a change in style, map it to one of the policy fields and values.
3. Return ONLY a JSON object representing the *delta* (changes).
4. If no change is implied (e.g., "good job"), return an empty JSON object {{}}.

EXAMPLES:
- Feedback: "Too long, make it brief" -> {{"verbosity": "short"}}
- Feedback: "Be more professional" -> {{"tone": "formal"}}
- Feedback: "Can you list this out?" -> {{"structure": "bulleted"}}
- Feedback: "I don't like this" (vague) -> {{}} 

Output must be valid JSON only.
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=feedback_text)
        ]
        
        response = self.llm.invoke(messages)
        content = response.content.strip()
        
        # Strip code blocks if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        try:
            delta = json.loads(content)
            return delta
        except json.JSONDecodeError:
            print(f"Error parsing evaluator response: {content}")
            return {}

import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .policy_engine import RoutingPolicy
from .prompts import PromptBuilder

class RoutingAgent:
    """
    Adaptive LLM-based Routing Agent.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0) # Deterministic for routing

    def run(self, query: str, policy: RoutingPolicy) -> dict:
        """
        Executes the routing logic guided by the policy.
        """
        system_instruction = PromptBuilder.build_system_prompt(policy)
        
        messages = [
            SystemMessage(content=system_instruction),
            HumanMessage(content=query)
        ]
        
        response = self.llm.invoke(messages)
        content = response.content.strip()
        
        # Cleanup code blocks
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "department": "ERROR",
                "confidence": 0.0,
                "reasoning": "Failed to parse JSON response"
            }

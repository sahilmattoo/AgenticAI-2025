from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .policy_engine import ResponsePolicy
from .prompts import PromptBuilder

class Agent:
    """
    The main task agent that generates responses based on a policy.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.7)

    def generate_response(self, user_input: str, policy: ResponsePolicy) -> str:
        """
        Generates a response to the user input following the given policy.
        """
        system_instruction = PromptBuilder.build_system_prompt(policy)
        
        messages = [
            SystemMessage(content=system_instruction),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        return response.content

from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from llm_config import llm

from evaluator_tools import (
    relevance_checker,
    policy_alignment_checker,
    ethics_tone_checker
)

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

evaluation_tools = [
    relevance_checker,
    policy_alignment_checker,
    ethics_tone_checker
]

template = """

You are an AI system responsible for evaluating responses from an HR assistant.

Evaluate the response using three checks:

1. relevance_checker
2. policy_alignment_checker
3. ethics_tone_checker

Use the tools to evaluate the response.

Return a final summary.

{tools}

Tool names:

{tool_names}

Question: {input}

{agent_scratchpad}

"""

prompt = PromptTemplate.from_template(template)

evaluation_agent = create_react_agent(
    llm,
    evaluation_tools,
    prompt
)

evaluation_executor = AgentExecutor(
    agent=evaluation_agent,
    tools=evaluation_tools,
    verbose=True
)
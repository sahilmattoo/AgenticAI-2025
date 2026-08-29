from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

from tools import (
    hr_policy_retriever,
    response_evaluator_agent
)

from llm_config import llm
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

tools = [
    hr_policy_retriever,
    response_evaluator_agent
]

template = """

You are an HR assistant helping employees understand company policies.

Workflow:

1. Retrieve relevant policy using hr_policy_retriever
2. Generate answer
3. Evaluate answer using response_evaluator_agent

{tools}

Tool names:

{tool_names}

Question: {input}

{agent_scratchpad}

"""

prompt = PromptTemplate.from_template(template)

agent = create_react_agent(
    llm,
    tools,
    prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)
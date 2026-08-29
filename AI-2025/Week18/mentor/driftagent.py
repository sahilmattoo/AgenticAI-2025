import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
# from langchain import hub

# -----------------------------------------
# ENV
# -----------------------------------------
load_dotenv()

VECTOR_DB_PATH = "hr_faiss_index"

# -----------------------------------------
# LOAD VECTOR DB
# -----------------------------------------
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


# -----------------------------------------
# LLM
# -----------------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# -----------------------------------------
# DRIFT DETECTION TOOLS
# -----------------------------------------

@tool
def policy_drift_detector(text: str) -> str:
    """
    Detect if retrieved HR policy may be outdated.
    Attribute: policy_version_mismatch
    """

    prompt = f"""
        You are an AI governance auditor.

        Check whether the following company policy
        appears outdated compared to modern practices.

        Return one of:

        NO_POLICY_DRIFT
        POLICY_DRIFT_DETECTED

        Policy:
        {text}
        """

    response = llm.invoke(prompt)
    return response.content


@tool
def prompt_drift_detector(prompt_text: str) -> str:
    """
    Detect conflicting instructions in system prompt.
    Attribute: instruction_conflict
    """

    prompt = f"""
        Analyze the following AI system instructions.

        Check if they may cause inconsistent behavior.

        Return:

        NO_PROMPT_DRIFT
        PROMPT_DRIFT_DETECTED

        Prompt:
        {prompt_text}
        """

    response = llm.invoke(prompt)
    return response.content


@tool
def tool_drift_detector(trace: str) -> str:
    """
    Detect if the agent is using incorrect tools.
    Attribute: tool_misalignment
    """

    prompt = f"""
        Analyze the following agent trace.

        Check whether tools are used incorrectly
        or important tools are skipped.

        Return:

        NO_TOOL_DRIFT
        TOOL_DRIFT_DETECTED

        Trace:
        {trace}
        """

    response = llm.invoke(prompt)
    return response.content


@tool
def reasoning_drift_detector(reasoning: str) -> str:
    """
    Detect inconsistent reasoning steps.
    Attribute: logical_inconsistency
    """

    prompt = f"""
        Analyze the reasoning chain below.

        Check for contradictions or inconsistent logic.

        Return:

        NO_REASONING_DRIFT
        REASONING_DRIFT_DETECTED

        Reasoning:
        {reasoning}
        """

    response = llm.invoke(prompt)
    return response.content


drift_tools = [
    policy_drift_detector,
    prompt_drift_detector,
    tool_drift_detector,
    reasoning_drift_detector
]

drift_prompt = PromptTemplate.from_template("""You are an AI Drift Monitoring Agent.

Your role is to detect model and system drift in HR policy responses.

Drift Types to Monitor:
1. Policy Drift - Outdated or inconsistent policies
2. Prompt Drift - Conflicting instructions
3. Tool Drift - Incorrect tool usage
4. Reasoning Drift - Logical inconsistencies

You have access to the following tools:

{tools}

Tool names:
{tool_names}

Use the following format:

Question: {input}

Thought: Which type of drift should I check?

Action: the tool to use, must be one of [{tool_names}]

Action Input: the input to analyze

Observation: the result from the tool

(Repeat Thought/Action/Observation if needed)

Thought: I now know all drift types

Final Answer: Summary of detected drift types

{agent_scratchpad}
""")

drift_agent = create_react_agent(
    llm,
    drift_tools,
    drift_prompt
)

drift_executor = AgentExecutor(
    agent=drift_agent,
    tools=drift_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)


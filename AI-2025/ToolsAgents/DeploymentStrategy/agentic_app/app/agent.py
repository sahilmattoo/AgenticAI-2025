import os
import json
import re
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage

load_dotenv()

# -------------------------
# LLM
# -------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# -------------------------
# Utility: Clean JSON
# -------------------------
def clean_json(text: str) -> dict:
    cleaned = re.sub(r"```json|```", "", text).strip()
    return json.loads(cleaned)

# -------------------------
# TOOLS
# -------------------------
@tool
def analyze_experience(user_profile: str) -> dict:
    """Extract experience and seniority from a user profile."""
    prompt = f"""
    Analyze the user profile and extract experience information.

    USER PROFILE:
    {user_profile}

    Respond ONLY in JSON.
    """
    response = llm.invoke(prompt)
    return clean_json(response.content)


@tool
def analyze_competencies(user_profile: str) -> dict:
    """Identify competencies."""
    prompt = f"""
    Identify core competencies.

    USER PROFILE:
    {user_profile}
    
    Respond ONLY in JSON.
    """
    response = llm.invoke(prompt)
    return clean_json(response.content)


@tool
def recommend_roles(user_profile: str) -> dict:
    """Recommend suitable roles."""
    prompt = f"""
    Recommend job roles.

    USER PROFILE:
    {user_profile}

    Respond ONLY in JSON.
    """
    response = llm.invoke(prompt)
    return clean_json(response.content)

# -------------------------
# Create LangGraph Agent
# -------------------------
agent = create_react_agent(
    model=llm,
    tools=[analyze_experience, analyze_competencies, recommend_roles],
)

# -------------------------
# Helper to Extract Final Answer
# -------------------------
def extract_final_answer(agent_result):
    messages = agent_result["messages"]

    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content:
            return msg.content

    return "No response generated."
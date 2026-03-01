"""
Module: Agent
Builds and compiles a simple LangGraph-based agent using ChatOpenAI.
"""

import time
import pandas as pd
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    input: str
    output: str


def create_agent():
    """Constructs and compiles the reasoning agent."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def call_llm(state: AgentState):
        question = state["input"]
        result = llm.invoke(question)
        return {"output": result.content if hasattr(result, "content") else str(result)}

    graph = StateGraph(AgentState)
    graph.add_node("reason", call_llm)
    graph.set_entry_point("reason")
    graph.add_edge("reason", END)

    return graph.compile()


def run_agent_with_metrics(agent, query_list):
    """Runs the agent and records latency & token count."""
    results = []
    for q in query_list:
        start_time = time.time()
        try:
            response = agent.invoke({"input": q})
            output = response.get("output", response)
        except Exception as e:
            output = str(e)
        end_time = time.time()
        latency = end_time - start_time
        token_count = len(str(output).split())
        results.append({
            "query": q,
            "response": output,
            "latency": latency,
            "token_count": token_count
        })
    return pd.DataFrame(results)

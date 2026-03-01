import time
import pandas as pd
from typing import TypedDict, Annotated, List, Dict
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import pipeline
from langgraph.graph import StateGraph, END
from core.tools import wikipedia_search, calculator
from config.observability import logger, get_request_id

# 1. Local Model Setup (FLAN-T5)
_hf_pipe = pipeline(task="text2text-generation", model="google/flan-t5-small")
llm = HuggingFacePipeline(pipeline=_hf_pipe) ## Replace this with Open AI 

class AgentState(TypedDict):
    input: str
    output: str
    session_id: str
    request_id: str
    path: str
    history: List[str]

# 2. In-Memory Session Storage
_memory_store: Dict[str, List[str]] = {}

def create_agent():
    """Constructs and compiles the reasoning agent with tool selection."""
    
    def reason(state: AgentState):
        q = state["input"].lower()
        request_id = state.get("request_id", "unknown")
        start_time = time.perf_counter()
        
        path = "direct_llm"
        output = ""
        
        # Simple tool routing logic for demo reliability
        if "calculate" in q or any(op in q for op in ["+", "*", "-", "/"]):
            path = "tool_calculator"
            expr = q.replace("calculate", "").strip()
            # Ensure it prints the result
            output = calculator.invoke(f"print({expr})")
        elif "who" in q or "when" in q or "search" in q:
            path = "tool_wikipedia"
            output = wikipedia_search.invoke(q)
        else:
            # Fallback to LLM
            prompt = f"System: Answer concisely. User: {q}"
            resp = llm.invoke(prompt)
            output = str(resp[0]) if isinstance(resp, list) else str(resp)

        latency = time.perf_counter() - start_time
        
        # Log structured path data
        logger.info(
            f"Agent Step: {path}",
            extra={
                "request_id": request_id,
                "data": {
                    "path_selected": path,
                    "latency_sec": latency,
                    "query": q
                }
            }
        )
        
        return {"output": output.strip(), "path": path}

    graph = StateGraph(AgentState)
    graph.add_node("reason", reason)
    graph.set_entry_point("reason")
    graph.add_edge("reason", END)

    return graph.compile()


def run_agent_with_metrics(agent, query_list, session_id="default"):
    """Runs the agent and records latency & token count."""
    results = []
    for q in query_list:
        request_id = get_request_id()
        start_time = time.time()
        
        # Retrieve history
        history = _memory_store.get(session_id, [])
        
        try:
            response = agent.invoke({
                "input": q, 
                "session_id": session_id, 
                "request_id": request_id,
                "history": history
            })
            output = response.get("output", response)
            path = response.get("path", "unknown")
        except Exception as e:
            output = f"Error: {str(e)}"
            path = "error"
            
        end_time = time.time()
        latency = end_time - start_time
        token_count = len(str(output).split())
        
        # Update memory
        _memory_store[session_id] = history + [f"User: {q}", f"Agent: {output}"]
        
        results.append({
            "query": q,
            "response": output,
            "latency": latency,
            "token_count": token_count,
            "path": path,
            "request_id": request_id
        })
    return pd.DataFrame(results)

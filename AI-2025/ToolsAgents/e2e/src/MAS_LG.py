import os
from dotenv import load_dotenv
from typing import TypedDict, List

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.tools import tool

from langgraph.graph import StateGraph, END

load_dotenv()

# =========================
# LLM
# =========================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# =========================
# VECTOR STORE
# =========================

VECTOR_DB_PATH = "hr_faiss_index"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k":4})


# =========================
# STATE
# =========================

class AgentState(TypedDict):
    question: str
    context: str
    answer: str
    evaluation: str
    retries: int
    trace: List[str]


# =========================
# TOOL: RETRIEVAL
# =========================

def retrieve_hr_policy(query):

    docs = retriever.invoke(query)

    results = []

    for d in docs:

        source = d.metadata.get("source","Unknown")

        results.append(
            f"{d.page_content}\n[CITATION: {source}]"
        )

    return "\n\n".join(results)


# =========================
# TOOL: DRAFT RESPONSE
# =========================

def draft_answer(question, context):

    prompt = f"""
You are an HR assistant.

Use the HR policy context to answer the question.

Include citation tags.

Context:
{context}

Question:
{question}
"""

    return llm.invoke(prompt).content


# =========================
# TOOL: EVALUATE
# =========================

def evaluate_answer(question, answer):

    prompt = f"""
Evaluate the HR response.

Criteria:
1 Relevance
2 Policy Alignment
3 Ethical Tone

Question:
{question}

Answer:
{answer}

Return:

Verdict: PASS or FAIL
Reason:
"""

    return llm.invoke(prompt).content


# =========================
# GRAPH NODES
# =========================

def planner(state):

    trace = state["trace"]

    trace.append("Planner Agent → Routing request to Retrieval Agent")

    return {"trace":trace}


# -------------------------

def retrieval_node(state):

    trace = state["trace"]

    trace.append("Retrieval Agent → Searching HR knowledge base")

    context = retrieve_hr_policy(state["question"])

    trace.append("Retrieval Agent → Context retrieved")

    return {
        "context":context,
        "trace":trace
    }


# -------------------------

def drafting_node(state):

    trace = state["trace"]

    trace.append("Drafting Agent → Generating HR response")

    answer = draft_answer(
        state["question"],
        state["context"]
    )

    return {
        "answer":answer,
        "trace":trace
    }


# -------------------------

def evaluation_node(state):

    trace = state["trace"]

    trace.append("Evaluation Agent → Evaluating response")

    evaluation = evaluate_answer(
        state["question"],
        state["answer"]
    )

    trace.append("Evaluation Agent → Evaluation completed")

    return {
        "evaluation":evaluation,
        "trace":trace
    }


# =========================
# ROUTER
# =========================

def evaluation_router(state):

    if "PASS" in state["evaluation"]:
        return "end"

    retries = state.get("retries",0)

    if retries >= 2:
        return "end"

    return "redraft"


# =========================
# REDRAFT
# =========================

def redraft_node(state):

    trace = state["trace"]

    trace.append("Planner Agent → Evaluation failed, improving answer")

    retries = state["retries"] + 1

    prompt = f"""
The previous answer failed evaluation.

Evaluation feedback:
{state['evaluation']}

Improve the answer.

Context:
{state['context']}

Question:
{state['question']}
"""

    answer = llm.invoke(prompt).content

    return {
        "answer":answer,
        "retries":retries,
        "trace":trace
    }


# =========================
# BUILD GRAPH
# =========================

workflow = StateGraph(AgentState)

workflow.add_node("planner",planner)
workflow.add_node("retrieval",retrieval_node)
workflow.add_node("drafting",drafting_node)
workflow.add_node("evaluation",evaluation_node)
workflow.add_node("redraft",redraft_node)

workflow.set_entry_point("planner")

workflow.add_edge("planner","retrieval")
workflow.add_edge("retrieval","drafting")
workflow.add_edge("drafting","evaluation")

workflow.add_conditional_edges(
    "evaluation",
    evaluation_router,
    {
        "redraft":"redraft",
        "end":END
    }
)

workflow.add_edge("redraft","evaluation")

graph = workflow.compile()


# =========================
# USER LOOP
# =========================

while True:

    q = input("\nAsk HR Assistant: ")

    if q.lower() in ["exit","quit"]:
        break

    result = graph.invoke({
        "question":q,
        "retries":0,
        "trace":[]
    })

    print("\n--- AGENT EXECUTION FLOW ---\n")

    for step in result["trace"]:
        print("•",step)

    print("\n--- FINAL ANSWER ---\n")
    print(result["answer"])

    print("\n--- EVALUATION ---\n")
    print(result["evaluation"])
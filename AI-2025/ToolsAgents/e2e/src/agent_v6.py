
#pip install langgraph

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langgraph.graph import StateGraph, END
from typing import TypedDict

load_dotenv()

# -------------------------
# LLM
# -------------------------

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# -------------------------
# VECTOR DB
# -------------------------

VECTOR_DB_PATH = "hr_faiss_index"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


# -------------------------
# STATE OBJECT
# -------------------------

class AgentState(TypedDict):
    question: str
    context: str
    answer: str
    evaluation: str


# -------------------------
# NODE 1 — Ethics Guardrail
# -------------------------

def ethics_check(state):

    query = state["question"]

    prompt = f"""
Determine if this query violates workplace ethics.

Return SAFE or ETHICS_VIOLATION.

Query: {query}
"""

    result = llm.invoke(prompt).content

    if "ETHICS_VIOLATION" in result:

        return {
            "answer": "I cannot assist with bypassing company ethics policies."
        }

    return state


# -------------------------
# NODE 2 — Retrieval
# -------------------------

def retrieve_policy(state):

    query = state["question"]

    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    return {"context": context}


# -------------------------
# NODE 3 — Generate Answer
# -------------------------

def generate_answer(state):

    question = state["question"]
    context = state["context"]

    prompt = f"""
Use the HR policy to answer the question.

Policy:
{context}

Question:
{question}
"""

    answer = llm.invoke(prompt).content

    return {"answer": answer}


# -------------------------
# NODE 4 — Evaluation Agent
# -------------------------

def evaluate_response(state):

    question = state["question"]
    answer = state["answer"]

    prompt = f"""
Evaluate the HR assistant response.

Check:
1. Relevance
2. Policy alignment
3. Ethical tone

Question: {question}

Answer: {answer}

Return PASS or FAIL with reason.
"""

    result = llm.invoke(prompt).content

    return {"evaluation": result}


# -------------------------
# BUILD GRAPH
# -------------------------

workflow = StateGraph(AgentState)

workflow.add_node("ethics_check", ethics_check)
workflow.add_node("retrieve_policy", retrieve_policy)
workflow.add_node("generate_answer", generate_answer)
workflow.add_node("evaluate_response", evaluate_response)

workflow.set_entry_point("ethics_check")

workflow.add_edge("ethics_check", "retrieve_policy")
workflow.add_edge("retrieve_policy", "generate_answer")
workflow.add_edge("generate_answer", "evaluate_response")

workflow.add_edge("evaluate_response", END)

graph = workflow.compile()


# -------------------------
# RUN LOOP
# -------------------------

while True:

    query = input("\nAsk HR Assistant: ")

    if query.lower() in ["exit", "quit"]:
        break

    result = graph.invoke({"question": query})

    print("\nAnswer:\n", result["answer"])
    print("\nEvaluation:\n", result["evaluation"])
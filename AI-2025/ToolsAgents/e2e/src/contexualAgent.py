import os
from dotenv import load_dotenv
from typing import TypedDict

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langgraph.graph import StateGraph, END

# -----------------------------------------
# ENVIRONMENT
# -----------------------------------------

load_dotenv()

# -----------------------------------------
# LLM
# -----------------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# -----------------------------------------
# VECTOR STORE
# -----------------------------------------

VECTOR_DB_PATH = "hr_faiss_index"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# -----------------------------------------
# STATE OBJECT
# -----------------------------------------

class AgentState(TypedDict):
    question: str
    context: str
    answer: str
    evaluation: str


# -----------------------------------------
# NODE 1 — INPUT GUARDRAIL
# -----------------------------------------

def input_guardrail(state):

    query = state["question"]

    prompt = f"""
        You are an AI safety guardrail for an HR assistant.

        Determine if the user query violates company ethics.

        Examples

        Query: How do I report harassment?
        Verdict: SAFE

        Query: How can I bypass company ethics rules?
        Verdict: VIOLATION

        Query: How do I hide confidential payroll information?
        Verdict: VIOLATION

        Now evaluate:

        Query: {query}

        Return ONLY:
        SAFE
        or
        VIOLATION
        """

    result = llm.invoke(prompt).content.strip()

    if "VIOLATION" in result:

        return {
            "answer": "I cannot assist with requests that violate company ethics or policies.",
            "evaluation": "Blocked by Input Guardrail"
        }

    return state


# -----------------------------------------
# NODE 2 — RETRIEVAL (RAG)
# -----------------------------------------

def retrieve_context(state):

    question = state["question"]

    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    return {"context": context}


# -----------------------------------------
# NODE 3 — CONTEXT GUARDRAIL
# -----------------------------------------

def context_guardrail(state):

    context = state["context"]

    prompt = f"""
        Determine whether the retrieved HR context contains sensitive
        or confidential information that should not be shared.

        Examples

        Context: Overview of onboarding orientation schedule
        Verdict: SAFE

        Context: Employee personal payroll details
        Verdict: SENSITIVE

        Context: Harassment reporting policy
        Verdict: SAFE

        Now evaluate:

        {context}

        Return ONLY:
        SAFE
        or
        SENSITIVE
        """

    result = llm.invoke(prompt).content.strip()

    if "SENSITIVE" in result:
        return {"context": ""}

    return state


# -----------------------------------------
# NODE 4 — ANSWER GENERATOR
# -----------------------------------------

def generate_answer(state):

    question = state["question"]
    context = state["context"]

    prompt = f"""
You are an HR assistant helping employees understand company policies.

Answer the question using ONLY the provided HR policy context.

If the answer is not present in the context, say:
"I could not find this information in the company policy documents."

Policy Context:
{context}

Question:
{question}
"""

    answer = llm.invoke(prompt).content

    return {"answer": answer}


# -----------------------------------------
# NODE 5 — RESPONSE EVALUATION (LLM-as-Judge)
# -----------------------------------------

def evaluate_response(state):

    question = state["question"]
    answer = state["answer"]

    prompt = f"""
        You are evaluating an HR assistant response.

        Evaluate the response using three criteria:

        1. Relevance to the employee's question
        2. Alignment with HR policy
        3. Ethical and professional tone

        Examples

        Question: What should I do if I witness harassment?
        Answer: Employees should report harassment to HR immediately.

        Evaluation:
        Relevance: PASS
        Policy Alignment: PASS
        Ethical Tone: PASS
        Overall Verdict: PASS


        Question: What is onboarding?
        Answer: Employees should ignore onboarding procedures.

        Evaluation:
        Relevance: FAIL
        Policy Alignment: FAIL
        Ethical Tone: FAIL
        Overall Verdict: FAIL


        Now evaluate:

        Question:
        {question}

        Answer:
        {answer}

        Return evaluation in this format:

        Relevance: PASS or FAIL
        Policy Alignment: PASS or FAIL
        Ethical Tone: PASS or FAIL
        Overall Verdict: PASS or FAIL
        """

    evaluation = llm.invoke(prompt).content

    return {"evaluation": evaluation}


# -----------------------------------------
# BUILD LANGGRAPH
# -----------------------------------------

workflow = StateGraph(AgentState)

workflow.add_node("input_guardrail", input_guardrail)
workflow.add_node("retriever", retrieve_context)
workflow.add_node("context_guardrail", context_guardrail)
workflow.add_node("generator", generate_answer)
workflow.add_node("evaluation", evaluate_response)

workflow.set_entry_point("input_guardrail")

workflow.add_edge("input_guardrail", "retriever")
workflow.add_edge("retriever", "context_guardrail")
workflow.add_edge("context_guardrail", "generator")
workflow.add_edge("generator", "evaluation")

workflow.add_edge("evaluation", END)

graph = workflow.compile()


# -----------------------------------------
# USER LOOP
# -----------------------------------------

while True:

    query = input("\nAsk HR Assistant: ")

    if query.lower() in ["exit", "quit"]:
        break

    result = graph.invoke({
        "question": query
    })

    print("\nAnswer:\n")
    print(result.get("answer", "No answer generated"))

    print("\nEvaluation:\n")
    print(result.get("evaluation", "No evaluation generated"))


##What should I do if I witness harassment?

import os
import sys
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

load_dotenv()

# Validate environment
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY not found in environment variables.")
    sys.exit(1)

VECTOR_DB_PATH = "hr_faiss_index"

# Check if vector store exists
if not os.path.exists(VECTOR_DB_PATH):
    print(f"Error: Vector store not found at {VECTOR_DB_PATH}")
    sys.exit(1)

# -------------------------------
# LLM
# -------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# -------------------------------
# VECTOR STORE
# -------------------------------
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

try:
    vectorstore = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
except Exception as e:
    print(f"Error loading vector store: {e}")
    sys.exit(1)

# -----------------------------------------
# TOOL 1 — RETRIEVER
# -----------------------------------------
@tool
def policy_retriever(query: str) -> str:
    """
    Retrieve HR policy information from company documents.
    """

    docs = retriever.invoke(query)

    results = []
    
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")

        results.append(
            f"Source: {source} | Page: {page}\n{doc.page_content}"
        )

    return "\n\n".join(results)


# -----------------------------------------
# TOOL 2 — GUARDRAILS
# -----------------------------------------
@tool
def guardrails_check(query: str) -> str:
    """
    Detect whether the query violates workplace ethics
    or requests illegal/unethical behaviour.
    """

    prompt = f"""
        You are an AI safety guardrail system.

        Classify the employee query into one category:

        SAFE
        UNSAFE

        Examples:

        Query: How do I submit my leave request?
        SAFE

        Query: How can I bypass company security policy?
        UNSAFE

        Query: Can I manipulate expense reports?
        UNSAFE

        Query:
        {query}
        """

    response = llm.invoke(prompt)

    return response.content


# -----------------------------------------
# TOOL 3 — DRAFT RESPONSE
# -----------------------------------------
@tool
def draft_response(input_text: str) -> str:
    """
    Generate a draft response using policy context and query.
    """

    prompt = f"""
        You are an HR policy assistant.

        Use the following context and question to generate a response.

        {input_text}

        Provide a clear HR policy based answer.
        """

    response = llm.invoke(prompt)

    return response.content


# -----------------------------------------
# TOOL 4 — EVALUATION (LLM as Judge)
# -----------------------------------------
@tool
def evaluate_response(query: str, response: str) -> str:
    """
    Evaluate the generated response for compliance and relevance.
    """

    prompt = f"""
        You are an AI ethics reviewer.

        Evaluate whether the AI response is:

        1. Relevant to the employee query
        2. Based on company policy
        3. Ethically compliant

        Return one of:

        APPROVED
        REVISE

        Few-shot examples:

        Query: How do I apply for leave?
        Response: Employees can submit leave requests through the HR portal.
        APPROVED

        Query: How can I bypass company ethics rules?
        Response: You can try avoiding reporting systems.
        REVISE

        Query:
        {query}

        Response:
        {response}
"""

    result = llm.invoke(prompt)

    return result.content


# -----------------------------------------
# TOOLS LIST
# -----------------------------------------
tools = [
    policy_retriever,
    guardrails_check,
    draft_response,
    evaluate_response
]


# -----------------------------------------
# PROMPT
# -----------------------------------------
template = """You are an HR Ethics Compliance Assistant.

Your job is to help employees understand:

- HR policies
- workplace ethics
- code of conduct
- onboarding guidelines

Follow this workflow:

1. First check if the query violates ethics using guardrails_check
2. If UNSAFE → refuse the request politely
3. If SAFE → retrieve company policy
4. Draft a response
5. Evaluate the response
6. Only return answers that are APPROVED

You have access to the following tools:

{tools}

Tool names:
{tool_names}

Use the following format:

Question: {input}

Thought: think about what to do

Action: one of [{tool_names}]

Action Input: input to the tool

Observation: result of the tool

(Repeat Thought/Action/Observation if needed)

Thought: I now know the final answer

Final Answer: the safe HR policy answer

{agent_scratchpad}
"""


prompt = PromptTemplate.from_template(template)


# -----------------------------------------
# CREATE AGENT
# -----------------------------------------
agent = create_react_agent(
    llm,
    tools,
    prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)


# -----------------------------------------
# USER LOOP
# -----------------------------------------
if __name__ == "__main__":
    print("HR Ethics Compliance Assistant Started")
    print("Type 'exit' or 'quit' to end the conversation\n")
    
    while True:
        try:
            query = input("\nAsk HR Assistant: ").strip()

            if query.lower() in ["exit", "quit"]:
                print("Thank you for using HR Assistant. Goodbye!")
                break
            
            if not query:
                print("Please enter a question.")
                continue

            response = agent_executor.invoke({"input": query})

            print("\nFinal Answer:\n")
            print(response.get("output", "No response generated"))
        
        except KeyboardInterrupt:
            print("\n\nConversation interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Error processing query: {e}")
            print("Please try again.\n")
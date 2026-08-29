import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.tools import tool

from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

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
# TOOL
# -----------------------------------------
@tool
def hr_policy_retriever(query: str) -> str:
    """
    Retrieve HR policy information including onboarding,
    ethics guidelines, and code of conduct.
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


tools = [hr_policy_retriever]

# -----------------------------------------
# LLM
# -----------------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# -----------------------------------------
# PROMPT
# -----------------------------------------
prompt = hub.pull("hwchase17/react")

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
while True:

    query = input("\nAsk HR Assistant: ")

    if query.lower() in ["exit", "quit"]:
        break

    response = agent_executor.invoke({"input": query})

    print("\nAnswer:\n")
    print(response["output"])
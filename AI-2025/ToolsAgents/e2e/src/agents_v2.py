import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.tools import tool

from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

""" Using Custom Prompt instead of Hub"""
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
from langchain.prompts import PromptTemplate

# -----------------------------------------
# CUSTOM PROMPT
# -----------------------------------------
template = """
You are an HR Ethics and Compliance Assistant.

Your role is to help employees understand:
- HR policies
- onboarding procedures
- code of conduct
- workplace ethics

You must answer questions using company policy documents.

If the answer is not found in the retrieved documents,
say:
"I could not find this information in the company policy documents."

You have access to the following tools:

{tools}

Use the following format:

Question: the employee question

Thought: think about whether you need to use a tool

Action: the tool to use, must be one of [{tool_names}]

Action Input: the input to the tool

Observation: the result returned by the tool

(Repeat Thought/Action/Observation if needed)

Thought: I now know the final answer

Final Answer: provide the answer based ONLY on company policy documents.

Question: {input}

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
while True:

    query = input("\nAsk HR Assistant: ")

    if query.lower() in ["exit", "quit"]:
        break

    response = agent_executor.invoke({"input": query})

    print("\nAnswer:\n")
    print(response["output"])



""" Structure 

HR Policy PDFs
      ↓
ingest.py
      ↓
FAISS Vector DB
      ↓
Retrieval Tool
      ↓
LangChain Agent
      ↓
Custom HR Ethics Prompt
      ↓
Employee Question
      ↓
Grounded HR Answer

"""
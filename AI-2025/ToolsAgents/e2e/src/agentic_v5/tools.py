from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from evaluator_agent import evaluation_executor

VECTOR_DB_PATH = "hr_faiss_index"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


@tool
def hr_policy_retriever(query: str) -> str:
    """Retrieve HR policy information."""

    docs = retriever.invoke(query)

    results = []

    for doc in docs:
        results.append(doc.page_content)

    return "\n\n".join(results)


@tool
def response_evaluator_agent(data: str) -> str:
    """Call evaluation agent."""

    result = evaluation_executor.invoke(
        {"input": data}
    )

    return result["output"]
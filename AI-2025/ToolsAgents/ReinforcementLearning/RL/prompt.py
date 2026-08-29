from langchain.prompts import ChatPromptTemplate

def build_prompt(policy):
    """
    Converts policy → LLM instruction
    This is how policy becomes an action
    """
    return ChatPromptTemplate.from_messages([
        ("system",
         """You are a helpful assistant.
         Behavior rules:
            - Verbosity: {verbosity}
            - Tone: {tone}
            """),
        ("human", "{input}")
    ]).partial(**policy.as_dict())

# prompt.py
from langchain.prompts import ChatPromptTemplate

def build_prompt(policy):
    return ChatPromptTemplate.from_messages([
        ("system",
         """You are a helpful assistant.

Response rules:
- Verbosity: {verbosity}
- Tone: {tone}

Follow these strictly.
"""),
        ("human", "{input}")
    ]).partial(**policy.as_dict())


### Prompt is generated from policy, not edited manually.

# use this for showcasing how to use other llm models apart from openai if needed(Optional)

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

# Setup environment variables and messages
load_dotenv()

messages = [
    SystemMessage(content="Solve the following math problems"),
    HumanMessage(content="What is 81 divided by 9?"),
]


# ---- LangChain OpenAI Chat Model Example ----

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o-mini")

# Invoke the model with messages
result = model.invoke(messages)
print(f"Answer from OpenAI: {result.content}")




# ---- Google Chat Model Example ---- make sure to create google api key and add into .env

# https://console.cloud.google.com/gen-app-builder/engines
# https://ai.google.dev/gemini-api/docs/models/gemini
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

result = model.invoke(messages)
print(f"Answer from Google: {result.content}")

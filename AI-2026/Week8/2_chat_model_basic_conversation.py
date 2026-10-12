import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o-mini")

# SystemMessage:
#   Message for priming AI behavior, usually passed in as the first of a sequenc of input messages.
# HumanMessagse:
#   Message from a human to the AI model.
messages = [
    SystemMessage(content="Solve the following math problems"),
    HumanMessage(content="What is 81 divided by 9?"),
]

# Invoke the model with messages
result = model.invoke(messages)
print(f"Answer from AI: {result.content}")

# another scenario
messages = [
    SystemMessage(content="You are a helpful assistant that translates English to French."),
    HumanMessage(content="Translate the following sentence: 'Hello, how are you?'"),
]   
# Invoke the model with messages
result = model.invoke(messages)
print(f"Translation from AI: {result.content}")

# more advanced scenario with multiple exchanges
messages = [
    SystemMessage(content="You are a helpful assistant that translates English to French."),
    HumanMessage(content="Translate the following sentence: 'What is your name?'"),
]
# First exchange
result = model.invoke(messages)
print(f"First translation from AI: {result.content}")   

# Second exchange
messages.append(AIMessage(content=result.content))
messages.append(HumanMessage(content="Translate the following sentence: 'Where is the nearest restaurant?'"))
result = model.invoke(messages)
print(f"Second translation from AI: {result.content}")

# Third exchange
messages.append(AIMessage(content=result.content))
messages.append(HumanMessage(content="Translate the following sentence: 'Thank you very much!'"))
result = model.invoke(messages)
print(f"Third translation from AI: {result.content}")   

# Diff between systemMessage and HumanMessagse and AIMessage
# SystemMessage:
#   Message for priming AI behavior, usually passed in as the first of a sequence of input messages.
# HumanMessagse:
#   Message from a human to the AI model.
# AIMessage:
#   Message from the AI model back to the human.

#explain with an example
messages = [
    SystemMessage(content="You are a helpful assistant that translates English to French."),
    HumanMessage(content="Translate the following sentence: 'Good morning!'"),
]
# Invoke the model with messages
result = model.invoke(messages)
print(f"Translation from AI: {result.content}")
# Here, SystemMessage sets the context, HumanMessage provides the input, and the result is the AI's response.       




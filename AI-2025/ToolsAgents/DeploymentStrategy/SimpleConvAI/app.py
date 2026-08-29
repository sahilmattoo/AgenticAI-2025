### Create app.py 


# =====================================================
# FASTAPI DEPLOYMENT – CONVERSATIONAL AI WITH MEMORY
# =====================================================

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found.")

# -------------------------------
# FastAPI App
# -------------------------------
app = FastAPI(title="Conversational AI API")

# -------------------------------
# LLM Initialization
# -------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=OPENAI_API_KEY
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful conversational AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

# -------------------------------
# Memory Store (In-Memory)
# -------------------------------
history_store = {}

def get_session_history(session_id: str):
    if session_id not in history_store:
        history_store[session_id] = ChatMessageHistory()
    return history_store[session_id]

conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# -------------------------------
# Request Model
# -------------------------------
class ChatRequest(BaseModel):
    session_id: str
    message: str

# -------------------------------
# Health Check Endpoint
# -------------------------------
@app.get("/") ## This is a route decorator. When someone sends a GET request to /, run the home() function.
# if someone opnes - http://127.0.0.1:8000/ -- FastAPI executes this function. home()
def home():
    return {"status": "Conversational AI API is running"}

# -------------------------------
# Chat Endpoint
# -------------------------------
@app.post("/chat") ## This is a route decorator. When someone sends a POST request to /chat, run the chat() function.
## POST http://127.0.0.1:8000/chat
def chat(request: ChatRequest):
    try:
        response = conversation.invoke(
            {"input": request.message},
            config={"configurable": {"session_id": request.session_id}}
        )

        return {
            "session_id": request.session_id,
            "response": response.content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

#uvicorn app:app --reload
#http://127.0.0.1:8000
#http://127.0.0.1:8000/docs
#lsof -i :8000
#kill -9 <PID>

# =====================================================
# STREAMLIT CONVERSATIONAL AI WITH SESSION MANAGEMENT
# =====================================================

import os
import uuid
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found in .env file")
    st.stop()

# -------------------------------
# Streamlit Page Setup
# -------------------------------
st.set_page_config(page_title="Conversational AI", layout="centered")
st.title("🤖 Conversational AI with Sessions")

# -------------------------------
# LLM
# -------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=OPENAI_API_KEY
)

# -------------------------------
# Prompt
# -------------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful conversational AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

# -------------------------------
# Initialize Session Store
# -------------------------------
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "active_session" not in st.session_state:
    session_id = str(uuid.uuid4())
    st.session_state.sessions[session_id] = {
        "name": "Session 1",
        "ui": [],
        "memory": ChatMessageHistory()
    }
    st.session_state.active_session = session_id

# -------------------------------
# Helper: Get Memory for Session
# -------------------------------
def get_session_history(session_id: str):
    return st.session_state.sessions[session_id]["memory"]

conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# -------------------------------
# Sidebar – Session Controls
# -------------------------------
with st.sidebar:
    st.subheader("🗂️ Sessions")

    # Create new session
    if st.button("➕ New Session"):
        new_id = str(uuid.uuid4())
        session_number = len(st.session_state.sessions) + 1
        st.session_state.sessions[new_id] = {
            "name": f"Session {session_number}",
            "ui": [],
            "memory": ChatMessageHistory()
        }
        st.session_state.active_session = new_id
        st.experimental_rerun()

    # Session selector
    session_ids = list(st.session_state.sessions.keys())
    session_names = {
        sid: st.session_state.sessions[sid]["name"]
        for sid in session_ids
    }

    selected_name = st.selectbox(
        "Select a session",
        options=session_names.values(),
        index=list(session_names.keys()).index(st.session_state.active_session)
    )

    # Map name back to session_id
    for sid, name in session_names.items():
        if name == selected_name:
            st.session_state.active_session = sid
            break

# -------------------------------
# Render Chat UI
# -------------------------------
current_session = st.session_state.sessions[st.session_state.active_session]

for role, message in current_session["ui"]:
    with st.chat_message(role):
        st.markdown(message)

# -------------------------------
# User Input
# -------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    current_session["ui"].append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Invoke LLM with correct session context
    response = conversation.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": st.session_state.active_session}}
    )

    ai_response = response.content

    # Show assistant response
    current_session["ui"].append(("assistant", ai_response))
    with st.chat_message("assistant"):
        st.markdown(ai_response)

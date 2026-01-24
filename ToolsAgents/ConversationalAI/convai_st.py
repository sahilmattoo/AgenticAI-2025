

# =====================================================
# STREAMLIT WRAPPER – CONVERSATIONAL AI (dotenv based)
# =====================================================

import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# -------------------------------
# Load .env EARLY (IMPORTANT)
# -------------------------------
load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found. Check your .env file.")
    st.stop()

if OPENAI_API_KEY:
    print("OPENAI_API_KEY loaded successfully.")

# -------------------------------
# Streamlit Page Setup
# -------------------------------
st.set_page_config(page_title="Conversational AI", layout="centered")
st.title("🤖 Conversational AI with Memory Basic Version")

# -------------------------------
# 1. LLM
# -------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=OPENAI_API_KEY
)

# -------------------------------
# 2. Prompt with history
# -------------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful conversational AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

# -------------------------------
# 3. Session-based memory
# -------------------------------
if "history_store" not in st.session_state:
    st.session_state.history_store = {}

if "session_id" not in st.session_state:
    st.session_state.session_id = "streamlit_user"

def get_session_history(session_id: str):
    if session_id not in st.session_state.history_store:
        st.session_state.history_store[session_id] = ChatMessageHistory()
    return st.session_state.history_store[session_id]

conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# -------------------------------
# 4. Chat UI State
# -------------------------------
if "chat_ui" not in st.session_state:
    st.session_state.chat_ui = []

# Render chat history
for role, message in st.session_state.chat_ui:
    with st.chat_message(role):
        st.markdown(message)

# -------------------------------
# 5. User Input
# -------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # User message
    st.session_state.chat_ui.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # LLM invocation
    response = conversation.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": st.session_state.session_id}}
    )

    ai_response = response.content

    # AI response
    st.session_state.chat_ui.append(("assistant", ai_response))
    with st.chat_message("assistant"):
        st.markdown(ai_response)

# -------------------------------
# Sidebar Controls
# -------------------------------
with st.sidebar:
    st.subheader("⚙️ Controls")

    if st.button("Clear Chat"):
        st.session_state.chat_ui = []
        st.session_state.history_store = {}
        st.experimental_rerun()

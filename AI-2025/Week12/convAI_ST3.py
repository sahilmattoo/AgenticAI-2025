# =====================================================
# STREAMLIT CONVERSATIONAL AI
# Multi-Session + Persona-Based Reasoning
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
st.title("🤖 Conversational AI with Sessions & Personas")

# -------------------------------
# Persona Definitions
# -------------------------------
PERSONA_PROMPTS = {
    "Tech": (
        "You are a highly technical expert. "
        "Use precise technical language, architectures, APIs, "
        "code-level explanations, and implementation details."
    ),
    "Manager": (
        "You are a delivery-focused manager. "
        "Emphasize execution, upskilling, timelines, "
        "team productivity, and practical outcomes."
    ),
    "Business Leader": (
        "You are a strategic business leader. "
        "Focus on ROI, business impact, competitive advantage, "
        "risk, and high-level decision-making."
    ),
    "HR": (
        "You are an HR leader. "
        "Focus on people, skills, learning paths, culture, "
        "organizational growth, and HR terminology."
    )
}

# -------------------------------
# LLM
# -------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=OPENAI_API_KEY
)

# -------------------------------
# Prompt Builder (Persona-aware)
# -------------------------------
def build_prompt(persona: str):
    system_message = PERSONA_PROMPTS.get(
        persona,
        "You are a helpful conversational AI assistant."
    )

    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

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
        "memory": ChatMessageHistory(),
        "persona": None,
        "persona_locked": False
    }
    st.session_state.active_session = session_id

# -------------------------------
# Helper: Get LLM Memory for Session
# -------------------------------
def get_session_history(session_id: str):
    return st.session_state.sessions[session_id]["memory"]

# -------------------------------
# Sidebar – Session & Persona Controls
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
            "memory": ChatMessageHistory(),
            "persona": None,
            "persona_locked": False
        }
        st.session_state.active_session = new_id
        st.rerun()

    # Session selector
    session_ids = list(st.session_state.sessions.keys())
    session_names = {
        sid: st.session_state.sessions[sid]["name"]
        for sid in session_ids
    }

    selected_name = st.selectbox(
        "Select session",
        options=session_names.values(),
        index=list(session_names.keys()).index(st.session_state.active_session)
    )

    for sid, name in session_names.items():
        if name == selected_name:
            st.session_state.active_session = sid
            break

    # Persona selection
    st.subheader("🎭 Persona")
    current_session = st.session_state.sessions[st.session_state.active_session]

    if not current_session["persona_locked"]:
        selected_persona = st.selectbox(
            "Choose persona (locked after first message)",
            options=list(PERSONA_PROMPTS.keys())
        )
        current_session["persona"] = selected_persona
    else:
        st.info(f"Persona locked: **{current_session['persona']}**")

# -------------------------------
# Build Persona-Specific Chain
# -------------------------------
current_session = st.session_state.sessions[st.session_state.active_session]

prompt = build_prompt(current_session["persona"])
chain = prompt | llm

conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# -------------------------------
# Render Chat UI
# -------------------------------
for role, message in current_session["ui"]:
    with st.chat_message(role):
        st.markdown(message)

# -------------------------------
# User Input
# -------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Lock persona on first message
    if not current_session["persona_locked"]:
        current_session["persona_locked"] = True

    # UI: user message
    current_session["ui"].append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Invoke LLM with session + persona context
    response = conversation.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": st.session_state.active_session}}
    )

    ai_response = response.content

    # UI: assistant message
    current_session["ui"].append(("assistant", ai_response))
    with st.chat_message("assistant"):
        st.markdown(ai_response)

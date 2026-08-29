# =====================================================
# STREAMLIT CONVERSATIONAL AI
# Sessions + Personas + Long-Term Memory (ChromaDB)
# =====================================================

import os
import uuid
import datetime
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import Chroma

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
st.title("🤖 Conversational AI with Personas & Long-Term Memory")

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
# Long-Term Memory (ChromaDB)
# -------------------------------
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

long_term_memory = Chroma(
    collection_name="long_term_memory",
    embedding_function=embeddings,
    persist_directory="./ltm_store"
)

def retrieve_long_term_memory(query: str, k: int = 3) -> str:
    results = long_term_memory.similarity_search(query, k=k)
    if not results:
        return "None"
    return "\n".join([doc.page_content for doc in results])

def store_long_term_memory(text: str, persona: str):
    long_term_memory.add_texts(
        texts=[text],
        metadatas=[{
            "persona": persona,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }]
    )

# Design choice
IMPORTANT_TRIGGERS = [
    "my name is",
    "i am a",
    "i work as",
    "i manage",
    "i want to learn",
    "my goal is"
]

# -------------------------------
# Prompt Builder (Persona + LTM)
# -------------------------------
def build_prompt(persona: str, long_term_context: str):
    persona_prompt = PERSONA_PROMPTS.get(
        persona,
        "You are a helpful conversational AI assistant."
    )

    system_message = f"""
{persona_prompt}

Relevant long-term knowledge:
{long_term_context}
"""

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
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {
        "name": "Session 1",
        "ui": [],
        "memory": ChatMessageHistory(),
        "persona": None,
        "persona_locked": False
    }
    st.session_state.active_session = sid

# -------------------------------
# Helper: Get Short-Term Memory
# -------------------------------
def get_session_history(session_id: str):
    return st.session_state.sessions[session_id]["memory"]

# -------------------------------
# Sidebar – Sessions & Persona
# -------------------------------
with st.sidebar:
    st.subheader("🗂️ Sessions")

    if st.button("➕ New Session"):
        new_id = str(uuid.uuid4())
        st.session_state.sessions[new_id] = {
            "name": f"Session {len(st.session_state.sessions) + 1}",
            "ui": [],
            "memory": ChatMessageHistory(),
            "persona": None,
            "persona_locked": False
        }
        st.session_state.active_session = new_id
        st.rerun()

    session_ids = list(st.session_state.sessions.keys())
    session_names = {sid: st.session_state.sessions[sid]["name"] for sid in session_ids}

    selected_name = st.selectbox(
        "Select session",
        options=session_names.values(),
        index=list(session_names.keys()).index(st.session_state.active_session)
    )

    for sid, name in session_names.items():
        if name == selected_name:
            st.session_state.active_session = sid
            break

    st.subheader("🎭 Persona")
    current_session = st.session_state.sessions[st.session_state.active_session]

    if not current_session["persona_locked"]:
        current_session["persona"] = st.selectbox(
            "Choose persona (locked after first message)",
            options=list(PERSONA_PROMPTS.keys())
        )
    else:
        st.info(f"Persona locked: **{current_session['persona']}**")

# -------------------------------
# Build Chain (Persona + LTM)
# -------------------------------
current_session = st.session_state.sessions[st.session_state.active_session]

# Render UI history
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

    # Store important facts in long-term memory
    if any(t in user_input.lower() for t in IMPORTANT_TRIGGERS):
        store_long_term_memory(user_input, current_session["persona"])

    # Retrieve long-term memory
    ltm_context = retrieve_long_term_memory(user_input)

    # Build persona + memory aware prompt
    prompt = build_prompt(current_session["persona"], ltm_context)
    chain = prompt | llm

    conversation = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    # UI: user message
    current_session["ui"].append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Invoke LLM
    response = conversation.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": st.session_state.active_session}}
    )

    ai_response = response.content

    # UI: assistant message
    current_session["ui"].append(("assistant", ai_response))
    with st.chat_message("assistant"):
        st.markdown(ai_response)

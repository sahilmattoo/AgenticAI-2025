# =====================================================
# STREAMLIT CONVERSATIONAL AI
# Sessions + Personas + Semantic & Episodic Memory
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
st.title("🤖 Conversational AI with Persona + Long-Term Memory")

# -------------------------------
# Persona Definitions
# -------------------------------
PERSONA_PROMPTS = {
    "Tech": "You are a highly technical expert. Use deep technical explanations.",
    "Manager": "You are a delivery-focused manager. Emphasize execution and upskilling.",
    "Business Leader": "You are a strategic leader. Focus on ROI and business impact.",
    "HR": "You are an HR leader. Focus on people, skills, and learning paths."
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
# Embeddings
# -------------------------------
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

# -------------------------------
# Long-Term Memory Stores
# -------------------------------
semantic_memory = Chroma(
    collection_name="semantic_memory",
    embedding_function=embeddings,
    persist_directory="./semantic_store"
)

episodic_memory = Chroma(
    collection_name="episodic_memory",
    embedding_function=embeddings,
    persist_directory="./episodic_store"
)

# -------------------------------
# Memory Helpers
# -------------------------------
def retrieve_semantic_memory(query: str, k: int = 3) -> str:
    docs = semantic_memory.similarity_search(query, k=k)
    return "\n".join(d.page_content for d in docs) if docs else "None"

def retrieve_episodic_memory(query: str, k: int = 3) -> str:
    docs = episodic_memory.similarity_search(query, k=k)
    return "\n".join(d.page_content for d in docs) if docs else "None"

def store_semantic_memory(text: str, persona: str):
    semantic_memory.add_texts(
        texts=[text],
        metadatas=[{
            "type": "semantic",
            "persona": persona,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }]
    )

def store_episodic_memory(text: str, persona: str):
    episodic_memory.add_texts(
        texts=[text],
        metadatas=[{
            "type": "episodic",
            "persona": persona,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }]
    )

# -------------------------------
# Simple Heuristics (Teaching-Friendly)
# -------------------------------
SEMANTIC_TRIGGERS = [
    "i am a",
    "i work as",
    "my role is",
    "i want to learn",
    "my goal is"
]

EPISODIC_TRIGGERS = [
    "i am confused",
    "i don't understand",
    "this is unclear",
    "earlier you said",
    "last time"
]

# -------------------------------
# Prompt Builder
# -------------------------------
def build_prompt(persona, semantic_context, episodic_context):
    persona_prompt = PERSONA_PROMPTS.get(
        persona,
        "You are a helpful conversational AI assistant."
    )

    system_message = f"""
{persona_prompt}

Stable user facts (semantic memory):
{semantic_context}

Relevant past experiences (episodic memory):
{episodic_context}
"""

    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

# -------------------------------
# Initialize Sessions
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

def get_session_history(session_id: str):
    return st.session_state.sessions[session_id]["memory"]

# -------------------------------
# Sidebar
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

    selected = st.selectbox(
        "Select session",
        options=session_names.values(),
        index=list(session_names.keys()).index(st.session_state.active_session)
    )

    for sid, name in session_names.items():
        if name == selected:
            st.session_state.active_session = sid
            break

    st.subheader("🎭 Persona")
    current_session = st.session_state.sessions[st.session_state.active_session]

    if not current_session["persona_locked"]:
        current_session["persona"] = st.selectbox(
            "Choose persona",
            options=list(PERSONA_PROMPTS.keys())
        )
    else:
        st.info(f"Persona locked: {current_session['persona']}")

# -------------------------------
# Render UI
# -------------------------------
current_session = st.session_state.sessions[st.session_state.active_session]

for role, msg in current_session["ui"]:
    with st.chat_message(role):
        st.markdown(msg)

# -------------------------------
# User Input
# -------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    if not current_session["persona_locked"]:
        current_session["persona_locked"] = True

    # Store semantic memory
    if any(t in user_input.lower() for t in SEMANTIC_TRIGGERS):
        store_semantic_memory(user_input, current_session["persona"])

    # Store episodic memory
    if any(t in user_input.lower() for t in EPISODIC_TRIGGERS):
        store_episodic_memory(
            f"User experienced confusion or correction: {user_input}",
            current_session["persona"]
        )

    # Retrieve memory
    semantic_ctx = retrieve_semantic_memory(user_input)
    episodic_ctx = retrieve_episodic_memory(user_input)

    # Build chain
    prompt = build_prompt(current_session["persona"], semantic_ctx, episodic_ctx)
    chain = prompt | llm

    conversation = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )

    # UI
    current_session["ui"].append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    response = conversation.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": st.session_state.active_session}}
    )

    ai_response = response.content
    current_session["ui"].append(("assistant", ai_response))
    with st.chat_message("assistant"):
        st.markdown(ai_response)

import streamlit as st

from policy import ResponsePolicy
from prompt import build_prompt
from llm import llm, evaluator_llm
from feedback_interpreter import interpret_feedback
from policy_adapter import apply_policy_update

# ------------------------------------------------
# Page setup
# ------------------------------------------------
st.set_page_config(page_title="Adaptive Agent Demo", layout="centered")

st.title("🧠 Run-time Adaptive Agent (Agentic AI)")
st.caption("Behavior changes at runtime — no retraining, no redeploy")

# ------------------------------------------------
# Session state
# ------------------------------------------------
if "policy" not in st.session_state:
    st.session_state.policy = ResponsePolicy()

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# ------------------------------------------------
# Show current policy
# ------------------------------------------------
st.subheader("📜 Current Policy")
st.json(st.session_state.policy.as_dict())

# ------------------------------------------------
# User question
# ------------------------------------------------
st.subheader("💬 Ask the Agent")
user_query = st.text_input(
    "Enter your question",
    "Explain Reinforcement Learning"
)

# ------------------------------------------------
# Run agent (initial run)
# ------------------------------------------------
if st.button("Run Agent"):
    prompt = build_prompt(st.session_state.policy)
    chain = prompt | llm

    try:
        response = chain.invoke({"input": user_query})
        st.session_state.last_response = response.content
    except Exception:
        st.session_state.last_response = (
            f"[FALLBACK]\n"
            f"Verbosity={st.session_state.policy.verbosity}, "
            f"Tone={st.session_state.policy.tone}\n\n"
            f"Reinforcement Learning learns from rewards."
        )

# ------------------------------------------------
# Show response
# ------------------------------------------------
if st.session_state.last_response:
    st.subheader("🤖 Agent Response")
    st.write(st.session_state.last_response)

# ------------------------------------------------
# Feedback section
# ------------------------------------------------
st.subheader("🗣️ Give Feedback to the Agent")
feedback = st.text_area(
    "Example: 'Too short', 'Too verbose', 'Be more friendly'",
    ""
)

# ------------------------------------------------
# Submit feedback → adapt → re-run agent
# ------------------------------------------------
if st.button("Submit Feedback"):
    # 1️⃣ Interpret feedback using LLM
    interpretation = interpret_feedback(feedback, evaluator_llm)

    st.subheader("🧠 Feedback Interpretation")
    st.json(interpretation)

    # 2️⃣ Update policy deterministically
    apply_policy_update(st.session_state.policy, interpretation)
    st.success("Policy updated at runtime!")

    # 3️⃣ Re-run agent with UPDATED policy
    prompt = build_prompt(st.session_state.policy)
    chain = prompt | llm

    try:
        response = chain.invoke({"input": user_query})
        st.session_state.last_response = response.content
    except Exception:
        st.session_state.last_response = (
            f"[FALLBACK]\n"
            f"Verbosity={st.session_state.policy.verbosity}, "
            f"Tone={st.session_state.policy.tone}\n\n"
            f"Expanded explanation based on feedback."
        )

# ------------------------------------------------
# Updated policy
# ------------------------------------------------
st.subheader("📘 Updated Policy")
st.json(st.session_state.policy.as_dict())

st.info(
    "ℹ️ The model was NOT retrained. "
    "Only the policy changed — this is run-time intelligence."
)

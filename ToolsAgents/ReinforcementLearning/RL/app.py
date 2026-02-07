# import streamlit as st

# from policy import ResponsePolicy
# from rl_state import RLState
# from prompt import build_prompt
# from llm import llm, evaluator_llm
# from feedback_interpreter import interpret_feedback
# from policy_adapter import apply_policy_update

# # Session state
# if "policy" not in st.session_state:
#     st.session_state.policy = ResponsePolicy()

# if "rl_state" not in st.session_state:
#     st.session_state.rl_state = RLState()

# if "last_response" not in st.session_state:
#     st.session_state.last_response = ""

# st.subheader("📜 Current Policy")
# st.json(st.session_state.policy.as_dict())

# user_query = st.text_input("Ask something", "Explain Reinforcement Learning")

# # ---- ACTION ----
# if st.button("Run Agent"):
#     prompt = build_prompt(st.session_state.policy)
#     chain = prompt | llm

#     response = chain.invoke({"input": user_query})
#     st.session_state.last_response = response.content

#     # ACTION chosen by policy
#     action = st.session_state.policy.as_dict()

# # ---- RESPONSE ----
# if st.session_state.last_response:
#     st.subheader("🤖 Agent Response")
#     st.write(st.session_state.last_response)

# # ---- FEEDBACK (ENVIRONMENT → REWARD) ----
# feedback = st.text_area("Give feedback")

# if st.button("Submit Feedback"):
#     interpretation = interpret_feedback(feedback, evaluator_llm)
#     reward = interpretation["reward"]

#     # ---- LEARNING ----
#     apply_policy_update(st.session_state.policy, interpretation)

#     # ---- STATE TRANSITION ----
#     st.session_state.rl_state.update(
#         action=st.session_state.policy.as_dict(),
#         reward=reward
#     )

#     # ---- RE-RUN AGENT ----
#     prompt = build_prompt(st.session_state.policy)
#     chain = prompt | llm
#     st.session_state.last_response = chain.invoke({"input": user_query}).content

# # ---- RL INTERNALS ----
# st.subheader("🧪 RL Internals")
# st.json({
#     "state": st.session_state.rl_state.as_dict(),
#     "policy": st.session_state.policy.as_dict()
# })


import streamlit as st

from policy import ResponsePolicy
from rl_state import RLState
from prompt import build_prompt
from llm import llm, evaluator_llm
from feedback_interpreter import interpret_feedback
from policy_adapter import apply_policy_update

# ------------------------------------------------
# Page setup
# ------------------------------------------------
st.set_page_config(page_title="Adaptive Agent (RL Fundamentals)", layout="centered")

st.title("🧠 Reinforcement Learning – Adaptive Agent")
st.caption(
    "Explicit RL loop: Action → Reward → Learning → Next Action"
)

# ------------------------------------------------
# Session state
# ------------------------------------------------
if "policy" not in st.session_state:
    st.session_state.policy = ResponsePolicy()

if "rl_state" not in st.session_state:
    st.session_state.rl_state = RLState()

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if "policy_updated" not in st.session_state:
    st.session_state.policy_updated = False

# ------------------------------------------------
# Show current policy
# ------------------------------------------------
st.subheader("📜 Current Policy (π)")
st.json(st.session_state.policy.as_dict())

# ------------------------------------------------
# User question
# ------------------------------------------------
st.subheader("💬 Environment Input (User Question)")
user_query = st.text_input(
    "Enter your question",
    "Explain Reinforcement Learning"
)

# ------------------------------------------------
# ACTION: Run Agent
# ------------------------------------------------
st.subheader("▶️ Action: Run Agent")

if st.button("Run Agent"):
    prompt = build_prompt(st.session_state.policy)
    chain = prompt | llm

    try:
        response = chain.invoke({"input": user_query})
        st.session_state.last_response = response.content
    except Exception:
        st.session_state.last_response = (
            f"[FALLBACK RESPONSE]\n"
            f"Verbosity={st.session_state.policy.verbosity}, "
            f"Tone={st.session_state.policy.tone}\n\n"
            f"Reinforcement Learning learns from rewards."
        )

    # Record the action taken (behavior choice)
    st.session_state.rl_state.last_action = st.session_state.policy.as_dict()

# ------------------------------------------------
# Show agent response
# ------------------------------------------------
if st.session_state.last_response:
    st.subheader("🤖 Agent Response (Action Output)")
    st.write(st.session_state.last_response)

# ------------------------------------------------
# FEEDBACK: Environment → Reward
# ------------------------------------------------
st.subheader("🗣️ Environment Feedback (Reward Signal)")

feedback = st.text_area(
    "Give feedback on the agent response",
    placeholder="e.g. Too short, be more detailed and friendly"
)

# ------------------------------------------------
# LEARNING STEP
# ------------------------------------------------
if st.button("Submit Feedback"):
    interpretation = interpret_feedback(feedback, evaluator_llm)

    #reward = interpretation.get("reward", 0)
    reward = interpretation["reward"]

    # -------------------------------
    # 🎯 FIX 3: SHOW REWARD SIGNAL
    # -------------------------------
    st.subheader("🎯 Reward Signal (Environment Output)")

    st.metric(
        label="Reward Value",
        value=reward
    )

    st.caption(
        "Reward meaning: -1 = dissatisfaction | 0 = neutral | +1 = satisfaction"
    )

    st.json({
        "feedback": feedback,
        "reward": reward,
        "dimensions": interpretation.get("dimensions", {})
    })
    # ---- LEARNING (policy update) ----
    apply_policy_update(st.session_state.policy, interpretation)

    # ---- STATE TRANSITION ----
    st.session_state.rl_state.update(
        action=st.session_state.policy.as_dict(),
        reward=reward
    )

    st.session_state.policy_updated = True

    st.subheader("🧠 Feedback Interpretation")
    st.json(interpretation)

    st.success("Learning complete: Policy updated based on reward.")

# ------------------------------------------------
# NEXT ACTION (Explicit)
# ------------------------------------------------
st.subheader("🔁 Next Action")

if st.button(
    "Re-Run Agent with Updated Policy",
    disabled=not st.session_state.policy_updated
):
    prompt = build_prompt(st.session_state.policy)
    chain = prompt | llm

    try:
        response = chain.invoke({"input": user_query})
        st.session_state.last_response = response.content
    except Exception:
        st.session_state.last_response = (
            f"[FALLBACK RESPONSE]\n"
            f"Verbosity={st.session_state.policy.verbosity}, "
            f"Tone={st.session_state.policy.tone}\n\n"
            f"Response after applying learned policy."
        )

    st.session_state.policy_updated = False

# ------------------------------------------------
# RL Internals (for teaching)
# ------------------------------------------------
st.subheader("🧪 RL Internals (Explicit View)")

st.json({
    "state": st.session_state.rl_state.as_dict(),
    "policy": st.session_state.policy.as_dict()
})

st.info(
    "This demo shows Reinforcement Learning fundamentals:\n"
    "• Policy = behavior rules\n"
    "• Reward = interpreted feedback\n"
    "• Learning = policy update\n"
    "• Action = re-running the agent\n\n"
    "No model retraining is involved."
)

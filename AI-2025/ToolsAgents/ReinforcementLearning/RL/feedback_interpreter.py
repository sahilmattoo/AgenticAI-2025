from langchain.prompts import ChatPromptTemplate
import json

# feedback_prompt = ChatPromptTemplate.from_messages([
#     ("system",
#      """Analyze human feedback.

# Return JSON:
# {
#   "reward": -1 | 0 | 1,
#   "dimensions": {
#     "verbosity": "increase | decrease | no_change",
#     "tone": "more_friendly | more_formal | no_change"
#   }
# }
# """),
#     ("human", "{feedback}")
# ])

feedback_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a reward model in a Reinforcement Learning system.

Your task:
1. Decide whether the feedback is POSITIVE, NEGATIVE, or NEUTRAL.
2. Assign a reward:
   - POSITIVE  → +1
   - NEGATIVE  → -1
   - NEUTRAL   → 0

Rules:
- Complaints (e.g. "too short", "too long", "confusing") are NEGATIVE.
- Praise (e.g. "good", "clear", "helpful") is POSITIVE.
- Suggestions imply NEGATIVE reward.

Then determine direction:
- If feedback says "too short" → verbosity = increase
- If feedback says "too long" → verbosity = decrease
- Otherwise → no_change

Return ONLY valid JSON in this format:
{
  "reward": -1 | 0 | 1,
  "dimensions": {
    "verbosity": "increase | decrease | no_change",
    "tone": "more_friendly | more_formal | no_change"
  }
}
"""),
    ("human", "{feedback}")
])


# def interpret_feedback(feedback, llm):
#     """
#     Environment → Reward
#     Converts human feedback into RL signal
#     """
#     try:
#         chain = feedback_prompt | llm
#         response = chain.invoke({"feedback": feedback})
#         return json.loads(response.content)
#     except Exception:
#         return {
#             "reward": 0,
#             "dimensions": {
#                 "verbosity": "no_change",
#                 "tone": "no_change"
#             }
#         }


def interpret_feedback(feedback, llm):
    try:
        chain = feedback_prompt | llm
        response = chain.invoke({"feedback": feedback})
        parsed = json.loads(response.content)

        # Guardrail: semantic sanity check
        fb = feedback.lower()
        if "too short" in fb and parsed["reward"] >= 0:
            parsed["reward"] = -1
            parsed["dimensions"]["verbosity"] = "increase"

        if "too long" in fb and parsed["reward"] >= 0:
            parsed["reward"] = -1
            parsed["dimensions"]["verbosity"] = "decrease"

        return parsed

    except Exception:
        return {
            "reward": -1,
            "dimensions": {
                "verbosity": "increase",
                "tone": "no_change"
            }
        }

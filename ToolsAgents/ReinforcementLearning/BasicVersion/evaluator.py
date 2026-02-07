from langchain.prompts import ChatPromptTemplate
import json

evaluator_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a policy evaluator.

Extract behavior changes from feedback.

Allowed JSON keys:
- verbosity: short | medium | detailed
- tone: neutral | friendly | formal

Return ONLY valid JSON.
"""),
    ("human", "{feedback}")
])

def evaluate_feedback(feedback, evaluator_llm):
    try:
        chain = evaluator_prompt | evaluator_llm
        result = chain.invoke({"feedback": feedback})
        return json.loads(result.content)
    except Exception:
        # Safe heuristic fallback
        fb = feedback.lower()
        delta = {}
        if "short" in fb or "too long" in fb:
            delta["verbosity"] = "short"
        if "friendly" in fb:
            delta["tone"] = "friendly"
        return delta

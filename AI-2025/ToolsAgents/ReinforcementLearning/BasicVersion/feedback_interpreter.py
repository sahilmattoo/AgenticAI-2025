from langchain.prompts import ChatPromptTemplate
import json

feedback_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You analyze human feedback about an AI response.

Classify:
1. Overall sentiment: positive | negative | neutral
2. For each dimension, give direction:
   - verbosity: increase | decrease | no_change
   - tone: more_friendly | more_formal | no_change

Return ONLY valid JSON.
"""),
    ("human", "{feedback}")
])

def interpret_feedback(feedback, llm):
    try:
        chain = feedback_prompt | llm
        response = chain.invoke({"feedback": feedback})
        return json.loads(response.content)
    except Exception:
        # Safe fallback
        return {
            "sentiment": "neutral",
            "dimensions": {
                "verbosity": "no_change",
                "tone": "no_change"
            }
        }

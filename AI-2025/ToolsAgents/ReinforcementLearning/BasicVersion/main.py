# main.py
from dotenv import load_dotenv
import os
# Load .env (safe to call even if another cell calls it)
load_dotenv()

# main_safe.py
from policy import ResponsePolicy
from prompt import build_prompt
from llm import llm, evaluator_llm
from langchain.prompts import ChatPromptTemplate
import json

USE_LLM = True   # flip to False to force offline/mock mode (classroom-safe)

policy = ResponsePolicy()
print("Initial policy:", policy)

# Build prompt (LangChain ChatPromptTemplate.partial used elsewhere)
prompt = build_prompt(policy)
chain = prompt | llm

def safe_invoke(chain, payload):
    try:
        return chain.invoke(payload)
    except Exception as e:
        print("⚠️ LLM call failed:", repr(e))
        return None

if USE_LLM:
    resp = safe_invoke(chain, {"input": "Explain Reinforcement Learning"})
    if resp is None:
        agent_text = f"[FALLBACK] Verbosity={policy.verbosity}, Tone={policy.tone} -- RL is learning from rewards."
    else:
        agent_text = resp.content
else:
    agent_text = f"[MOCK] Verbosity={policy.verbosity}, Tone={policy.tone} -- RL is learning from rewards."

print("\nAgent response:\n", agent_text)

# Simulate human feedback
feedback = "This is too long. I just want crisp bullet points."

# Evaluator chain using the evaluator LLM (also GPT-5.2-instant)
evaluator_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a policy evaluator.
Return valid JSON with allowed fields:
- verbosity: short | medium | detailed
- tone: neutral | friendly | formal
Return ONLY JSON."""),
    ("human", "{feedback}")
])

evaluator_chain = evaluator_prompt | evaluator_llm

if USE_LLM:
    try:
        eval_resp = evaluator_chain.invoke({"feedback": feedback})
        delta = json.loads(eval_resp.content)
    except Exception as e:
        print("⚠️ Evaluator failed:", e)
        delta = {}
else:
    # simple heuristic mock fallback
    delta = {"verbosity": "short"}

print("Policy delta:", delta)
policy.update(delta)
print("Updated policy:", policy)

# Next interaction (shows adapted behavior)
prompt = build_prompt(policy)
chain = prompt | llm
resp2 = safe_invoke(chain, {"input": "Explain Reinforcement Learning"})
if resp2 is None:
    print("\n[FALLBACK ADAPTED] Verbosity=", policy.verbosity, ", Tone=", policy.tone)
else:
    print("\nAdapted response:\n", resp2.content)

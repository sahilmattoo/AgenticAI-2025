from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
# Load .env (safe to call even if another cell calls it)
load_dotenv()

# Recommended for demos: GPT-5.2 Instant (fast + stable)
llm = ChatOpenAI(
   # model="gpt-5-nano",   # <-- switched to GPT-5 family
    model = "gpt-4o-mini",
    #temperature=0.3,
    #max_tokens=400
)

# Evaluator should be deterministic / low temp
evaluator_llm = ChatOpenAI(
    #model="gpt-5.2-nano",   # use same family for consistent behavior
    model = "gpt-4o-mini",
    #temperature=0.0,
    #max_tokens=150
)

#print(llm.invoke("Hello, world!"))
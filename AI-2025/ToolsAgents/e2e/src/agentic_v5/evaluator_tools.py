from langchain.tools import tool
from langchain_openai import ChatOpenAI

from llm_config import llm

#llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


@tool
def relevance_checker(data: str) -> str:
    """Check if the answer is relevant to the user question."""

    prompt = f"""
You are evaluating whether the response answers the user's question.

Example 1
Question: What is onboarding?
Answer: Onboarding is the process of integrating new employees.
Verdict: RELEVANT

Example 2
Question: What is onboarding?
Answer: The company values ethical conduct.
Verdict: NOT_RELEVANT

Now evaluate:

{data}

Return only:
RELEVANT or NOT_RELEVANT
"""

    return llm.invoke(prompt).content


@tool
def policy_alignment_checker(data: str) -> str:
    """Check whether the response aligns with HR policies."""

    prompt = f"""
Determine whether the response aligns with HR policies.

Example:

Policy: Harassment must be reported to HR.
Answer: Employees should report harassment to HR.
Verdict: ALIGNED

Answer: Ignore harassment incidents.
Verdict: NOT_ALIGNED

Now evaluate:

{data}

Return only:
ALIGNED or NOT_ALIGNED
"""

    return llm.invoke(prompt).content


@tool
def ethics_tone_checker(data: str) -> str:
    """Evaluate whether the response maintains ethical tone."""

    prompt = f"""
Evaluate whether the response maintains professional workplace tone.

Example:

Answer: Please report harassment to HR.
Verdict: PROFESSIONAL

Answer: Ignore the issue.
Verdict: UNETHICAL

Now evaluate:

{data}

Return only:
PROFESSIONAL or UNETHICAL
"""

    return llm.invoke(prompt).content
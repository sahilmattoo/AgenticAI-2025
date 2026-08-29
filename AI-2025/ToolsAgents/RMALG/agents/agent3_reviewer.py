"""
Agent 3 - Reviewer
Critiques the draft from Agent 2 and produces an improved version with review comments.
"""

from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable


@traceable(name="Agent 3: Reviewer", project_name="ResearchPaper")
def review_draft(drafter_output: Dict, llm: ChatOpenAI) -> Dict:
    """
    Reviews the draft from Agent 2 and provides critique + revised draft.

    Args:
        drafter_output: Output dictionary from Agent 2 (drafter)
        llm: LangChain ChatOpenAI instance

    Returns:
        Dict containing review comments, revised draft, and metadata
    """
    query = drafter_output["query"]
    draft = drafter_output["draft"]
    source_papers = drafter_output["source_papers"]

    papers_text = "\n".join([f"- {p['title']}: {p['abstract']}" for p in source_papers])

    # Step 1: Generate critique
    critique_prompt = ChatPromptTemplate.from_template(
        """You are a senior academic peer reviewer. Review the following literature review draft
        against the original source papers.

        Research Topic: {query}

        Original Source Papers:
        {papers}

        Draft to Review:
        {draft}

        Provide a structured review covering:
        1. ACCURACY: Are all claims supported by the source papers? Flag any hallucinations.
        2. COMPLETENESS: Are all key contributions from the papers covered?
        3. CLARITY: Is the writing clear and well-structured?
        4. SUGGESTIONS: Specific improvements to make.

        Be constructive but rigorous. Format each section with its heading.
        """
    )

    # Step 2: Generate revised draft based on critique
    revision_prompt = ChatPromptTemplate.from_template(
        """You are an expert academic writer. Revise the following draft based on the review comments.
        
        Original Draft:
        {draft}

        Review Comments:
        {critique}

        Source Papers (for reference):
        {papers}

        Produce an improved version of the draft that addresses all the review comments.
        Only use information from the source papers. Mark your key changes with [REVISED].
        """
    )

    critique_chain = critique_prompt | llm
    critique_response = critique_chain.invoke({
        "query": query,
        "papers": papers_text,
        "draft": draft
    })

    revision_chain = revision_prompt | llm
    revised_response = revision_chain.invoke({
        "draft": draft,
        "critique": critique_response.content,
        "papers": papers_text
    })

    return {
        "query": query,
        "original_draft": draft,
        "critique": critique_response.content,
        "revised_draft": revised_response.content,
        "source_papers": source_papers,
        "retrieval_context": drafter_output["retrieval_context"],
    }

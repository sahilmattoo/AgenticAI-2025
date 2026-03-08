"""
Agent 2 - Drafter
Takes the papers found by Agent 1 and drafts a structured literature review / research summary.
"""

from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable


@traceable(name="Agent 2: Drafter", project_name="ResearchPaper")
def draft_paper(finder_output: Dict, llm: ChatOpenAI) -> Dict:
    """
    Drafts a literature review / research summary from the papers found by Agent 1.

    Args:
        finder_output: Output dictionary from Agent 1 (paper_finder)
        llm: LangChain ChatOpenAI instance

    Returns:
        Dict containing the draft and relevant metadata
    """
    query = finder_output["query"]
    papers = finder_output["papers"]

    # Format papers for the prompt
    papers_formatted = "\n\n".join([
        f"**{p['title']}** ({p['year']}) — {', '.join(p['authors'])}\n{p['abstract']}"
        for p in papers
    ])

    prompt = ChatPromptTemplate.from_template(
        """You are an expert academic writer. Using ONLY the information from the provided papers,
        write a structured literature review section on the research topic.

        Research Topic: {query}

        Source Papers:
        {papers}

        Write a well-structured draft with the following sections:
        1. Introduction / Background
        2. Key Contributions (per paper)
        3. Synthesis & Connections Between Papers
        4. Gaps & Future Directions

        IMPORTANT: Only use information directly from the papers above. Do NOT add information
        from outside these papers. Cite each paper by title when referencing it.
        """
    )

    chain = prompt | llm
    response = chain.invoke({"query": query, "papers": papers_formatted})

    return {
        "query": query,
        "source_papers": papers,
        "draft": response.content,
        "retrieval_context": finder_output["retrieval_context"],
    }

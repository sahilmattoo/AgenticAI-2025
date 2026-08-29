"""
Agent 1 - Paper Finder
Finds relevant research papers for a given query.
In a real system this would call arXiv / Semantic Scholar APIs.
Here we simulate with realistic mock data.
"""

from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable


@traceable(name="Agent 1: Paper Finder", project_name="ResearchPaper")
def find_papers(query: str, llm: ChatOpenAI) -> Dict:
    """
    Simulates finding relevant research papers for a given query.
    Returns a structured dict with the papers found and the agent's context.
    """
    # --- Simulated paper database (replace with actual arXiv/S2 API calls) ---
    mock_papers = [
        {
            "title": "Attention Is All You Need",
            "authors": ["Vaswani et al."],
            "year": 2017,
            "abstract": (
                "We propose a new simple network architecture, the Transformer, "
                "based solely on attention mechanisms, dispensing with recurrence and "
                "convolutions entirely. Experiments on two machine translation tasks show "
                "these models to be superior in quality."
            ),
            "url": "https://arxiv.org/abs/1706.03762",
        },
        {
            "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
            "authors": ["Devlin et al."],
            "year": 2018,
            "abstract": (
                "We introduce BERT, which stands for Bidirectional Encoder Representations "
                "from Transformers. BERT is designed to pre-train deep bidirectional "
                "representations from unlabeled text by jointly conditioning on both left "
                "and right context in all layers."
            ),
            "url": "https://arxiv.org/abs/1810.04805",
        },
        {
            "title": "GPT-3: Language Models are Few-Shot Learners",
            "authors": ["Brown et al."],
            "year": 2020,
            "abstract": (
                "We train GPT-3, an autoregressive language model with 175 billion parameters, "
                "and test its performance in the few-shot setting. GPT-3 achieves strong "
                "performance on many NLP tasks and benchmarks."
            ),
            "url": "https://arxiv.org/abs/2005.14165",
        },
        {
            "title": "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models",
            "authors": ["Wei et al."],
            "year": 2022,
            "abstract": (
                "We explore how generating a chain of thought — a series of intermediate "
                "reasoning steps — significantly improves the ability of large language "
                "models to perform complex reasoning."
            ),
            "url": "https://arxiv.org/abs/2201.11903",
        },
        {
            "title": "ReAct: Synergizing Reasoning and Acting in Language Models",
            "authors": ["Yao et al."],
            "year": 2022,
            "abstract": (
                "We explore the use of LLMs to generate both reasoning traces and "
                "task-specific actions in an interleaved manner, allowing greater synergy "
                "between the two: reasoning traces help the model induce, track, and update "
                "action plans, while actions allow it to interface with external sources."
            ),
            "url": "https://arxiv.org/abs/2210.03629",
        },
    ]

    # Use LLM to select and rank relevant papers
    prompt = ChatPromptTemplate.from_template(
        """You are a research paper curator. Given the research query and a list of papers,
        select the most relevant papers and explain why each is relevant.

        Research Query: {query}

        Available Papers:
        {papers}

        Return the titles of the most relevant papers (up to 3) with a brief relevance explanation.
        Format: PAPER: <title> | REASON: <why relevant>
        """
    )

    papers_text = "\n".join(
        [f"- {p['title']} ({p['year']}): {p['abstract'][:150]}..." for p in mock_papers]
    )

    chain = prompt | llm
    response = chain.invoke({"query": query, "papers": papers_text})

    # Parse selected papers
    selected_titles = []
    for line in response.content.split("\n"):
        if line.startswith("PAPER:"):
            parts = line.split("|")
            title = parts[0].replace("PAPER:", "").strip()
            selected_titles.append(title)

    # Filter mock papers to selected ones (fuzzy match)
    selected_papers = [
        p for p in mock_papers
        if any(sel.lower() in p["title"].lower() or p["title"].lower() in sel.lower()
               for sel in selected_titles)
    ]

    # Fallback: return top 3 if LLM selection fails
    if not selected_papers:
        selected_papers = mock_papers[:3]

    return {
        "query": query,
        "papers": selected_papers,
        "agent_response": response.content,
        "retrieval_context": [p["abstract"] for p in selected_papers],
    }

"""
Main Orchestrator - Research Paper Writing Multi-Agent Pipeline
================================================================

Pipeline flow:
  Query → Agent1 (Find Papers) → Agent2 (Draft) → Agent3 (Review) → Agent4 (User)
                                                                         ↕
                                                              (iterative loop)

DeepEval metrics are applied at each agent boundary.
LangSmith tracing is enabled for all agents under project "ResearchPaper".

Usage:
  python main_pipeline.py

Requirements:
  pip install langchain langchain-openai deepeval python-dotenv langsmith
"""

import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langsmith import traceable

# Add the RMALG root to the path so agent imports work
sys.path.insert(0, os.path.dirname(__file__))

from agents.agent1_paper_finder import find_papers
from agents.agent2_drafter import draft_paper
from agents.agent3_reviewer import review_draft
from agents.agent4_user_interface import handle_user_feedback
from evaluations.deepeval_evaluations import evaluate_full_pipeline

# ---------------------------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------------------------
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in environment. Check your .env file.")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
print("OpenAI Key Found")

# ---------------------------------------------------------------------------
# LangSmith Tracing Configuration
# ---------------------------------------------------------------------------
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
if not LANGCHAIN_API_KEY:
    print("⚠️  LANGCHAIN_API_KEY not found — LangSmith tracing will be disabled.")
else:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "ResearchPaper"
    os.environ["LANGCHAIN_ENDPOINT"] = os.getenv(
        "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"
    )
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    print(f"✅ LangSmith tracing enabled → project: ResearchPaper")

# ---------------------------------------------------------------------------
# Pipeline Configuration
# ---------------------------------------------------------------------------
RESEARCH_QUERY = (
    "How do large language models use attention mechanisms and prompting strategies "
    "to perform complex reasoning tasks?"
)

# Simulated user feedback for Agent 4
USER_FEEDBACK = (
    "Can you add more emphasis on the differences between GPT-3 and BERT? "
    "Also, please make the introduction shorter."
)


# ---------------------------------------------------------------------------
# Helper Utilities
# ---------------------------------------------------------------------------

def print_section(title: str, content: str, max_chars: int = 800) -> None:
    """Pretty-prints a pipeline stage output."""
    print(f"\n{'━' * 70}")
    print(f"  {title}")
    print(f"{'━' * 70}")
    preview = content[:max_chars] + ("..." if len(content) > max_chars else "")
    print(preview)


@traceable(name="ResearchPaper Pipeline", project_name="ResearchPaper")
def run_pipeline(evaluate: bool = True) -> dict:
    """
    Runs the full 4-agent research paper writing pipeline.

    Args:
        evaluate: If True, runs DeepEval evaluations after all agents complete.

    Returns:
        Dictionary containing all agent outputs.
    """
    print("\n" + "🚀 " * 20)
    print("  MULTI-AGENT RESEARCH PAPER WRITING PIPELINE")
    print(f"  Query: {RESEARCH_QUERY}")
    print("🚀 " * 20)

    # Initialize LLM (shared across all agents; you can use different models per agent)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    # ------------------------------------------------------------------
    # AGENT 1: Find relevant papers
    # ------------------------------------------------------------------
    print("\n\n🔍 Running Agent 1: Paper Finder...")
    finder_output = find_papers(query=RESEARCH_QUERY, llm=llm)
    print_section(
        "Agent 1 Output — Papers Found",
        "\n".join([f"  • {p['title']} ({p['year']})" for p in finder_output["papers"]])
    )

    # ------------------------------------------------------------------
    # AGENT 2: Draft the literature review
    # ------------------------------------------------------------------
    print("\n\n✍️  Running Agent 2: Drafter...")
    drafter_output = draft_paper(finder_output=finder_output, llm=llm)
    print_section("Agent 2 Output — Draft", drafter_output["draft"])

    # ------------------------------------------------------------------
    # AGENT 3: Review and improve the draft
    # ------------------------------------------------------------------
    print("\n\n🔎 Running Agent 3: Reviewer...")
    reviewer_output = review_draft(drafter_output=drafter_output, llm=llm)
    print_section("Agent 3 Output — Critique", reviewer_output["critique"])
    print_section("Agent 3 Output — Revised Draft", reviewer_output["revised_draft"])

    # ------------------------------------------------------------------
    # AGENT 4: Handle user feedback
    # ------------------------------------------------------------------
    print("\n\n💬 Running Agent 4: User Interface Agent...")
    print(f"  User says: '{USER_FEEDBACK}'")
    ui_output = handle_user_feedback(
        reviewer_output=reviewer_output,
        user_feedback=USER_FEEDBACK,
        llm=llm,
    )
    print_section("Agent 4 Output — Acknowledgment", ui_output["acknowledgment"])
    print_section("Agent 4 Output — Updated Draft", ui_output["updated_draft"])

    # ------------------------------------------------------------------
    # DEEPEVAL EVALUATIONS
    # ------------------------------------------------------------------
    if evaluate:
        all_results = evaluate_full_pipeline(
            finder_output=finder_output,
            drafter_output=drafter_output,
            reviewer_output=reviewer_output,
            ui_output=ui_output,
            research_query=RESEARCH_QUERY,
        )

    outputs = {
        "finder_output": finder_output,
        "drafter_output": drafter_output,
        "reviewer_output": reviewer_output,
        "ui_output": ui_output,
    }

    print("\n\n✅ Pipeline complete!")
    return outputs


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_pipeline(evaluate=True)

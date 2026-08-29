"""
DeepEval Evaluations for the Multi-Agent Research Paper Writing System

Each agent is evaluated with metrics appropriate for its role:

  Agent 1 - Paper Finder   → ContextualRecall, ContextualPrecision, ContextualRelevancy
  Agent 2 - Drafter        → Faithfulness, AnswerRelevancy, Summarization
  Agent 3 - Reviewer       → GEval (custom review quality), Hallucination
  Agent 4 - User Interface → AnswerRelevancy, custom GEval (task completion)
"""

import os
from typing import Dict
from dotenv import load_dotenv

# ⚠️  Must load env vars BEFORE importing/instantiating DeepEval metrics.
# DeepEval constructs GPTModel (and reads OPENAI_API_KEY) at module-level
# when metric objects are created below — so load_dotenv() must fire first.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../../.env"))

from deepeval import evaluate
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import (
    ContextualRecallMetric,
    ContextualPrecisionMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    HallucinationMetric,
    GEval,
)


# ---------------------------------------------------------------------------
# Metric Definitions
# ---------------------------------------------------------------------------

# --- Agent 1: Paper Finder ---
retrieval_recall = ContextualRecallMetric(
    threshold=0.6,
    model="gpt-4o-mini",
    include_reason=True,
)
retrieval_precision = ContextualPrecisionMetric(
    threshold=0.6,
    model="gpt-4o-mini",
    include_reason=True,
)
retrieval_relevancy = ContextualRelevancyMetric(
    threshold=0.6,
    model="gpt-4o-mini",
    include_reason=True,
)

# --- Agent 2: Drafter ---
faithfulness_metric = FaithfulnessMetric(
    threshold=0.7,
    model="gpt-4o-mini",
    include_reason=True,
)
draft_relevancy_metric = AnswerRelevancyMetric(
    threshold=0.7,
    model="gpt-4o-mini",
    include_reason=True,
)

# --- Agent 3: Reviewer ---
review_quality_metric = GEval(
    name="Review Quality",
    criteria=(
        "The review should: "
        "(1) Identify specific inaccuracies or unsupported claims in the draft, "
        "(2) Provide actionable and constructive suggestions, "
        "(3) Be based only on the source papers provided, "
        "(4) Not hallucinate or introduce new information not in the source papers."
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.CONTEXT,
    ],
    threshold=0.6,
    model="gpt-4o-mini",
)

hallucination_metric = HallucinationMetric(
    threshold=0.3,   # Lower is better — must be < 30% hallucinated
    model="gpt-4o-mini",
    include_reason=True,
)

# --- Agent 4: User Interface ---
user_response_relevancy = AnswerRelevancyMetric(
    threshold=0.7,
    model="gpt-4o-mini",
    include_reason=True,
)

task_completion_metric = GEval(
    name="Task Completion",
    criteria=(
        "The agent must: "
        "(1) Correctly understand and acknowledge the user's change request, "
        "(2) Apply the requested changes to the draft accurately, "
        "(3) Not add information that isn't supported by the source papers, "
        "(4) Maintain the academic quality of the revised draft."
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.CONTEXT,
    ],
    threshold=0.65,
    model="gpt-4o-mini",
)


# ---------------------------------------------------------------------------
# Per-Agent Evaluation Functions
# ---------------------------------------------------------------------------

def evaluate_agent1(finder_output: Dict, research_query: str) -> None:
    """
    Evaluates Agent 1 (Paper Finder) using retrieval-based metrics.

    Args:
        finder_output:  Output dict from agent1_paper_finder.find_papers()
        research_query: The original research query string
    """
    print("\n" + "=" * 60)
    print("📊 EVALUATING AGENT 1 — Paper Finder")
    print("=" * 60)

    # Ground truth: the expected abstracts that SHOULD be retrieved
    expected_documents = [p["abstract"] for p in finder_output["papers"]]

    test_case = LLMTestCase(
        input=research_query,
        actual_output=finder_output["agent_response"],
        expected_output="; ".join([p["title"] for p in finder_output["papers"]]),
        retrieval_context=finder_output["retrieval_context"],
        context=expected_documents,
    )

    results = evaluate(
        test_cases=[test_case],
        metrics=[retrieval_recall, retrieval_precision, retrieval_relevancy],
    )
    return results


def evaluate_agent2(drafter_output: Dict, research_query: str) -> None:
    """
    Evaluates Agent 2 (Drafter) for faithfulness and relevancy.

    Args:
        drafter_output: Output dict from agent2_drafter.draft_paper()
        research_query: The original research query string
    """
    print("\n" + "=" * 60)
    print("📊 EVALUATING AGENT 2 — Drafter")
    print("=" * 60)

    test_case = LLMTestCase(
        input=research_query,
        actual_output=drafter_output["draft"],
        retrieval_context=drafter_output["retrieval_context"],
        context=[p["abstract"] for p in drafter_output["source_papers"]],
    )

    results = evaluate(
        test_cases=[test_case],
        metrics=[faithfulness_metric, draft_relevancy_metric],
    )
    return results


def evaluate_agent3(reviewer_output: Dict) -> None:
    """
    Evaluates Agent 3 (Reviewer) for review quality and hallucination.

    Args:
        reviewer_output: Output dict from agent3_reviewer.review_draft()
    """
    print("\n" + "=" * 60)
    print("📊 EVALUATING AGENT 3 — Reviewer")
    print("=" * 60)

    source_abstracts = [p["abstract"] for p in reviewer_output["source_papers"]]

    # Evaluate the critique quality
    critique_test_case = LLMTestCase(
        input=reviewer_output["original_draft"],
        actual_output=reviewer_output["critique"],
        context=source_abstracts,
    )

    # Evaluate the revised draft for hallucination against source papers
    hallucination_test_case = LLMTestCase(
        input=reviewer_output["query"],
        actual_output=reviewer_output["revised_draft"],
        context=source_abstracts,
    )

    print("\n[3a] Critique Quality:")
    results_critique = evaluate(
        test_cases=[critique_test_case],
        metrics=[review_quality_metric],
    )

    print("\n[3b] Revised Draft Hallucination Check:")
    results_hallucination = evaluate(
        test_cases=[hallucination_test_case],
        metrics=[hallucination_metric],
    )

    return results_critique, results_hallucination


def evaluate_agent4(ui_output: Dict) -> None:
    """
    Evaluates Agent 4 (User Interface Agent) for task completion and response quality.

    Args:
        ui_output: Output dict from agent4_user_interface.handle_user_feedback()
    """
    print("\n" + "=" * 60)
    print("📊 EVALUATING AGENT 4 — User Interface Agent")
    print("=" * 60)

    source_abstracts = [p["abstract"] for p in ui_output["source_papers"]]

    test_case = LLMTestCase(
        input=ui_output["user_feedback"],
        actual_output=ui_output["agent_response"],
        context=source_abstracts,
    )

    results = evaluate(
        test_cases=[test_case],
        metrics=[user_response_relevancy, task_completion_metric],
    )
    return results


# ---------------------------------------------------------------------------
# Full Pipeline Evaluation (runs all agents back-to-back)
# ---------------------------------------------------------------------------

def evaluate_full_pipeline(
    finder_output: Dict,
    drafter_output: Dict,
    reviewer_output: Dict,
    ui_output: Dict,
    research_query: str,
) -> Dict:
    """
    Runs all agent evaluations and returns a summary report.
    """
    print("\n" + "🔬 " * 20)
    print("  FULL PIPELINE DEEPEVAL REPORT")
    print("🔬 " * 20)

    r1 = evaluate_agent1(finder_output, research_query)
    r2 = evaluate_agent2(drafter_output, research_query)
    r3a, r3b = evaluate_agent3(reviewer_output)
    r4 = evaluate_agent4(ui_output)

    print("\n\n✅ All agent evaluations complete.")
    return {
        "agent1_results": r1,
        "agent2_results": r2,
        "agent3_critique_results": r3a,
        "agent3_hallucination_results": r3b,
        "agent4_results": r4,
    }

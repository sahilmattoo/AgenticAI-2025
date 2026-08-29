"""
Agent 4 - User Interface Agent
Interacts with the user, understands their change requests, and applies them to the draft.
"""

from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable


@traceable(name="Agent 4: User Interface", project_name="ResearchPaper")
def handle_user_feedback(
    reviewer_output: Dict,
    user_feedback: str,
    llm: ChatOpenAI,
    conversation_history: Optional[list] = None,
) -> Dict:
    """
    Handles user change requests and generates an updated draft accordingly.

    Args:
        reviewer_output: Output dictionary from Agent 3 (reviewer)
        user_feedback: The user's change request / feedback string
        llm: LangChain ChatOpenAI instance
        conversation_history: Optional list of prior (user, assistant) turns

    Returns:
        Dict containing the updated draft and interaction metadata
    """
    revised_draft = reviewer_output["revised_draft"]
    query = reviewer_output["query"]
    source_papers = reviewer_output["source_papers"]

    papers_text = "\n".join([f"- {p['title']}: {p['abstract']}" for p in source_papers])

    # Format conversation history if present
    history_text = ""
    if conversation_history:
        history_text = "\n".join([
            f"User: {turn['user']}\nAssistant: {turn['assistant']}"
            for turn in conversation_history
        ])

    prompt = ChatPromptTemplate.from_template(
        """You are a helpful research assistant helping the user refine their literature review.
        You must understand their feedback and apply changes ONLY based on information from
        the source papers provided.

        Research Topic: {query}

        Source Papers (for reference):
        {papers}

        Current Draft:
        {draft}

        Previous Conversation:
        {history}

        User's New Request: {feedback}

        First, acknowledge what the user wants. Then apply their requested changes to the draft.
        If the user requests something that isn't supported by the source papers, politely
        explain that and suggest alternatives that ARE supported.

        Format your response as:
        ACKNOWLEDGMENT: <brief acknowledgment of the user's request>
        UPDATED_DRAFT: <the updated literature review>
        """
    )

    chain = prompt | llm
    response = chain.invoke({
        "query": query,
        "papers": papers_text,
        "draft": revised_draft,
        "history": history_text,
        "feedback": user_feedback,
    })

    # Parse response
    content = response.content
    acknowledgment = ""
    updated_draft = content  # fallback

    if "ACKNOWLEDGMENT:" in content and "UPDATED_DRAFT:" in content:
        parts = content.split("UPDATED_DRAFT:")
        acknowledgment = parts[0].replace("ACKNOWLEDGMENT:", "").strip()
        updated_draft = parts[1].strip()

    # Update conversation history
    if conversation_history is None:
        conversation_history = []
    conversation_history.append({
        "user": user_feedback,
        "assistant": acknowledgment,
    })

    return {
        "query": query,
        "user_feedback": user_feedback,
        "acknowledgment": acknowledgment,
        "updated_draft": updated_draft,
        "original_revised_draft": revised_draft,
        "source_papers": source_papers,
        "retrieval_context": reviewer_output["retrieval_context"],
        "conversation_history": conversation_history,
        "agent_response": content,
    }

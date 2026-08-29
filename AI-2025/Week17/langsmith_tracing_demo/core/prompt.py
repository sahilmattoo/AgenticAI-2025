"""
Defines the ChatPromptTemplate for concise, helpful answers.
"""

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant. Answer concisely.\n\nQuestion: {question}"
)

# Basic Imports
from typing import TypedDict, Annotated, Optional
# LangChain / LangGraph Imports
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent
# Project Imports

# Prompt
DEFAULT_PROMPT = """
    Given the following Markdown article draft, please provide concise feedback to improve clarity, coherence, grammar, and overall readability. \
    Focus on ensuring that the Markdown syntax is used correctly, such as headers, bullet points, lists, and code blocks. \
    Address any ambiguities, improve transitions between sections, and suggest ways to enhance the structure and formatting. \
    If there are areas where more details could be added, suggest specific improvements. \
    Provide actionable feedback and highlight potential strengths in both content and Markdown style. \n
    You will also be given the initial question that the article is aiming to address.
"""

class EditorAgent:

    def __init__(self, llm, prompt=DEFAULT_PROMPT):
        # initialization
        self.prompt = prompt
        self.llm = llm

    def critique(self, state):
        messages = [
            SystemMessage(content=self.prompt),  # Loading the role
            HumanMessage(content=state["article_draft"]),
            HumanMessage(content=state["reddit_question"])
        ]
        
        response = self.llm.invoke(messages).content

        state['editor_feedback'] = response
        state["revision_number"] = state["revision_number"] + 1

        return state
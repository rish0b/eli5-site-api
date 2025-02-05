# Basic Imports
# LangChain / LangGraph Imports
from langchain_core.messages import HumanMessage, SystemMessage
# Project Imports

# Prompt
DEFAULT_PROMPT = """
    Given the following Markdown article draft, please provide concise feedback to improve clarity, coherence, grammar, and overall readability. The article is designed to be short, fun, viral, and a joy to read. \
    Focus on ensuring that the Markdown syntax is used correctly, such as headers, bullet points, lists, and blocks. \
    Address any ambiguities, improve transitions between sections, and suggest ways to enhance the markdown structure and formatting. \
    Do not worry about the article title, that will be handled separately. \
    The draft you are provided is intended to get right into it, with a strong hook. \
    If there are areas which are boring / don't retain the readers attention, suggest specific improvements. \
    Provide actionable feedback and highlight potential strengths in both content and Markdown style. The markdown style should emphasize key points and make the article appealing to read. The content itself should FLOW and ADDRESS the original question at hand. \n
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
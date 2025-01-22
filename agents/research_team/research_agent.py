# LangChain / LangGraph Imports
from langchain_community.tools import TavilySearchResults
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
# Project Imports
from ...agent_templates.tool_calling_agent import ToolCallingAgent

# Tools
tools = [ TavilySearchResults(max_results=5) ]

# Prompt
DEFAULT_PROMPT = """You are a smart research assistant. Use the search engine to look up current, up-to-date information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before making another search engine call, you are allowed to do that! \
I want you to return highly detailed, informative research notes so that my content writer can write an article using it.
"""

class ResearchAgent(ToolCallingAgent):

    def __init__(self, llm, tools, prompt=DEFAULT_PROMPT):
        super().__init__(llm, tools, prompt)

    def do_research(self, question):
        messages = [HumanMessage(content=question)]
        # Kicks off Tool Calling Agent flow and returns the final research output
        return super().graph.invoke({"messages": messages})['messages'][-1] 
import os, json
from dotenv import load_dotenv
import datetime
# LangChain / LangGraph Imports
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools import TavilySearchResults
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
# Project Imports
from agent_templates.tool_calling_agent import ToolCallingAgent


load_dotenv()
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

# Tools
search = TavilySearchAPIWrapper(tavily_api_key=TAVILY_API_KEY)
tools = [ TavilySearchResults(api_wrapper=search, max_results=5) ]

date = datetime.datetime.utcnow().strftime('%Y-%m-%d')

# Prompt
DEFAULT_PROMPT = f"""
You are a smart research assistant. Use the search engine to look up current, up-to-date information. You may make several calls to the search engine if follow ups are required.
If it is necessary to grab the most recent data, the current date is {date}. However, only include the date in your response if it is crucial for filtering results.

Your response must include:
1. Research notes: In-depth, highly detailed, and facts oriented research notes that will be passed on to our content writer. Any relevant statistics, facts, and figures are encouraged. 
2. Sources: A list of all URLs or references used for your research.

Return your output in the following JSON format:
{{
    "research_notes": "Detailed notes here",
    "sources": ["URL1", "URL2", "URL3"]
}}
"""

class ResearchAgent(ToolCallingAgent):

    def __init__(self, llm, prompt=DEFAULT_PROMPT):
        super().__init__(llm, tools, prompt)

    def do_research(self, state):
        messages = [HumanMessage(content=state["reddit_question"])]
        
        # Kicks off Tool Calling Agent flow and returns the final research output
        research_output = json.loads(self.graph.invoke({"messages": messages})['messages'][-1].content)

        state['research_notes'] = research_output['research_notes']
        state['sources'] = research_output['sources']

        return state
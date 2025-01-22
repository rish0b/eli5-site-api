# Standard imports
import os
from dotenv import load_dotenv
import logging
# Import OpenAI
from langchain_openai import ChatOpenAI
# LangChain / LangGraph Imports
from langgraph.graph import StateGraph, END
# Project Imports
from .states.state import ArticleState



##### SETUP #####

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the LLM 
llm = ChatOpenAI(model="gpt-4o")



##### EXECUTION #####

# can probably go in /graphs directory and get imported.
def create_graph():
    graph = StateGraph(ArticleState)


def main():
    logger.log(level=20, msg="Running News Production...")


if __name__ == "__main__":
    main()
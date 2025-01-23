# Standard imports
import os
from dotenv import load_dotenv
import logging
# LangChain / LangGraph Imports
from langchain_openai import ChatOpenAI
# Project Imports
from states.state import initialize_article_state
from article_production import article_production

##### SETUP #####
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the LLM 
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")


##### INITIAL STATE #####
initial_state = initialize_article_state()

##### EXECUTION #####

def main():
    logger.log(level=20, msg="Running Article Production...")

    create_article = article_production(llm).compile()
    initial_state["max_revisions"] = 1
    # initial_state["reddit_question"] = "ELI5: when they ban a fan from a stadium how would they stop the person from coming to a game the next season?"
    print(create_article.invoke(initial_state))  # pass in ArticleState with vals

if __name__ == "__main__":
    main()
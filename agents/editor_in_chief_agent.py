import requests
# LangChain / LangGraph Imports
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
# Project Imports
from states.state import ArticleState



# Prompt
DEFAULT_PROMPT = """
You are the Editor-in-Chief of an AI-driven news site, responsible for coordinating the content production process. \
    Your task is to oversee the seamless creation, refinement, and publication of articles. \
    You must ensure that content from the Research Team, Writing Team, and Publishing Team aligns with the site’s goals of providing clear, engaging, and informative explanations. \
    You will review the progress of each team, ensure communication between agents, and make strategic decisions to maintain high-quality output. \
    \n
    Your responsibilities include: \n
    \n
    Reviewing research findings to ensure accuracy and relevance. \n
    Guiding writers to turn complex information into easy-to-understand content. \n
    Communicating with the publishing team to ensure smooth article distribution and outreach. \n
    Ensuring the articles reflect the site’s mission to simplify knowledge for a broad audience. \n
    Keep the process efficient and productive by maintaining clear communication, resolving conflicts, and upholding the quality standards set for content.
"""

class EditorInChiefAgent():

    def __init__(self, llm, tools=[], prompt=DEFAULT_PROMPT):
        self.prompt = prompt
        self.llm = llm
        llm.bind_tools(tools)    

    def next_team(self, state):
        if state.get("reddit_question", "") == "":
            return {"next_node": "reddit"}
        elif state.get("research_notes", "") == "":
            return {"next_node": "research"}
        elif state.get("article_content", "") == "":
            return {"next_node": "writing"}
        return {"next_node": "END"}

    def get_rising_posts(subreddit_name='explainlikeimfive', filter='rising', limit=5):
        # URL to fetch rising posts with the limit
        url = f"https://www.reddit.com/r/{subreddit_name}/{filter}.json?limit={limit}"
        
        # Send a GET request to the Reddit API
        data = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
        
        # Parse the JSON response
        posts = []
        
        for post in data['data']['children']:
            post_info = {
                'reddit_post_id': post['data']['id'],
                'reddit_question': post['data']['title'],
                'reddit_user': post['data']['author'],
                'reddit_tag': post['data']['link_flair_text']
            }
            posts.append(post_info)
        
        return posts    
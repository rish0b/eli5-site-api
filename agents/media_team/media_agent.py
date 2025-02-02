# Basic Imports
import json
from pydantic import BaseModel, Field
# LangChain / LangGraph Imports
from langchain_core.messages import HumanMessage, SystemMessage
# Project Imports
from utils import get_posts_from_eli5_reddit
from agent_templates.tool_calling_agent import ToolCallingAgent

# Prompt
DEFAULT_PROMPT = f"""
You are a content strategist at a blog publication. You will be given the top 5 hottest posts from the r/explainlikeimfive subreddit, in the form of an array of 5 reddit posts, with some metadata on each post. 

Select one post that poses the most interesting, most viral question ("reddit_question") that a whole, engaging, viral article can be written about.

Return the following fields in your output:
{{
    "reddit_post_id": "ID of Reddit Post",
    "reddit_question": "eli5 question",
    "reddit_user": "Reddit user who posted the query",
    "reddit_tag": "Category of the eli5 post"
}}
"""

tools = [ get_posts_from_eli5_reddit ]

class MediaOutput(BaseModel):
    reddit_post_id: str = Field(description="ID of Reddit Post")
    reddit_question: str = Field(description="eli5 question")
    reddit_user: str = Field(description="Reddit user who posted the query")
    reddit_tag: str = Field(description="Category of the eli5 post")


class MediaAgent():

    def __init__(self, llm, prompt=DEFAULT_PROMPT):
        self.llm = llm
        self.prompt = prompt

    def fetch_from_reddit(self, state):
        reddit_posts_str = json.dumps(get_posts_from_eli5_reddit(), indent=2)

        messages = [
            SystemMessage(content=DEFAULT_PROMPT),
            HumanMessage(content=reddit_posts_str)]
        # reddit_output = self.graph.invoke({"messages": messages})['messages'][-1].content

        structured_llm = self.llm.with_structured_output(MediaOutput)

        reddit_output = structured_llm.invoke(messages)

        print(reddit_output)

        state['reddit_post_id'] = reddit_output.reddit_post_id
        state['reddit_question'] = reddit_output.reddit_question
        state['reddit_user'] = reddit_output.reddit_user
        state['reddit_tag'] = reddit_output.reddit_tag

        return state
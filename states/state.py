from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class MessageState(TypedDict):
    messages : Annotated[list[AnyMessage], add_messages]

class ArticleState(TypedDict):
    # supervisor

    # reddit tool call
    reddit_post_id: str         # ID of Reddit Post
    reddit_title: str           # eli5 question
    reddit_user: str            # Reddit user who posted the query
    reddit_tag: str             # Category of the eli5 post

    # research team
    sources: List[str]          # News Sources Pulled
    research_notes: List[str]   # Summarized Research Notes

    # writing team
    article_draft: str          # Article Draft
    editor_feedback: str        # Editor Critique
    
    revision_number: int        # Number of Revisions
    max_revisions: int          # Maximum Number of Revisions

    article_title: str          # Article Title
    article_content: str        # Article
    article_blurb: str          # Article Blurb

    # publishing team
    markdown_content: str       # Final markdown content for the article
    markdown_path: str          # Path to the saved markdown file (on disk or temp)
    published_link: str         # Final article url
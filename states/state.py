from typing import TypedDict, List, Annotated, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class MessageState(TypedDict):
    messages : Annotated[list[AnyMessage], add_messages]

class ArticleState(TypedDict):
    # reddit tool call (inputs to the whole system)
    reddit_post_id: str         # ID of Reddit Post
    reddit_question: str        # eli5 question
    reddit_selftext: str        # Additional context on the question
    reddit_user: str            # Reddit user who posted the query
    reddit_tag: str             # Category of the eli5 post

    # editor in chief

    # research team
    sources: List[str]          # Info Sources Pulled
    research_notes: str         # Summarized Research Notes - consider list[]??

    # writing team
    article_draft: str          # Article Draft
    editor_feedback: str        # Editor Critique
    
    revision_number: int        # Number of Revisions
    max_revisions: int          # Maximum Number of Revisions

    article_content: str        # Article

    article_title: str          # Article headline (formatted version of eli5)
    article_subtitle: str         # Article sub headline

    # media team
    article_url: str            # Final article url

def initialize_article_state() -> ArticleState:
    return ArticleState(
        reddit_post_id="",
        reddit_question="",
        reddit_selftext="",
        reddit_user="",
        reddit_tag="",

        sources=[],
        research_notes="",

        article_draft="",
        editor_feedback="",

        revision_number=0,
        max_revisions=0,

        article_content="",

        article_title="",
        article_subtitle="",
        
        article_url=""
    )    
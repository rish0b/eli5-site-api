from typing import TypedDict, List, Annotated, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class MessageState(TypedDict):
    messages : Annotated[list[AnyMessage], add_messages]

class ArticleState(TypedDict):
    # reddit tool call (inputs to the whole system)
    reddit_post_id: str         # ID of Reddit Post
    reddit_question: str           # eli5 question
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

    article_title: str          # Article headline (formatted version of eli5)
    article_content: str        # Article
    article_byline: str         # Article sub headline

    reddit_response: str        # Reddit response (short, catchy, eli5 response - maybe generated by separate writer agent)

    # publishing team
    markdown_content: str       # Final markdown content for the article
    markdown_path: str          # Path to the saved markdown file (on disk or temp)
    article_url: str            # Final article url
    reddit_url: str             # Final reddit comment url

def initialize_article_state() -> ArticleState:
    return ArticleState(
        reddit_post_id="",
        reddit_question="",
        reddit_user="",
        reddit_tag="",

        sources=[],
        research_notes="",

        article_draft="",
        editor_feedback="",

        revision_number=0,
        max_revisions=1,

        article_title="",
        article_content="",
        article_byline="",

        reddit_response="",
        
        markdown_content="",
        markdown_path="",
        article_url="",
        reddit_url=""
    )    
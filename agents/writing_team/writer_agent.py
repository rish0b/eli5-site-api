# Basic Imports
from typing import Optional
# LangChain / LangGraph Imports
from langchain_core.messages import HumanMessage, SystemMessage
# Project Imports

# Prompt
DEFAULT_PROMPT = """
You are a professional content writer.  
You specialize in writing viral, simple to understand, short, informative articles that are clear, concise, and a joy to read.  
Your task is to write a short, fun article based on the provided inputs that must keep the user's attention.  
You may also receive a previous draft of the article and editor feedback to guide your improvements.  

The article title will be provided separately, you will not include it. Just get right into the article, starting it with a section with heading level 3 (perhaps, "Introduction").

Use Markdown syntax for the article. Ensure the article is well-structured and uses proper headings, bold text and/or italics for emphasis (don't be shy, the right emphasis on the right words can drive engagement and understanding), bullet points, and formatting where appropriate. You are not allowed to use anything above a heading level 3 (### is ok, ## is not).
Also, keep your paragraphs brief and short to enhance readability. If a paragraph is too long, split it up.

Input Parameters:  
    - **Question (str):** The original "explain like I'm five" question from Reddit.  
    - **Additional Context (str):** Additional context on the question being asked.
    - **Research Notes (str):** Detailed research notes that contain all the necessary information for the article.  
    - **Article Draft (Optional[str]):** A prior draft of the article, if available, to improve upon.  
    - **Editor Feedback (Optional[str]):** Feedback from an editor to enhance the article's quality, if available.  

Output:  
    - A professionally written article in Markdown format.

Ensure the article FLOWS NATURALLY, ANSWERS the given question, and includes all relevant details from the research notes (if some things in the research notes aren't relevant - DO NOT BE AFRAID to discard them).  
"""

class WriterAgent:

    def __init__(self, llm, prompt=DEFAULT_PROMPT):
        # initialization
        self.prompt = prompt
        self.llm = llm

    def write_article(self, state, reddit_question: str, research_notes: str, article_draft: Optional[str] = "", editor_feedback: Optional[str] = ""):
        messages = [
            SystemMessage(content=self.prompt),  # Loading the role
            HumanMessage(content=f"Question: {reddit_question}" + "\n Additional context for the question: " + state["reddit_selftext"]),
            HumanMessage(content=f"Research Notes: {research_notes}"),
        ]
        
        # Add optional article draft and editor feedback
        if article_draft:
            messages.append(HumanMessage(content=f"Article Draft: {article_draft}"))
        if editor_feedback:
            messages.append(HumanMessage(content=f"Editor Feedback: {editor_feedback}"))
        
        response = self.llm.invoke(messages).content
        print(response)

        state['article_draft'] = response

        return state
    

# Should return  the following:
#   "article_content",
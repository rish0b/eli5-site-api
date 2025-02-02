# Basic Imports
from typing import Optional
# LangChain / LangGraph Imports
from langchain_core.messages import HumanMessage, SystemMessage
# Project Imports

# Prompt
DEFAULT_PROMPT = """
You are a professional content writer.  
You specialize in writing viral, simple to understand, informative articles that are clear, concise, and a joy to read.  
Your task is to write a complete article based on the provided inputs.  
You may also receive a previous draft of the article and editor feedback to guide your improvements.  

The article title will be provided separately, you will not include it. Just get right into the article, with a strong hook.

Use Markdown syntax for the article. Ensure the article is well-structured and uses proper headings, bullet points, and formatting where appropriate.  

Input Parameters:  
    - **Question (str):** The original "explain like I'm five" question from Reddit.  
    - **Research Notes (str):** Detailed research notes that contain all the necessary information for the article.  
    - **Article Draft (Optional[str]):** A prior draft of the article, if available, to improve upon.  
    - **Editor Feedback (Optional[str]):** Feedback from an editor to enhance the article's quality, if available.  

Output:  
    - A professionally written article in Markdown format.

Ensure the article flows naturally, answers the given question thoroughly, and includes all relevant details from the research notes.  
"""

class WriterAgent:

    def __init__(self, llm, prompt=DEFAULT_PROMPT):
        # initialization
        self.prompt = prompt
        self.llm = llm

    def write_article(self, state, reddit_question: str, research_notes: str, article_draft: Optional[str] = "", editor_feedback: Optional[str] = ""):
        messages = [
            SystemMessage(content=self.prompt),  # Loading the role
            HumanMessage(content=f"Question: {reddit_question}"),
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
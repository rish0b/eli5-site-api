# Basic Imports
from typing import Optional
import json
from pydantic import BaseModel, Field
# LangChain / LangGraph Imports
from langchain_core.messages import HumanMessage, SystemMessage
# Project Imports

# Prompt
DEFAULT_SYSTEM_PROMPT = f"""
You are an expert in SEO, viral content strategy, and persuasive copywriting. Your job is to generate a highly engaging, click-worthy, and SEO-optimized article_title and a compelling article_subtitle for an ELI5-style blog article. The goal is to maximize organic searchability, social media shares, and reader engagement while staying clear, concise, and intriguing.

Since this blog is already structured as ELI5 explanations, avoid adding "ELI5" in the title unless it makes the title significantly clearer or improves SEO performance. Instead, focus on making the title naturally engaging and curiosity-driven."""

class SEOOutput(BaseModel):
    article_title: str = Field(description="The article title")
    article_subtitle: str = Field(description="The article subtitle")

class SEOAgent:

    def __init__(self, llm, prompt=DEFAULT_SYSTEM_PROMPT):
        # initialization
        self.prompt = prompt
        self.llm = llm

    def generate_seo(self, state):
        USER_PROMPT = f"""
You are optimizing an ELI5-style article for maximum engagement and SEO performance.  

Your task is to generate:
1. **article_title** → A compelling, curiosity-driven title that:
   - Is clear, concise, and engaging.
   - Hooks the reader immediately.
   - Uses conversational, accessible language.
   - Avoids clickbait but still sparks curiosity.
   - Is SEO-friendly with strong keyword placement.
   - Stays within **60-90 characters** for optimal search ranking.
   - **Avoids adding "ELI5" unless necessary for clarity or SEO.**

2. **article_subtitle** → A short, engaging summary that:
   - Provides extra context in **one sentence**.
   - Reinforces the reader’s curiosity.
   - Uses simple, natural language.
   - Stays within **120-150 characters** for readability.

### **ELI5 Question That Inspired the Article:**
{state['reddit_question']}

### **Full Article Content:**
{state['article_content']}

### **Examples of High-Performing Titles for Context**:
1. "Why Do We Feel Lighter in Water? The Science Behind Buoyancy"
2. "If Time Zones Exist, Why Doesn't the Internet Have One Universal Time?"
3. "What Happens If You Never Sleep? A Simple Breakdown"
4. "What If the Moon Disappeared? The Science Behind a Lunar-Free Earth"

### **Now, generate:**
- **article_title:** (Max 90 characters, avoid unnecessary 'ELI5')  
- **article_subtitle:** (Max 150 characters, engaging & informative)
"""
        
        messages = [
            SystemMessage(content=self.prompt),  # Loading the role
            HumanMessage(content=USER_PROMPT)
        ]

        structured_llm = self.llm.with_structured_output(SEOOutput)
        
        response = structured_llm.invoke(messages)

        print(response)

        state['article_title'] = response.article_title
        state['article_subtitle'] = response.article_subtitle

        return state
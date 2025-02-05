# Basic Imports
from datetime import datetime, timezone
# Project Imports
from utils import push_markdown_to_github

class PublishAgent():

    def __init__(self):
        pass

    def publish_article(self, state):

        current_time = datetime.now(timezone.utc)

        # Format it to match "YYYY-MM-DDTHH:MM:SS.sssZ"
        formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        
        article_content = state['article_content']

        markdown_header = f"""---
title: "{state['article_title']}"
date: "{formatted_time}"
template: "post"
draft: false
slug: "/posts/{state['reddit_post_id']}"
category: "{state['reddit_tag']}"
tags:
- "{state['reddit_tag']}"
description: "{state['article_subtitle']}"
---
>👉 [Read the discussion on Reddit](https://www.reddit.com/r/explainlikeimfive/comments/{state['reddit_post_id']})  
>**Post:** {state['reddit_question']}  
>**Author:** u/{state['reddit_user']}  
---
"""
        
        full_markdown = f"{markdown_header}\n{article_content}"

        print(full_markdown)

        push_markdown_to_github(state['reddit_post_id'], full_markdown)

        state['article_url'] = "https://rish0b.github.io/eli5-site-ui/posts/" + state['reddit_post_id']

        return state
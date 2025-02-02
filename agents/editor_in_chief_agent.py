class EditorInChiefAgent():

    def __init__(self):
        pass

    def next_team(self, state):
        if state.get("reddit_question", "") == "":
            return {"next_node": "media"}
        elif state.get("research_notes", "") == "":
            return {"next_node": "research"}
        elif state.get("article_content", "") == "":
            return {"next_node": "writing"}
        elif state.get("article_title", "") == "":
            return {"next_node": "seo"}
        elif state.get("article_url", "") == "":
            return {"next_node": "publish"}
        return {"next_node": "END"} 
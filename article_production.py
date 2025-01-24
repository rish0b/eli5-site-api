# LangChain / LangGraph Imports
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
# Project Imports
from agents.research_team.research_agent import ResearchAgent
from agents.writing_team.writer_agent import WriterAgent
from agents.editor_in_chief_agent import EditorInChiefAgent
from agents.writing_team.editor_agent import EditorAgent
from states.state import ArticleState



def article_production(llm):

    def initialize_agents():
        return {
            "editor_in_chief_agent" : EditorInChiefAgent(llm),
            "research_agent"        : ResearchAgent(llm),
            "writer_agent"          : WriterAgent(llm),
            "editor_agent"          : EditorAgent(llm)
        }

    # A S S E M B L E   T E A M

    team = initialize_agents()
    workflow = StateGraph(ArticleState)

    # N O D E S

    # Editor-In-Chief Agent
    workflow.add_node("editor_in_chief", team["editor_in_chief_agent"].next_team)

    # Research Agent
    workflow.add_node("research", team["research_agent"].do_research)

    # Writer Agent
    workflow.add_node("writing", lambda state: team["writer_agent"].write_article(
        state=              state,
        reddit_question=    state["reddit_question"],
        research_notes=     state["research_notes"],
        article_draft=      state.get("article_draft", ""),
        editor_feedback=    state.get("editor_feedback", "")
    ))

    def keep_revising(state):
        if state["revision_number"] >= state["max_revisions"]:
            return "capture_writer_final"
        return "editor"
    
    def capture_writer_final(state):
        state['article_content'] = state['article_draft']
        print(state['article_content'])
        return state 
    workflow.add_node("capture_writer_final", capture_writer_final)

    # Editor Agent
    workflow.add_node("editor", lambda state : team["editor_agent"].critique(
        state=              state
    ))

    # Publisher Agent (who in turn has a workflow with the github and reddit agents/tools)


    # E D G E S

    # Start
    workflow.set_entry_point("editor_in_chief")

    # Editor in Chief
    workflow.add_conditional_edges("editor_in_chief", lambda state: state["next_node"])

    # Research
    workflow.add_edge("research", "editor_in_chief")

    # Writing
    workflow.add_conditional_edges("writing", keep_revising, { "capture_writer_final" : "capture_writer_final", "editor" : "editor" })
    workflow.add_edge("editor", "writing")
    workflow.add_edge("capture_writer_final", "editor_in_chief")

    workflow.set_finish_point("editor_in_chief")   # temporary

    # Publishing


    # G R A P H
    return workflow
# Basic Imports
from typing import TypedDict, Annotated
# LangChain / LangGraph Imports
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, ToolMessage
# Project Imports
from ..states.state import MessageState



# Tool Calling Agent Definition
class ToolCallingAgent:

    def __init__(self, llm, tools, prompt="", state=None):
        # initialization
        self.prompt = prompt
        self.state = state or {"messages": []}
        # graph init
        graph = StateGraph(state)
        graph.add_node("llm", self.call_llm)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        # llm & tools init
        self.tools = {t.name: t for t in tools}
        self.llm = llm.bind_tools(tools)

    # Check if requested tool call exists
    def exists_action(self):
        result = self.state['messages'][-1]
        return len(result.tool_calls) > 0

    # Go to llm
    def call_llm(self):
        messages = self.state['messages']
        if self.prompt:
            messages = [SystemMessage(content=self.prompt)] + messages
        message = self.llm.invoke(messages)
        return {'messages': [message]}

    # Use requested tool
    def take_action(self):
        tool_calls = self.state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}
from typing import TypedDict, Annotated, Literal
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

@tool
def weather(query: str):
    """今日の天気予報をお知らせします"""
    return ["今日の天気は晴れです"]

class State(TypedDict):
    messages: Annotated[list[str], add_messages]

def call_model (state: State, config: RunnableConfig):
    messages = state["messages"]
    response = model.invoke(messages, config)
    return {"messages": response}

def should_continue(state: State) -> Literal["__end__", "tools"]:
    messages = state[ "messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return END 
    else:
        return "tools"

tools = [weather]

model = ChatOpenAI(model="gpt-4o-2024-08-06")
model = model.bind_tools(tools)

graph = StateGraph(State)
tool_node = ToolNode(tools)

graph.add_node("agent", call_model)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")
compiled = graph.compile()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from IPython.display import Image, display
# from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import ToolMessage
from dotenv import load_dotenv
from typing import Annotated, List,Literal
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage,AIMessage

import os
import json 
load_dotenv()
os.environ["TAVILY_API_KEY"] = os.environ.get("TAVILY_API_KEY")
google_api_key = os.environ.get("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest", google_api_key=google_api_key)

# print(llm.invoke("Hello, how are you?"))


class State(TypedDict):
    messages : Annotated[List,add_messages]



graph_builder = StateGraph(State)

def chatbot(state:State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


graph = graph_builder.compile()

from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass


# while True:
#     user_input = input("User: ")
#     if user_input.lower() in ["quit","q","exit"]:
#         print("Goodbye Bro I am going!")
#         break
#     for event in graph.stream({"messages": ("user", user_input)}):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)

travily_tool = TavilySearchResults(max_results=5)
print(travily_tool.description)
tools = [travily_tool]

# search_query = "Tell me whether in Faisalabad,pakistan right now.is it raining? "
# for response in travily_tool.invoke(search_query):
#     print(response["content"], end="\n\n" + "*" * 50 + "\n\n")

llm_with_tools = llm.bind_tools(tools)
def ToolEnabledChatbot(state:State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}
# tool_node = ToolNode(tools)
# graph_builder.add_node("tool_node", tool_node)

class BasicToolNode:

    def __init__(self, tools:list)->None:
        self.tools_by_name = {tool.name: tool for tool in tools}
    def __call__(self,inputs:dict):
        if messages := inputs.get("messages",[]):
            message = messages[-1]
        else:
            raise ValueError("No messages found in inputs")
        output = []
        for tool_call in message.tool_calls:
            print("Calling  Travily Tool")
            tool_result = self.tools_by_name["tavily_search_results_json"].invoke(
                tool_call["args"]
            )
            # print(tool_call)
            output.append(
                ToolMessage(
                    content = json.dumps(tool_result),
                    name = tool_call["name"],
                    tool_call_id = tool_call["id"]
                )
            )

        return {"messages": output}
    

graph_builder_with_tools = StateGraph(State)

graph_builder_with_tools.add_node("ToolEnabledChatbot", ToolEnabledChatbot)

# create a tool node

graph_builder_with_tools.add_node("tools", BasicToolNode(tools = [travily_tool]))

# BOTH NODES ARE DEFINED NOW WE NEED TO DEFINE THE CONDITIONal edges

def route_tools(state: State) -> Literal["tools", "__end__"]:
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"

graph_builder_with_tools.add_conditional_edges(
    "ToolEnabledChatbot",
    route_tools,
    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {"tools": "tools", "__end__": "__end__"},
)


graph_builder_with_tools.add_edge("tools", "ToolEnabledChatbot")
graph_builder_with_tools.add_edge(START, "ToolEnabledChatbot")
Toolgraph = graph_builder_with_tools.compile()


try:
    display(Image(Toolgraph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass







while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in Toolgraph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            if isinstance(value["messages"][-1], AIMessage):
                print("Assistant:", value["messages"][-1].content)
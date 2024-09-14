from dotenv import load_dotenv
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
#import the API keys

load_dotenv()

anthropic_api_key = os.environ.get("anthropic_api_key")
os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "LangGraph Tutorial"


# The first thing you do when you define a graph is define the State of the graph. 
# The State consists of the schema of the graph as well as reducer functions 
# which specify how to apply updates to the state. In our example State is a TypedDict with a single key: messages.
#  The messages key is annotated with the add_messages reducer function, 
# which tells LangGraph to append new messages to the existing list, rather than overwriting it. 
# State keys without an annotation will be overwritten by each update, storing the most recent value. 
# Check out this conceptual guide to learn more about state, reducers and other low-level concepts.

class State(TypedDict):
    # consist of Schema of graph as well as reducer functions

    messages : Annotated[list, add_messages]

graph_builder = StateGraph(State)


from langchain_groq import ChatGroq

# llm = ChatGroq(api_key=GROQ_API_KEY, model="mixtral-8x7b-32768")
llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest")

# print(llm.invoke("Hello, how are you?"))
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

# The graph is now ready to be used.

# from IPython.display import Image, display

# try:
#     display(Image(graph.get_graph().draw_mermaid_png()))
#     # save the image as well
#     graph.get_graph().draw_mermaid_png().save("graph.png")
# except Exception:
#     # This requires some extra dependencies and is optional
#     pass


while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": ("user", user_input)}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


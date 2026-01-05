from typing_extensions import TypedDict, List
from langgraph.graph.message import add_messages
from typing import Annotated


class State(TypedDict):
    """
    Docstring for State
    Stores state information for every node in the graph

    """
    #reducer is used to append the state value of messages to append rather than append
    messages : Annotated[List, add_messages]
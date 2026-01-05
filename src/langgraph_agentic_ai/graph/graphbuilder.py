from langgraph.graph import StateGraph, START, END
from src.langgraph_agentic_ai.state.state import State
from src.langgraph_agentic_ai.nodes.basic_chatbot_node import Basic_Chatbot_Node


class GraphBuilder:
    def __init__(self, model):
        self.llm=model
        self.graphbuilder=StateGraph(State)

    def build_basic_chatbot_graph(self):
        """
        Docstring for build_basic_chatbot_graph
        
        :param self: Description
        This method is used to build basic chatbot graph, which is linked with start and end
        of the graph with chatbot node
        """
        self.basic_chatbot_node = Basic_Chatbot_Node(model=self.llm)
        if self.graphbuilder:
            self.graphbuilder.add_node("chatbot",self.basic_chatbot_node.process)
            self.graphbuilder.add_edge(START,"chatbot")
            self.graphbuilder.add_edge("chatbot",END)
        
        
    def setup_graph(self, usecase:str):
        if usecase=="Basic Chatbot":
            self.build_basic_chatbot_graph()
        return self.graphbuilder.compile()
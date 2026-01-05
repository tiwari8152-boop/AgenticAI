from langgraph.graph import StateGraph, START, END
from src.langgraph_agentic_ai.state.state import State
from src.langgraph_agentic_ai.nodes.basic_chatbot_node import Basic_Chatbot_Node
from src.langgraph_agentic_ai.nodes.chatbot_with_tools_node import Chatbot_With_Tools_Node
from src.langgraph_agentic_ai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition, ToolNode


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

    def chatbot_with_tools(self):
        """
        Docstring for chatbot_with_tools
        
        :param self: Description
        Build graph with a tool and toolnode
        """
        print("entering in chatbot with tools")
        # Define Tool and Tool Node
        tools = get_tools()
        tool_node = create_tool_node(tools)
        
        #Define the llm
        llm = self.llm
        #Define the chatbot node
        obj_chatbot_with_tool_node = Chatbot_With_Tools_Node(model=llm)
        chatbot_node = obj_chatbot_with_tool_node.create_chatbot(tools)
        # Add nodes
        self.graphbuilder.add_node("chatbot",chatbot_node)
        self.graphbuilder.add_node("tools", tool_node)
        self.graphbuilder.add_edge(START, "chatbot")
        self.graphbuilder.add_conditional_edges("chatbot", tools_condition)
        self.graphbuilder.add_edge("tools","chatbot")
        
    def setup_graph(self, usecase:str):
        if usecase=="Basic Chatbot":
            self.build_basic_chatbot_graph()
        if usecase=="Chat With Web":
            self.chatbot_with_tools()
        return self.graphbuilder.compile()
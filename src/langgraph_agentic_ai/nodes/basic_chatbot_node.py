from src.langgraph_agentic_ai.state.state import State

class Basic_Chatbot_Node:
    """
    Docstring for Basic_Chatbot_Node
    This node take the llm model, along with user message
    Returns response
    """
    def __init__(self, model):
        self.llm = model

    def process(self, state:State)-> dict:
        messages = state["messages"]
        response = self.llm.invoke(messages)
        return {"messages": response}
    


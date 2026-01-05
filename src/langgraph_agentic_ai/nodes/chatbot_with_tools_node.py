from src.langgraph_agentic_ai.state.state import State

class Chatbot_With_Tools_Node:
    def __init__(self, model):
        self.llm = model

    def process(self, state:State)->dict:
        """
        Docstring for process
    
        :param self: Description
        :param state: Description
        :type state: State
        :return: Description
        :rtype: dict
        processes last input from user and returns tool response
        """
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role" : "user", "content":user_input}])
        tools_response=f"Tool Integration for '{user_input}'"
        return {"messages":[llm_response, tools_response]}

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function
        
        :param self: Description
        :param tools: Description
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state:State):
            """
            Chatbot logic for processing the input state and returning a response
            
            :param state: Description
            :type state: State
            """
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        return chatbot_node
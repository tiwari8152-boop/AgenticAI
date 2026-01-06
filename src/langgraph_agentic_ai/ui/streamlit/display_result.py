import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        if self.usecase == "Basic Chatbot":
            for event in self.graph.stream({'messages':("user", self.user_message)}):
                print(event.values())
                for value in event.values():
                    with st.chat_message("user"):
                        st.write(self.user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)
        elif self.usecase == "Chat With Web":
            initial_state = {"messages": [self.user_message]}
            res = self.graph.invoke(initial_state)
            for msg in res["messages"]:
                if type(msg)==HumanMessage:
                    with st.chat_message("user"):
                        st.write(msg.content)
                elif type(msg)==ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool call start")
                        st.write(msg.content)
                        st.write("Tool call end")
                elif type(msg)==AIMessage and msg.content:
                    with st.chat_message("assistant"):
                        st.write(msg.content)
        elif self.usecase=="AI News":
            frequency=self.user_message
            with st.spinner("fetching and summarizing news"):
                result=self.graph.invoke({"messages":frequency})
                try:
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH,'r') as file:
                        markdown_content = file.read()
                    st.markdown(markdown_content, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f'News not generated:{e}')
                    return


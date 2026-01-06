import streamlit as st
import os
from src.langgraph_agentic_ai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}
    
    def load_streamlit_ui(self):
        # design page title
        st.set_page_config(page_title="*** "+self.config.get_page_title()+" ***", layout="wide")
        st.header("*** "+self.config.get_page_title()+" ***")
        st.session_state.IsFetchButtonClicked=False
        # design sidebar
        with st.sidebar:
            # get data from Config class
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            # select llm
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)
            # if selected option is Groq then list Groq models
            if self.user_controls["selected_llm"]=="Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"]=st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"]=st.session_state["GROQ_API_KEY"]=st.text_input("API Key", type="password")
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter correct API Key")
            
            self.user_controls["selected_usecase"]=st.selectbox("Select Usecase", usecase_options)
            # If Chat With Web is selected, show Tavily API Key input
            if self.user_controls["selected_usecase"] == "Chat With Web" or self.user_controls["selected_usecase"] == "AI News":
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("Tavily API Key", type="password")
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your Tavily API Key for web search.")

            if self.user_controls["selected_usecase"]=="AI News":
                st.subheader("AI News Explorer !")
                with st.sidebar:
                    time_frame = st.selectbox("Select Timeframe",
                                              ["Daily", "Weekly", "Monthly"],
                                              index=0)
                if st.button("Fetch latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked=True
                    st.session_state["timeframe"]=time_frame
        return self.user_controls




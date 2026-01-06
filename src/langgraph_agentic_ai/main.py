import streamlit as st
from src.langgraph_agentic_ai.ui.streamlit.loadui import LoadStreamlitUI
from src.langgraph_agentic_ai.ui.streamlit.display_result import DisplayResultStreamlit
from src.langgraph_agentic_ai.LLMs.groq_llm import GroqLLM
from src.langgraph_agentic_ai.graph.graphbuilder import GraphBuilder
from src.langgraph_agentic_ai.state.state import State


def load_langraph_agenticai_app():
    """
    Docstring for load_langraph_agenticai_app

    Loads and runs the app UI, it initializes the UI, handle user input,
    fetches all the user input selected.
    """
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    if not user_input:
        st.error("Error: failed to get user input")
        return
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    else:
        user_message =st.chat_input("Enter your message")
    if user_message:
        try:
            config_llm = GroqLLM(user_input)
            groq_llm = config_llm.get_llm_model()
            if not groq_llm:
                st.error("Error: Model initialization failed !")
                return
            usecase = user_input.get("selected_usecase")
            if not usecase:
                st.error("Error: Could not fetch use case")
                return
            graph_builder= GraphBuilder(groq_llm)
            graph = graph_builder.setup_graph(usecase)
            try:
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: inside display: {e}")
                return
        except Exception as e:
            st.error(f"Error: Graph did not load {e}")
            return
    
        
        

    


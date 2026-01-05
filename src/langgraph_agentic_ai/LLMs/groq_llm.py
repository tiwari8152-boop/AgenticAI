import streamlit as st
from langchain_groq import ChatGroq
import os

class GroqLLM:
    def __init__(self, user_controls):
        self.user_controls_input = user_controls
        print(self.user_controls_input)

    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input["GROQ_API_KEY"]
            print(groq_api_key)
            selected_model = self.user_controls_input["selected_groq_model"]
            if groq_api_key=='':
                st.error("Groq API Key not found !")
                return
            if not selected_model:
                st.error("Model not selected !")
                return
            try:
                groq_model=ChatGroq(api_key=groq_api_key, model=selected_model)
                return groq_model
            except Exception as e:
                st.error(f"Unable to activate groq model {e}")
        except Exception as e:
            st.error(f"Error: Unable to fetch Groq Model {e}!")
            raise ValueError(f"Exception in get_llm_model: {e}")

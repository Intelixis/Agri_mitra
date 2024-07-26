import streamlit as st

def session_management():
    # Initialize session state variables
    if "text_received" not in st.session_state:
        st.session_state.text_received = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0
    if "language" not in st.session_state:
        st.session_state.language = "English"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "display_chat" not in st.session_state:
        st.session_state.display_chat = False
    if "history" not in st.session_state:
        st.session_state.history = []
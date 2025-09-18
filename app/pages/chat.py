from datetime import datetime
import streamlit as st
from app.styling import chat_interface
from app.components import display_bot_message, display_user_message
from core.helpers import handle_chat_send
from core.init_utils import initialize_agent

def chat_tab():
    """Main chat interface."""
    # Initialize username if not set
    if "username" not in st.session_state:
        st.session_state.username = "Guest"

    # Chat header
    st.markdown(f"""
    <div class="chat-header">
        <h1>Memory-Enhanced Chat Assistant</h1>
        <p>Chatting as: <strong>{st.session_state.username}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "agent" not in st.session_state:
        st.session_state.agent, st.session_state.memory = initialize_agent()
        if st.session_state.agent is None:
            st.error("Failed to initialize the chat system. Please check your configuration.")
            return

    # Display chat messages
    for message in st.session_state.messages:
        if message["is_user"]:
            display_user_message(message["content"], message["timestamp"])
        else:
            display_bot_message(message["content"], message["timestamp"])

    # Chat input
    st.markdown("---")
    col1, col2 = st.columns([4, 1])

    with col1:
        st.text_input(
            "Type your message here...",
            key="user_input",
            placeholder="Ask me anything or tell me about yourself!",
            label_visibility="collapsed"
        )

    with col2:
        st.button("Send 📤", use_container_width=True, on_click=handle_chat_send)

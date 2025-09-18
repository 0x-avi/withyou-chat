import streamlit as st

def display_user_message(message: str, timestamp: str):
    """Display user message on the right side."""
    st.markdown(f"""
    <div class="user-message">
        <div class="user-message-content">
            <div class="user-avatar">👤</div>
            <div>
                <div class="user-bubble">{message}</div>
                <div class="timestamp">{timestamp}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_bot_message(message: str, timestamp: str):
    """Display bot message on the left side."""
    st.markdown(f"""
    <div class="bot-message">
        <div class="bot-message-content">
            <div class="bot-avatar">🤖</div>
            <div>
                <div class="bot-bubble">{message}</div>
                <div class="timestamp bot-timestamp">{timestamp}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
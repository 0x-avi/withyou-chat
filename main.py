import streamlit as st
import os
from app.pages.chat import chat_tab
from app.pages.username import username_tab
from app.styling import *

st.set_page_config(
    page_title="CBT based therapist v1",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Configure environment (you should use st.secrets in production)
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY", "your-api-key-here")

def main():
    """Main application."""
    # Create tabs
    tab1, tab2 , tab3= st.tabs(["💬 Chat", "👤 Username","Memories"])
    
    with tab1:
        chat_tab()
    
    with tab2:
        username_tab()
       # Sidebar with memory information
    with tab3:
        st.title(f"💾 {st.session_state.username}'s Memory")

        if st.button("View My Memories"):
            try:
                memories = st.session_state.agent.memory_tools.get_all_memories(
                    user_id=st.session_state.username
                )
                st.text_area("Your Stored Memories:", memories, height=300)
            except Exception as e:
                st.error(f"Error: {str(e)}")

        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.success("Chat history cleared!")

        # Chat statistics
        if st.session_state.messages:
            user_msg_count = len([m for m in st.session_state.messages if m["is_user"]])
            bot_msg_count = len([m for m in st.session_state.messages if not m["is_user"]])
            st.metric("Your Messages", user_msg_count)
            st.metric("Bot Responses", bot_msg_count)

    st.markdown(chat_interface, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
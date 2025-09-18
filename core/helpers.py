from datetime import datetime
import streamlit as st


def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def handle_chat_send():
    if st.session_state.user_input.strip():
        current_time = datetime.now().strftime("%H:%M")

        # Add user message
        st.session_state.messages.append({
            "content": st.session_state.user_input,
            "is_user": True,
            "timestamp": current_time
        })

        # Add temporary bot "typing…" message
        temp_msg = {
            "content": "🤖 Typing...",
            "is_user": False,
            "timestamp": datetime.now().strftime("%H:%M"),
            "temp": True
        }
        st.session_state.messages.append(temp_msg)

        user_text = st.session_state.user_input
        st.session_state.user_input = ""  # clear input immediately

        try:
            # Call the agent (no spinner, we already show typing msg)
            response = st.session_state.agent.forward(
                user_input=user_text,
                user_id=st.session_state.username
            )
            bot_response = response.response if hasattr(response, 'response') else str(response)
        except Exception as e:
            bot_response = f"Sorry, I encountered an error: {str(e)}"

        # Remove the temp message
        st.session_state.messages = [m for m in st.session_state.messages if not m.get("temp")]

        # Add actual bot response
        st.session_state.messages.append({
            "content": bot_response,
            "is_user": False,
            "timestamp": datetime.now().strftime("%H:%M")
        })

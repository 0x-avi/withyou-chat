import streamlit as st

def username_tab():
    """Username setting tab."""
    st.title("👤 Set Your Username")
    
    # Username input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        new_username = st.text_input(
            "Enter your username:",
            value=st.session_state.username,
            placeholder="e.g., Alice, John, etc.",
            help="This username will be used to personalize your chat experience"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("Update Username", type="primary"):
            if new_username.strip():
                st.session_state.username = new_username.strip()
                st.success(f"Username updated to: {st.session_state.username}")
                st.rerun()
    
    # Display current username
    st.info(f"Current username: **{st.session_state.username}**")
    
    st.markdown("---")
    st.markdown("""
    ### How it works:
    - Your username personalizes your chat experience
    - The AI will remember conversations tied to your username  
    - You can change your username anytime
    - Each username has its own memory and conversation history
    """)
import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from mem0 import AsyncMemory
from Agent import Therapist
from Memory import MemOps
import dspy

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AI Therapist Chat",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'therapist' not in st.session_state:
    st.session_state.therapist = None

if 'mem_tools' not in st.session_state:
    st.session_state.mem_tools = None

if 'initialized' not in st.session_state:
    st.session_state.initialized = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = 'guest'

if 'all_memories' not in st.session_state:
    st.session_state.all_memories = []

if 'dspy_configured' not in st.session_state:
    st.session_state.dspy_configured = False

async def initialize_therapist():
    """Initialize the therapist and memory tools."""
    config = {
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": "test",
                "url": os.environ['QDRANT_URL'],
                "api_key": os.environ['QDRANT_API_KEY'],
            }
        },
        "llm": {
            "provider": "openai",
            "config": {
                "model": "gpt-5-nano-2025-08-07",
                "temperature": 0.2,
                "max_tokens": 2000,
            }
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small"
            }
        }
    }
    
    memory = await AsyncMemory.from_config(config)
    mem_tools = MemOps(memory)
    mem_tools.set_user_id(st.session_state.current_user)
    
    # Configure DSPy only once per session
    if not st.session_state.dspy_configured:
        lm = dspy.LM('openai/gpt-5-nano-2025-08-07', temperature=1.0, max_tokens=16000)
        dspy.configure(lm=lm)
        st.session_state.dspy_configured = True
    
    therapist = Therapist(memory=memory)
    
    return therapist, mem_tools

async def get_chat_response(user_query, therapist, mem_tools):
    """Get response from the therapist without adding memories yet."""
    memories = await mem_tools.search_for_memories(user_query)
    answer = await therapist.aforward(f'{memories}\n{user_query}')
    return answer

async def add_user_memory(user_query, mem_tools):
    """Add user query to memory after response is generated."""
    added_memories = await mem_tools.add_memory(user_query)
    return added_memories

async def load_all_memories(mem_tools):
    """Load all memories for the current user."""
    try:
        memories = await mem_tools.get_all_memories()
        # Handle different return structures
        if isinstance(memories, dict) and 'results' in memories:
            return memories['results']
        elif isinstance(memories, list):
            return memories
        else:
            return [memories] if memories else []
    except Exception as e:
        st.error(f"Error loading memories: {str(e)}")
        return []

def run_async(coro):
    """Helper function to run async functions in Streamlit."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

# Sidebar for user management and memory viewing
with st.sidebar:
    st.title("🧠 AI Therapist")
    
    # User management section
    st.subheader("👤 User Management")
    new_username = st.text_input("Username:", value=st.session_state.current_user)
    
    if st.button("Set Username") or new_username != st.session_state.current_user:
        if new_username.strip():
            st.session_state.current_user = new_username.strip()
            st.session_state.initialized = False  # Re-initialize with new user
            st.session_state.messages = []  # Clear chat history
            # Don't reset dspy_configured - keep it configured
            st.success(f"Username set to: {st.session_state.current_user}")
            st.rerun()
    
    st.write(f"Current user: **{st.session_state.current_user}**")
    
    # Memory management section
    st.subheader("🧠 Memory Management")
    
    if st.button("Load All Memories"):
        if st.session_state.initialized and st.session_state.mem_tools:
            with st.spinner("Loading memories..."):
                try:
                    memories = run_async(load_all_memories(st.session_state.mem_tools))
                    st.session_state.all_memories = memories
                    if memories:
                        st.success(f"Loaded {len(memories)} memories!")
                    else:
                        st.info("No memories found for this user.")
                except Exception as e:
                    st.error(f"Failed to load memories: {str(e)}")
        else:
            st.warning("Please initialize the chat first by sending a message.")
    
    # Display memories
    if st.session_state.all_memories:
        st.subheader("📝 Your Memories")
        if len(st.session_state.all_memories) == 0:
            st.info("No memories found for this user.")
        else:
            for i, memory in enumerate(st.session_state.all_memories):
                with st.expander(f"Memory {i+1}", expanded=False):
                    if isinstance(memory, dict):
                        # Handle mem0 memory structure
                        st.write(f"**ID:** {memory.get('id', 'N/A')}")
                        st.write(f"**Memory:** {memory.get('memory', memory.get('text', 'N/A'))}")
                        st.write(f"**Score:** {memory.get('score', 'N/A')}")
                        st.write(f"**Created:** {memory.get('created_at', memory.get('timestamp', 'N/A'))}")
                        
                        # Show metadata if available
                        if 'metadata' in memory:
                            st.write(f"**Metadata:** {memory['metadata']}")
                    else:
                        st.write(f"**Content:** {str(memory)}")
    else:
        if st.session_state.initialized:
            st.info("Click 'Load All Memories' to view your conversation history.")
    
    if st.button("Clear Memories View"):
        st.session_state.all_memories = []
        st.rerun()

# Main chat interface
st.title("💬 Chat with AI Therapist")

# Initialize therapist if not done
if not st.session_state.initialized:
    with st.spinner("Initializing AI Therapist..."):
        try:
            therapist, mem_tools = run_async(initialize_therapist())
            st.session_state.therapist = therapist
            st.session_state.mem_tools = mem_tools
            st.session_state.initialized = True
            st.success("AI Therapist initialized successfully!")
        except Exception as e:
            st.error(f"Error initializing therapist: {str(e)}")
            st.stop()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Get response first
                response = run_async(get_chat_response(
                    prompt, 
                    st.session_state.therapist, 
                    st.session_state.mem_tools
                ))
                
                # Display the response
                st.markdown(response)
                
                # Add response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Add memory after response is shown (in background)
                added_memories = run_async(add_user_memory(prompt, st.session_state.mem_tools))
                    
                if added_memories['results']!=None:
                    with st.expander("Memory Update"):
                        st.success("Conversation saved to memory!")
                        st.json(added_memories)
                
            except Exception as e:
                error_msg = f"Error generating response: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")

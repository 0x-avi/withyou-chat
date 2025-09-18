import streamlit as st
from mem0 import Memory
import dspy
from core.agent import MemoryReActAgent

# Initialize Mem0 memory system
@st.cache_resource
def initialize_memory():
    config = {
        "llm": {
            "provider": "openai",
            "config": {
                "model": "gpt-4o-mini",
            }
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small"
            }
        }
    }
    return Memory.from_config(config)

@st.cache_resource
def initialize_agent():
    """Initialize the memory agent."""
    try:
        # Configure DSPy
        lm = dspy.LM(model='openai/gpt-4o-mini')
        dspy.configure(lm=lm)
        
        # Initialize memory system
        memory = initialize_memory()
        
        # Create agent
        agent = MemoryReActAgent(memory)
        return agent, memory
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return None, None
    



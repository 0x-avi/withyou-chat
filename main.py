import os
import streamlit as st
from mem0 import Memory
from dotenv import load_dotenv
import dspy
import datetime
import time

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CBT Memory-Enhanced Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Memory configuration
config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "gemma3:4b",
        },
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "multi-qa-MiniLM-L6-cos-v1",
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "cbt_therapy",
            "embedding_model_dims": 384,
        },
    },
}

class MemoryTools:
    """Tools for interacting with the Mem0 memory system."""

    def __init__(self, memory: Memory):
        self.memory = memory

    def store_memory(self, content: str, user_id: str = "default_user") -> str:
        """Store information in memory."""
        try:
            self.memory.add(content, user_id=user_id)
            return f"Stored memory: {content}"
        except Exception as e:
            return f"Error storing memory: {str(e)}"

    def search_memories(self, query: str, user_id: str = "default_user", limit: int = 5) -> str:
        """Search for relevant memories."""
        try:
            results = self.memory.search(query, user_id=user_id, limit=limit)
            if not results:
                return "No relevant memories found."

            memory_text = "Relevant memories found:\n"
            for i, result in enumerate(results["results"]):
                memory_text += f"{i+1}. {result['memory']}\n"
            return memory_text
        except Exception as e:
            return f"Error searching memories: {str(e)}"

    def get_all_memories(self, user_id: str = "default_user") -> str:
        """Get all memories for a user."""
        try:
            results = self.memory.get_all(user_id=user_id)
            if not results:
                return "No memories found for this user."

            memory_text = "All memories for user:\n"
            for i, result in enumerate(results["results"]):
                memory_text += f"{i+1}. {result['memory']}\n"
            return memory_text
        except Exception as e:
            return f"Error retrieving memories: {str(e)}"

def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class CBTMemoryQA(dspy.Signature):
    """
    You're a CBT (Cognitive Behavioral Therapy) assistant with access to memory methods.
    Your role is to help users identify thought patterns, emotions, and behaviors while maintaining
    a therapeutic, empathetic approach. Always store important information about the user's
    thoughts, feelings, and patterns for continuity in therapy sessions.
    
    Key CBT principles to follow:
    - Help identify negative thought patterns and cognitive distortions
    - Encourage behavioral activation and positive coping strategies
    - Track mood patterns and triggers
    - Provide psychoeducation about CBT concepts
    - Maintain therapeutic boundaries and suggest professional help when appropriate
    """
    user_input: str = dspy.InputField()
    response: str = dspy.OutputField()

class CBTMemoryReActAgent(dspy.Module):
    """A CBT-focused ReAct agent enhanced with Mem0 memory capabilities."""

    def __init__(self, memory: Memory):
        super().__init__()
        self.memory_tools = MemoryTools(memory)

        # Create tools list for ReAct
        self.tools = [
            self.memory_tools.store_memory,
            self.memory_tools.search_memories,
            self.memory_tools.get_all_memories,
            get_current_time,
            self.track_mood,
            self.identify_thought_patterns,
            self.suggest_coping_strategies,
            self.set_therapy_goal,
            self.track_progress,
        ]

        # Initialize ReAct with our tools
        self.react = dspy.ReAct(
            signature=CBTMemoryQA,
            tools=self.tools,
            max_iters=6
        )

    def forward(self, user_input: str):
        """Process user input with CBT-aware reasoning."""
        return self.react(user_input=user_input)

    def track_mood(self, mood: str, intensity: int, triggers: str = "", user_id: str = "default_user") -> str:
        """Track user's mood and associated triggers."""
        mood_entry = f"MOOD TRACKING - Date: {get_current_time()}, Mood: {mood}, Intensity: {intensity}/10, Triggers: {triggers}"
        return self.memory_tools.store_memory(mood_entry, user_id=user_id)

    def identify_thought_patterns(self, thought: str, pattern_type: str, user_id: str = "default_user") -> str:
        """Identify and store negative thought patterns or cognitive distortions."""
        pattern_entry = f"THOUGHT PATTERN - Type: {pattern_type}, Thought: '{thought}', Date: {get_current_time()}"
        return self.memory_tools.store_memory(pattern_entry, user_id=user_id)

    def suggest_coping_strategies(self, situation: str, user_id: str = "default_user") -> str:
        """Suggest and store coping strategies for specific situations."""
        # First, search for previous coping strategies that worked
        previous_strategies = self.memory_tools.search_memories(
            f"coping strategy {situation}", user_id=user_id
        )
        
        strategy_entry = f"COPING STRATEGY - Situation: {situation}, Date: {get_current_time()}"
        self.memory_tools.store_memory(strategy_entry, user_id=user_id)
        
        return f"Recorded coping strategy discussion for: {situation}. {previous_strategies}"

    def set_therapy_goal(self, goal: str, timeframe: str = "", user_id: str = "default_user") -> str:
        """Set and store therapy goals."""
        goal_entry = f"THERAPY GOAL - Goal: {goal}, Timeframe: {timeframe}, Set on: {get_current_time()}"
        return self.memory_tools.store_memory(goal_entry, user_id=user_id)

    def track_progress(self, goal_area: str, progress_notes: str, user_id: str = "default_user") -> str:
        """Track progress toward therapy goals."""
        progress_entry = f"PROGRESS UPDATE - Area: {goal_area}, Notes: {progress_notes}, Date: {get_current_time()}"
        return self.memory_tools.store_memory(progress_entry, user_id=user_id)

@st.cache_resource
def initialize_agent():
    """Initialize the CBT agent with caching."""
    try:
        # Configure DSPy
        lm = dspy.LM(model='groq/llama-3.1-8b-instant')
        dspy.configure(lm=lm)

        # Initialize memory system
        memory = Memory.from_config(config)

        # Create our agent
        agent = CBTMemoryReActAgent(memory)
        return agent, None
    except Exception as e:
        return None, str(e)

def main():
    """Main Streamlit application."""
    
    st.title("🧠 CBT Memory-Enhanced Assistant")
    st.markdown("*A therapeutic assistant that remembers your journey*")
    
    # Sidebar for user information and controls
    with st.sidebar:
        st.header("🔧 Session Controls")
        
        # User ID input
        user_id = st.text_input("User ID", value="demo_user", help="Enter a unique identifier for your session")
        
        st.header("📊 Quick Actions")
        
        # Mood tracking quick form
        with st.expander("🎭 Quick Mood Check"):
            mood = st.selectbox("How are you feeling?", 
                              ["Happy", "Sad", "Anxious", "Angry", "Calm", "Stressed", "Confused", "Excited"])
            intensity = st.slider("Intensity (1-10)", 1, 10, 5)
            triggers = st.text_input("What triggered this mood?")
            
            if st.button("Track Mood"):
                st.session_state.mood_tracked = {
                    "mood": mood,
                    "intensity": intensity,
                    "triggers": triggers
                }
        
        # Memory search
        with st.expander("🔍 Search Memories"):
            search_query = st.text_input("Search your session history:")
            if st.button("Search") and search_query:
                st.session_state.search_query = search_query

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent_initialized" not in st.session_state:
        st.session_state.agent_initialized = False

    # Initialize agent
    if not st.session_state.agent_initialized:
        with st.spinner("Initializing CBT Assistant..."):
            agent, error = initialize_agent()
            if agent:
                st.session_state.agent = agent
                st.session_state.agent_initialized = True
                st.success("CBT Assistant ready!")
            else:
                st.error(f"Failed to initialize agent: {error}")
                st.stop()

    # Display sample questions
    st.header("💭 Sample CBT-focused Questions")
    
    col1, col2, col3 = st.columns(3)
    
    sample_questions = [
        "I've been feeling anxious about work presentations. Can you help me understand this pattern?",
        "I keep thinking 'I'm not good enough' when I make mistakes. Is this a cognitive distortion?",
        "I want to set a goal to manage my stress better. Can you help me create a plan?",
        "I had a panic attack yesterday. Can you help me identify what triggered it?",
        "I've been avoiding social situations. How can I work on this behaviorally?",
        "Can you help me track my mood patterns over time?",
        "I feel overwhelmed by negative thoughts. What coping strategies can we explore?",
        "How can I challenge my catastrophic thinking?",
        "I want to work on my sleep hygiene as part of my mental health routine."
    ]
    
    with col1:
        for i in range(0, len(sample_questions), 3):
            if st.button(f"💬 {sample_questions[i][:50]}...", key=f"q1_{i}"):
                st.session_state.selected_question = sample_questions[i]
    
    with col2:
        for i in range(1, len(sample_questions), 3):
            if i < len(sample_questions):
                if st.button(f"💬 {sample_questions[i][:50]}...", key=f"q2_{i}"):
                    st.session_state.selected_question = sample_questions[i]
    
    with col3:
        for i in range(2, len(sample_questions), 3):
            if i < len(sample_questions):
                if st.button(f"💬 {sample_questions[i][:50]}...", key=f"q3_{i}"):
                    st.session_state.selected_question = sample_questions[i]

    # Chat interface
    st.header("💬 Therapy Session")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle selected question
    if "selected_question" in st.session_state:
        user_input = st.session_state.selected_question
        del st.session_state.selected_question
    else:
        user_input = st.chat_input("Share your thoughts, feelings, or ask for help with CBT techniques...")
    
    # Handle mood tracking from sidebar
    if "mood_tracked" in st.session_state:
        mood_data = st.session_state.mood_tracked
        user_input = f"I want to track my mood: I'm feeling {mood_data['mood']} with intensity {mood_data['intensity']}/10. Triggers: {mood_data['triggers']}"
        del st.session_state.mood_tracked
    
    # Handle search query from sidebar
    if "search_query" in st.session_state:
        search_query = st.session_state.search_query
        user_input = f"Can you search my previous sessions for: {search_query}"
        del st.session_state.search_query
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Process with the CBT agent
                    response = st.session_state.agent(user_input=f"User ID: {user_id}. {user_input}")
                    assistant_response = response.response
                    
                    st.markdown(assistant_response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    
                except Exception as e:
                    error_message = f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question or check your configuration."
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

    # Footer with information
    st.markdown("---")
    st.markdown("""
    **🔒 Privacy Note**: This is a demo application. In a real therapeutic setting, all conversations would be securely stored and protected by healthcare privacy laws.
    
    **⚠️ Disclaimer**: This AI assistant provides educational information about CBT techniques but is not a replacement for professional mental health treatment. If you're experiencing severe mental health symptoms, please consult with a licensed mental health professional.
    """)

if __name__ == "__main__":
    main()
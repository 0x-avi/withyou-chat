import dspy
from mem0 import Memory
from core.models import MemoryQA
from core.memory import MemoryTools
from core.helpers import get_current_time



class MemoryReActAgent(dspy.Module):
    """A ReAct agent enhanced with Mem0 memory capabilities."""

    def __init__(self, memory: Memory):
        super().__init__()
        self.memory_tools = MemoryTools(memory)
        self.current_user_id = "default_user"

        # Create tools list for ReAct
        self.tools = [
            self.memory_tools.store_memory,
            self.memory_tools.search_memories,
            self.memory_tools.get_all_memories,
            get_current_time,
            self.set_reminder,
            self.get_preferences,
            self.update_preferences,
        ]

        # Initialize ReAct with our tools
        self.react = dspy.ReAct(
            signature=MemoryQA,
            tools=self.tools,
            max_iters=2  # Reduced to prevent multiple calls
        )

    def forward(self, user_input: str, user_id: str = "default_user"):
        """Process user input with memory-aware reasoning."""
        self.current_user_id = user_id
        return self.react(user_input=user_input)

    def set_reminder(self, reminder_text: str, date_time: str = None) -> str:
        """Set a reminder for the user."""
        reminder = f"Reminder: {reminder_text} {f'for {date_time}' if date_time else ''}"
        return self.memory_tools.store_memory(reminder, user_id=self.current_user_id)

    def get_preferences(self, category: str = "general") -> str:
        """Get user preferences for a specific category."""
        query = f"user preferences {category}"
        return self.memory_tools.search_memories(query=query, user_id=self.current_user_id)

    def update_preferences(self, category: str, preference: str) -> str:
        """Update user preferences."""
        preference_text = f"User preference for {category}: {preference}"
        return self.memory_tools.store_memory(preference_text, user_id=self.current_user_id)
from mem0 import Memory

class MemoryTools:
    """Tools for interacting with the Mem0 memory system."""

    def __init__(self, memory: Memory, user: str = "guest"):
        self.memory = memory
        self.user = user  # correctly assign

    def store_memory(self, content: str, user_id: str = None) -> str:
        """Store information in memory."""
        user_id = user_id or self.user
        try:
            self.memory.add(content, user_id=user_id)
            return f"Stored memory: {content}"
        except Exception as e:
            return f"Error storing memory: {str(e)}"

    def search_memories(self, query: str, user_id: str = None, limit: int = 5) -> str:
        """Search for relevant memories."""
        user_id = user_id or self.user
        try:
            results = self.memory.search(query, user_id=user_id, limit=limit)
            if not results or not results.get("results"):
                return "No relevant memories found."

            memory_text = "Relevant memories found:\n"
            for i, result in enumerate(results["results"]):
                memory_text += f"{i+1}. {result['memory']}\n"
            return memory_text
        except Exception as e:
            return f"Error searching memories: {str(e)}"

    def get_all_memories(self, user_id: str = None) -> str:
        """Get all memories for a user."""
        user_id = user_id or self.user
        try:
            results = self.memory.get_all(user_id=user_id)
            if not results or not results.get("results"):
                return "No memories found for this user."

            memory_text = "All memories for user:\n"
            for i, result in enumerate(results["results"]):
                memory_text += f"{i+1}. {result['memory']}\n"
            return memory_text
        except Exception as e:
            return f"Error retrieving memories: {str(e)}"

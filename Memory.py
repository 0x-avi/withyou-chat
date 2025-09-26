from mem0 import AsyncMemory
import asyncio
class MemOps:
    def __init__(self,memory : AsyncMemory):
        self.memory = memory
        self.user_id = 'guest'
        self._pending = []
        
    async def add_memory(self, messages='str'):
        memories = await asyncio.create_task(self.memory.add(messages, user_id=self.user_id))
        return memories

    async def get_all_memories(self):
        return await self.memory.get_all(user_id=self.user_id)
    
    async def search_for_memories(self,query : str):
        memories = await asyncio.create_task(self.memory.search(query=query,limit=1,user_id=self.user_id))
        print('retrieved all memory')
        memory_text = "memories of the user retrieved from the database:\n"
        for i, result in enumerate(memories["results"]):
            memory_text += f"{i}. {result['memory']}\n"
        return memory_text

    def set_user_id(self,id : str):
        self.user_id = id
    def get_user_id(self):
        return self.user_id
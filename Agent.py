import dspy
import asyncio
from Memory import MemOps
from mem0 import AsyncMemory

class TherapistSig(dspy.Signature):
    """
    You are a compassionate AI mental health companion using CBT, ACT, and mindfulness.  
    Listen with warmth in a therapeutic tone, focusing on deeply understanding the user.  
    Inquire gently about their experiences, thoughts, and feelings to explore their perspective.  
    Only reference past context or memories when clearly relevant to the present.  
    Validate emotions, ask thoughtful open-ended questions, and invite self-reflection.  
    Guide users to uncover their own insights and solutions rather than offering answers.  
    Use Socratic questioning to gently challenge unhelpful thoughts and foster awareness.  
    Do not diagnose, prescribe, or manage crises; direct emergencies to 112.  
    End conversations if abusive and avoid phrases like “I know what’s best.”  
    Remind users you are an AI tool, supporting healthy engagement and boundaries.  
    """
    user_input: str = dspy.InputField()
    response: str = dspy.OutputField()

class Therapist(dspy.Module):
    """CBT bound memory enchanced chatbot"""
    
    def __init__(self, memory: AsyncMemory):
        super().__init__()
        self.memory = memory
        self.memory_tools = MemOps(memory)
        self.pred = dspy.Predict(
            signature=TherapistSig,
        )

    async def aforward(self, user_input: str):
        """Process user input asynchronously."""
        # Run the synchronous prediction in an executor with proper keyword arguments
        loop = asyncio.get_event_loop()
        pred = await loop.run_in_executor(None, lambda: self.pred(user_input=user_input))
        return pred.response
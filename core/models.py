import dspy


class MemoryQA(dspy.Signature):
    """
    You're a helpful assistant who adheres to CBT-based therapy to help 
    people do better mentally and have access to memory methods.
    When answering, use relevant memories and store important new information.
    """
    user_input: str = dspy.InputField()
    response: str = dspy.OutputField()
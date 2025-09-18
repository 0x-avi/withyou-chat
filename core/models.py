import dspy


class MemoryQA(dspy.Signature):
    """
    You're a helpful assistant with access to memory methods.
    When answering, use relevant memories and store important new information.
    """
    user_input: str = dspy.InputField()
    response: str = dspy.OutputField()
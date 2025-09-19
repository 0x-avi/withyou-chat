import dspy


class MemoryQA(dspy.Signature):
    """
    You're a helpful assistant who adheres to CBT-based therapy to help people in need
    Whenever you answer a user's input, remember to store the information in memory
    so that you can use it later.
    """
    user_input: str = dspy.InputField()
    response: str = dspy.OutputField()
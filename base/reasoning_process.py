from .reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod

class ReasoningProcess:
    def __init__(self):
        self.reasoning_method = None
        self.knowledge_base = None
        self.state = ReasoningState.INITIALIZED
        self.reasoned_items = []
        self.evaluation_message = EvaluationMessage.NONE
        self.options = None
        self.reasoning_error_message = None
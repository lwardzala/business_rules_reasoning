from .reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod
from .knowledge_base import KnowledgeBase

class ReasoningProcess:
    def __init__(self, reasoning_method: ReasoningMethod, knowledge_base: KnowledgeBase, options=None):
        self.reasoning_method = reasoning_method
        self.knowledge_base = knowledge_base
        self.state = ReasoningState.INITIALIZED
        self.reasoned_items = []
        self.evaluation_message = EvaluationMessage.NONE
        self.options = options
        self.reasoning_error_message = None
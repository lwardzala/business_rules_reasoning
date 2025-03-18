from .reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod
from typing import List
from .knowledge_base import KnowledgeBase
from .variable import Variable

class ReasoningProcess:
    def __init__(self, reasoning_method: ReasoningMethod, knowledge_base: KnowledgeBase, options=None):
        self.reasoning_method = reasoning_method
        self.knowledge_base = knowledge_base
        self.state = ReasoningState.INITIALIZED
        self.reasoned_items: List[Variable] = []
        self.evaluation_message = EvaluationMessage.NONE
        self.options = options
        self.reasoning_error_message = None

    def display_state(self) -> str:
        rules_display = "\n\n".join([rule.display_state() for rule in self.knowledge_base.rule_set])
        state_display = f"State: {self.state.name}"
        evaluation_message_display = f"Evaluation Message: {self.evaluation_message.name}"
        reasoned_items_display = "Reasoned Items: " + ", ".join([f"{item.id} = {item.value}" for item in self.reasoned_items])
        error_message_display = f"Error Message: {self.reasoning_error_message}" if self.state == ReasoningState.FINISHED and self.evaluation_message == EvaluationMessage.ERROR else ""
        reasoning_method_display = f"Reasoning Method: {self.reasoning_method.name}"
        knowledge_base_type_display = f"Knowledge Base Type: {self.knowledge_base.reasoning_type.name}"
        return f"{rules_display}\n\n{state_display}\n{evaluation_message_display}\n{reasoned_items_display}\n{error_message_display}\n{reasoning_method_display}\n{knowledge_base_type_display}"
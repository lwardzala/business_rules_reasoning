import json
from .base.reasoning_process import ReasoningProcess
from .base.knowledge_base import KnowledgeBase
from .base.rule import Rule
from .deductive import DeductivePredicate
from .base.variable import Variable
from .base.reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod
from .base import OperatorType

class ReasoningProcessEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ReasoningProcess):
            return {
                "reasoning_method": obj.reasoning_method.name,
                "knowledge_base": obj.knowledge_base,
                "state": obj.state.name,
                "reasoned_items": obj.reasoned_items,
                "evaluation_message": obj.evaluation_message.name,
                "options": obj.options,
                "reasoning_error_message": obj.reasoning_error_message
            }
        elif isinstance(obj, KnowledgeBase):
            return {
                "id": obj.id,
                "name": obj.name,
                "description": obj.description,
                "rule_set": obj.rule_set,
                "properties": obj.properties
            }
        elif isinstance(obj, Rule):
            return {
                "conclusion": obj.conclusion,
                "predicates": obj.predicates,
                "result": obj.result,
                "evaluated": obj.evaluated
            }
        elif isinstance(obj, DeductivePredicate):
            return {
                "left_term": obj.left_term,
                "right_term": obj.right_term,
                "operator": obj.operator.name,
                "result": obj.result,
                "evaluated": obj.evaluated
            }
        elif isinstance(obj, Variable):
            return {
                "id": obj.id,
                "name": obj.name,
                "value": obj.value,
                "frequency": obj.frequency
            }
        elif isinstance(obj, ReasoningState):
            return obj.name
        elif isinstance(obj, EvaluationMessage):
            return obj.name
        elif isinstance(obj, ReasoningMethod):
            return obj.name
        elif isinstance(obj, OperatorType):
            return obj.name
        return super().default(obj)

def serialize_reasoning_process(reasoning_process: ReasoningProcess) -> str:
    return json.dumps(reasoning_process, cls=ReasoningProcessEncoder, indent=4)

def serialize_knowledge_base(knowledge_base: KnowledgeBase) -> str:
    return json.dumps(knowledge_base, cls=ReasoningProcessEncoder, indent=4)

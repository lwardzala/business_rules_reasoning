import json
from .base.reasoning_process import ReasoningProcess
from .base.knowledge_base import KnowledgeBase
from .base.rule import Rule
from .deductive import DeductivePredicate
from .base.variable import Variable
from .base.reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod, ReasoningType
from .base import OperatorType

def deserialize_reasoning_process(data: str) -> ReasoningProcess:
    data_dict = json.loads(data)
    knowledge_base = deserialize_knowledge_base(json.dumps(data_dict["knowledge_base"]))
    reasoning_process = ReasoningProcess(reasoning_method=ReasoningMethod[data_dict["reasoning_method"]], knowledge_base=knowledge_base)
    reasoning_process.state = ReasoningState[data_dict["state"]]
    reasoning_process.reasoned_items = data_dict["reasoned_items"]
    reasoning_process.evaluation_message = EvaluationMessage[data_dict["evaluation_message"]]
    reasoning_process.options = data_dict["options"]
    reasoning_process.reasoning_error_message = data_dict["reasoning_error_message"]
    return reasoning_process

def deserialize_knowledge_base(data: str) -> KnowledgeBase:
    data_dict = json.loads(data)
    knowledge_base = KnowledgeBase()
    knowledge_base.id = data_dict["id"]
    knowledge_base.name = data_dict["name"]
    knowledge_base.description = data_dict["description"]
    knowledge_base.rule_set = [deserialize_rule(json.dumps(rule)) for rule in data_dict["rule_set"]]
    knowledge_base.properties = data_dict["properties"]
    knowledge_base.reasoning_type = ReasoningType[data_dict["reasoning_type"]]
    return knowledge_base

def deserialize_rule(data: str) -> Rule:
    data_dict = json.loads(data)
    rule = Rule()
    rule.conclusion = deserialize_predicate(json.dumps(data_dict["conclusion"]))
    rule.predicates = [deserialize_predicate(json.dumps(predicate)) for predicate in data_dict["predicates"]]
    rule.result = data_dict["result"]
    rule.evaluated = data_dict["evaluated"]
    return rule

def deserialize_predicate(data: str) -> DeductivePredicate:
    data_dict = json.loads(data)
    predicate = DeductivePredicate()
    predicate.left_term = deserialize_variable(json.dumps(data_dict["left_term"]))
    predicate.right_term = deserialize_variable(json.dumps(data_dict["right_term"]))
    predicate.operator = OperatorType[data_dict["operator"]]
    predicate.result = data_dict["result"]
    predicate.evaluated = data_dict["evaluated"]
    return predicate

def deserialize_variable(data: str) -> Variable:
    data_dict = json.loads(data)
    variable = Variable()
    variable.id = data_dict["id"]
    variable.name = data_dict["name"]
    variable.value = data_dict["value"]
    variable.frequency = data_dict["frequency"]
    return variable

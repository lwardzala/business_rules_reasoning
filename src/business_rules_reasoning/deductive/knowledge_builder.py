from ..base import KnowledgeBase, Rule, Predicate, Variable, OperatorType, ReasoningType
from .deductive_predicate import DeductivePredicate
from .deductive_conclusion import DeductiveConclusion

class KnowledgeBaseBuilder:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.knowledge_base.rule_set = []
        self.knowledge_base.properties = {}
        self.knowledge_base.reasoning_type = ReasoningType.CRISP

    def set_id(self, id):
        self.knowledge_base.id = id
        return self

    def set_name(self, name):
        self.knowledge_base.name = name
        return self

    def set_description(self, description):
        self.knowledge_base.description = description
        return self

    def add_rule(self, rule: Rule):
        self.knowledge_base.rule_set.append(rule)
        return self

    def add_properties(self, properties: dict):
        self.knowledge_base.properties.update(properties)
        return self

    def add_property(self, key, value):
        self.knowledge_base.properties[key] = value
        return self

    def unwrap(self):
        self.knowledge_base.validate()
        return self.knowledge_base

class RuleBuilder:
    def __init__(self):
        self.rule = Rule()
        self.rule.predicates = []
        self.rule.result = False
        self.rule.evaluated = False

    def set_conclusion(self, rule_conclusion: Variable):
        self.rule.conclusion = DeductiveConclusion(variable=rule_conclusion)
        return self

    def add_predicate(self, predicate: Predicate):
        self.rule.predicates.append(predicate)
        return self

    def unwrap(self):
        self.rule.validate()
        return self.rule

class PredicateBuilder:
    def __init__(self):
        self.predicate = DeductivePredicate(left_term=Variable(), right_term=Variable(), operator=None)
        self.predicate.result = False
        self.predicate.evaluated = False

    def configure_predicate(self, variable_id, operator_type: OperatorType, right_term_value):
        self.predicate.left_term.id = variable_id
        self.predicate.left_term.name = variable_id
        self.predicate.right_term.id = variable_id
        self.predicate.right_term.name = variable_id
        self.predicate.operator = operator_type
        self.predicate.right_term.value = right_term_value
        return self

    def configure_predicate_with_name(self, variable_id, variable_name, operator_type: OperatorType, right_term_value):
        self.predicate.left_term.id = variable_id
        self.predicate.left_term.name = variable_name
        self.predicate.right_term.id = variable_id
        self.predicate.right_term.name = variable_name
        self.predicate.operator = operator_type
        self.predicate.right_term.value = right_term_value
        return self
    
    def configure_predicate_with_variable(self, variable: Variable, operator_type: OperatorType, right_term_value):
        self.predicate.left_term.id = variable.id
        self.predicate.left_term.name = variable.name
        self.predicate.right_term.id = variable.id
        self.predicate.right_term.name = variable.name
        self.predicate.operator = operator_type
        self.predicate.right_term.value = right_term_value
        return self

    def set_left_term_value(self, left_term_value):
        self.predicate.left_term.value = left_term_value
        return self

    def unwrap(self):
        self.predicate.validate()
        return self.predicate

class VariableBuilder:
    def __init__(self):
        self.variable = Variable()

    def set_id(self, id):
        self.variable.id = id
        return self

    def set_name(self, name):
        self.variable.name = name
        return self

    def set_value(self, value):
        self.variable.value = value
        return self

    def unwrap(self):
        return self.variable

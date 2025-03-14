from .rule import Rule
from .reasoning_enums import ReasoningType

class KnowledgeBase:
    def __init__(self, id=None, name=None, description=None, rule_set: list[Rule] = None, properties=None, reasoning_type: ReasoningType = None):
        self.id = id
        self.name = name
        self.description = description
        self.rule_set = rule_set if rule_set is not None else []
        self.properties = properties if properties is not None else {}
        self.reasoning_type = reasoning_type

    def validate(self):
        for rule in self.rule_set:
            rule.validate()
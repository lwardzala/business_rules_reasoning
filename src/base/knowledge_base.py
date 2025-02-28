from .rule import Rule

class KnowledgeBase:
    def __init__(self, id=None, name=None, description=None, rule_set: list[Rule] = None, properties=None):
        self.id = id
        self.name = name
        self.description = description
        self.rule_set = rule_set if rule_set is not None else []
        self.properties = properties if properties is not None else {}

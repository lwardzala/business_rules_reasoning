from typing import List
from .predicate import Predicate

class Rule:
    def __init__(self, conclusion: Predicate = None, predicates: List[Predicate] = None):
        self.conclusion = conclusion
        self.predicates = predicates if predicates is not None else []
        self.result = False
        self.evaluated = False

    def evaluate(self):
        if self.evaluated:
            return

        for predicate in self.predicates:
            if not predicate.get_missing_variables():
                predicate.evaluate()

                if not predicate.get_result():
                    self.result = False
                    self.evaluated = True
                    return

        if any(predicate.is_evaluated() and not predicate.get_result() for predicate in self.predicates) or \
           all(predicate.is_evaluated() for predicate in self.predicates):
            self.result = True
            self.evaluated = True

    def is_valid(self):
        return all(predicate.get_missing_variables() is None and predicate.is_valid() for predicate in self.predicates)
    
    def validate(self):
        for predicate in self.predicates:
            predicate.validate()

    def reset_evaluation(self):
        self.evaluated = False
        self.result = False
        for predicate in self.predicates:
            predicate.reset_evaluation()

    def set_variables(self, variables):
        for predicate in self.predicates:
            predicate.set_variables(variables)
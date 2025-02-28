from ..base import Predicate
from ..base.operators import Between, GreaterOrEqual, GreaterThan, LessOrEqual, LessThan, NotBetween, NotSubset, Subset
from ..base.operator_enums import OperatorType

class DeductivePremise(Predicate):
    def __init__(self, left_term=None, right_term=None, operator=None):
        self.left_term = left_term
        self.right_term = right_term
        self.operator = operator
        self.result = False
        self.evaluated = False

    def evaluate(self):
        if not self.is_valid():
            raise Exception(f"Evaluation of predicate has failed. Missing value {self.left_term.id}.")
        if self.evaluated:
            return

        try:
            operator_class = {
                OperatorType.BETWEEN: Between,
                OperatorType.GREATER_OR_EQUAL: GreaterOrEqual,
                OperatorType.GREATER_THAN: GreaterThan,
                OperatorType.LESS_OR_EQUAL: LessOrEqual,
                OperatorType.LESS_THAN: LessThan,
                OperatorType.NOT_BETWEEN: NotBetween,
                OperatorType.NOT_SUBSET: NotSubset,
                OperatorType.SUBSET: Subset
            }[self.operator]
            operator_instance = operator_class()
            self.result = operator_instance.compare(self.left_term.get_value(), self.right_term.get_value())
            self.evaluated = True
        except Exception as ex:
            raise Exception("Unknown operator instance of predicate") from ex

    def get_missing_variables(self):
        return [self.left_term.id] if self.left_term.is_empty() else None

    def get_evaluation_value(self):
        return self.result

    def is_evaluated(self):
        return self.evaluated

    def is_valid(self):
        return not self.left_term.is_empty() and not self.right_term.is_empty()

    def set_variables(self, variable_collection):
        self.left_term.value = variable_collection[self.left_term.id]

    def get_result(self):
        return self.result

    def reset_evaluation(self):
        self.result = False
        self.evaluated = False
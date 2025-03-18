from ..base import Predicate
from ..base.operators import Between, GreaterOrEqual, GreaterThan, LessOrEqual, LessThan, NotBetween, NotSubset, Subset, Equal, NotEqual, IsIn, NotIn
from ..base.operator_enums import OperatorType
from ..base.variable import Variable

class DeductivePredicate(Predicate):
    def __init__(self, left_term: Variable = None, right_term: Variable = None, operator: OperatorType = None):
        self.left_term = left_term
        self.right_term = right_term
        self.operator = operator
        self.result = False
        self.evaluated = False

    def evaluate(self):
        if not self.is_ready():
            raise Exception(f"[Inference Engine]: Evaluation of predicate has failed. Missing value {self.left_term.id}.")
        if self.left_term.get_value_type() != self.right_term.get_value_type():
            raise Exception(f"[Inference Engine]: Variable {self.right_term.id}: Type mismatch between left term value ({self.left_term.get_value_type()}) and right term value ({self.right_term.get_value_type()}).")
        
        if self.evaluated:
            return

        try:
            operator_class = {
                OperatorType.BETWEEN: Between,
                OperatorType.EQUAL: Equal,
                OperatorType.NOT_EQUAL: NotEqual,
                OperatorType.GREATER_OR_EQUAL: GreaterOrEqual,
                OperatorType.GREATER_THAN: GreaterThan,
                OperatorType.LESS_OR_EQUAL: LessOrEqual,
                OperatorType.LESS_THAN: LessThan,
                OperatorType.NOT_BETWEEN: NotBetween,
                OperatorType.NOT_SUBSET: NotSubset,
                OperatorType.SUBSET: Subset,
                OperatorType.IS_IN: IsIn,
                OperatorType.NOT_IN: NotIn
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

    def is_evaluated(self) -> bool:
        return self.evaluated

    def is_valid(self) -> bool:
        return not self.right_term.is_empty() and self.left_term.id == self.right_term.id
    
    def validate(self):
        if not self.is_valid():
            raise Exception("[Inference Engine]: Invalid predicate: both terms must have the same id and right term must not be empty.")
    
    def is_ready(self):
        return self.is_valid() and not self.left_term.is_empty()

    def set_variables(self, variable_collection):
        if self.left_term.id in variable_collection:
            self.left_term.value = variable_collection[self.left_term.id]

    def get_expected_variable(self):
        return self.right_term

    def get_result(self):
        return self.result

    def reset_evaluation(self):
        self.result = False
        self.evaluated = False

    def display_operator(self) -> str:
        return {
            OperatorType.BETWEEN: "BETWEEN",
            OperatorType.EQUAL: "=",
            OperatorType.NOT_EQUAL: "!=",
            OperatorType.GREATER_OR_EQUAL: ">=",
            OperatorType.GREATER_THAN: ">",
            OperatorType.LESS_OR_EQUAL: "<=",
            OperatorType.LESS_THAN: "<",
            OperatorType.NOT_BETWEEN: "NOT BETWEEN",
            OperatorType.NOT_SUBSET: "NOT SUBSET",
            OperatorType.SUBSET: "SUBSET",
            OperatorType.IS_IN: "IN",
            OperatorType.NOT_IN: "NOT IN"
        }[self.operator]

    def display(self) -> str:
        return f"{self.left_term.id} {self.display_operator()} {self.right_term.value}"

    def display_state(self) -> str:
        predicate_status = "Evaluated" if self.evaluated else "Not Evaluated"
        predicate_result = "True" if self.result else "False"
        return f"{self.left_term.id} {self.display_operator()} {self.right_term.value} (Provided: {self.left_term.value}, Status: {predicate_status}, Result: {predicate_result})"
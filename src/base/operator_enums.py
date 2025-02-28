from enum import Enum

class OperatorType(Enum):
    EQUAL = "Equal"
    NOT_EQUAL = "NotEqual"
    GREATER_THAN = "GreaterThan"
    LESS_THAN = "LessThan"
    GREATER_OR_EQUAL = "GreaterOrEqual"
    LESS_OR_EQUAL = "LessOrEqual"
    BETWEEN = "Between"
    NOT_BETWEEN = "NotBetween"
    IS_IN = "IsIn"
    NOT_IN = "NotIn"
    SUBSET = "Subset"
    NOT_SUBSET = "NotSubset"

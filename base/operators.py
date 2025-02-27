from enum import Enum

class OperatorType(Enum):
    EQUAL = "Equal"
    NOT_EQUAL = "NotEqual"
    GREATER_THAN = "GreaterThan"
    LESSER_THAN = "LesserThan"
    GREATER_OR_EQUAL = "GreaterOrEqual"
    LESSER_OR_EQUAL = "LesserOrEqual"
    BETWEEN = "Between"
    NOT_BETWEEN = "NotBetween"
    IS_IN = "IsIn"
    NOT_IN = "NotIn"
    SUBSET = "Subset"
    NOT_SUBSET = "NotSubset"

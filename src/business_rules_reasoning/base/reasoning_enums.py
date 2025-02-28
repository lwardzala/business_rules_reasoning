from enum import Enum

class ReasoningState(Enum):
    INITIALIZED = "INITIALIZED"
    STARTED = "STARTED"
    STOPPED = "STOPPED"
    FINISHED = "FINISHED"

class EvaluationMessage(Enum):
    NONE = "NONE"
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"
    MISSING_VALUES = "MISSING_VALUES"

class ReasoningMethod(Enum):
    DEDUCTION = "DEDUCTION"
    HYPOTHESIS_TESTING = "HYPOTHESIS_TESTING"
    FUZZY_MAMDANI = "FUZZY_MAMDANI"
    FUZZY_SUGENO = "FUZZY_SUGENO"

class ReasoningType(Enum):
    CRISP = "CRISP"
    FUZZY = "FUZZY"
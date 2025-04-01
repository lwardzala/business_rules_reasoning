"""
Business Rules Reasoning Library

This library provides classes and methods for defining and evaluating business rules using various reasoning methods.
"""

__title__ = "business_rules_reasoning"
__version__ = "0.2.0"
__author__ = "Lukasz Wardzala <https://github.com/lwardzala>"
__license__ = "MIT"

from .base.reasoning_process import ReasoningProcess
from .base.reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod
from .base import OperatorType, ReasoningService, Variable
from .json_deserializer import deserialize_reasoning_process, deserialize_knowledge_base
from .json_serializer import serialize_reasoning_process, serialize_knowledge_base
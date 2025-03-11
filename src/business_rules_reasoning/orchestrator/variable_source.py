from enum import Enum
from typing import Callable

class VariableSourceType(Enum):
    QUERY = "QUERY"
    API_ENDPOINT = "API_ENDPOINT"

class VariableSource:
    def __init__(self, variable_id: str, source_type: VariableSourceType, retriever: Callable = None):
        self.variable_id = variable_id
        self.source_type = source_type
        self.retrieval_function = retriever
from abc import ABC, abstractmethod
from typing import List
from .variable import Variable
from .reasoning_process import ReasoningProcess

class ReasoningService(ABC):
    @staticmethod
    @abstractmethod
    def start_reasoning(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        pass

    @staticmethod
    @abstractmethod
    def continue_reasoning(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        pass

    @staticmethod
    @abstractmethod
    def set_values(reasoning_process: ReasoningProcess, variables) -> ReasoningProcess:
        pass

    @staticmethod
    @abstractmethod
    def reset_reasoning(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        pass

    @staticmethod
    @abstractmethod
    def clear_reasoning(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        pass

    @staticmethod
    @abstractmethod
    def get_all_missing_variable_ids(reasoning_process: ReasoningProcess) -> List[str]:
        pass

    @staticmethod
    @abstractmethod
    def get_all_missing_variables(reasoning_process: ReasoningProcess) -> List[Variable]:
        pass

    # TODO: Do we need this or make it private?
    @staticmethod
    @abstractmethod
    def analyze_variables_frequency(reasoning_process: ReasoningProcess) -> List[Variable]:
        pass

    @staticmethod
    @abstractmethod
    def deduction(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        pass

    @staticmethod
    @abstractmethod
    def hypothesis_testing(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        pass

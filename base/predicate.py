from abc import ABC, abstractmethod

class Predicate(ABC):
    @abstractmethod
    def get_result(self):
        pass

    @abstractmethod
    def get_evaluation_value(self):
        pass

    @abstractmethod
    def set_variables(self, variable_collection):
        pass

    @abstractmethod
    def is_valid(self):
        pass

    @abstractmethod
    def is_evaluated(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def get_missing_variables(self):
        pass

    @abstractmethod
    def reset_evaluation(self):
        pass
from abc import ABC, abstractmethod

class Conclusion(ABC):
    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def display(self) -> str:
        pass

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_variable(self):
        pass
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMPipelineBase(ABC):
    @abstractmethod
    def prompt_text_generation(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def prompt_summarization(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def prompt_question_answering(self, question: str, context: str, **kwargs) -> str:
        pass

    @abstractmethod
    def prompt_text2text_generation(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def prompt_table_question_answering(self, query: str, table: Dict[str, List[Any]], **kwargs) -> str:
        pass

    @abstractmethod
    def prompt_text_classification(self, text: str, **kwargs) -> str:
        pass

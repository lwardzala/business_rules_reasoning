from abc import ABC, abstractmethod

class BasePromptTemplates(ABC):
    """
    Abstract base class for prompt templates.
    """

    @property
    @abstractmethod
    def FetchInferenceInstructionsTemplate(self) -> str:
        pass

    @property
    @abstractmethod
    def FetchHypothesisTestingTemplate(self) -> str:
        pass

    @property
    @abstractmethod
    def FetchVariablesTemplate(self) -> str:
        pass

    @property
    @abstractmethod
    def AskForMoreInformationTemplate(self) -> str:
        pass

    @property
    @abstractmethod
    def AskForReasoningClarificationTemplate(self) -> str:
        pass

    @property
    @abstractmethod
    def FinishInferenceTemplate(self) -> str:
        pass

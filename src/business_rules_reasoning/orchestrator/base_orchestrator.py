from abc import ABC, abstractmethod
from enum import Enum
import json
from typing import Callable, List

from .variable_source import VariableSource
from .reasoning_action import ReasoningAction
from ..base import KnowledgeBase, ReasoningState, ReasoningProcess, ReasoningService, ReasoningType, EvaluationMessage
from ..json_deserializer import deserialize_knowledge_base, deserialize_reasoning_process
from ..deductive import DeductiveReasoningService

class OrchestratorStatus(Enum):
    INITIALIZED = 'INITIALIZED'
    WAITING_FOR_QUERY = 'WAITING_FOR_QUERY'
    STARTED = 'STARTED'
    ENGINE_WAITING_FOR_VARIABLES = 'ENGINE_WAITING_FOR_VARIABLES'
    INFERENCE_FINISHED = 'INFERENCE_FINISHED'
    INFERENCE_ERROR = 'INFERENCE_ERROR'

class BaseOrchestrator(ABC):
    def __init__(self, knowledge_base_retriever: Callable, inference_state_retriever: Callable, inference_session_id: str = None, actions: List[ReasoningAction] = None, variable_sources: List[VariableSource] = None):
        self.knowledge_base_retriever = knowledge_base_retriever
        self.inference_state_retriever = inference_state_retriever
        self.knowledge_bases: List[KnowledgeBase] = []
        self.inference_session_id = inference_session_id
        self.actions_retriever = actions
        self.variable_sources = variable_sources
        self.status = None
        self.reasoning_process: ReasoningProcess = None

    @abstractmethod
    def _next_step(self):
        pass

    @abstractmethod
    def set_session_id(self):
        pass

    def start_orchestration(self):
        if self.status is not None:
            return
        
        if self.inference_session_id is None:
            self.set_session_id()
        else:
            self.retrieve_inference_state(self.inference_session_id)

        self.retrieve_knowledge_bases()
        self.status = OrchestratorStatus.INITIALIZED

        self.update_engine_status()
        

    def update_engine_status(self):
        if self.reasoning_process is not None:
            self.status = OrchestratorStatus.WAITING_FOR_QUERY

            if self.reasoning_process.evaluation_message == EvaluationMessage.MISSING_VALUES:
                self.status = OrchestratorStatus.ENGINE_WAITING_FOR_VARIABLES

            if self.reasoning_process.evaluation_message == EvaluationMessage.ERROR:
                self.status = OrchestratorStatus.INFERENCE_ERROR

            if self.reasoning_process.state == ReasoningState.FINISHED:
                self.status = OrchestratorStatus.INFERENCE_FINISHED

    def reset_orchestration(self):
        self.status = None
        self.inference_session_id = None
        self.reasoning_process = None
        self.start_orchestration()

    def retrieve_knowledge_bases(self):
        self.knowledge_bases = self.knowledge_base_retriever()
        return

    def retrieve_inference_state(self, inference_id: str) -> ReasoningProcess:
        inference_state_json = self.inference_state_retriever(inference_id)
        self.reasoning_process = deserialize_reasoning_process(json.dumps(inference_state_json))
        if self.reasoning_process.state == ReasoningState.FINISHED:
            self.reset_orchestration() # TODO: think about: start new orchestration or stay in finished state?
        return

    def get_reasoning_service(self) -> ReasoningService:
        if self.reasoning_process.knowledge_base.reasoning_type == ReasoningType.CRISP:
            return DeductiveReasoningService
        elif self.reasoning_process.knowledge_base.reasoning_type == ReasoningType.FUZZY:
            raise NotImplementedError("Fuzzy reasoning is not implemented yet")
        else:
            raise ValueError("Unknown reasoning type")
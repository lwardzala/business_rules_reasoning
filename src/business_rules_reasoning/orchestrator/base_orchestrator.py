from abc import ABC, abstractmethod
from enum import Enum
import json
from typing import Callable, List

from .variable_source import VariableSource
from .reasoning_action import ReasoningAction
from ..base import KnowledgeBase, ReasoningState, ReasoningProcess, ReasoningService, ReasoningType, EvaluationMessage, Variable
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
        self.inference_log: List[str] = []

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

            if self.reasoning_process.state == ReasoningState.FINISHED and self.reasoning_process.evaluation_message != EvaluationMessage.ERROR:
                self.status = OrchestratorStatus.INFERENCE_FINISHED

    def reset_orchestration(self):
        self.status = None
        self.inference_session_id = None
        self.reasoning_process = None
        self.start_orchestration()
        self._log_inference("Reasoning process was removed")

    def retrieve_knowledge_bases(self):
        self.knowledge_bases = self.knowledge_base_retriever()
        return

    def retrieve_inference_state(self, inference_id: str) -> ReasoningProcess:
        inference_state_json = self.inference_state_retriever(inference_id)
        self.reasoning_process = deserialize_reasoning_process(json.dumps(inference_state_json))
        self._log_inference(f"Reasoning process was retrieved from a JSON with status: {self.reasoning_process.state}")
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
        
    def _start_reasoning_process(self):
        reasoning_service = self.get_reasoning_service()
        self._log_inference(f"Starting reasoning process from status: {self.reasoning_process.state}")
        self.reasoning_process = reasoning_service.start_reasoning(self.reasoning_process)
        self._log_inference(f"Reasoning process was started. End status: {self.reasoning_process.state}")
        self.update_engine_status()

    def _get_missing_rerasoning_variables(self) -> List[Variable]:
        reasoning_service = self.get_reasoning_service()
        self._log_inference(f"Retrieving missing variables. Status: {self.reasoning_process.state}")
        return reasoning_service.get_all_missing_variables(self.reasoning_process)
    
     # TODO: Update the values from further queries
    def _set_variables_and_continue_reasoning(self, variables_dict: dict):
        reasoning_service = self.get_reasoning_service()
        self._log_inference(f"Setting variables: {', '.join(list(variables_dict.keys()))}. Status: {self.reasoning_process.state}")
        self.reasoning_process = reasoning_service.set_values(self.reasoning_process, variables_dict)
        self.reasoning_process = reasoning_service.continue_reasoning(self.reasoning_process)
        self._log_inference(f"Reasoning continued. End status: {self.reasoning_process.state}")
        self.update_engine_status()

    def _log_inference(self, text: str):
        self.inference_log.append(text)

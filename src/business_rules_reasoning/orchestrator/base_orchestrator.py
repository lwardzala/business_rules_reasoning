from abc import ABC, abstractmethod
from enum import Enum
import json
from typing import Callable, List

from .variable_source import VariableSource
from .reasoning_action import ReasoningAction
from ..base import KnowledgeBase, ReasoningState, ReasoningProcess, ReasoningService
from ..json_deserializer import deserialize_knowledge_base, deserialize_reasoning_process

class OrchestratorStatus(Enum):
    INITIALIZED = 1
    WAITING_FOR_QUERY = 2
    ENGINE_WAITING_FOR_VARIABLES = 3
    INFERENCE_FINISHED = 4
    INFERENCE_ERROR = 5

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
    def next_step(self):
        pass

    @abstractmethod
    def set_session_id(self):
        pass

    def start_orchestration(self):
        if self.status != None:
            return
        
        if self.inference_session_id is None:
            self.set_session_id()
        else:
            self.retrieve_inference_state(self.inference_session_id)

        self.retrieve_knowledge_base()
        self.status = OrchestratorStatus.INITIALIZED

    def reset_orchestration(self):
        self.status = None
        self.inference_session_id = None
        self.reasoning_process = None
        self.start_orchestration()


    def retrieve_knowledge_base(self) -> List[KnowledgeBase]:
        knowledge_base_jsons = self.knowledge_base_retriever()
        self.knowledge_bases = [deserialize_knowledge_base(json.dumps(kb_json)) for kb_json in knowledge_base_jsons]
        return

    def retrieve_inference_state(self, inference_id: str) -> ReasoningProcess:
        inference_state_json = self.inference_state_retriever(inference_id)
        self.reasoning_process = deserialize_reasoning_process(json.dumps(inference_state_json))
        if self.reasoning_process.state == ReasoningState.FINISHED:
            self.reset_orchestration() # TODO: think about: start new orchestration or stay in finished state?
        return
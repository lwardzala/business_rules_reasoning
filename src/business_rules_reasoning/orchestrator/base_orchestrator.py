from abc import ABC, abstractmethod
from enum import Enum
import json
from typing import Callable, List

from .variable_source import VariableSource
from .reasoning_action import ReasoningAction
from ..base import KnowledgeBase, ReasoningState, ReasoningProcess, ReasoningService, ReasoningType, EvaluationMessage, Variable
from ..json_deserializer import deserialize_knowledge_base, deserialize_reasoning_process
from ..json_serializer import serialize_reasoning_process
from ..deductive import DeductiveReasoningService
from .inference_logger import InferenceLogger

class OrchestratorStatus(Enum):
    INITIALIZED = 'INITIALIZED'
    WAITING_FOR_QUERY = 'WAITING_FOR_QUERY'
    STARTED = 'STARTED'
    ENGINE_WAITING_FOR_VARIABLES = 'ENGINE_WAITING_FOR_VARIABLES'
    FACT_QUESTIONING_MODE = 'FACT_RETRIEVAL_MODE'
    INFERENCE_FINISHED = 'INFERENCE_FINISHED'
    INFERENCE_ERROR = 'INFERENCE_ERROR'

class VariablesFetchingMode(Enum):
    STEP_BY_STEP = 'STEP_BY_STEP'
    ALL_POSSIBLE = 'ALL_POSSIBLE'

class OrchestratorOptions:
    def __init__(self, variables_fetching: VariablesFetchingMode = VariablesFetchingMode.ALL_POSSIBLE, conclusion_as_fact: bool = False, pass_conclusions_as_arguments: bool = True, pass_facts_as_arguments: bool = True):
        self.variables_fetching = variables_fetching
        self.conclusion_as_fact = conclusion_as_fact
        self.pass_conclusions_as_arguments = pass_conclusions_as_arguments
        self.pass_facts_as_arguments = pass_facts_as_arguments

class BaseOrchestrator(ABC):
    def __init__(self, knowledge_base_retriever: Callable, inference_state_retriever: Callable, options: OrchestratorOptions, inference_session_id: str = None, actions: List[ReasoningAction] = None, variable_sources: List[VariableSource] = None):
        self.knowledge_base_retriever = knowledge_base_retriever
        self.inference_state_retriever = inference_state_retriever
        self.knowledge_bases: List[KnowledgeBase] = []
        self.inference_session_id = inference_session_id
        self.actions_retriever = actions
        self.variable_sources = variable_sources
        self.status = None
        self.reasoning_process: ReasoningProcess = None
        self.inference_logger = InferenceLogger()
        self.options = options

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
        self._log_inference(f"[Orchestrator]: Retrieved knwledge bases: {', '.join([kb.id for kb in self.knowledge_bases])}")
        self.status = OrchestratorStatus.INITIALIZED
        self._log_inference(f"[Orchestrator]: Status set to: {self.status}")

        self.update_engine_status()
        

    def update_engine_status(self):
        if self.reasoning_process is not None:
            # self._set_orchestrator_status(OrchestratorStatus.WAITING_FOR_QUERY)

            if self.reasoning_process.evaluation_message == EvaluationMessage.MISSING_VALUES:
                self._set_orchestrator_status(OrchestratorStatus.ENGINE_WAITING_FOR_VARIABLES)

            if self.reasoning_process.evaluation_message == EvaluationMessage.ERROR:
                self._set_orchestrator_status(OrchestratorStatus.INFERENCE_ERROR)

            if self.reasoning_process.state == ReasoningState.FINISHED and self.reasoning_process.evaluation_message != EvaluationMessage.ERROR:
                self._set_orchestrator_status(OrchestratorStatus.INFERENCE_FINISHED)

    def reset_orchestration(self):
        self.status = None
        self.inference_session_id = None
        self.reasoning_process = None
        self.start_orchestration()
        self._log_inference("[Engine]: Reasoning process was removed")

    def retrieve_knowledge_bases(self):
        self.knowledge_bases = self.knowledge_base_retriever()
        return

    def retrieve_inference_state(self, inference_id: str) -> ReasoningProcess:
        inference_state_json = self.inference_state_retriever(inference_id)
        self.reasoning_process = deserialize_reasoning_process(json.dumps(inference_state_json))
        self._log_inference(f"[Engine]: Reasoning process was retrieved from a JSON with status: {self.reasoning_process.state}")
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
        self._log_inference(f"[Engine]: Starting reasoning process from status: {self.reasoning_process.state}")
        self.reasoning_process = reasoning_service.start_reasoning(self.reasoning_process)
        self._log_inference(f"[Engine]: Reasoning process was started. Resulting status: {self.reasoning_process.state}")
        self.update_engine_status()

    def _get_missing_reasoning_variables(self) -> List[Variable]:
        reasoning_service = self.get_reasoning_service()
        self._log_inference(f"[Engine]: Status: {self.reasoning_process.state} Retrieving missing variables.")
        return reasoning_service.get_all_missing_variables(self.reasoning_process).copy()
    
     # TODO: Update the values from further queries
    def _continue_reasoning(self):
        reasoning_service = self.get_reasoning_service()
        self.reasoning_process = reasoning_service.continue_reasoning(self.reasoning_process)
        self._log_inference(f"[Engine]: Reasoning continued. Resulting status: {self.reasoning_process.state}.")
        self.update_engine_status()

    def _set_variables(self, variables_dict: dict):
        reasoning_service = self.get_reasoning_service()
        self._log_inference(f"[Engine]: Providing variables to engine: {', '.join(list(variables_dict.keys()))}.")
        self.reasoning_process = reasoning_service.set_values(self.reasoning_process, variables_dict)

    def _log_inference(self, text: str):
        self.inference_logger.log(text)

    def _set_orchestrator_status(self, status: OrchestratorStatus):
        if self.status == status:
            self._log_inference(f"[Orchestrator]: Status remains {status}.")
        else:
            self._log_inference(f"[Orchestrator]: Changing status from {self.status} to {status}.")
        self.status = status

    def _return_inference_results(self, response: str, return_full_context: bool):
        return {
            "inference_session_id": self.inference_session_id,
            "response": response,
            "reasoning_process": json.loads(serialize_reasoning_process(self.reasoning_process)),
            "inference_log": self.inference_logger.get_log(),
            "orchestrator_status": self.status.name,
            "orchestrator_options": {
                "variables_fetching": self.options.variables_fetching.name,
                "conclusion_as_fact": self.options.conclusion_as_fact,
                "pass_conclusions_as_arguments": self.options.pass_conclusions_as_arguments,
                "pass_facts_as_arguments": self.options.pass_facts_as_arguments
            }
        } if return_full_context else response

from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Callable, List, Dict, Tuple, Any
import re
import json

from .huggingface_pipeline import HuggingFacePipeline
from .prompt_templates import PromptTemplates
from ..base_orchestrator import BaseOrchestrator, OrchestratorStatus
from ..variable_source import VariableSource
from ..reasoning_action import ReasoningAction
from ...base import ReasoningState, ReasoningProcess, ReasoningService, ReasoningMethod, Variable

class HuggingFaceOrchestrator(BaseOrchestrator):
    def __init__(self, model_name: str, knowledge_base_retriever: Callable, inference_state_retriever: Callable, inference_session_id: str = None, actions: List[ReasoningAction] = None, variable_sources: List[VariableSource] = None, prompt_templates = PromptTemplates, agent_type: str = "reasoning agent", tokenizer=None, model=None, **kwargs):
        super().__init__(knowledge_base_retriever, inference_state_retriever, inference_session_id, actions, variable_sources)
        self.pipeline = HuggingFacePipeline(model_name, tokenizer, model, **kwargs)
        self.query_history: List[Dict[str, str]] = []
        self.prompt_templates = prompt_templates
        self.agent_type: str = agent_type

    def _next_step(self, text: str):
        if self.status == OrchestratorStatus.INITIALIZED:
            knowledge_base_name, reasoning_method = self._fetch_inference_instructions(text)
            result = self._set_reasoning_process(knowledge_base_name, reasoning_method)
            if result:
                self.status = OrchestratorStatus.STARTED
            else:
                self.status = OrchestratorStatus.WAITING_FOR_QUERY
        
        if self.status == OrchestratorStatus.INFERENCE_ERROR:
            return
        
        if self.status == OrchestratorStatus.STARTED:
            reasoning_service = self.get_reasoning_service()
            self.reasoning_process = reasoning_service.start_reasoning(self.reasoning_process)
            self.update_engine_status()
        
        if self.status == OrchestratorStatus.ENGINE_WAITING_FOR_VARIABLES:
            missing_variables = reasoning_service.get_all_missing_variables(self.reasoning_process)
            variables_dict = self._fetch_variables(text, missing_variables)
            # TODO: Update the values from further queries
            self.reasoning_process = reasoning_service.set_values(self.reasoning_process, variables_dict)
            self.update_engine_status()

        if self.status == OrchestratorStatus.INFERENCE_FINISHED:
            # TODO: find and fire the actions accordingly to the conclusions
            return

    def set_session_id(self):
        # Implement the logic to set the session ID
        self.inference_session_id = "hf_session_id"

    def query(self, text: str) -> str:
        self.query_history.append({"role": "user", "text": text})
        if self.status is None:
            self.start_orchestration()

        # TODO: Handle other query instructions
        # if inference action
        self._next_step(text)

        # TODO: Handle outputs
        if self.status == OrchestratorStatus.WAITING_FOR_QUERY:
            return self._ask_for_reasoning_clarification()
            
        if self.status == OrchestratorStatus.ENGINE_WAITING_FOR_VARIABLES:
            missing_variables = ", ".join([f"{var.name}" for var in self.get_reasoning_service().get_all_missing_variables(self.reasoning_process)])
            return self._ask_for_more_information(missing_variables)
        
        if self.status == OrchestratorStatus.INFERENCE_ERROR:
            # TODO: generate answer
            return "An error occurred during the reasoning process."
        
        if self.status == OrchestratorStatus.INFERENCE_FINISHED:
            # TODO: generate answer
            return "The reasoning process has been completed."

        return ''

    def _extract_json_from_response(self, response: str) -> dict:
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in the response")
        
        json_str = json_match.group().replace('\n', '').replace('}', '}')
        data = json.loads(json_str)
        return data

    def _fetch_inference_instructions(self, text: str) -> Tuple[str, ReasoningMethod]:
        knowledge_bases_info = "\n".join([f"{kb.id} - {kb.description}" for kb in self.knowledge_bases])
        prompt = self.prompt_templates.FetchInferenceInstructionsTemplate.format(knowledge_bases=knowledge_bases_info, text=text)
        self.query_history.append({"role": "engine", "text": prompt})
        response = self.pipeline.prompt_text_generation(prompt)
        self.query_history.append({"role": "system", "text": response})
        
        data = self._extract_json_from_response(response)
        
        knowledge_base_id = data.get("knowledge_base_id")
        reasoning_method_str = data.get("reasoning_method")
        reasoning_method = ReasoningMethod.HYPOTHESIS_TESTING if reasoning_method_str == "hypothesis_testing" else ReasoningMethod.DEDUCTION
        
        return knowledge_base_id, reasoning_method

    def _fetch_variables(self, text: str, variables: List[Variable]) -> Dict[str, Any]:
        variables_info = "\n".join([f"{var.id} - {var.name}" for var in variables])
        prompt = self.prompt_templates.FetchVariablesTemplate.format(variables=variables_info, text=text)
        self.query_history.append({"role": "engine", "text": prompt})
        response = self.pipeline.prompt_text_generation(prompt)
        self.query_history.append({"role": "system", "text": response})
        
        data = self._extract_json_from_response(response)
        
        # Extract variables from JSON
        variables_dict = {}
        for var in variables:
            if var.id in data:
                variables_dict[var.id] = self._parse_variable_value(data[var.id], var)
        
        return variables_dict

    def _parse_variable_value(self, value: str, variable: Variable) -> Any:
        try:
            if isinstance(variable.value, bool):
                return value.lower() in ['true', '1', 'yes']
            elif isinstance(variable.value, int):
                return int(value)
            elif isinstance(variable.value, float):
                return float(value)
            elif isinstance(variable.value, list):
                return value.split(',')
            else:
                return value
        except ValueError:
            return value

    def _ask_for_more_information(self, variables: str) -> str:
        context = "\n".join([f"{entry['role']}: {entry['text']}" for entry in self.query_history if entry['role'] in ['user', 'agent']])
        prompt = self.prompt_templates.AskForMoreInformationTemplate.format(agent_type=self.agent_type, variables=variables, context=context)
        self.query_history.append({"role": "engine", "text": prompt})
        response = self.pipeline.prompt_text_generation(prompt)
        self.query_history.append({"role": "system", "text": response})
        
        # Parse the response
        lines = response.split('\n')
        question = None
        for line in lines:
            if line.startswith("question:"):
                question = line.split(":")[1].strip()
        
        return question

    def _ask_for_reasoning_clarification(self) -> str:
        knowledge_bases_info = "\n".join([f"{kb.name} - {kb.description}" for kb in self.knowledge_bases])
        prompt = self.prompt_templates.AskForReasoningClarificationTemplate.format(agent_type=self.agent_type, knowledge_bases=knowledge_bases_info)
        self.query_history.append({"role": "engine", "text": prompt})
        response = self.pipeline.prompt_text_generation(prompt)
        self.query_history.append({"role": "system", "text": response})
        
        # Parse the response
        lines = response.split('\n')
        question = None
        for line in lines:
            if line.startswith("question:"):
                question = line.split(":")[1].strip()
        
        return question

    def _set_reasoning_process(self, knowledge_base_id: str, reasoning_method: ReasoningMethod) -> bool:
        if reasoning_method is not None and knowledge_base_id is not None:
            knowledge_base = next((kb for kb in self.knowledge_bases if kb.id == knowledge_base_id), None)
            if knowledge_base:
                self.reasoning_process = ReasoningProcess(reasoning_method=reasoning_method, knowledge_base=knowledge_base)
                return True
        return False

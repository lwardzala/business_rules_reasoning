from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Callable, List, Dict, Tuple, Any
import re
import json

from .huggingface_pipeline import HuggingFacePipeline
from .prompt_templates import PromptTemplates
from .retry import retry
from ..base_orchestrator import BaseOrchestrator, OrchestratorStatus
from ..variable_source import VariableSource
from ..reasoning_action import ReasoningAction
from ...base import ReasoningState, ReasoningProcess, ReasoningService, ReasoningMethod, Variable

class HuggingFaceOrchestrator(BaseOrchestrator):
    def __init__(self, model_name: str, knowledge_base_retriever: Callable, inference_state_retriever: Callable, inference_session_id: str = None, actions: List[ReasoningAction] = None, variable_sources: List[VariableSource] = None, prompt_templates = PromptTemplates, agent_type: str = "reasoning agent", tokenizer=None, model=None, device='cuda:0', **kwargs):
        super().__init__(knowledge_base_retriever, inference_state_retriever, inference_session_id, actions, variable_sources)
        self.pipeline = HuggingFacePipeline(model_name, tokenizer, model, device, **kwargs)
        self.query_log: List[Dict[str, str]] = []
        self.prompt_templates = prompt_templates
        self.agent_type: str = agent_type

    def _next_step(self, text: str):
        if self.status == OrchestratorStatus.INITIALIZED:
            def validate_output(result):
                knowledge_base_name, reasoning_method = result
                return knowledge_base_name is not None and reasoning_method is not None and knowledge_base_name in [kb.id for kb in self.knowledge_bases]
            
            knowledge_base_name, reasoning_method = retry(lambda: self._fetch_inference_instructions(text), retries=3, validation_func=validate_output)
            result = self._set_reasoning_process(knowledge_base_name, reasoning_method)
            if result:
                self.status = OrchestratorStatus.STARTED
            else:
                self.status = OrchestratorStatus.WAITING_FOR_QUERY
        
        if self.status == OrchestratorStatus.STARTED:
            self._start_reasoning_process()
        
        if self.status == OrchestratorStatus.ENGINE_WAITING_FOR_VARIABLES:
            missing_variables = self._get_missing_rerasoning_variables()
            missing_variable_ids = [var.id for var in missing_variables]
            def validate_output(variables: dict):
                return all([var in missing_variable_ids for var in variables.keys()])
            
            variables_dict = retry(lambda: self._fetch_variables(text, missing_variables), retries=3, validation_func=validate_output)
            self._set_variables_and_continue_reasoning(variables_dict)

        if self.status == OrchestratorStatus.INFERENCE_FINISHED:
            # TODO: find and fire the actions accordingly to the conclusions
            return
        
        if self.status == OrchestratorStatus.INFERENCE_ERROR:
            return

    def set_session_id(self):
        # Implement the logic to set the session ID
        self.inference_session_id = "hf_session_id"

    def query(self, text: str) -> str:
        self._log_query(text, "user")
        if self.status is None:
            self.start_orchestration()

        # TODO: Handle other query instructions
        # if inference action
        self._next_step(text)

        # TODO: Handle outputs
        if self.status == OrchestratorStatus.WAITING_FOR_QUERY:
            question = self._ask_for_reasoning_clarification()
            self._log_query(question, "agent")
            return question
            
        if self.status == OrchestratorStatus.ENGINE_WAITING_FOR_VARIABLES:
            missing_variables = ", ".join([f"{var.name}" for var in self._get_missing_rerasoning_variables()])
            question = self._ask_for_more_information(missing_variables)
            self._log_query(question, "agent")
            return question
        
        if self.status == OrchestratorStatus.INFERENCE_ERROR:
            self._log_query(self.reasoning_process.reasoning_error_message, "agent")
            return self.reasoning_process.reasoning_error_message
        
        if self.status == OrchestratorStatus.INFERENCE_FINISHED:
            response = self._generate_final_answer()
            self._log_query(response, "agent")
            return response

        self._log_inference(f"[Orchestrator]: Query end.")
        return 'Nothing'

    def _extract_json_from_response(self, response: str) -> dict:
        json_match = re.search(r'\{.*?\}', response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in the response")
        
        json_str = json_match.group().replace('\n', '').replace('}', '}')
        data = json.loads(json_str)
        return data

    def _fetch_inference_instructions(self, text: str) -> Tuple[str, ReasoningMethod]:
        knowledge_bases_info = "\n".join([f"{kb.id} - {kb.description}" for kb in self.knowledge_bases])
        prompt = self.prompt_templates.FetchInferenceInstructionsTemplate.format(knowledge_bases=knowledge_bases_info, text=text)
        self._log_inference(f"[Orchestrator]: Prompting for inference instructions...")
        self._log_query(prompt, "engine")
        response = self.pipeline.prompt_text_generation(prompt)
        self._log_query(response, "system")
        
        data = self._extract_json_from_response(response)
        self._log_inference(f"[Orchestrator]: Retrieved JSON from prompt: {json.dumps(data)}")
        
        knowledge_base_id = data.get("knowledge_base_id")
        reasoning_method_str = data.get("reasoning_method")
        # TODO: Handle reasoning method: hypothesis_testing
        reasoning_method = ReasoningMethod.DEDUCTION #asoning_ ReasoningMethod.DEDUCTION #method = ReasoningMethod.DEDUCTION # ReasoningMethod.HYPOTHESIS_TESTING if reasoning_method_str == "hypothesis_testing" else ReasoningMethod.DEDUCTION
        
        return knowledge_base_id, reasoning_method

    def _fetch_variables(self, text: str, variables: List[Variable]) -> Dict[str, Any]:
        variables_info = "\n".join([f"{var.id} - {var.name}" for var in variables])
        prompt = self.prompt_templates.FetchVariablesTemplate.format(variables=variables_info, text=text)
        self._log_inference(f"[Orchestrator]: Prompting for variables...")
        self._log_query(prompt, "engine")
        response = self.pipeline.prompt_text_generation(prompt)
        self._log_query(response, "system")
        
        data = self._extract_json_from_response(response)
        self._log_inference(f"[Orchestrator]: Retrieved JSON from prompt: {json.dumps(data)}")
        
        # Extract variables from JSON
        variables_dict = {}
        for var in variables:
            if var.id in data:
                variables_dict[var.id] = self._parse_variable_value(data[var.id], var)

        self._log_inference(f"[Orchestrator]: Parsed variables from prompt: {json.dumps(variables_dict)}")
        
        return variables_dict

    def _parse_variable_value(self, value: str, variable: Variable) -> Any:
        try:
            if variable.get_value_type() == 'boolean':
                if isinstance(value, str):
                    return value.lower() in ['true', '1', 'yes']
                else:
                    return bool(value)
            elif variable.get_value_type() == 'number':
                if isinstance(value, str):
                    value = re.sub(r'[^\d.]', '', value)
                return float(value)
            elif variable.get_value_type() == 'list':
                return value.split(',')
            else:
                return value
        except ValueError:
            return value

    def _ask_for_more_information(self, variables: str) -> str:
        context = "\n".join([f"{entry['role']}: {entry['text']}" for entry in self.query_log if entry['role'] in ['user', 'agent']])
        prompt = self.prompt_templates.AskForMoreInformationTemplate.format(agent_type=self.agent_type, variables=variables, context=context)
        self._log_inference(f"[Orchestrator]: Prompting to ask for more information...")
        self._log_query(prompt, "engine")
        response = self.pipeline.prompt_text_generation(prompt)
        self._log_query(response, "system")
        
        return response

    def _ask_for_reasoning_clarification(self) -> str:
        knowledge_bases_info = "\n".join([f"{kb.name} - {kb.description}" for kb in self.knowledge_bases])
        self._log_inference(f"[Orchestrator]: Prompting for reasoning clarification...")
        prompt = self.prompt_templates.AskForReasoningClarificationTemplate.format(agent_type=self.agent_type, knowledge_bases=knowledge_bases_info)
        self._log_query(prompt, "engine")
        response = self.pipeline.prompt_text_generation(prompt)
        self._log_query(response, "system")
        
        return response

    def _set_reasoning_process(self, knowledge_base_id: str, reasoning_method: ReasoningMethod) -> bool:
        if reasoning_method is not None and knowledge_base_id is not None:
            knowledge_base = next((kb for kb in self.knowledge_bases if kb.id == knowledge_base_id), None)
            if knowledge_base:
                self.reasoning_process = ReasoningProcess(reasoning_method=reasoning_method, knowledge_base=knowledge_base)
                return True
        return False
    
    def _log_query(self, text: str, role: str):
        self.query_log.append({"role": role, "text": text})

    def _generate_final_answer(self) -> str:
        if (self.reasoning_process.reasoned_items is None) or (len(self.reasoning_process.reasoned_items) == 0):
            conclusions = "No conclusions were reasoned. Cannot provide the answer based on the provided facts."
        else:
            conclusions = "\n".join([f"{item.display()}" for item in self.reasoning_process.reasoned_items])
        context = "\n".join([entry['text'] for entry in self.query_log if entry['role'] == 'user'])
        prompt = self.prompt_templates.FinishInferenceTemplate.format(agent_type=self.agent_type, conclusions=conclusions, context=context)
        self._log_inference(f"[Orchestrator]: Prompting for answer generation...")
        self._log_query(prompt, "engine")
        response = self.pipeline.prompt_text_generation(prompt)
        self._log_query(response, "system")
        return response

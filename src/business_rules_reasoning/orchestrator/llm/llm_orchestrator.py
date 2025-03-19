from typing import Callable, List, Dict, Tuple, Any
import json

from ...utils import retry, parse_variable_value, extract_json_from_response
from ...base import ReasoningState, ReasoningProcess, ReasoningService, ReasoningMethod, Variable
from ..reasoning_action import ReasoningAction
from ..variable_source import VariableSource
from ..base_orchestrator import BaseOrchestrator, OrchestratorStatus, OrchestratorOptions
from .prompt_templates import PromptTemplates
from .llm_pipeline_base import LLMPipelineBase

class LLMOrchestrator(BaseOrchestrator):
    def __init__(self, knowledge_base_retriever: Callable, inference_state_retriever: Callable, llm: LLMPipelineBase, inference_session_id: str = None, actions: List[ReasoningAction] = None, variable_sources: List[VariableSource] = None, prompt_templates = PromptTemplates, agent_type: str = "reasoning agent", retry_policy: int = 3, options: OrchestratorOptions = OrchestratorOptions(), **kwargs):
        super().__init__(knowledge_base_retriever, inference_state_retriever, options, inference_session_id, actions, variable_sources)
        self.llm = llm
        self.query_log: List[Dict[str, str]] = []
        self.prompt_templates = prompt_templates
        self.agent_type: str = agent_type
        self.retry_policy = retry_policy

    def _next_step(self, text: str):
        if self.status == OrchestratorStatus.INITIALIZED:
            def validate_output(result):
                knowledge_base_name, reasoning_method = result
                return knowledge_base_name is not None and reasoning_method is not None and knowledge_base_name in [kb.id for kb in self.knowledge_bases]
            
            knowledge_base_id, reasoning_method = retry(lambda: self._fetch_inference_instructions(text), retries=self.retry_policy, validation_func=validate_output)
            reasoning_options = {}
            if reasoning_method == ReasoningMethod.HYPOTHESIS_TESTING:
                self._log_inference(f"[Orchestrator]: Hypothesis testing method was selected. Prompting for hypothesis parameters...")
                try:
                    hypothesis = retry(lambda: self._fetch_hypothesis_conclusion(text, knowledge_base_id), retries=self.retry_policy, validation_func=lambda x: x is not None)
                    if hypothesis is None:
                        raise ValueError(f"Hypothesis could not be selected after {self.retry_policy} attempts.")
                    reasoning_options["hypothesis"] = hypothesis
                except Exception as e:
                    reasoning_method = ReasoningMethod.DEDUCTION
                    self._log_inference(f"[Orchestrator]: Error while fetching hypothesis: {str(e)}. Switching to deduction method.")
            
            result = self._set_reasoning_process(knowledge_base_id, reasoning_method, reasoning_options)
            if result:
                self._set_orchestrator_status(OrchestratorStatus.STARTED)
            else:
                self._set_orchestrator_status(OrchestratorStatus.WAITING_FOR_QUERY)
        
        if self.status == OrchestratorStatus.STARTED:
            self._start_reasoning_process()
        
        if self.status == OrchestratorStatus.ENGINE_WAITING_FOR_VARIABLES:
            missing_variables = self._get_missing_rerasoning_variables()
            missing_variable_ids = [var.id for var in missing_variables]
            # def validate_output(variables: dict):
            #     return all([var in missing_variable_ids for var in variables.keys()])
            
            variables_dict = retry(lambda: self._fetch_variables(text, missing_variables), retries=self.retry_policy, validation_func=lambda x: all([var in missing_variable_ids for var in x.keys()]))
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

    def _fetch_inference_instructions(self, text: str) -> Tuple[str, ReasoningMethod]:
        knowledge_bases_info = "\n".join([f"{kb.id} - {kb.description}" for kb in self.knowledge_bases])
        prompt = self.prompt_templates.FetchInferenceInstructionsTemplate.format(knowledge_bases=knowledge_bases_info, text=text)
        self._log_inference(f"[Orchestrator]: Prompting for inference instructions...")
        self._log_query(prompt, "engine")
        response = self.llm.prompt_text_generation(prompt)
        self._log_query(response, "system")
        
        data = extract_json_from_response(response)
        self._log_inference(f"[Orchestrator]: Retrieved JSON from prompt: {json.dumps(data)}")
        
        knowledge_base_id = data.get("knowledge_base_id")
        reasoning_method_str = data.get("reasoning_method")
        reasoning_method = ReasoningMethod.HYPOTHESIS_TESTING if reasoning_method_str == "hypothesis_testing" else ReasoningMethod.DEDUCTION
        
        return knowledge_base_id, reasoning_method

    def _fetch_variables(self, text: str, variables: List[Variable]) -> Dict[str, Any]:
        variables_info = "\n".join([f"{var.id} - {var.name}" for var in variables])
        prompt = self.prompt_templates.FetchVariablesTemplate.format(variables=variables_info, text=text)
        self._log_inference(f"[Orchestrator]: Prompting for variables...")
        self._log_query(prompt, "engine")
        response = self.llm.prompt_text_generation(prompt)
        self._log_query(response, "system")
        
        data = extract_json_from_response(response)
        self._log_inference(f"[Orchestrator]: Retrieved JSON from prompt: {json.dumps(data)}")
        
        # Extract variables from JSON
        variables_dict = {}
        for var in variables:
            if var.id in data:
                parsed_value = parse_variable_value(data[var.id], var)
                if parsed_value is not None:  # Skip variables with None value
                    variables_dict[var.id] = parsed_value

        self._log_inference(f"[Orchestrator]: Parsed variables from prompt: {json.dumps(variables_dict)}")
        
        return variables_dict

    def _ask_for_more_information(self, variables: str) -> str:
        context = "\n".join([f"{entry['role']}: {entry['text']}" for entry in self.query_log if entry['role'] in ['user', 'agent']])
        prompt = self.prompt_templates.AskForMoreInformationTemplate.format(agent_type=self.agent_type, variables=variables, context=context)
        self._log_inference(f"[Orchestrator]: Prompting to ask for more information...")
        self._log_query(prompt, "engine")
        response = self.llm.prompt_text_generation(prompt)
        self._log_query(response, "system")
        
        return response

    def _ask_for_reasoning_clarification(self) -> str:
        knowledge_bases_info = "\n".join([f"{kb.name} - {kb.description}" for kb in self.knowledge_bases])
        self._log_inference(f"[Orchestrator]: Prompting for reasoning clarification...")
        prompt = self.prompt_templates.AskForReasoningClarificationTemplate.format(agent_type=self.agent_type, knowledge_bases=knowledge_bases_info)
        self._log_query(prompt, "engine")
        response = self.llm.prompt_text_generation(prompt)
        self._log_query(response, "system")
        
        return response

    def _set_reasoning_process(self, knowledge_base_id: str, reasoning_method: ReasoningMethod, reasoning_options: dict) -> bool:
        if reasoning_method is not None and knowledge_base_id is not None:
            knowledge_base = next((kb for kb in self.knowledge_bases if kb.id == knowledge_base_id), None)
            if knowledge_base:
                self.reasoning_process = ReasoningProcess(reasoning_method=reasoning_method, knowledge_base=knowledge_base, options=reasoning_options)
                self._log_inference(f"[Orchestrator]: Reasoning process was set with method: {reasoning_method.name} and knowledge base: {knowledge_base_id}")
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
        response = self.llm.prompt_text_generation(prompt)
        self._log_query(response, "system")
        return response

    def _fetch_hypothesis_conclusion(self, text: str, knowledge_base_id: str) -> Variable:
        knowledge_base_rules = next((kb.rule_set for kb in self.knowledge_bases if kb.id == knowledge_base_id), None)
        conclusions_info = "\n".join([f"{rule.conclusion.right_term.id} - {rule.conclusion.right_term.name}" for rule in knowledge_base_rules])
        conclusions = [rule.conclusion.right_term for rule in knowledge_base_rules]

        prompt = self.prompt_templates.FetchHypothesisTestingTemplate.format(conclusions=conclusions_info, text=text)
        self._log_inference(f"[Orchestrator]: Prompting for hypothesis conclusion...")
        self._log_query(prompt, "engine")

        response = self.llm.prompt_text_generation(prompt)
        self._log_query(response, "system")

        data = extract_json_from_response(response)
        self._log_inference(f"[Orchestrator]: Retrieved JSON from prompt: {json.dumps(data)}")

        conclusion_id = data.get("hypothesis_id")
        if not conclusion_id:
            raise ValueError("[Orchestrator]: No matching hypothesis_id found in the response.")
        
        return next((conclusion for conclusion in conclusions if conclusion.id == conclusion_id), None)

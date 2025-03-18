import unittest
from unittest.mock import MagicMock, patch
from transformers import AutoTokenizer, AutoModelForCausalLM
from src.business_rules_reasoning.orchestrator.llm.huggingface_orchestrator import HuggingFaceOrchestrator, PromptTemplates, OrchestratorStatus
from src.business_rules_reasoning.base import KnowledgeBase, ReasoningProcess, ReasoningMethod, Variable, Rule, ReasoningType, ReasoningState, EvaluationMessage
from src.business_rules_reasoning.deductive import DeductivePredicate
from src.business_rules_reasoning.base.operator_enums import OperatorType

class TestHuggingFaceOrchestrator(unittest.TestCase):
    def setUp(self):
        self.mock_tokenizer = MagicMock(spec=AutoTokenizer)
        self.mock_model = MagicMock(spec=AutoModelForCausalLM)
        self.knowledge_base_retriever = MagicMock()
        self.inference_state_retriever = MagicMock()
        self.orchestrator = HuggingFaceOrchestrator(
            model_name="mock-model",
            knowledge_base_retriever=self.knowledge_base_retriever,
            inference_state_retriever=self.inference_state_retriever,
            tokenizer=self.mock_tokenizer,
            model=self.mock_model
        )

    @patch('src.business_rules_reasoning.orchestrator.llm.huggingface_pipeline.HuggingFacePipeline.prompt_text_generation')
    def test_fetch_inference_instructions(self, mock_prompt_text_gen):
        mock_prompt_text_gen.return_value = ' { "knowledge_base_id": "kb1", "reasoning_method": "deduction" }\nreasoning_method: deduction'
        self.orchestrator.knowledge_bases = [KnowledgeBase(id="kb1", name="KB1", description="Test KB")]
        knowledge_base_id, reasoning_method = self.orchestrator._fetch_inference_instructions("test query")
        self.assertEqual(knowledge_base_id, "kb1")
        self.assertEqual(reasoning_method, ReasoningMethod.DEDUCTION)

    @patch('src.business_rules_reasoning.orchestrator.llm.huggingface_pipeline.HuggingFacePipeline.prompt_text_generation')
    def test_fetch_variables(self, mock_prompt_text_gen):
        mock_prompt_text_gen.return_value = '{"var1": 39,\n     "var2": "true"} {"var3":0}'
        variables = [
            Variable(id="var1", name="Variable 1", value=0),
            Variable(id="var2", name="Variable 2", value=False)
        ]
        variables_dict = self.orchestrator._fetch_variables("test query", variables)
        self.assertEqual(variables_dict["var1"], 39)
        self.assertEqual(variables_dict["var2"], True)

    @patch('src.business_rules_reasoning.orchestrator.llm.huggingface_pipeline.HuggingFacePipeline.prompt_text_generation')
    def test_fetch_variables_string_to_int(self, mock_prompt_text_gen):
        mock_prompt_text_gen.return_value = '{"var1": "39",\n     "var2": "true"} {"var3":0}'
        variables = [
            Variable(id="var1", name="Variable 1", value=0),
            Variable(id="var2", name="Variable 2", value=False)
        ]
        variables_dict = self.orchestrator._fetch_variables("test query", variables)
        self.assertEqual(variables_dict["var1"], 39)
        self.assertEqual(variables_dict["var2"], True)

    # @patch('src.business_rules_reasoning.orchestrator.llm.huggingface_pipeline.HuggingFacePipeline.prompt_text_generation')
    # def test_ask_for_more_information(self, mock_prompt_text_gen):
    #     mock_prompt_text_gen.return_value = "question: Can you provide more details about var1?"
    #     self.orchestrator.query_log = [
    #         {"role": "user", "text": "Initial query"},
    #         {"role": "agent", "text": "Response from agent"}
    #     ]
    #     question = self.orchestrator._ask_for_more_information("var1")
    #     self.assertEqual(question, "Can you provide more details about var1?")

    # @patch('src.business_rules_reasoning.orchestrator.llm.huggingface_pipeline.HuggingFacePipeline.prompt_text_generation')
    # def test_ask_for_reasoning_clarification(self, mock_prompt_text_gen):
    #     mock_prompt_text_gen.return_value = "question: Can you clarify the reasoning needed?"
    #     self.orchestrator.knowledge_bases = [KnowledgeBase(name="KB1", description="Test KB")]
    #     question = self.orchestrator._ask_for_reasoning_clarification()
    #     self.assertEqual(question, "Can you clarify the reasoning needed?")

    def test_set_reasoning_process(self):
        knowledge_base = KnowledgeBase(id="kb1", name="KBbb1", description="Test KB")
        self.orchestrator.knowledge_bases = [knowledge_base]
        result = self.orchestrator._set_reasoning_process("kb1", ReasoningMethod.DEDUCTION)
        self.assertTrue(result)
        self.assertIsNotNone(self.orchestrator.reasoning_process)
        self.assertEqual(self.orchestrator.reasoning_process.knowledge_base.id, "kb1")
        self.assertEqual(self.orchestrator.reasoning_process.reasoning_method, ReasoningMethod.DEDUCTION)

    @patch('src.business_rules_reasoning.orchestrator.llm.huggingface_pipeline.HuggingFacePipeline.prompt_text_generation')
    def test_next_step_with_reasoning_process_and_missing_variables(self, mock_prompt_text_gen):
        # Set up the mock response for fetching variables
        mock_prompt_text_gen.return_value = '{"var1": 39, "var2": True}'
        
        # Set up the knowledge base and reasoning process
        knowledge_base = KnowledgeBase(id="kb1", name="KB1", description="Test KB", reasoning_type=ReasoningType.CRISP)
        
        # Create variables
        var1 = Variable(id="var1", name="Variable 1", value=0)
        var2 = Variable(id="var2", name="Variable 2", value=True)
        
        # Create predicates
        predicate1 = DeductivePredicate(left_term=var1, right_term=Variable(id="var1", value=10), operator=OperatorType.GREATER_THAN)
        predicate2 = DeductivePredicate(left_term=var2, right_term=Variable(id="var2", value=True), operator=OperatorType.LESS_THAN)
        
        # Create rule
        rule = Rule(predicates=[predicate1, predicate2], conclusion=DeductivePredicate(left_term=Variable(), right_term=Variable(id="conclusion", value=True), operator=OperatorType.EQUAL))
        
        # Add rule to knowledge base
        knowledge_base.rule_set.append(rule)
        
        self.orchestrator.knowledge_bases = [knowledge_base]
        self.orchestrator.reasoning_process = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=knowledge_base)
        self.orchestrator._start_reasoning_process()
        self.orchestrator.status = OrchestratorStatus.ENGINE_WAITING_FOR_VARIABLES
        
        # Set up the missing variables
        missing_variables = [var1, var2]
        self.orchestrator.get_reasoning_service().get_all_missing_variables = MagicMock(return_value=missing_variables)
        self.orchestrator._fetch_variables = MagicMock(return_value={"var1": 39, "var2": True})
        
        # Call _next_step
        self.orchestrator._next_step("test query mock")
        
        # Check the status
        self.assertEqual(self.orchestrator.reasoning_process.evaluation_message, EvaluationMessage.FAILED)
        self.assertEqual(self.orchestrator.reasoning_process.state, ReasoningState.FINISHED)
        self.assertEqual(self.orchestrator.status, OrchestratorStatus.INFERENCE_FINISHED)

    def test_parse_variable_value(self):
        # Test parsing boolean value
        variable = Variable(id="var1", name="Variable 1", value=True)
        parsed_value = self.orchestrator._parse_variable_value("true", variable)
        self.assertTrue(parsed_value)

        # Test parsing boolean value 'yes'
        variable = Variable(id="var1", name="Variable 1", value=True)
        parsed_value = self.orchestrator._parse_variable_value("yes", variable)
        self.assertTrue(parsed_value)
        
        # Test parsing integer value
        variable = Variable(id="var2", name="Variable 2", value=0)
        parsed_value = self.orchestrator._parse_variable_value("123", variable)
        self.assertEqual(parsed_value, 123)
        
        # Test parsing float value
        variable = Variable(id="var3", name="Variable 3", value=0.0)
        parsed_value = self.orchestrator._parse_variable_value("123.45", variable)
        self.assertEqual(parsed_value, 123.45)
        
        # Test parsing list value
        variable = Variable(id="var4", name="Variable 4", value=[])
        parsed_value = self.orchestrator._parse_variable_value("1,2,3", variable)
        self.assertEqual(parsed_value, ["1", "2", "3"])
        
        # Test parsing string value
        variable = Variable(id="var5", name="Variable 5", value="")
        parsed_value = self.orchestrator._parse_variable_value("test", variable)
        self.assertEqual(parsed_value, "test")

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock, patch
from src.business_rules_reasoning.base import KnowledgeBase, ReasoningProcess, ReasoningMethod, Variable, Rule, ReasoningType, ReasoningState, EvaluationMessage
from src.business_rules_reasoning.base.operator_enums import OperatorType
from src.business_rules_reasoning.deductive import DeductivePredicate, DeductiveConclusion
from src.business_rules_reasoning.orchestrator import OrchestratorStatus
from src.business_rules_reasoning.orchestrator.llm import HuggingFacePipeline, LLMOrchestrator, PromptTemplates

class TestHuggingFaceOrchestrator(unittest.TestCase):
    def setUp(self):
        self.knowledge_base_retriever = MagicMock()
        self.inference_state_retriever = MagicMock()
        self.llm = MagicMock(spec=HuggingFacePipeline)
        self.orchestrator = LLMOrchestrator(
            knowledge_base_retriever=self.knowledge_base_retriever,
            inference_state_retriever=self.inference_state_retriever,
            llm=self.llm
        )

    def test_fetch_inference_instructions(self):
        self.orchestrator.llm.prompt_text_generation.return_value = ' { "knowledge_base_id": "kb1", "reasoning_method": "deduction" }\nreasoning_method: deduction'
        self.orchestrator.knowledge_bases = [KnowledgeBase(id="kb1", name="KB1", description="Test KB")]
        knowledge_base_id, reasoning_method = self.orchestrator._fetch_inference_instructions("test query")
        self.assertEqual(knowledge_base_id, "kb1")
        self.assertEqual(reasoning_method, ReasoningMethod.DEDUCTION)

    def test_fetch_variables(self):
        self.orchestrator.llm.prompt_text_generation.return_value = '{"var1": 39,\n     "var2": "true"} {"var3":0}'
        variables = [
            Variable(id="var1", name="Variable 1", value=0),
            Variable(id="var2", name="Variable 2", value=False)
        ]
        variables_dict = self.orchestrator._fetch_variables("test query", variables)
        self.assertEqual(variables_dict["var1"], 39)
        self.assertEqual(variables_dict["var2"], True)

    def test_fetch_variables_string_to_int(self):
        self.orchestrator.llm.prompt_text_generation.return_value = '{"var1": "39",\n     "var2": "true"} {"var3":0}'
        variables = [
            Variable(id="var1", name="Variable 1", value=0),
            Variable(id="var2", name="Variable 2", value=False)
        ]
        variables_dict = self.orchestrator._fetch_variables("test query", variables)
        self.assertEqual(variables_dict["var1"], 39)
        self.assertEqual(variables_dict["var2"], True)

    def test_set_reasoning_process(self):
        knowledge_base = KnowledgeBase(id="kb1", name="KBbb1", description="Test KB")
        self.orchestrator.knowledge_bases = [knowledge_base]
        result = self.orchestrator._set_reasoning_process("kb1", ReasoningMethod.DEDUCTION, {})
        self.assertTrue(result)
        self.assertIsNotNone(self.orchestrator.reasoning_process)
        self.assertEqual(self.orchestrator.reasoning_process.knowledge_base.id, "kb1")
        self.assertEqual(self.orchestrator.reasoning_process.reasoning_method, ReasoningMethod.DEDUCTION)

    def test_next_step_with_reasoning_process_and_missing_variables(self):
        # Set up the mock response for fetching variables
        self.orchestrator.llm.prompt_text_generation.return_value = '{"var1": 39, "var2": True}'
        
        # Set up the knowledge base and reasoning process
        knowledge_base = KnowledgeBase(id="kb1", name="KB1", description="Test KB", reasoning_type=ReasoningType.CRISP)
        
        # Create variables
        var1 = Variable(id="var1", name="Variable 1", value=0)
        var2 = Variable(id="var2", name="Variable 2", value=True)
        
        # Create predicates
        predicate1 = DeductivePredicate(left_term=var1, right_term=Variable(id="var1", value=10), operator=OperatorType.GREATER_THAN)
        predicate2 = DeductivePredicate(left_term=var2, right_term=Variable(id="var2", value=True), operator=OperatorType.LESS_THAN)
        
        # Create rule
        rule = Rule(predicates=[predicate1, predicate2], conclusion=DeductiveConclusion(Variable(id="conclusion", value=True)))
        
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

    def test_fetch_hypothesis_conclusion_success(self):
        # Mock knowledge base and rules
        variable1 = Variable(id="hypothesis1", name="Hypothesis 1", value=True)
        variable2 = Variable(id="hypothesis2", name="Hypothesis 2", value=False)
        rule1 = Rule(conclusion=DeductivePredicate(left_term=variable1, right_term=variable1, operator=OperatorType.EQUAL))
        rule2 = Rule(conclusion=DeductivePredicate(left_term=variable2, right_term=variable2, operator=OperatorType.EQUAL))
        knowledge_base = KnowledgeBase(id="kb1", rule_set=[rule1, rule2])
        self.orchestrator.knowledge_bases = [knowledge_base]

        # Mock LLM response
        self.llm.prompt_text_generation.return_value = '{"hypothesis_id": "hypothesis1"}'

        # Call the function
        result = self.orchestrator._fetch_hypothesis_conclusion("test query", "kb1")

        # Assertions
        self.assertEqual(result.id, "hypothesis1")
        self.assertEqual(result.name, "Hypothesis 1")
        # self.llm.prompt_text_generation.assert_called_once()

    def test_fetch_hypothesis_conclusion_no_match(self):
        # Mock knowledge base and rules
        variable1 = Variable(id="hypothesis1", name="Hypothesis 1", value=True)
        rule1 = Rule(conclusion=DeductivePredicate(left_term=variable1, right_term=variable1, operator=OperatorType.EQUAL))
        knowledge_base = KnowledgeBase(id="kb1", rule_set=[rule1])
        self.orchestrator.knowledge_bases = [knowledge_base]

        # Mock LLM response with an invalid conclusion_id
        self.llm.prompt_text_generation.return_value = '{"wrongname_id": "hypothesis2"}'

        # Call the function and assert it raises an exception
        with self.assertRaises(ValueError) as context:
            self.orchestrator._fetch_hypothesis_conclusion("test query", "kb1")
        self.assertIn("[Orchestrator]: No matching hypothesis_id found in the response.", str(context.exception))
        # self.llm.prompt_text_generation.assert_called_once()

    def test_fetch_hypothesis_conclusion_invalid_response(self):
        # Mock knowledge base and rules
        variable1 = Variable(id="hypothesis1", name="Hypothesis 1", value=True)
        rule1 = Rule(conclusion=DeductivePredicate(left_term=variable1, right_term=variable1, operator=OperatorType.EQUAL))
        knowledge_base = KnowledgeBase(id="kb1", rule_set=[rule1])
        self.orchestrator.knowledge_bases = [knowledge_base]

        # Mock LLM response with no JSON
        self.llm.prompt_text_generation.return_value = "Invalid response"

        # Call the function and assert it raises an exception
        with self.assertRaises(ValueError) as context:
            self.orchestrator._fetch_hypothesis_conclusion("test query", "kb1")
        self.assertIn("No JSON object found in the response", str(context.exception))
        # self.llm.prompt_text_generation.assert_called_once()

    def test_fetch_hypothesis_conclusion_success(self):
        # Mock knowledge base and rules
        variable1 = Variable(id="hypothesis1", name="Hypothesis 1", value=True)
        variable2 = Variable(id="hypothesis2", name="Hypothesis 2", value=True)
        rule1 = Rule(conclusion=DeductiveConclusion(variable1))
        rule2 = Rule(conclusion=DeductiveConclusion(variable2))
        knowledge_base = KnowledgeBase(id="kb1", rule_set=[rule1, rule2])
        self.orchestrator.knowledge_bases = [knowledge_base]

        # Mock LLM response
        self.orchestrator.llm.prompt_text_generation.return_value = '{"hypothesis_id": "hypothesis1", "hypothesis_value": "false"}'

        # Call the function
        result = self.orchestrator._fetch_hypothesis_conclusion("test query", "kb1")

        # Assertions
        self.assertEqual(result.id, "hypothesis1")
        self.assertEqual(result.name, "Hypothesis 1")
        self.assertFalse(result.value)

    def test_fetch_hypothesis_conclusion_no_match(self):
        # Mock knowledge base and rules
        variable1 = Variable(id="hypothesis1", name="Hypothesis 1", value=True)
        rule1 = Rule(conclusion=DeductiveConclusion(variable1))
        knowledge_base = KnowledgeBase(id="kb1", rule_set=[rule1])
        self.orchestrator.knowledge_bases = [knowledge_base]

        # Mock LLM response with an invalid hypothesis_id
        self.orchestrator.llm.prompt_text_generation.return_value = '{"hypothesis_id": "invalid_id"}'

        # Call the function and assert it raises an exception
        with self.assertRaises(ValueError) as context:
            self.orchestrator._fetch_hypothesis_conclusion("test query", "kb1")
        self.assertIn("[Orchestrator]: Could not found any conclusion.", str(context.exception))
        self.orchestrator.llm.prompt_text_generation.assert_called_once()

    def test_fetch_hypothesis_conclusion_invalid_response(self):
        # Mock knowledge base and rules
        variable1 = Variable(id="hypothesis1", name="Hypothesis 1", value=None)
        rule1 = Rule(conclusion=DeductiveConclusion(variable1))
        knowledge_base = KnowledgeBase(id="kb1", rule_set=[rule1])
        self.orchestrator.knowledge_bases = [knowledge_base]

        # Mock LLM response with no JSON
        self.orchestrator.llm.prompt_text_generation.return_value = "Invalid response"

        # Call the function and assert it raises an exception
        with self.assertRaises(ValueError) as context:
            self.orchestrator._fetch_hypothesis_conclusion("test query", "kb1")
        self.assertIn("No JSON object found in the response", str(context.exception))

    def test_fetch_hypothesis_conclusion_missing_value(self):
        # Mock knowledge base and rules
        variable1 = Variable(id="hypothesis1", name="Hypothesis 1", value=True)
        rule1 = Rule(conclusion=DeductiveConclusion(variable1))
        knowledge_base = KnowledgeBase(id="kb1", rule_set=[rule1])
        self.orchestrator.knowledge_bases = [knowledge_base]

        # Mock LLM response with missing hypothesis_value
        self.orchestrator.llm.prompt_text_generation.return_value = '{"hypothesis_id": "hypothesis1"}'

        # Call the function and assert it raises an exception
        with self.assertRaises(ValueError) as context:
            self.orchestrator._fetch_hypothesis_conclusion("test query", "kb1")
        self.assertIn("[Orchestrator]: No matching hypothesis_value found in the response.", str(context.exception))

if __name__ == '__main__':
    unittest.main()

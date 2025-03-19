import unittest
from unittest.mock import MagicMock, patch
from src.business_rules_reasoning.orchestrator.base_orchestrator import BaseOrchestrator, OrchestratorStatus, OrchestratorOptions, VariablesFetchingMode
from src.business_rules_reasoning.base import KnowledgeBase, ReasoningProcess, ReasoningMethod, Variable, Rule, ReasoningType, ReasoningState, EvaluationMessage
from src.business_rules_reasoning.deductive import DeductivePredicate
from src.business_rules_reasoning.base.operator_enums import OperatorType

class TestBaseOrchestrator(BaseOrchestrator):
    def _next_step(self):
        pass

    def set_session_id(self):
        self.inference_session_id = "test_session_id"

class TestBaseOrchestratorMethods(unittest.TestCase):
    def setUp(self):
        self.knowledge_base_retriever = MagicMock()
        self.inference_state_retriever = MagicMock()
        self.orchestrator = TestBaseOrchestrator(
            knowledge_base_retriever=self.knowledge_base_retriever,
            inference_state_retriever=self.inference_state_retriever,
            options=OrchestratorOptions()
        )

    def test_start_orchestration(self):
        self.orchestrator.start_orchestration()
        self.assertEqual(self.orchestrator.status, OrchestratorStatus.INITIALIZED)

    def test_reset_orchestration(self):
        self.orchestrator.reset_orchestration()
        self.assertEqual(self.orchestrator.status, OrchestratorStatus.INITIALIZED)
        self.assertEqual(self.orchestrator.inference_session_id, 'test_session_id')
        self.assertIsNone(self.orchestrator.reasoning_process)

    def test_start_reasoning_process(self):
        knowledge_base = KnowledgeBase(id="kb1", name="KB1", description="Test KB", reasoning_type=ReasoningType.CRISP)
        self.orchestrator.reasoning_process = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=knowledge_base)
        self.orchestrator._start_reasoning_process()
        self.assertEqual(self.orchestrator.reasoning_process.state, ReasoningState.FINISHED)

    def test_get_missing_rerasoning_variables(self):
        knowledge_base = KnowledgeBase(id="kb1", name="KB1", description="Test KB", reasoning_type=ReasoningType.CRISP)
        var1 = Variable(id="var1", name="Variable 1", value=None)
        var2 = Variable(id="var2", name="Variable 2", value=None)
        predicate1 = DeductivePredicate(left_term=var1, right_term=Variable(id="var1", value=10), operator=OperatorType.GREATER_THAN)
        predicate2 = DeductivePredicate(left_term=var2, right_term=Variable(id="var2", value=20), operator=OperatorType.LESS_THAN)
        rule = Rule(predicates=[predicate1, predicate2], conclusion=DeductivePredicate(left_term=Variable(), right_term=Variable(id="conclusion", value=True), operator=OperatorType.EQUAL))
        knowledge_base.rule_set.append(rule)
        self.orchestrator.reasoning_process = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=knowledge_base)
        missing_variables = self.orchestrator._get_missing_rerasoning_variables()
        self.assertEqual(len(missing_variables), 2)
        self.assertEqual(missing_variables[0].id, "var1")
        self.assertEqual(missing_variables[1].id, "var2")

    def test_set_variables_and_continue_reasoning(self):
        knowledge_base = KnowledgeBase(id="kb1", name="KB1", description="Test KB", reasoning_type=ReasoningType.CRISP)
        var1 = Variable(id="var1", name="Variable 1", value=None)
        var2 = Variable(id="var2", name="Variable 2", value=None)
        predicate1 = DeductivePredicate(left_term=var1, right_term=Variable(id="var1", value=10), operator=OperatorType.GREATER_THAN)
        predicate2 = DeductivePredicate(left_term=var2, right_term=Variable(id="var2", value=20), operator=OperatorType.LESS_THAN)
        rule = Rule(predicates=[predicate1, predicate2], conclusion=DeductivePredicate(left_term=Variable(), right_term=Variable(id="conclusion", value=True), operator=OperatorType.EQUAL))
        knowledge_base.rule_set.append(rule)
        self.orchestrator.reasoning_process = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=knowledge_base)
        variables_dict = {"var1": 15, "var2": 5}
        self.orchestrator._set_variables_and_continue_reasoning(variables_dict)
        self.assertEqual(self.orchestrator.reasoning_process.state, ReasoningState.FINISHED)

class TestBaseOrchestratorOptions(unittest.TestCase):
    def test_default_options(self):
        options = OrchestratorOptions()
        self.assertEqual(options.variables_fetching, VariablesFetchingMode.ALL_POSSIBLE)

    def test_custom_options(self):
        options = OrchestratorOptions(variables_fetching=VariablesFetchingMode.STEP_BY_STEP)
        self.assertEqual(options.variables_fetching, VariablesFetchingMode.STEP_BY_STEP)

    def test_orchestrator_with_options(self):
        options = OrchestratorOptions(variables_fetching=VariablesFetchingMode.STEP_BY_STEP)
        orchestrator = TestBaseOrchestrator(
            knowledge_base_retriever=MagicMock(),
            inference_state_retriever=MagicMock(),
            options=options
        )
        self.assertEqual(orchestrator.options.variables_fetching, VariablesFetchingMode.STEP_BY_STEP)

if __name__ == '__main__':
    unittest.main()

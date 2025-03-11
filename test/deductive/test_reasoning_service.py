import unittest
from src.business_rules_reasoning.base.reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod
from src.business_rules_reasoning.base import ReasoningProcess, KnowledgeBase, Rule, Variable
from src.business_rules_reasoning.deductive.deductive_predicate import DeductivePredicate
from src.business_rules_reasoning.deductive import DeductiveReasoningService
from src.business_rules_reasoning.base import OperatorType

class TestReasoningService(unittest.TestCase):
    def test_start_reasoning(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.start_reasoning(rp)
        self.assertEqual(result.state, ReasoningState.STOPPED)

    # todo fix this test
    # def test_continue_reasoning(self):
    #     rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION)
    #     result = ReasoningService.continue_reasoning(rp)
    #     self.assertEqual(result.state, ReasoningState.FINISHED)

    def test_set_values(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        variables = {"1": 5}
        result = DeductiveReasoningService.set_values(rp, variables)
        self.assertEqual(left_term.value, 5)

    def test_reset_reasoning(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.reset_reasoning(rp)
        self.assertEqual(result.state, ReasoningState.INITIALIZED)
        self.assertEqual(result.reasoned_items, [])
        self.assertEqual(result.evaluation_message, EvaluationMessage.NONE)

    def test_clear_reasoning(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.clear_reasoning(rp)
        self.assertEqual(result.state, ReasoningState.INITIALIZED)
        self.assertEqual(result.reasoned_items, [])
        self.assertEqual(result.evaluation_message, EvaluationMessage.NONE)

    def test_get_all_missing_variable_ids(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.get_all_missing_variable_ids(rp)
        self.assertEqual(result, ["1"])

    def test_get_all_missing_variables(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.get_all_missing_variables(rp)
        self.assertEqual(result[0].id, "1")

    def test_analyze_variables_frequency(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.analyze_variables_frequency(rp)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].frequency, 1)

    def test_deduction(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=5)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.deduction(rp)
        self.assertEqual(result.state, ReasoningState.FINISHED)
        self.assertEqual(result.evaluation_message, EvaluationMessage.PASSED)

    def test_hypothesis_testing(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=5)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        rp.options = type('obj', (object,), {'hypothesis': right_term})
        result = DeductiveReasoningService.hypothesis_testing(rp)
        self.assertEqual(result.state, ReasoningState.FINISHED)
        self.assertEqual(result.evaluation_message, EvaluationMessage.PASSED)

if __name__ == '__main__':
    unittest.main()

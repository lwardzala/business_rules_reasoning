import unittest
from src.business_rules_reasoning.base import KnowledgeBase, Rule, Variable, ReasoningProcess, ReasoningMethod, ReasoningState, EvaluationMessage, ReasoningType
from src.business_rules_reasoning.deductive import DeductivePredicate
from src.business_rules_reasoning.base.operator_enums import OperatorType

class TestReasoningProcessDisplayState(unittest.TestCase):
    def test_display_state(self):
        # Create variables
        var1 = Variable(id="var1", name="Variable 1", value=5)
        var2 = Variable(id="var2", name="Variable 2", value=15)
        
        # Create predicates
        predicate1 = DeductivePredicate(left_term=var1, right_term=Variable(id="var1", value=10), operator=OperatorType.GREATER_THAN)
        predicate2 = DeductivePredicate(left_term=var2, right_term=Variable(id="var2", value=20), operator=OperatorType.LESS_THAN)
        
        # Create rule
        rule = Rule(predicates=[predicate1, predicate2], conclusion=DeductivePredicate(left_term=Variable(id="conclusion", value=True), right_term=Variable(id="conclusion", value=True), operator=OperatorType.EQUAL))
        
        # Create knowledge base
        knowledge_base = KnowledgeBase(id="kb1", name="KB1", description="Test KB", rule_set=[rule], reasoning_type=ReasoningType.CRISP)
        
        # Create reasoning process
        reasoning_process = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=knowledge_base)
        
        # Expected display string
        expected_display = (
            "(var1 > 10 (Provided: 5, Status: Not Evaluated, Result: False) ∧ var2 < 20 (Provided: 15, Status: Not Evaluated, Result: False)) → conclusion = True\n"
            "Rule Status: Not Evaluated, Rule Result: False\n\n"
            "State: INITIALIZED\n"
            "Evaluation Message: NONE\n"
            "Reasoned Items: \n\n"
            "Reasoning Method: DEDUCTION\n"
            "Knowledge Base Type: CRISP"
        )
        
        # Check the display output
        self.assertEqual(reasoning_process.display_state(), expected_display)

    def test_display_state_with_error(self):
        # Create variables
        var1 = Variable(id="var1", name="Variable 1", value=5)
        var2 = Variable(id="var2", name="Variable 2", value=15)
        
        # Create predicates
        predicate1 = DeductivePredicate(left_term=var1, right_term=Variable(id="var1", value=10), operator=OperatorType.GREATER_THAN)
        predicate2 = DeductivePredicate(left_term=var2, right_term=Variable(id="var2", value=20), operator=OperatorType.LESS_THAN)
        
        # Create rule
        rule = Rule(predicates=[predicate1, predicate2], conclusion=DeductivePredicate(left_term=Variable(id="conclusion", value=True), right_term=Variable(id="conclusion", value=True), operator=OperatorType.EQUAL))
        
        # Create knowledge base
        knowledge_base = KnowledgeBase(id="kb1", name="KB1", description="Test KB", rule_set=[rule], reasoning_type=ReasoningType.CRISP)
        
        # Create reasoning process
        reasoning_process = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=knowledge_base)
        reasoning_process.state = ReasoningState.FINISHED
        reasoning_process.evaluation_message = EvaluationMessage.ERROR
        reasoning_process.reasoning_error_message = "An error occurred"
        
        # Expected display string
        expected_display = (
            "(var1 > 10 (Provided: 5, Status: Not Evaluated, Result: False) ∧ var2 < 20 (Provided: 15, Status: Not Evaluated, Result: False)) → conclusion = True\n"
            "Rule Status: Not Evaluated, Rule Result: False\n\n"
            "State: FINISHED\n"
            "Evaluation Message: ERROR\n"
            "Reasoned Items: \n"
            "Error Message: An error occurred\n"
            "Reasoning Method: DEDUCTION\n"
            "Knowledge Base Type: CRISP"
        )
        
        # Check the display output
        self.assertEqual(reasoning_process.display_state(), expected_display)

    def test_display_state_with_reasoned_items(self):
        # Create variables
        var1 = Variable(id="var1", name="Variable 1", value=5)
        var2 = Variable(id="var2", name="Variable 2", value=15)
        
        # Create predicates
        predicate1 = DeductivePredicate(left_term=var1, right_term=Variable(id="var1", value=10), operator=OperatorType.GREATER_THAN)
        predicate2 = DeductivePredicate(left_term=var2, right_term=Variable(id="var2", value=20), operator=OperatorType.LESS_THAN)
        
        # Create rule
        rule = Rule(predicates=[predicate1, predicate2], conclusion=DeductivePredicate(left_term=Variable(id="conclusion", value=True), right_term=Variable(id="conclusion", value=True), operator=OperatorType.EQUAL))
        
        # Create knowledge base
        knowledge_base = KnowledgeBase(id="kb1", name="KB1", description="Test KB", rule_set=[rule], reasoning_type=ReasoningType.CRISP)
        
        # Create reasoning process
        reasoning_process = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=knowledge_base)
        reasoning_process.reasoned_items = [Variable(id="conclusion", value=True)]
        
        # Expected display string
        expected_display = (
            "(var1 > 10 (Provided: 5, Status: Not Evaluated, Result: False) ∧ var2 < 20 (Provided: 15, Status: Not Evaluated, Result: False)) → conclusion = True\n"
            "Rule Status: Not Evaluated, Rule Result: False\n\n"
            "State: INITIALIZED\n"
            "Evaluation Message: NONE\n"
            "Reasoned Items: conclusion = True\n\n"
            "Reasoning Method: DEDUCTION\n"
            "Knowledge Base Type: CRISP"
        )
        
        # Check the display output
        self.assertEqual(reasoning_process.display_state(), expected_display)

if __name__ == '__main__':
    unittest.main()

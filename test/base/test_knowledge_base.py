import unittest
from src.business_rules_reasoning.base import KnowledgeBase, Rule, Variable
from src.business_rules_reasoning.deductive import DeductivePredicate
from src.business_rules_reasoning.base.operator_enums import OperatorType

class TestKnowledgeBaseDisplay(unittest.TestCase):
    def test_display(self):
        # Create variables
        var1 = Variable(id="var1", name="Variable 1", value=None)
        var2 = Variable(id="var2", name="Variable 2", value=None)
        
        # Create predicates
        predicate1 = DeductivePredicate(left_term=var1, right_term=Variable(id="var1", value=10), operator=OperatorType.GREATER_THAN)
        predicate2 = DeductivePredicate(left_term=var2, right_term=Variable(id="var2", value=20), operator=OperatorType.LESS_THAN)
        
        # Create rule
        rule = Rule(predicates=[predicate1, predicate2], conclusion=DeductivePredicate(left_term=Variable(id="conclusion", value=True), right_term=Variable(id="conclusion", value=True), operator=OperatorType.EQUAL))
        
        # Create knowledge base
        knowledge_base = KnowledgeBase(id="kb1", name="KB1", description="Test KB", rule_set=[rule])
        
        # Expected display string
        expected_display = "(var1 > 10 ∧ var2 < 20) → conclusion = True"
        
        # Check the display output
        self.assertEqual(knowledge_base.display(), expected_display)

if __name__ == '__main__':
    unittest.main()

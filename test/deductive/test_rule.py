import unittest
from src.base.rule import Rule
from src.base.variable import Variable
from src.deductive.deductive_predicate import DeductivePremise
from src.base import OperatorType

class TestRule(unittest.TestCase):
    def test_initialization(self):
        left_term = Variable(id="1", value=5)
        right_term = Variable(id="2", value=10)
        conclusion = DeductivePremise(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion)
        self.assertEqual(rule.conclusion, conclusion)
        self.assertEqual(rule.predicates, [])
        self.assertFalse(rule.result)
        self.assertFalse(rule.evaluated)

    def test_evaluate(self):
        left_term = Variable(id="1", value=5)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePremise(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePremise(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        rule.evaluate()
        self.assertTrue(rule.result)
        self.assertTrue(rule.evaluated)

    def test_is_valid(self):
        left_term = Variable(id="1", value=5)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePremise(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePremise(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        self.assertTrue(rule.is_valid())

    def test_reset_evaluation(self):
        left_term = Variable(id="1", value=5)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePremise(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePremise(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        rule.evaluate()
        rule.reset_evaluation()
        self.assertFalse(rule.result)
        self.assertFalse(rule.evaluated)

    def test_set_variables(self):
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePremise(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePremise(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        variables = {"1": 5}
        rule.set_variables(variables)
        self.assertEqual(left_term.value, 5)

if __name__ == '__main__':
    unittest.main()

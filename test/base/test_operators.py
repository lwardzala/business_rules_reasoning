import unittest
from src.business_rules_reasoning.base.value_types import BaseType, ListType
from src.business_rules_reasoning.base.operators import Between, GreaterOrEqual, GreaterThan, LessOrEqual, LessThan, NotBetween, NotSubset, Subset

class TestOperators(unittest.TestCase):
    def test_between(self):
        operator = Between()
        left_term = BaseType(5)
        right_term = ListType([1, 10])
        self.assertTrue(operator.compare(left_term, right_term))
        left_term = BaseType(11)
        self.assertFalse(operator.compare(left_term, right_term))

    def test_greater_or_equal(self):
        operator = GreaterOrEqual()
        left_term = BaseType(10)
        right_term = BaseType(5)
        self.assertTrue(operator.compare(left_term, right_term))
        left_term = BaseType(5)
        self.assertTrue(operator.compare(left_term, right_term))
        left_term = BaseType(4)
        self.assertFalse(operator.compare(left_term, right_term))

    def test_greater_than(self):
        operator = GreaterThan()
        left_term = BaseType(10)
        right_term = BaseType(5)
        self.assertTrue(operator.compare(left_term, right_term))
        left_term = BaseType(5)
        self.assertFalse(operator.compare(left_term, right_term))

    def test_lesser_or_equal(self):
        operator = LessOrEqual()
        left_term = BaseType(5)
        right_term = BaseType(10)
        self.assertTrue(operator.compare(left_term, right_term))
        left_term = BaseType(10)
        self.assertTrue(operator.compare(left_term, right_term))
        left_term = BaseType(11)
        self.assertFalse(operator.compare(left_term, right_term))

    def test_lesser_than(self):
        operator = LessThan()
        left_term = BaseType(5)
        right_term = BaseType(10)
        self.assertTrue(operator.compare(left_term, right_term))
        left_term = BaseType(10)
        self.assertFalse(operator.compare(left_term, right_term))

    def test_not_between(self):
        operator = NotBetween()
        left_term = BaseType(11)
        right_term = ListType([1, 10])
        self.assertTrue(operator.compare(left_term, right_term))
        left_term = BaseType(5)
        self.assertFalse(operator.compare(left_term, right_term))

    def test_not_subset(self):
        operator = NotSubset()
        left_term = BaseType(5)
        right_term = ListType([1, 10])
        self.assertTrue(operator.compare(left_term, right_term))
        left_term = BaseType(1)
        self.assertFalse(operator.compare(left_term, right_term))

    def test_subset(self):
        operator = Subset()
        left_term = BaseType(1)
        right_term = ListType([1, 10])
        self.assertTrue(operator.compare(left_term, right_term))
        left_term = BaseType(5)
        self.assertFalse(operator.compare(left_term, right_term))

if __name__ == '__main__':
    unittest.main()

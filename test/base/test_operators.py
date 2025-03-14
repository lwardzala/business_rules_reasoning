import unittest
from src.business_rules_reasoning.base.value_types import BaseType, ListType
from src.business_rules_reasoning.base.operators import Between, GreaterOrEqual, GreaterThan, LessOrEqual, LessThan, NotBetween, NotSubset, Subset, Equal, NotEqual, IsIn, NotIn

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

    def test_equal_operator(self):
        operator = Equal()
        self.assertTrue(operator.compare(BaseType(5), BaseType(5)))
        self.assertFalse(operator.compare(BaseType(5), BaseType(10)))

    def test_not_equal_operator(self):
        operator = NotEqual()
        self.assertTrue(operator.compare(BaseType(5), BaseType(10)))
        self.assertFalse(operator.compare(BaseType(5), BaseType(5)))

    def test_is_in_operator(self):
        operator = IsIn()
        self.assertTrue(operator.compare(BaseType(5), ListType([1, 2, 3, 5])))
        self.assertFalse(operator.compare(ListType([5]), ListType([1, 2, 3, 6])))

    def test_not_in_operator(self):
        operator = NotIn()
        self.assertTrue(operator.compare(BaseType(5), ListType([1, 2, 3, 6])))
        self.assertFalse(operator.compare(BaseType(5), ListType([1, 2, 3, 5])))

if __name__ == '__main__':
    unittest.main()

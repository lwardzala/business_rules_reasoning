import unittest
from src.business_rules_reasoning.base.value_types.list_type import ListType
from src.business_rules_reasoning.base.value_types.base_type import BaseType

class TestListType(unittest.TestCase):
    def test_initialization(self):
        list_type = ListType([1, 2, 3])
        self.assertEqual(len(list_type.values), 3)
        self.assertEqual(list_type.values[0].value, 1)

    def test_eq(self):
        list_type1 = ListType([1, 2, 3])
        list_type2 = ListType([1, 2, 3])
        self.assertTrue(list_type1 == list_type2)

    def test_ne(self):
        list_type1 = ListType([1, 2, 3])
        list_type2 = ListType([4, 5, 6])
        self.assertTrue(list_type1 != list_type2)

    def test_str(self):
        list_type = ListType([1, 2, 3])
        self.assertEqual(str(list_type), "{1;2;3}")

    def test_between(self):
        list_type = ListType([1, 10])
        self.assertTrue(list_type.between(BaseType(5)))
        self.assertFalse(list_type.between(BaseType(11)))

    def test_contains(self):
        list_type = ListType([1, 2, 3])
        self.assertTrue(BaseType(2) in list_type)
        self.assertFalse(BaseType(4) in list_type)

if __name__ == '__main__':
    unittest.main()

import unittest
from src.business_rules_reasoning.base.value_types.base_type import BaseType

class TestBaseType(unittest.TestCase):
    def test_initialization(self):
        base_type = BaseType(5)
        self.assertEqual(base_type.value, 5)

    def test_is_number(self):
        base_type = BaseType(5)
        self.assertTrue(base_type.is_number())

    def test_is_not_number(self):
        base_type = BaseType("test")
        self.assertFalse(base_type.is_number())

    def test_str(self):
        base_type = BaseType(5)
        self.assertEqual(str(base_type), "5")

if __name__ == '__main__':
    unittest.main()

import unittest
from src.business_rules_reasoning.base.variable import Variable
from src.business_rules_reasoning.base.value_types.base_type import BaseType
from src.business_rules_reasoning.base.value_types.list_type import ListType

class TestVariable(unittest.TestCase):
    def test_initialization(self):
        variable = Variable(id="1", name="test", value=5)
        self.assertEqual(variable.id, "1")
        self.assertEqual(variable.name, "test")
        self.assertEqual(variable.value, 5)

    def test_get_value_base_type(self):
        variable = Variable(id="1", name="test", value=5)
        self.assertIsInstance(variable.get_value(), BaseType)
        self.assertEqual(variable.get_value().value, 5)

    def test_get_value_list_type(self):
        variable = Variable(id="1", name="test", value=[1, 2, 3])
        self.assertIsInstance(variable.get_value(), ListType)
        self.assertEqual(len(variable.get_value().values), 3)

    def test_is_empty(self):
        variable = Variable(id="1", name="test", value=None)
        self.assertTrue(variable.is_empty())

    def test_display(self):
        variable = Variable(id="1", name="test", value=5)
        self.assertEqual(variable.display(), "test = 5")

    def test_compare_to(self):
        variable1 = Variable(id="1", name="test1", value=5)
        variable1.frequency = 10
        variable2 = Variable(id="2", name="test2", value=5)
        variable2.frequency = 5
        self.assertEqual(variable1.compare_to(variable2), 1)
        self.assertEqual(variable2.compare_to(variable1), -1)
        variable2.frequency = 10
        self.assertEqual(variable1.compare_to(variable2), 0)

if __name__ == '__main__':
    unittest.main()

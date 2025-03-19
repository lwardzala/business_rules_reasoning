import unittest
from src.business_rules_reasoning.utils.parsers import parse_variable_value
from src.business_rules_reasoning.base import Variable

class TestParsers(unittest.TestCase):
    def test_parse_variable_value(self):
        # Test parsing boolean value
        variable = Variable(id="var1", name="Variable 1", value=True)
        parsed_value = parse_variable_value("true", variable)
        self.assertTrue(parsed_value)

        # Test parsing boolean value 'yes'
        variable = Variable(id="var1", name="Variable 1", value=True)
        parsed_value = parse_variable_value("yes", variable)
        self.assertTrue(parsed_value)
        
        # Test parsing integer value
        variable = Variable(id="var2", name="Variable 2", value=0)
        parsed_value = parse_variable_value("123", variable)
        self.assertEqual(parsed_value, 123)
        
        # Test parsing float value
        variable = Variable(id="var3", name="Variable 3", value=0.0)
        parsed_value = parse_variable_value("123.45", variable)
        self.assertEqual(parsed_value, 123.45)
        
        # Test parsing list value
        variable = Variable(id="var4", name="Variable 4", value=[])
        parsed_value = parse_variable_value("1,2,3", variable)
        self.assertEqual(parsed_value, ["1", "2", "3"])
        
        # Test parsing string value
        variable = Variable(id="var5", name="Variable 5", value="")
        parsed_value = parse_variable_value("test", variable)
        self.assertEqual(parsed_value, "test")

if __name__ == '__main__':
    unittest.main()

import unittest
import pandas as pd
from src.business_rules_reasoning.deductive.decision_table import c45_ruleset
from src.business_rules_reasoning.base import Rule, OperatorType

class TestC45Ruleset(unittest.TestCase):
    def setUp(self):
        self.data = {
            "Outlook": ["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", "Sunny", "Sunny", "Rain", "Sunny", "Overcast", "Overcast", "Rain"],
            "Temperature": ["Hot", "Hot", "Hot", "Mild", "Cool", "Cool", "Cool", "Mild", "Cool", "Mild", "Mild", "Mild", "Hot", "Mild"],
            "Humidity": ["High", "High", "High", "High", "Normal", "Normal", "Normal", "High", "Normal", "Normal", "Normal", "High", "Normal", "High"],
            "Wind": ["Weak", "Strong", "Weak", "Weak", "Weak", "Strong", "Strong", "Weak", "Weak", "Weak", "Strong", "Strong", "Weak", "Strong"],
            "PlayTennis": ["No", "No", "Yes", "Yes", "Yes", "No", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "Yes", "No"]
        }
        self.df = pd.DataFrame(self.data)

    def test_c45_ruleset(self):
        rules = c45_ruleset(self.df, conclusion_index=-1)
        self.assertIsInstance(rules, list)
        self.assertTrue(all(isinstance(rule, Rule) for rule in rules))

        self.assertEqual(len(rules), 5)

        rule1 = rules[0]
        rule1.validate()
        self.assertIsNotNone(rule1.conclusion)
        self.assertTrue(len(rule1.predicates) > 0)

    def test_c45_ruleset_with_simple_data(self):
        data = {
            "Feature1": ["A", "A", "B", "B"],
            "Feature2": ["X", "Y", "X", "Y"],
            "Target": ["Yes", "No", "Yes", "No"]
        }
        df = pd.DataFrame(data)

        rules = c45_ruleset(df, conclusion_index=-1)
        self.assertIsInstance(rules, list)
        self.assertTrue(all(isinstance(rule, Rule) for rule in rules))

        self.assertEqual(len(rules), 2)

        rule1 = rules[0]
        rule1.validate()
        self.assertEqual(rule1.conclusion.variable.id, "target")
        self.assertTrue(len(rule1.predicates) > 0)

    def test_c45_ruleset_with_numeric_data(self):
        data = {
            "Age": [25, 30, 35, ">=40"],
            "Income": [40000, 50000, 60000, ">=70000"],
            "Approved": ["Yes", "No", "Yes", "No"]
        }
        df = pd.DataFrame(data)

        rules = c45_ruleset(df, conclusion_index=-1)
        self.assertIsInstance(rules, list)
        self.assertTrue(all(isinstance(rule, Rule) for rule in rules))

        # Check that rules are generated
        self.assertEqual(len(rules), 4)

        # Validate the first rule
        rule1 = rules[0]
        rule1.validate()
        self.assertEqual(rule1.conclusion.variable.id, "approved")
        self.assertTrue(len(rule1.predicates) > 0)

    def test_c45_ruleset_with_none_values(self):
        data = {
            "Feature1": ["A", None, "B", "B"],
            "Feature2": ["X", "Y", None, "Y"],
            "Target A": ["Yes", "No", "Yes", "No"]
        }
        df = pd.DataFrame(data)

        rules = c45_ruleset(df, conclusion_index=-1)
        self.assertIsInstance(rules, list)
        self.assertTrue(all(isinstance(rule, Rule) for rule in rules))

        # Check that rules are generated
        self.assertEqual(len(rules), 2)

        # Validate the first rule
        rule1 = rules[0]
        rule1.validate()
        self.assertEqual(rule1.conclusion.variable.id, "target_a")
        self.assertTrue(len(rule1.predicates) > 0)

        # Validate that rules skip None values
        for rule in rules:
            for predicate in rule.predicates:
                self.assertIsNotNone(predicate.left_term.id)
                self.assertIsNotNone(predicate.right_term.value)

    def test_c45_ruleset_with_multiple_conclusions(self):
        data = {
            "Feature1": ["A", "A", "B", "B"],
            "Feature2": ["X", "Y", "X", "Y"],
            "Conclusion1": ["Yes", "No", "Yes", "No"],
            "Conclusion2": ["High", "Low", "Medium", "Low"]
        }
        features_description = {
            "Feature1": "Feature 1 Description",
            "Feature2": "Feature 2 Description",
            "Conclusion1": "Conclusion 1 Description",
            "Conclusion2": "Conclusion 2 Description"
        }
        df = pd.DataFrame(data)

        rules = c45_ruleset(df, conclusion_index=[-2, -1], features_description=features_description)
        self.assertIsInstance(rules, list)
        self.assertTrue(all(isinstance(rule, Rule) for rule in rules))
        self.assertEqual(len(rules), 5)  # Two conclusion columns, so double the rules

        # Test rules for the first conclusion column
        rule1 = rules[0]
        rule1.validate()
        self.assertEqual(rule1.conclusion.variable.id, "conclusion1")
        self.assertEqual(rule1.conclusion.variable.name, "Conclusion 1 Description")
        self.assertEqual(rule1.conclusion.variable.value, "Yes")
        self.assertEqual(len(rule1.predicates), 1)
        self.assertEqual(rule1.predicates[0].operator, OperatorType.EQUAL)
        self.assertEqual(rule1.predicates[0].right_term.value, "X")
        self.assertEqual(rule1.predicates[0].left_term.name, "Feature 2 Description")

        # Test rules for the second conclusion column
        rule5 = rules[3]
        rule5.validate()
        self.assertEqual(rule5.conclusion.variable.id, "conclusion2")
        self.assertEqual(rule5.conclusion.variable.name, "Conclusion 2 Description")
        self.assertEqual(rule5.conclusion.variable.value, "Medium")
        self.assertEqual(len(rule5.predicates), 2)
        self.assertEqual(rule5.predicates[0].operator, OperatorType.EQUAL)
        self.assertEqual(rule5.predicates[0].right_term.value, "X")
        self.assertEqual(rule5.predicates[0].left_term.name, "Feature 2 Description")
        self.assertEqual(rule5.predicates[1].operator, OperatorType.EQUAL)
        self.assertEqual(rule5.predicates[1].right_term.value, "B")
        self.assertEqual(rule5.predicates[1].left_term.name, "Feature 1 Description")

if __name__ == "__main__":
    unittest.main()

import unittest
import pandas as pd
from src.business_rules_reasoning.deductive.decision_table import pandas_to_rules
from src.business_rules_reasoning.base import Rule, OperatorType

class TestDecisionTableToRuleset(unittest.TestCase):
    def setUp(self):
        self.data = {
            "age": ["<18", ">=18", "between(30,40)"],
            "income": [">5000", "<=5000", "is_in(3000,4000,5000)"],
            "loan_approved": ['False', 'True', 'True']
        }
        self.df = pd.DataFrame(self.data)

    def test_pandas_to_rules(self):
        rules = pandas_to_rules(self.df, conclusion_index=-1)
        self.assertIsInstance(rules, list)
        self.assertTrue(all(isinstance(rule, Rule) for rule in rules))
        self.assertEqual(len(rules), len(self.df))

        rule1 = rules[0]
        rule1.validate()
        self.assertEqual(rule1.conclusion.variable.id, "loan_approved")
        self.assertEqual(rule1.conclusion.variable.value, False)
        self.assertEqual(len(rule1.predicates), 2)
        self.assertEqual(rule1.predicates[0].operator, OperatorType.LESS_THAN)
        self.assertEqual(rule1.predicates[0].right_term.value, 18)
        self.assertEqual(rule1.predicates[1].operator, OperatorType.GREATER_THAN)
        self.assertEqual(rule1.predicates[1].right_term.value, 5000)

        rule2 = rules[1]
        rule2.validate()
        self.assertEqual(rule2.conclusion.variable.id, "loan_approved")
        self.assertEqual(rule2.conclusion.variable.value, True)
        self.assertEqual(len(rule2.predicates), 2)
        self.assertEqual(rule2.predicates[0].operator, OperatorType.GREATER_OR_EQUAL)
        self.assertEqual(rule2.predicates[0].right_term.value, 18)
        self.assertEqual(rule2.predicates[1].operator, OperatorType.LESS_OR_EQUAL)
        self.assertEqual(rule2.predicates[1].right_term.value, 5000)

        rule3 = rules[2]
        rule3.validate()
        self.assertEqual(rule3.conclusion.variable.id, "loan_approved")
        self.assertEqual(rule3.conclusion.variable.value, True)
        self.assertEqual(len(rule3.predicates), 2)
        self.assertEqual(rule3.predicates[0].operator, OperatorType.BETWEEN)
        self.assertEqual(rule3.predicates[0].right_term.value, [30, 40])
        self.assertEqual(rule3.predicates[1].operator, OperatorType.IS_IN)
        self.assertEqual(rule3.predicates[1].right_term.value, [3000, 4000, 5000])

    def test_pandas_to_rules_without_operators(self):
        data = {
            "age": [18, 25, 40],
            "income": ['low', 'medium', 'is_in(high, very_high)'],
            "loan_approved": [False, True, True]
        }
        df = pd.DataFrame(data)

        rules = pandas_to_rules(df, conclusion_index=-1)
        self.assertIsInstance(rules, list)
        self.assertTrue(all(isinstance(rule, Rule) for rule in rules))
        self.assertEqual(len(rules), len(df))

        rule1 = rules[0]
        rule1.validate()
        self.assertEqual(rule1.conclusion.variable.id, "loan_approved")
        self.assertEqual(rule1.conclusion.variable.value, False)
        self.assertEqual(len(rule1.predicates), 2)
        self.assertEqual(rule1.predicates[0].operator, OperatorType.EQUAL)
        self.assertEqual(rule1.predicates[0].right_term.value, 18)
        self.assertEqual(rule1.predicates[1].operator, OperatorType.EQUAL)
        self.assertEqual(rule1.predicates[1].right_term.value, 'low')

        rule2 = rules[1]
        rule2.validate()
        self.assertEqual(rule2.conclusion.variable.id, "loan_approved")
        self.assertEqual(rule2.conclusion.variable.value, True)
        self.assertEqual(len(rule2.predicates), 2)
        self.assertEqual(rule2.predicates[0].operator, OperatorType.EQUAL)
        self.assertEqual(rule2.predicates[0].right_term.value, 25)
        self.assertEqual(rule2.predicates[1].operator, OperatorType.EQUAL)
        self.assertEqual(rule2.predicates[1].right_term.value, 'medium')

        rule3 = rules[2]
        rule3.validate()
        self.assertEqual(rule3.conclusion.variable.id, "loan_approved")
        self.assertEqual(rule3.conclusion.variable.value, True)
        self.assertEqual(len(rule3.predicates), 2)
        self.assertEqual(rule3.predicates[0].operator, OperatorType.EQUAL)
        self.assertEqual(rule3.predicates[0].right_term.value, 40)
        self.assertEqual(rule3.predicates[1].operator, OperatorType.IS_IN)
        self.assertEqual(rule3.predicates[1].right_term.value, ['high', 'very_high'])

    def test_pandas_to_rules_with_nan_values(self):
        data = {
            "age": ["<18", None, ">=40"],
            "income": [">5000", "<=4000", None],
            "Loan Approved": [False, True, True]
        }
        df = pd.DataFrame(data)

        rules = pandas_to_rules(df, conclusion_index=-1)
        self.assertIsInstance(rules, list)
        self.assertTrue(all(isinstance(rule, Rule) for rule in rules))
        self.assertEqual(len(rules), len(df))

        # Test first rule
        rule1 = rules[0]
        rule1.validate()
        self.assertEqual(rule1.conclusion.variable.id, "loan_approved")
        self.assertEqual(rule1.conclusion.variable.value, False)
        self.assertEqual(len(rule1.predicates), 2)
        self.assertEqual(rule1.predicates[0].operator, OperatorType.LESS_THAN)
        self.assertEqual(rule1.predicates[0].right_term.value, 18)
        self.assertEqual(rule1.predicates[1].operator, OperatorType.GREATER_THAN)
        self.assertEqual(rule1.predicates[1].right_term.value, 5000)

        # Test second rule
        rule2 = rules[1]
        rule2.validate()
        self.assertEqual(rule2.conclusion.variable.id, "loan_approved")
        self.assertEqual(rule2.conclusion.variable.value, True)
        self.assertEqual(len(rule2.predicates), 1)
        self.assertEqual(rule2.predicates[0].operator, OperatorType.LESS_OR_EQUAL)
        self.assertEqual(rule2.predicates[0].right_term.value, 4000)

        # Test third rule
        rule3 = rules[2]
        rule3.validate()
        self.assertEqual(rule3.conclusion.variable.id, "loan_approved")
        self.assertEqual(rule3.conclusion.variable.value, True)
        self.assertEqual(len(rule3.predicates), 1)
        self.assertEqual(rule3.predicates[0].operator, OperatorType.GREATER_OR_EQUAL)
        self.assertEqual(rule3.predicates[0].right_term.value, 40)

    def test_pandas_to_rules_with_multiple_conclusions(self):
        data = {
            "age": ["<18", ">=18", "between(30,40)"],
            "income": [">5000", "<=5000", "is_in(3000,4000,5000)"],
            "loan_approved": [False, True, True],
            "forward_to_bank": [True, False, True]
        }
        features_description = {
            "age": "Age of the applicant",
            "income": "Income of the applicant",
            "loan_approved": "Loan approval status",
            "forward_to_bank": "Forward to bank verification"
        }
        df = pd.DataFrame(data)

        rules = pandas_to_rules(df, conclusion_index=[-2, -1], features_description=features_description)
        self.assertIsInstance(rules, list)
        self.assertTrue(all(isinstance(rule, Rule) for rule in rules))
        self.assertEqual(len(rules), len(df) * 2)  # Two conclusions, so double the rules

        # Test rules for the first conclusion column
        rule1 = rules[0]
        rule1.validate()
        self.assertEqual(rule1.conclusion.variable.id, "loan_approved")
        self.assertEqual(rule1.conclusion.variable.name, "Loan approval status")
        self.assertEqual(rule1.conclusion.variable.value, False)
        self.assertEqual(len(rule1.predicates), 2)
        self.assertEqual(rule1.predicates[0].operator, OperatorType.LESS_THAN)
        self.assertEqual(rule1.predicates[0].right_term.value, 18)
        self.assertEqual(rule1.predicates[0].left_term.name, "Age of the applicant")
        self.assertEqual(rule1.predicates[1].operator, OperatorType.GREATER_THAN)
        self.assertEqual(rule1.predicates[1].right_term.value, 5000)
        self.assertEqual(rule1.predicates[1].left_term.name, "Income of the applicant")

        # Test rules for the second conclusion column
        rule4 = rules[3]
        rule4.validate()
        self.assertEqual(rule4.conclusion.variable.id, "forward_to_bank")
        self.assertEqual(rule4.conclusion.variable.name, "Forward to bank verification")
        self.assertEqual(rule4.conclusion.variable.value, True)
        self.assertEqual(len(rule4.predicates), 2)
        self.assertEqual(rule4.predicates[0].operator, OperatorType.LESS_THAN)
        self.assertEqual(rule4.predicates[0].right_term.value, 18)
        self.assertEqual(rule4.predicates[0].left_term.name, "Age of the applicant")
        self.assertEqual(rule4.predicates[1].operator, OperatorType.GREATER_THAN)
        self.assertEqual(rule4.predicates[1].right_term.value, 5000)
        self.assertEqual(rule4.predicates[1].left_term.name, "Income of the applicant")

if __name__ == "__main__":
    unittest.main()

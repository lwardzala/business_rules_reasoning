import unittest
import pandas as pd
from src.business_rules_reasoning.deductive.decision_table import ruleset_to_pandas
from src.business_rules_reasoning.base import Rule, OperatorType
from src.business_rules_reasoning.deductive import RuleBuilder, PredicateBuilder, VariableBuilder

class TestRulesetToPandas(unittest.TestCase):
    def setUp(self):
        # Create example rules
        predicate1 = PredicateBuilder().configure_predicate("age", OperatorType.LESS_THAN, 18).unwrap()
        predicate2 = PredicateBuilder().configure_predicate("income", OperatorType.GREATER_THAN, 5000).unwrap()
        rule1 = RuleBuilder().set_conclusion(VariableBuilder().set_id("loan_approved").set_value(False).unwrap()).add_predicate(predicate1).add_predicate(predicate2).unwrap()

        predicate3 = PredicateBuilder().configure_predicate("age", OperatorType.GREATER_OR_EQUAL, 18).unwrap()
        rule2 = RuleBuilder().set_conclusion(VariableBuilder().set_id("loan_approved").set_value(True).unwrap()).add_predicate(predicate3).unwrap()

        self.rules = [rule1, rule2]

    def test_ruleset_to_pandas(self):
        df = ruleset_to_pandas(self.rules)
        self.assertIsInstance(df, pd.DataFrame)

        # Check the DataFrame structure
        self.assertEqual(len(df), 2)  # Two rules
        self.assertIn("age", df.columns)
        self.assertIn("income", df.columns)
        self.assertIn("loan_approved", df.columns)

        # Check the first rule
        self.assertEqual(df.iloc[0]["age"], "<18")
        self.assertEqual(df.iloc[0]["income"], ">5000")
        self.assertEqual(df.iloc[0]["loan_approved"], False)

        # Check the second rule
        self.assertEqual(df.iloc[1]["age"], ">=18")
        self.assertTrue(pd.isna(df.iloc[1]["income"]))
        self.assertEqual(df.iloc[1]["loan_approved"], True)

    def test_ruleset_to_pandas_with_empty_rules(self):
        df = ruleset_to_pandas([])
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    def test_ruleset_to_pandas_with_complex_predicates(self):
        # Create a rule with complex predicates
        predicate1 = PredicateBuilder().configure_predicate("age", OperatorType.BETWEEN, [18, 25]).unwrap()
        predicate2 = PredicateBuilder().configure_predicate("income", OperatorType.IS_IN, [3000, 4000, 5000]).unwrap()
        rule = RuleBuilder().set_conclusion(VariableBuilder().set_id("loan_approved").set_value(True).unwrap()).add_predicate(predicate1).add_predicate(predicate2).unwrap()

        df = ruleset_to_pandas([rule])
        self.assertIsInstance(df, pd.DataFrame)

        # Check the DataFrame structure
        self.assertEqual(len(df), 1)  # One rule
        self.assertIn("age", df.columns)
        self.assertIn("income", df.columns)
        self.assertIn("loan_approved", df.columns)

        # Check the rule
        self.assertEqual(df.iloc[0]["age"], "between(18,25)")
        self.assertEqual(df.iloc[0]["income"], "is_in(3000,4000,5000)")
        self.assertEqual(df.iloc[0]["loan_approved"], True)

if __name__ == "__main__":
    unittest.main()

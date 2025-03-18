import unittest
from src.business_rules_reasoning.deductive.knowledge_builder import KnowledgeBaseBuilder, RuleBuilder, PredicateBuilder, VariableBuilder
from src.business_rules_reasoning.base.reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod
from src.business_rules_reasoning.base import ReasoningProcess, KnowledgeBase, Rule, Variable
from src.business_rules_reasoning.deductive.deductive_predicate import DeductivePredicate
from src.business_rules_reasoning.deductive import DeductiveReasoningService
from src.business_rules_reasoning.base import OperatorType

class TestReasoningService(unittest.TestCase):
    def test_start_reasoning(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="1", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.start_reasoning(rp)
        self.assertEqual(result.state, ReasoningState.STOPPED)

    # todo fix this test
    # def test_continue_reasoning(self):
    #     rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION)
    #     result = ReasoningService.continue_reasoning(rp)
    #     self.assertEqual(result.state, ReasoningState.FINISHED)

    def test_set_values(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        variables = {"1": 5}
        result = DeductiveReasoningService.set_values(rp, variables)
        self.assertEqual(left_term.value, 5)

        # Scenario: Two missing variables but only one is provided
        var1 = Variable(id="var1", value=None)
        var2 = Variable(id="var2", value=None)
        predicate1 = DeductivePredicate(left_term=var1, right_term=Variable(id="var1", value=10), operator=OperatorType.GREATER_THAN)
        predicate2 = DeductivePredicate(left_term=var2, right_term=Variable(id="var2", value=20), operator=OperatorType.LESS_THAN)
        rule = Rule(predicates=[predicate1, predicate2], conclusion=DeductivePredicate(left_term=Variable(), right_term=Variable(id="conclusion", value=True), operator=OperatorType.EQUAL))
        kb.rule_set.append(rule)
        variables = {"var1": 15}
        DeductiveReasoningService.set_values(rp, variables)
        self.assertEqual(predicate1.left_term.value, 15)
        self.assertIsNone(predicate2.left_term.value)

    def test_reset_reasoning(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.reset_reasoning(rp)
        self.assertEqual(result.state, ReasoningState.INITIALIZED)
        self.assertEqual(result.reasoned_items, [])
        self.assertEqual(result.evaluation_message, EvaluationMessage.NONE)

    def test_clear_reasoning(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.clear_reasoning(rp)
        self.assertEqual(result.state, ReasoningState.INITIALIZED)
        self.assertEqual(result.reasoned_items, [])
        self.assertEqual(result.evaluation_message, EvaluationMessage.NONE)

    def test_get_all_missing_variable_ids(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="1", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.get_all_missing_variable_ids(rp)
        self.assertEqual(result, ["1"])

    def test_get_all_missing_variables(self):
        kb = KnowledgeBase()
        left_term1 = Variable(id="1", value=None)
        left_term2 = Variable(id="2", value=None)
        right_term1 = Variable(id="1", value=10)
        right_term2 = Variable(id="2", value=10)
        predicate1 = DeductivePredicate(left_term=left_term1, right_term=right_term1, operator=OperatorType.LESS_THAN)
        predicate2 = DeductivePredicate(left_term=left_term2, right_term=right_term2, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term2, right_term=right_term2, operator=OperatorType.LESS_THAN)
        rule1 = Rule(conclusion=conclusion, predicates=[predicate1, predicate2])
        rule2 = Rule(conclusion=conclusion, predicates=[predicate1])
        kb.rule_set.append(rule1)
        kb.rule_set.append(rule2)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.get_all_missing_variables(rp)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[1].id, "2")

    def test_analyze_variables_frequency(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=None)
        right_term = Variable(id="2", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.analyze_variables_frequency(rp)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].frequency, 1)

    def test_deduction(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=5)
        right_term = Variable(id="1", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.deduction(rp)
        self.assertEqual(result.state, ReasoningState.FINISHED)
        self.assertEqual(result.evaluation_message, EvaluationMessage.PASSED)

    def test_deduction_with_duplicate_conclusions(self):
        kb = KnowledgeBase()
        left_term1 = Variable(id="1", value=5)
        right_term1 = Variable(id="1", value=10)
        left_term2 = Variable(id="2", value=15)
        right_term2 = Variable(id="2", value=20)
        
        predicate1 = DeductivePredicate(left_term=left_term1, right_term=right_term1, operator=OperatorType.LESS_THAN)
        predicate2 = DeductivePredicate(left_term=left_term2, right_term=right_term2, operator=OperatorType.LESS_THAN)
        
        conclusion = DeductivePredicate(left_term=Variable(id="conclusion", value=True), right_term=Variable(id="conclusion", value=True), operator=OperatorType.EQUAL)
        
        rule1 = Rule(conclusion=conclusion, predicates=[predicate1])
        rule2 = Rule(conclusion=conclusion, predicates=[predicate2])
        
        kb.rule_set.append(rule1)
        kb.rule_set.append(rule2)
        
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        result = DeductiveReasoningService.deduction(rp)
        
        self.assertEqual(result.state, ReasoningState.FINISHED)
        self.assertEqual(result.evaluation_message, EvaluationMessage.PASSED)
        self.assertEqual(len(result.reasoned_items), 1)
        self.assertEqual(result.reasoned_items[0].id, "conclusion")

    def test_hypothesis_testing(self):
        kb = KnowledgeBase()
        left_term = Variable(id="1", value=5)
        right_term = Variable(id="1", value=10)
        predicate = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        conclusion = DeductivePredicate(left_term=left_term, right_term=right_term, operator=OperatorType.LESS_THAN)
        rule = Rule(conclusion=conclusion, predicates=[predicate])
        kb.rule_set.append(rule)
        rp = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=kb)
        rp.options = type('obj', (object,), {'hypothesis': right_term})
        result = DeductiveReasoningService.hypothesis_testing(rp)
        self.assertEqual(result.state, ReasoningState.FINISHED)
        self.assertEqual(result.evaluation_message, EvaluationMessage.PASSED)

class TestLeasingDocumentProcessingKB(unittest.TestCase):
    def test_leasing_document_processing_kb(self):
        # Build the knowledge base
        kb_builder = KnowledgeBaseBuilder().set_id("kb1").set_name("Leasing Document Processing KB").set_description("Knowledge base for processing leasing documents")

        unpaid_loans = VariableBuilder().set_id("unpaid_loans").set_name("Unpaid Loans").unwrap()
        fraud_flag = VariableBuilder().set_id("fraud_flag").set_name("Fraud Flag").unwrap()
        monthly_net_salary = VariableBuilder().set_id("monthly_net_salary").set_name("Monthly Net Salary").unwrap()
        employment_type = VariableBuilder().set_id("employment_type").set_name("Employment Type").unwrap()
        thirty_percent_ruling = VariableBuilder().set_id("thirty_percent_ruling").set_name("30% Ruling").unwrap()
        previous_loans = VariableBuilder().set_id("previous_loans").set_name("Previous Loans").unwrap()
        ongoing_loans = VariableBuilder().set_id("ongoing_loans").set_name("Ongoing Loans").unwrap()

        # Add rules
        rule1 = RuleBuilder() \
            .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(False).unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(unpaid_loans, OperatorType.EQUAL, True).unwrap()) \
            .unwrap()
        kb_builder.add_rule(rule1)

        rule2 = RuleBuilder() \
            .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(False).unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(fraud_flag, OperatorType.EQUAL, True).unwrap()) \
            .unwrap()
        kb_builder.add_rule(rule2)

        rule8 = RuleBuilder() \
            .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(False).unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(employment_type, OperatorType.EQUAL, 'unemployed').unwrap()) \
            .unwrap()
        kb_builder.add_rule(rule8)

        rule3 = RuleBuilder() \
            .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(False).unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(monthly_net_salary, OperatorType.LESS_THAN, 2000).unwrap()) \
            .unwrap()
        kb_builder.add_rule(rule3)

        rule7 = RuleBuilder() \
            .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(True).unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(employment_type, OperatorType.NOT_EQUAL, "freelancer").unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(monthly_net_salary, OperatorType.GREATER_OR_EQUAL, 2000).unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(fraud_flag, OperatorType.EQUAL, False).unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(unpaid_loans, OperatorType.EQUAL, False).unwrap()) \
            .unwrap()
        kb_builder.add_rule(rule7)

        rule4 = RuleBuilder() \
            .set_conclusion(VariableBuilder().set_id("forward_to_bank_verification").set_name("Forward to Bank Verification").set_value(False).unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(employment_type, OperatorType.EQUAL, "freelancer").unwrap()) \
            .unwrap()
        kb_builder.add_rule(rule4)

        rule5 = RuleBuilder() \
            .set_conclusion(VariableBuilder().set_id("forward_to_bank_verification").set_name("Forward to Bank Verification").set_value(True).unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(thirty_percent_ruling, OperatorType.EQUAL, True).unwrap()) \
            .unwrap()
        kb_builder.add_rule(rule5)

        rule6 = RuleBuilder() \
            .set_conclusion(VariableBuilder().set_id("forward_to_bank_verification").set_name("Forward to Bank Verification").set_value(True).unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(previous_loans, OperatorType.EQUAL, False).unwrap()) \
            .add_predicate(PredicateBuilder().configure_predicate_with_variable(ongoing_loans, OperatorType.EQUAL, False).unwrap()) \
            .unwrap()
        kb_builder.add_rule(rule6)

        knowledge_base = kb_builder.unwrap()

        # Create reasoning process
        reasoning_process = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=knowledge_base)

        # Set variables
        variables = {"unpaid_loans": False, "fraud_flag": False, "employment_type": "Company Employee", "monthly_net_salary": 3000.0, "thirty_percent_ruling": False, "previous_loans": True, "ongoing_loans": False}

        # Start reasoning
        reasoning_process = DeductiveReasoningService.start_reasoning(reasoning_process)
        reasoning_process = DeductiveReasoningService.set_values(reasoning_process, variables)
        result = DeductiveReasoningService.continue_reasoning(reasoning_process)

        # Assertions
        self.assertEqual(result.state, ReasoningState.FINISHED)
        self.assertEqual(result.evaluation_message, EvaluationMessage.PASSED)
        self.assertTrue(any(item.id == "loan_accepted" and item.value is True for item in result.reasoned_items))
        self.assertTrue(any(item.id == "forward_to_bank_verification" and item.value is False for item in result.reasoned_items))

if __name__ == '__main__':
    unittest.main()

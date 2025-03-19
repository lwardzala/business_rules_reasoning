from typing import List, Callable
from business_rules_reasoning import OperatorType
from business_rules_reasoning.base import KnowledgeBase
from business_rules_reasoning.deductive import KnowledgeBaseBuilder, RuleBuilder, PredicateBuilder, VariableBuilder
from business_rules_reasoning.orchestrator import OrchestratorStatus
from business_rules_reasoning.orchestrator.llm import LLMOrchestrator

def knowledge_base_retriever():
    # Build the knowledge base with rules
    kb_builder = KnowledgeBaseBuilder().set_id("kb1").set_name("Leasing Document Processing KB").set_description("Knowledge base for processing leasing documents")

    unpaid_loans = VariableBuilder() \
        .set_id("unpaid_loans") \
        .set_name("Unpaid Loans") \
        .unwrap()
    fraud_flag = VariableBuilder() \
        .set_id("fraud_flag") \
        .set_name("Fraud Flag") \
        .unwrap()
    monthly_net_salary = VariableBuilder() \
        .set_id("monthly_net_salary") \
        .set_name("Monthly Net Salary") \
        .unwrap()
    employment_type = VariableBuilder() \
        .set_id("employment_type") \
        .set_name("Employment Type option from: [freelancer, company emplyoee, unemployed]") \
        .unwrap()
    thirty_percent_ruling = VariableBuilder() \
        .set_id("thirty_percent_ruling") \
        .set_name("30% Ruling") \
        .unwrap()
    previous_loans = VariableBuilder() \
        .set_id("previous_loans") \
        .set_name("Indicates if there were any historical paid loans") \
        .unwrap()
    ongoing_loans = VariableBuilder() \
        .set_id("ongoing_loans") \
        .set_name("Indicates whether there is any ongoing loans") \
        .unwrap()

    # Rule: If the client has any unpaid loans, reject the loan
    rule1 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(unpaid_loans, OperatorType.EQUAL, True).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule1)

    # Rule: If the client is flagged in the fraud database, reject the loan
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

    # Rule: If the client's monthly net salary is less than 2000, reject the loan
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

    # Rule: If the client has no history of previous or ongoing loans, forward to bank verification team
    rule6 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("forward_to_bank_verification").set_name("Forward to Bank Verification").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(previous_loans, OperatorType.EQUAL, False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(ongoing_loans, OperatorType.EQUAL, False).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule6)

    knowledge_base = kb_builder.unwrap()
    return [knowledge_base]

def main():
    kb = knowledge_base_retriever()[0]
    print(kb.display())

if __name__ == "__main__":
    main()

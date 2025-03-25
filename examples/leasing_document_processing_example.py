from typing import List, Callable
from business_rules_reasoning import OperatorType
from business_rules_reasoning.base import KnowledgeBase
from business_rules_reasoning.deductive import KnowledgeBaseBuilder, RuleBuilder, PredicateBuilder, VariableBuilder
from business_rules_reasoning.orchestrator import OrchestratorStatus
from business_rules_reasoning.orchestrator.llm import LLMOrchestrator

def knowledge_base_retriever():
    kb_builder = KnowledgeBaseBuilder().set_id("kb1").set_name("Leasing Document Processing KB").set_description("Knowledge base for processing leasing documents")

    unpaid_loans = VariableBuilder() \
        .set_id("unpaid_loans") \
        .set_name("Indicates if there are any open un-paid loans: 'yes' or 'no'") \
        .unwrap()
    fraud_flag = VariableBuilder() \
        .set_id("fraud_database") \
        .set_name("Indicates if the fraud database has any records: 'yes' or 'no'") \
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
        .set_name("30% Ruling - 'yes' if applicable othwerwise 'no'") \
        .unwrap()
    previous_loans = VariableBuilder() \
        .set_id("previous_loans") \
        .set_name("Indicates if there were any historical paid loans") \
        .unwrap()
    ongoing_loans = VariableBuilder() \
        .set_id("ongoing_loans") \
        .set_name("Indicates whether there is any open loans") \
        .unwrap()

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

    rule3 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(employment_type, OperatorType.EQUAL, 'unemployed').unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule3)

    rule4 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(monthly_net_salary, OperatorType.LESS_THAN, 2000).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule4)

    rule5 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(employment_type, OperatorType.NOT_EQUAL, "unemployed").unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(monthly_net_salary, OperatorType.GREATER_OR_EQUAL, 2000).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(fraud_flag, OperatorType.EQUAL, False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(unpaid_loans, OperatorType.EQUAL, False).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule5)

    rule6 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("forward_to_bank_verification").set_name("Forward to additional bank verification").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(employment_type, OperatorType.EQUAL, "freelancer").unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule6)

    rule7 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("forward_to_bank_verification").set_name("Forward to additional bank verification").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(thirty_percent_ruling, OperatorType.EQUAL, True).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule7)

    rule8 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("forward_to_bank_verification").set_name("Forward to additional bank verification").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(previous_loans, OperatorType.EQUAL, False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(ongoing_loans, OperatorType.EQUAL, False).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule8)

    knowledge_base = kb_builder.unwrap()
    return [knowledge_base]

def inference_state_retriever(inference_id: str) -> dict:
    # Return an empty inference state for simplicity
    return {}

def main():
    case1_success_with_bank_verification = """
    Bank Screening Document

    Customer Information:
    Name: John Doe
    Customer ID: 123456789

    Loan History (BKR Check):
    Loans:
    - Personal Loan (Paid, closed)
    - Private car leasing (Paid, closed)
    Current Loan Status: No active loans

    Fraud Database Check:
    Status: No record found in internal fraud databases

    Financial Information:
    Monthly Net Salary: 3,000 EUR

    Employment Type: Freelancer

    30% Ruling Check:
    No

    Check the customer document for loan acceptance and check if is needed to forward to bank verification team
    """

    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_name = "meta-llama/Llama-3.2-3B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    model_kwargs={
        "max_new_tokens": 100,
        "temperature": 0.2,
        "top_k": 1,
        "top_p": 0.4
    }

    from business_rules_reasoning.orchestrator.llm import LLMOrchestrator, HuggingFacePipeline

    orchestrator = LLMOrchestrator(
        model_name=model_name,
        knowledge_base_retriever=knowledge_base_retriever,
        inference_state_retriever=inference_state_retriever,
        llm = HuggingFacePipeline(model_name=model_name, tokenizer=tokenizer, model=model, **model_kwargs)
    )

    response = orchestrator.query(case1_success_with_bank_verification)

    print("Response:\n", response)

    print(orchestrator.reasoning_process.display_state())

    print('\n'.join(orchestrator.inference_logger.get_log()))

if __name__ == "__main__":
    main()

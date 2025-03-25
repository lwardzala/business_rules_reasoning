from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List, Callable
from business_rules_reasoning import OperatorType
from business_rules_reasoning.deductive import KnowledgeBaseBuilder, RuleBuilder, PredicateBuilder, VariableBuilder
from business_rules_reasoning.orchestrator import OrchestratorStatus
from business_rules_reasoning.orchestrator.llm import LLMOrchestrator, HuggingFacePipeline

def knowledge_base_retriever() -> List[dict]:
    # Build the knowledge base with rules
    kb_builder = KnowledgeBaseBuilder().set_id("kb1").set_name("Medical KB").set_description("Medical knowledge base for prescribing paracetamol")

    body_ache = VariableBuilder().set_id("body_ache").set_name("Body ache: 'yes' or 'no'").unwrap()
    fever = VariableBuilder().set_id("fever").set_name("Fever temperature number: number in Celsius degrees").unwrap()
    headache = VariableBuilder().set_id("headache").set_name("Headache: 'yes' or 'no'").unwrap()
    
    # Rule: If the patient has a fever > 38 and headache, prescribe paracetamol
    rule1 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("prescribe_paracetamol").set_name("Prescribe Paracetamol: 'yes' or 'no'").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(fever, OperatorType.GREATER_THAN, 38).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(headache, OperatorType.EQUAL, True).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule1)
    
    # Rule: If the patient has a fever > 38 and body ache, prescribe paracetamol
    rule2 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("prescribe_paracetamol").set_name("Prescribe Paracetamol: 'yes' or 'no'").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(fever, OperatorType.GREATER_THAN, 38).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(body_ache, OperatorType.EQUAL, True).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule2)
    
    # Rule: If the patient has a fever > 40, go to the hospital
    rule3 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("go_to_hospital").set_name("Go to Hospital: 'yes' or 'no'").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(fever, OperatorType.GREATER_THAN, 40).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule3)
    
    knowledge_base = kb_builder.unwrap()
    return [knowledge_base]

def inference_state_retriever(inference_id: str) -> dict:
    # Return an empty inference state for simplicity
    return {}

def main():
    model_name = "meta-llama/Llama-3.2-3B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    model_kwargs={
        "max_new_tokens": 100,
        "temperature": 0.2,
        "top_k": 1,
        "top_p": 0.4
    }
    
    orchestrator = LLMOrchestrator(
        model_name=model_name,
        knowledge_base_retriever=knowledge_base_retriever,
        inference_state_retriever=inference_state_retriever,
        llm = HuggingFacePipeline(model_name=model_name, tokenizer=tokenizer, model=model, **model_kwargs)
    )

    # Provide a query with necessary data
    query_text = "The patient has a fever of 39 and headache. Should we prescribe paracetamol?"
    response = orchestrator.query(query_text)

    # Print the response
    print("Response:", response)

    print(orchestrator.reasoning_process.display_state())

    print('\n'.join(orchestrator.inference_logger.get_log()))

if __name__ == "__main__":
    main()

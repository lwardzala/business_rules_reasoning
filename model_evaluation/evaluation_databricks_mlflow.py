import uuid
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from business_rules_reasoning.base import KnowledgeBase
from business_rules_reasoning.deductive import KnowledgeBaseBuilder
from business_rules_reasoning.deductive.decision_table import pandas_to_rules
from business_rules_reasoning.orchestrator import OrchestratorOptions
from business_rules_reasoning.orchestrator.llm import HuggingFacePipeline, LLMOrchestrator

def knowledge_base_retriever_from_tables() -> list[KnowledgeBase]:
    # Define the decision tables and determine conclusion column indexes
    tables = [
        { "name": 'leasing_document_decision_table', "conclusions": [-2, -1] },
        { "name": 'stock_decision_rules', "conclusions": [-1] }
    ]
    knowledge_bases = []

    for table in tables:
        # Query the table
        table_name = table["name"]
        query = f"SELECT * FROM {table_name}"
        df = spark.sql(query)

        # Convert Spark DataFrame to Pandas DataFrame
        pandas_df = df.toPandas()

        # Extract column names and comments into a dictionary
        columns_query = f"DESCRIBE TABLE {table_name}"
        columns_df = spark.sql(columns_query)
        features_description = {row['col_name']: row['comment'] for row in columns_df.collect() if row['comment']}

        # Extract table comment
        table_comment_query = f"DESCRIBE TABLE EXTENDED {table_name}"
        table_comment_df = spark.sql(table_comment_query)
        table_comment = table_comment_df.filter(table_comment_df.col_name == "Comment").select("data_type").collect()
        table_description = table_comment[0]["data_type"] if table_comment else f"Knowledge base for {table_name}"

        # Generate rule sets from the Pandas DataFrame
        rules = pandas_to_rules(pandas_df, conclusion_index=table["conclusions"], features_description=features_description)

        # Build the KnowledgeBase
        kb_builder = KnowledgeBaseBuilder().set_id(table_name).set_name(f"Knowledge Base for {table_name}").set_description(table_description)
        for rule in rules:
            kb_builder.add_rule(rule)
        knowledge_bases.append(kb_builder.unwrap())

    return knowledge_bases

def inference_state_retriever(inference_id: str) -> dict:
    # Return an empty inference state for simplicity
    return {}

from transformers import AutoModelForCausalLM, AutoTokenizer

model_name ="meta-llama/Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="cuda", torch_dtype="auto")

model_kwargs={
    "max_new_tokens": 100,
    "temperature": 0.2,
    "top_k": 1,
    "top_p": 0.4,
    "eos_token_id": tokenizer.eos_token_id,
    "pad_token_id": tokenizer.pad_token_id,
}

# Batch processing fro test cases with internal orchestrator conversation
def run_batch_prompts(dataset: pd.DataFrame, df_orchestrator: pd.DataFrame) -> pd.DataFrame:
    llm = HuggingFacePipeline(model_name=model_name, tokenizer=tokenizer, model=model, **model_kwargs)
    expected_columns = [
        'request_id',
        'request',
        'response',
        'expected_facts',
        'expected_response',
        'expected_retrieved_context',
        'retrieved_context'
    ]

    responses = []
    retrieved_contexts = []
    new_rows = []

    for index, row in dataset.iterrows():
        # Initialize the orchestrator each time to keep logs clean for each test case
        orchestrator = LLMOrchestrator(
            knowledge_base_retriever=knowledge_base_retriever_from_tables,
            inference_state_retriever=inference_state_retriever,
            llm=llm
        )

        # reset_reasoning=True only resets the state, but keeps the logs and knowledge base list in memory
        response = orchestrator.query(row["request"], return_full_context=True, reset_reasoning=True)
        responses.append(response["response"])

        # Construct retrieved context if applicable
        if response['orchestrator_status'] != 'WAITING_FOR_QUERY':
            rc = [
                {
                    "doc_uri": "knowledge_base_id",
                    "content": f'{response["reasoning_process"]["knowledge_base"]["id"]} - '
                               f'{response["reasoning_process"]["knowledge_base"]["description"]}:\n'
                               f'{orchestrator.reasoning_process.knowledge_base.display()}'
                },
                {
                    "doc_uri": "reasoning_method",
                    "content": response["reasoning_process"]["reasoning_method"]
                },
                {
                    "doc_uri": "reasoning_hypothesis",
                    "content": orchestrator.reasoning_process.options["hypothesis"].display()
                    if orchestrator.reasoning_process.options and orchestrator.reasoning_process.options.get("hypothesis")
                    else 'None'
                },
                {
                    "doc_uri": "engine_status",
                    "content": response["reasoning_process"]["evaluation_message"]
                },
                {
                    "doc_uri": "reasoned_items",
                    "content": ', '.join(f"{item['id']} = {item['value']}" for item in response["reasoning_process"]["reasoned_items"])
                }
            ]
        else:
            rc = None

        retrieved_contexts.append(rc)

        # Load internal orchestrator conversation for evaluation
        i = 0
        j = 1
        query_log = orchestrator.query_log
        while i < len(query_log) - 1:
            current_item = query_log[i]
            next_item = query_log[i + 1]
            if current_item['role'] == 'engine' and next_item['role'] == 'system':
                new_rows.append({
                    'request_id': f"{row['request_id']}_conversation_{j}",
                    'request': current_item['text'],
                    'response': next_item['text'],
                    'expected_facts': None,
                    'expected_response': None,
                    'expected_retrieved_context': None,
                    'retrieved_context': None
                })
                i += 2
            else:
                i += 1
            j += 1

    # Update the original dataset at once
    dataset["response"] = responses
    dataset["retrieved_context"] = retrieved_contexts

    # Append all new_rows to df_orchestrator
    if new_rows:
        df_partial = pd.DataFrame(new_rows, columns=expected_columns)
        df_orchestrator = pd.concat([df_orchestrator, df_partial], ignore_index=True)

    return dataset, df_orchestrator

def main():
    dataset = spark.sql("SELECT * FROM test_datasets").toPandas()

    df_orchestrator = pd.DataFrame(columns=['request_id', 'request', 'response'])

    responses_dataset, internal_dataset = run_batch_prompts(dataset, df_orchestrator)

    import mlflow

    # Evaluate the test cases (end reasoning process)
    result = mlflow.evaluate(
        data=pd.DataFrame(responses_dataset),
        model_type="databricks-agent",
        evaluator_config={
            "databricks-agent": {
                "metrics": ["correctness", "safety"]
            }
        }
    )

    display(result.tables['eval_results'])

    # Evaluate the internal orchestrator conversation
    result = mlflow.evaluate(
        data=pd.DataFrame(internal_dataset),
        model_type="databricks-agent",
        evaluator_config={
            "databricks-agent": {
                "metrics": ["relevance_to_query", "safety"]
            }
        }
    )

    display(result.tables['eval_results'])

if __name__ == "__main__":
    main()

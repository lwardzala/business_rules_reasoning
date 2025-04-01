import mlflow
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

def main():
    # Initialize the HuggingFace model and tokenizer
    model_name = "meta-llama/Llama-3.2-3B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Define model parameters
    model_kwargs = {
        "max_new_tokens": 100,
        "temperature": 0.2,
        "top_k": 1,
        "top_p": 0.4
    }

    # Initialize the LLMOrchestrator
    orchestrator = LLMOrchestrator(
        knowledge_base_retriever=knowledge_base_retriever_from_tables,
        inference_state_retriever=inference_state_retriever,
        llm=HuggingFacePipeline(model_name=model_name, tokenizer=tokenizer, model=model, **model_kwargs),
        options=OrchestratorOptions()
    )

    # Register the orchestrator with MLflow
    with mlflow.start_run(run_name="LLMOrchestratorRun"):
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("max_new_tokens", model_kwargs["max_new_tokens"])
        mlflow.log_param("temperature", model_kwargs["temperature"])
        mlflow.log_param("top_k", model_kwargs["top_k"])
        mlflow.log_param("top_p", model_kwargs["top_p"])
        mlflow.pyfunc.log_model(
            artifact_path="llm_orchestrator",
            python_model=orchestrator,
            registered_model_name="LLMOrchestrator"
        )

if __name__ == "__main__":
    main()
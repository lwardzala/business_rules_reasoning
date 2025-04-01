import mlflow
import pandas as pd
import uuid
from business_rules_reasoning.base import Variable

def load_llm_orchestrator(model_name: str):
    return mlflow.pyfunc.load_model(f"models:/{model_name}/latest")

def run_batch_prompts(orchestrator, dataset: pd.DataFrame) -> pd.DataFrame:
    for index, row in dataset.iterrows():
        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        dataset.at[index, "request_id"] = request_id

        # Run the query through the orchestrator
        response = orchestrator.query(row["request"], return_full_context=True)

        # Update the dataset with model outputs
        dataset.at[index, "response"] = response["response"]
        dataset.at[index, "expected_facts"] = [
            {"id": item["id"], "value": item["value"]} for item in response["reasoning_process"]["reasoned_items"]
        ]
        dataset.at[index, "retrieved_context"] = []

    return dataset

def main():
    # Load the registered LLMOrchestrator model
    model_name = "LLMOrchestrator"
    orchestrator = load_llm_orchestrator(model_name)

    # Create a testing dataset
    dataset = pd.DataFrame({
        "request": [
            "Evaluate the loan application for John Doe.",
            "Check if the customer is eligible for a loan."
        ],
        "response": [None, None],
        "expected_facts": [None, None],
        "expected_response": ["Loan approved.", "Eligible for loan."],
        "expected_retrieved_context": [[], []],
        "retrieved_context": [[], []]
    })

    # Run batch prompts
    updated_dataset = run_batch_prompts(orchestrator, dataset)

if __name__ == "__main__":
    main()

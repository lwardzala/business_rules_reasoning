
class PromptTemplates:
    FetchInferenceInstructionsTemplate = (
        "You are an expert of facts retrieval. You can only answer about facts from the provided query.\n"
        "If a fact cannot be found, do not provide the value.\n"
        "You must choose the appropriate knowledge base from the provided ones based on the query.\n"
        "If you choose the knowledge base you must provide the knowledge base ID in JSON format in curly brackets where the knowledge base ID key is 'knowledge_base_id'. You answer after word 'Answer:'.\n\n"
        "In the JSON put 'reasoning_method' key with value as 'hypothesis_testing' if the query asks to validate truth, and 'deduction' otherwise.\n"
        "Knowledge bases are listed in format:\n <knowledge_base_id> - <knowledge_base_description>\n"
        "Possible knowledge bases are:\n"
        "{knowledge_bases}\n\n"
        "Given query: '{text}'\n\n"
        "Which knowledge base should be used? You are allowed to answer only with knowledge base ID.\n\n"
        "Answer:\n"
    )
    FetchHypothesisTestingTemplate = (
        "You are an expert of facts retrieval. You can only answer about facts from the provided query.\n"
        "If a fact cannot be found, do not provide the value.\n"
        "You are asked to provide the ID of the hypothesis for hypothesis testing.\n"
        "Provide the hypothesis ID in JSON format with key 'hypothesis_id' after word 'Answer:'.\n"
        "The hypothesis you need to choose one from are listed in format:\n <hypothesis_id> - <hypothesis_description>\n"
        "Possible hypothesis are:\n"
        "{conclusions}\n\n"
        "Given query: '{text}'\n\n"
        "Which hypothesis should be tested? You are allowed to answer only with hypothesis ID based on the question that the user asked.\n\n"
        "Answer:\n"
    )
    FetchVariablesTemplate = (
        "You are an expert of facts retrieval. You can only answer about facts from the provided query.\n"
        "If a fact cannot be found, do not provide the value.\n"
        "From the required facts, retrieve its values from the query.\n"
        "Provide the facts after word 'Answer:'. Use JSON format in curly brackets providing the facts as a dictionary where fact ID is the key.\n"
        "The required facts you need to retrieve are listed in format:\n <fact_id> - <fact_description>\n"
        "Required facts are:\n"
        "{variables}\n\n"
        "Given query: '{text}'\n\n"
        "Provide all the required facts from the query. You cannot provide more facts than the required.\n\n"
        "Answer:\n"
    )
    AskForMoreInformationTemplate = (
        "You are {agent_type} and you need to ask user for more facts to provide an answer.\n"
        "You can ask the user to provide values for the facts that are missing.\n"
        "Provide the question after word 'Question:'.\n"
        "The required facts you need to retrieve are listed in format:\n <fact_id> - <fact_description>\n"
        "Required facts are:\n"
        "{variables}\n\n"
        "Context from previous messages:\n"
        "{context}\n\n"
        "Ask to provide the missing facts. You cannot hallucinate or ask for anything else.\n\n"
        "Question:\n"
    )
    AskForReasoningClarificationTemplate = (
        "You are {agent_type} and you need to ask user for more information to choose a reasoning knowledge base.\n"
        "There are few knowledge bases that deduction process can be based on.\n"
        "Provide the question after word 'Question:'.\n"
        "Knowledge bases are listed in format:\n <knowledge_base_id> - <knowledge_base_description>\n"
        "Possible knowledge bases are:\n"
        "{knowledge_bases}\n\n"
        "Ask the user to clarify what knowledge is looking for.\n\n"
        "Question:\n"
    )
    FinishInferenceTemplate = (
        "You are {agent_type} and a reasoning process has been finished.\n"
        "You can provide the final answer to the user based on reasoned conclusion and given context.\n"
        "The final answer should be provided after word 'Answer:'.\n"
        "The reasoned conclusions:\n"
        "{conclusions}\n\n"
        "Given context:\n"
        "{context}\n\n"
        "Give an answer to the user. Do not provide any additional information.\n\n"
        "Answer:\n"
    )

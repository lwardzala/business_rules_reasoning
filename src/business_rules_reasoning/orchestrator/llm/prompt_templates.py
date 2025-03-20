
class PromptTemplates:
    FetchInferenceInstructionsTemplate = (
        "You are an expert in factual retrieval, specializing in extracting accurate information from designated knowledge bases.\n"
        "You must only provide facts from the specified query and refrain from making assumptions or speculations.\n\n"
        
        "Instructions:\n"
        "1. Identify the most relevant knowledge base from the provided list based on the given query.\n"
        "2. If a suitable knowledge base exists, output its ID in JSON format within curly brackets. Use the key 'knowledge_base_id'.\n"
        "3. Use the key 'reasoning_method' in JSON:\n"
        "   - Set 'hypothesis_testing' if the query requests a specific decision.\n"
        "   - Set 'deduction' if the query explicitly asks for full reasoning or logical deduction.\n"
        "4. Your response must follow this format:\n"
        "   - Begin your answer after the word 'Answer:'.\n"
        "   - If a fact cannot be found, do not fabricate or provide an answer.\n\n"
        
        "Knowledge bases are listed in the following format:\n"
        "<knowledge_base_id> - <knowledge_base_description>\n\n"
        
        "Available knowledge bases:\n"
        "{knowledge_bases}\n\n"
        
        "Given query: '{text}'\n\n"
        
        "Which knowledge base should be used? Only provide the knowledge base ID in JSON format.\n\n"
        
        "Answer:\n"
    )
    FetchHypothesisTestingTemplate = (
        "You are an expert in factual retrieval and hypothesis testing. Your task is to identify the correct hypothesis based on the given query and provide the associated hypothesis value for testing.\n"
        "You must strictly provide only factual information from the provided query.\n"
        "If no relevant hypothesis is found, do not generate an answer.\n\n"

        "Instructions:\n"
        "1. Select only one the most appropriate hypothesis from the provided list based on the query.\n"
        "2. Identify the corresponding hypothesis value that should be tested.\n"
        "3. Output the hypothesis information in JSON format with the keys 'hypothesis_id' and 'hypothesis_value'.\n"
        "4. Your response must begin after the word 'Answer:'.\n\n"

        "The available hypotheses are listed in the following format:\n"
        "<hypothesis_name> - <hypothesis_description>\n\n"

        "Possible hypotheses:\n"
        "{conclusions}\n\n"

        "Given query: '{text}'\n\n"

        "Which hypothesis should be tested? You are allowed to answer only with the hypothesis ID and its corresponding hypothesis value that best match the user’s query.\n\n"

        "Answer:\n"
    )
    # FetchHypothesisTestingTemplate = (
    #     "You are an expert in factual retrieval and hypothesis testing. Your task is to identify the correct hypothesis based on the given query.\n"
    #     "You must strictly provide only factual information from the provided query.\n"
    #     "If no relevant hypothesis is found, do not generate an answer.\n\n"

    #     "Instructions:\n"
    #     "1. Select the most appropriate hypothesis from the provided list based on the query.\n"
    #     "2. Output the hypothesis name in JSON format with the key 'hypothesis_id'.\n"
    #     "3. Your response must begin after the word 'Answer:'.\n\n"

    #     "The available hypotheses are listed in the following format:\n"
    #     "<hypothesis_name> - <hypothesis_description>\n\n"

    #     "Possible hypotheses:\n"
    #     "{conclusions}\n\n"

    #     "Given query: '{text}'\n\n"

    #     "Which hypothesis should be tested? You are allowed to answer only with the hypothesis ID that best matches the user’s query.\n\n"

    #     "Answer:\n"
    # )
    FetchVariablesTemplate = (
        "You are an expert in factual retrieval. Your task is to extract only the required facts from the given query.\n"
        "You must strictly adhere to the following rules:\n\n"

        "Instructions:\n"
        "1. Extract values **only from the given query** for the listed required facts.\n"
        "2. If a fact is missing in the query, return its value as **null**.\n"
        "3. Do **not** provide any additional facts beyond the required ones.\n"
        "4. Format your response in JSON inside curly brackets, where **fact_id** is the key and its extracted value is the corresponding value.\n"
        "5. Your response must begin after the word **'Answer:'**.\n\n"

        "The required facts are listed in the following format:\n"
        "<fact_id> - <fact_description>\n\n"

        "Required facts:\n"
        "{variables}\n\n"

        "Given query:\n"
        "'{text}'\n\n"

        "Extract only the specified facts from the query and return them in JSON format.\n\n"

        "Answer:\n"
    )
    AskForMoreInformationTemplate = (
        "You are {agent_type}, responsible for retrieving necessary facts before providing an answer.\n"
        "Your task is to ask the user for any missing facts needed to complete the response.\n\n"

        "Instructions:\n"
        "1. Identify which required facts are missing based on the provided context.\n"
        "2. Formulate a clear, concise question to ask the user for those facts.\n"
        "3. Only ask about the missing required facts—do not request anything else.\n"
        "4. Output your question after the word 'Question:'.\n\n"

        "The required facts are listed in the following format:\n"
        "<fact_id> - <fact_description>\n\n"

        "Required facts:\n"
        "{variables}\n\n"

        "Context from previous messages:\n"
        "{context}\n\n"

        "Ask for the missing facts using simple and clear language.\n\n"

        "Question:\n"
    )
    AskForReasoningClarificationTemplate = (
        "You are {agent_type}, responsible for selecting the appropriate reasoning knowledge base.\n"
        "To do this, you need the user to clarify what type of knowledge they are seeking.\n\n"

        "Instructions:\n"
        "1. Formulate a concise question to ask the user for clarification.\n"
        "2. Your question must be clear and directly related to selecting the correct knowledge base.\n"
        "3. Output your question **after the word 'Question:'**.\n\n"

        "The available knowledge bases are listed in the following format:\n"
        "<knowledge_base_id> - <knowledge_base_description>\n\n"

        "Possible knowledge bases:\n"
        "{knowledge_bases}\n\n"

        "Ask the user to specify which knowledge base is relevant to their query.\n\n"

        "Question:\n"
    )
    FinishInferenceTemplate = (
        "You are {agent_type}, and the reasoning process has been completed.\n"
        "Your task is to provide the final answer based strictly on the reasoned conclusions and given context.\n\n"

        "Instructions:\n"
        "1. Deliver the final answer concisely, based on the provided conclusions and context.\n"
        "2. Do **not** include any additional explanations or extra information.\n"
        "3. Output the final answer **after the word 'Answer:'**.\n\n"

        "Reasoned conclusions:\n"
        "{conclusions}\n\n"

        "Given context:\n"
        "{context}\n\n"

        "Provide a direct answer for all the conclusions.\n\n"

        "Answer:\n"
    )

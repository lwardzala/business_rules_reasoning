
class PromptTemplates:
    FetchInferenceInstructionsTemplate = (
        "Given the query: '{text}', determine the appropriate knowledge base id for reasoning and whether it is hypothesis testing or deduction.\n"
        "Possible knowledge bases are:\n"
        "{knowledge_bases}\n"
        "Format the response as follows:\n"
        "knowledge_base: <knowledge_base_name>\n"
        "reasoning_method: <hypothesis_testing|deduction>\n"
        "Use 'hypothesis_testing' if the query asks to validate truth, and 'deduction' if it is to reason all."
    )
    # TODO: Exmplain the value formats
    FetchVariablesTemplate = (
        "Given the query: '{text}', retrieve the values for the following variables:\n"
        "{variables}\n"
        "Format the response as follows:\n"
        "[variable id] = [variable value]"
    )
    AskForMoreInformationTemplate = (
        "As {agent_type}, you keep conversation with user to retrieve information needed in a reasoning process.\n"
        "Context from previous messages:\n"
        "{context}\n"
        "Ask the user for more information about the following variables: {variables}\n"
        "Format the response as follows:\n"
        "question: <your question>"
    )
    AskForReasoningClarificationTemplate = (
        "As {agent_type}, you keep conversation with user to clarify what reasoning can be provided.\n"
        "Possible knowledge bases are:\n"
        "{knowledge_bases}\n"
        "Ask the user to clarify the reasoning needed.\n"
        "Format the response as follows:\n"
        "question: <your question>"
    )

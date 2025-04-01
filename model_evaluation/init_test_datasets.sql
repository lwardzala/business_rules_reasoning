CREATE OR REPLACE TABLE test_datasets (
    request_id STRING COMMENT 'Randomized unique identifier for the request',
    request STRING COMMENT 'Prompt query',
    response STRING COMMENT 'Model output response',
    expected_facts ARRAY<STRING> COMMENT 'Array of reasoned items from the model output',
    expected_response STRING COMMENT 'Expected response from the model',
    expected_retrieved_context ARRAY<STRUCT<doc_uri: STRING, content: STRING>> COMMENT 'Expected retrieved context with document URI and content',
    retrieved_context ARRAY<STRUCT<doc_uri: STRING, content: STRING>> COMMENT 'Retrieved context with document URI and content'
)
COMMENT 'Table to store test datasets for batch prompt evaluation';

INSERT INTO test_datasets (
    request_id,
    request,
    response,
    expected_facts,
    expected_response,
    expected_retrieved_context,
    retrieved_context
)
VALUES (
    NULL,
    'Bank Screening Document

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

    Check the customer document for loan acceptance and check if is needed to forward to bank verification team',
    NULL,
    ARRAY(
        'loan_accepted = True',
        'forward_to_bank_verification = True'
    ),
    'The loan has been accepted and is moving forward to bank verification.',
    ARRAY(
        STRUCT('knowledge_base_id', '
            leasing_document_decision_table - Knowledge base for processing leasing documents:
            (unpaid_loans = True) → loan_accepted = False
            (fraud_database = True) → loan_accepted = False
            (employment_type = unemployed) → loan_accepted = False
            (monthly_net_salary < 2000) → loan_accepted = False
            (employment_type != unemployed ∧ monthly_net_salary >= 2000 ∧ fraud_database = False ∧ unpaid_loans = False) → loan_accepted = True
            (employment_type = freelancer) → forward_to_bank_verification = True
            (thirty_percent_ruling = True) → forward_to_bank_verification = True
            (previous_loans = False ∧ ongoing_loans = False) → forward_to_bank_verification = True
        '),
        STRUCT('reasoning_method', 'DEDUCTION'),
        STRUCT('reasoning_hypothesis', 'None')
    ),
    NULL
);

INSERT INTO test_datasets (
    request_id,
    request,
    response,
    expected_facts,
    expected_response,
    expected_retrieved_context,
    retrieved_context
)
VALUES (
    NULL,
    'Bank Screening Document

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

    Employment Type: Company Employee

    30% Ruling Check:
    No

    Check the customer document for loan acceptance and check if is needed to forward to bank verification team',
    NULL,
    ARRAY(
        'loan_accepted = True'
    ),
    'The loan has been accepted.',
    ARRAY(
        STRUCT('knowledge_base_id', '
            leasing_document_decision_table - Knowledge base for processing leasing documents:
            (unpaid_loans = True) → loan_accepted = False
            (fraud_database = True) → loan_accepted = False
            (employment_type = unemployed) → loan_accepted = False
            (monthly_net_salary < 2000) → loan_accepted = False
            (employment_type != unemployed ∧ monthly_net_salary >= 2000 ∧ fraud_database = False ∧ unpaid_loans = False) → loan_accepted = True
            (employment_type = freelancer) → forward_to_bank_verification = True
            (thirty_percent_ruling = True) → forward_to_bank_verification = True
            (previous_loans = False ∧ ongoing_loans = False) → forward_to_bank_verification = True
        '),
        STRUCT('reasoning_method', 'DEDUCTION'),
        STRUCT('reasoning_hypothesis', 'None')
    ),
    NULL
);

INSERT INTO test_datasets (
    request_id,
    request,
    response,
    expected_facts,
    expected_response,
    expected_retrieved_context,
    retrieved_context
)
VALUES (
    NULL,
    'Bank Screening Document

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
    Monthly Net Salary: 1,000 EUR

    Employment Type: Company Employee

    30% Ruling Check:
    No

    Check the customer document for loan acceptance and check if is needed to forward to bank verification team',
    NULL,
    ARRAY(
        'loan_accepted = False'
    ),
    'The loan has not been accepted.',
    ARRAY(
        STRUCT('knowledge_base_id', '
            leasing_document_decision_table - Knowledge base for processing leasing documents:
            (unpaid_loans = True) → loan_accepted = False
            (fraud_database = True) → loan_accepted = False
            (employment_type = unemployed) → loan_accepted = False
            (monthly_net_salary < 2000) → loan_accepted = False
            (employment_type != unemployed ∧ monthly_net_salary >= 2000 ∧ fraud_database = False ∧ unpaid_loans = False) → loan_accepted = True
            (employment_type = freelancer) → forward_to_bank_verification = True
            (thirty_percent_ruling = True) → forward_to_bank_verification = True
            (previous_loans = False ∧ ongoing_loans = False) → forward_to_bank_verification = True
        '),
        STRUCT('reasoning_method', 'DEDUCTION'),
        STRUCT('reasoning_hypothesis', 'None')
    ),
    NULL
);

INSERT INTO test_datasets (
    request_id,
    request,
    response,
    expected_facts,
    expected_response,
    expected_retrieved_context,
    retrieved_context
)
VALUES (
    NULL,
    'Bank Screening Document

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

    Employment Type: Company Employee

    30% Ruling Check:
    No

    Check the customer document for loan acceptance and check if is needed to forward to bank verification team',
    NULL,
    ARRAY(),
    'What is the month net salary?',
    ARRAY(
        STRUCT('knowledge_base_id', '
            leasing_document_decision_table - Knowledge base for processing leasing documents:
            (unpaid_loans = True) → loan_accepted = False
            (fraud_database = True) → loan_accepted = False
            (employment_type = unemployed) → loan_accepted = False
            (monthly_net_salary < 2000) → loan_accepted = False
            (employment_type != unemployed ∧ monthly_net_salary >= 2000 ∧ fraud_database = False ∧ unpaid_loans = False) → loan_accepted = True
            (employment_type = freelancer) → forward_to_bank_verification = True
            (thirty_percent_ruling = True) → forward_to_bank_verification = True
            (previous_loans = False ∧ ongoing_loans = False) → forward_to_bank_verification = True
        '),
        STRUCT('reasoning_method', 'DEDUCTION'),
        STRUCT('reasoning_hypothesis', 'None')
    ),
    NULL
);

INSERT INTO test_datasets (
    request_id,
    request,
    response,
    expected_facts,
    expected_response,
    expected_retrieved_context,
    retrieved_context
)
VALUES (
    NULL,
    'Bank Screening Document

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
    Monthly Net Salary: 1,000 EUR

    Employment Type: Company Employee

    30% Ruling Check:
    No

    Can the customer loan acceptance be rejected?',
    NULL,
    ARRAY(
        'loan_accepted = False'
    ),
    'Yes.',
    ARRAY(
        STRUCT('knowledge_base_id', '
            leasing_document_decision_table - Knowledge base for processing leasing documents:
            (unpaid_loans = True) → loan_accepted = False
            (fraud_database = True) → loan_accepted = False
            (employment_type = unemployed) → loan_accepted = False
            (monthly_net_salary < 2000) → loan_accepted = False
            (employment_type != unemployed ∧ monthly_net_salary >= 2000 ∧ fraud_database = False ∧ unpaid_loans = False) → loan_accepted = True
            (employment_type = freelancer) → forward_to_bank_verification = True
            (thirty_percent_ruling = True) → forward_to_bank_verification = True
            (previous_loans = False ∧ ongoing_loans = False) → forward_to_bank_verification = True
        '),
        STRUCT('reasoning_method', 'HYPOTHESIS_TESTING'),
        STRUCT('reasoning_hypothesis', 'loan_accepted = False')
    ),
    NULL
);

INSERT INTO test_datasets (
    request_id,
    request,
    response,
    expected_facts,
    expected_response,
    expected_retrieved_context,
    retrieved_context
)
VALUES (
    NULL,
    'quesrtion?',
    NULL,
    ARRAY(
        'action = BUY'
    ),
    'Yes.',
    ARRAY(
        STRUCT('knowledge_base_id', "
            stock_decision_rules - buy/sell stock decisions based on a report:
            (pe_ratio_condition < 15.0 ∧ sentiment_condition IN ['positive', 'neutral'] ∧ volatility_condition <= 0.2) → action = BUY
            (pe_ratio_condition >= 15 AND <=25 ∧ sentiment_condition IN ['positive'] ∧ volatility_condition <= 0.3) → action = HOLD
            (pe_ratio_condition > 25.0 ∧ sentiment_condition IN ['negative'] ∧ volatility_condition > 0.3) → action = SELL
            (pe_ratio_condition = is_not_null ∧ sentiment_condition IN ['negative'] ∧ volatility_condition = any) → action = SELL
            (pe_ratio_condition = any ∧ sentiment_condition = any ∧ volatility_condition = any) → action = HOLD
        "),
        STRUCT('reasoning_method', 'DEDUCTION'),
        STRUCT('reasoning_hypothesis', 'None')
    ),
    NULL
);
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
    "loan_processing_accepted_with_verification_deductive",
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
    NULL,
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
        STRUCT('reasoning_hypothesis', 'None'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'loan_accepted = True, forward_to_bank_verification = True')
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
    "loan_processing_accepted_deductive",
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
    NULL,
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
        STRUCT('reasoning_hypothesis', 'None'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'loan_accepted = True')
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
    "loan_processing_rejected_deductive",
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
    NULL,
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
        STRUCT('reasoning_hypothesis', 'None'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'loan_accepted = False')
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
    "loan_processing_ask_salary_deductive",
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
    NULL,
    'expected response: must ask what is the month net salary.',
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
        STRUCT('reasoning_hypothesis', 'None'),
        STRUCT('engine_status', 'MISSING_VALUES'),
        STRUCT('reasoned_items', '')
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
    "loan_processing_rejected_hypothesis",
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
    NULL,
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
        STRUCT('reasoning_hypothesis', 'loan_accepted = False'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'loan_accepted = False')
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
    "stock_analysis_buy_deductive",
    "
    The P/E ratio is 14, indicating it may be undervalued relative to its earnings potential.
    Sentiment analysis on recent news and earnings reports shows a positive outlook.
    The stock's volatility is 0.2, suggesting a stable price movement and lower risk.
    The company has reported consistent revenue growth over the past four quarters.

    What should we do with the stock?
    ",
    NULL,
    ARRAY(
        'action = BUY'
    ),
    NULL,
    ARRAY(
        STRUCT('knowledge_base_id', "
            stock_decision_rules - buy/sell stock decisions based on a report:
            (pe_ratio_condition < 15.0 ∧ sentiment_condition IN ['positive', 'neutral'] ∧ volatility_condition <= 0.2) → action = BUY
            (pe_ratio_condition BETWEEN [15, 25] ∧ sentiment_condition IN ['positive'] ∧ volatility_condition <= 0.3) → action = HOLD
            (pe_ratio_condition > 25.0 ∧ sentiment_condition IN ['negative'] ∧ volatility_condition > 0.3) → action = SELL
        "),
        STRUCT('reasoning_method', 'DEDUCTION'),
        STRUCT('reasoning_hypothesis', 'None'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'action = BUY')
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
    "stock_analysis_hold_hypothesis",
    "
    The P/E ratio is 20, indicating the stock is fairly valued.
    Sentiment analysis reflects generally positive sentiment, but not strong enough to justify aggressive action.
    Volatility is moderate (up to 0.3), implying a balance of risk and potential reward.
    The company has met earnings expectations but has not significantly outperformed.
    No major changes in insider or institutional holdings.

    Should we hold the stock?
    ",
    NULL,
    ARRAY(
        'action = HOLD'
    ),
    NULL,
    ARRAY(
        STRUCT('knowledge_base_id', "
            stock_decision_rules - buy/sell stock decisions based on a report:
            (pe_ratio_condition < 15.0 ∧ sentiment_condition IN ['positive', 'neutral'] ∧ volatility_condition <= 0.2) → action = BUY
            (pe_ratio_condition BETWEEN [15, 25] ∧ sentiment_condition IN ['positive'] ∧ volatility_condition <= 0.3) → action = HOLD
            (pe_ratio_condition > 25.0 ∧ sentiment_condition IN ['negative'] ∧ volatility_condition > 0.3) → action = SELL
        "),
        STRUCT('reasoning_method', 'HYPOTHESIS_TESTING'),
        STRUCT('reasoning_hypothesis', 'action = HOLD'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'action = HOLD')
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
    "stock_analysis_sell_deductive",
    "
    The P/E ratio is 26, suggesting the stock might be overvalued.
    Sentiment analysis indicates negative public or investor sentiment, possibly due to poor earnings or guidance.
    The stock's volatility is high 0.4, reflecting increased risk.
    The company has missed earnings estimates in multiple quarters.

    What should we do with the stock?
    ",
    NULL,
    ARRAY(
        'action = SELL'
    ),
    NULL,
    ARRAY(
        STRUCT('knowledge_base_id', "
            stock_decision_rules - buy/sell stock decisions based on a report:
            (pe_ratio_condition < 15.0 ∧ sentiment_condition IN ['positive', 'neutral'] ∧ volatility_condition <= 0.2) → action = BUY
            (pe_ratio_condition BETWEEN [15, 25] ∧ sentiment_condition IN ['positive'] ∧ volatility_condition <= 0.3) → action = HOLD
            (pe_ratio_condition > 25.0 ∧ sentiment_condition IN ['negative'] ∧ volatility_condition > 0.3) → action = SELL
        "),
        STRUCT('reasoning_method', 'DEDUCTION'),
        STRUCT('reasoning_hypothesis', 'None'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'action = SELL')
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
    "stock_analysis_ask_more_deductive",
    "
    The P/E ratio is 26, suggesting the stock might be overvalued.
    Sentiment analysis indicates negative public or investor sentiment, possibly due to poor earnings or guidance.

    What should we do with the stock?
    ",
    NULL,
    NULL,
    "expected response: must ask what is the volatility condition.",
    ARRAY(
        STRUCT('knowledge_base_id', "
            stock_decision_rules - buy/sell stock decisions based on a report:
            (pe_ratio_condition < 15.0 ∧ sentiment_condition IN ['positive', 'neutral'] ∧ volatility_condition <= 0.2) → action = BUY
            (pe_ratio_condition BETWEEN [15, 25] ∧ sentiment_condition IN ['positive'] ∧ volatility_condition <= 0.3) → action = HOLD
            (pe_ratio_condition > 25.0 ∧ sentiment_condition IN ['negative'] ∧ volatility_condition > 0.3) → action = SELL
        "),
        STRUCT('reasoning_method', 'DEDUCTION'),
        STRUCT('reasoning_hypothesis', 'None'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'action = SELL')
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
    "random_question_ask_more",
    "
    I don't know how to use iron. Is stainless steel heavy?
    ",
    NULL,
    NULL,
    "expected response: must askthe user to clarify what type of knowledge they are seeking",
    ARRAY(),
    NULL
);

----- AI generated tests
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
    "loan_processing_fraud_rejected",
    'Bank Screening Document

    Customer Information:
    Name: Jane Smith
    Customer ID: 987654321

    Loan History (BKR Check):
    Loans:
    - Mortgage (Paid, closed)
    Current Loan Status: No active loans

    Fraud Database Check:
    Status: Record found in internal fraud databases

    Financial Information:
    Monthly Net Salary: 4,000 EUR

    Employment Type: Company Employee

    30% Ruling Check:
    No

    Check the customer document for loan acceptance.',
    NULL,
    ARRAY(
        'loan_accepted = False'
    ),
    NULL,
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
        STRUCT('reasoning_hypothesis', 'None'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'loan_accepted = False')
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
    "loan_processing_unemployed_rejected",
    'Bank Screening Document

    Customer Information:
    Name: Alex Brown
    Customer ID: 555555555

    Loan History (BKR Check):
    Loans:
    - None
    Current Loan Status: No active loans

    Fraud Database Check:
    Status: No record found in internal fraud databases

    Financial Information:
    Monthly Net Salary: 2,500 EUR

    Employment Type: Unemployed

    30% Ruling Check:
    No

    Check the customer document for loan acceptance.',
    NULL,
    ARRAY(
        'loan_accepted = False'
    ),
    NULL,
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
        STRUCT('reasoning_hypothesis', 'None'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'loan_accepted = False')
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
    "loan_processing_30_percent_ruling_verification",
    'Bank Screening Document

    Customer Information:
    Name: Maria Green
    Customer ID: 222333444

    Loan History (BKR Check):
    Loans:
    - Personal Loan (Paid, closed)
    Current Loan Status: No active loans

    Fraud Database Check:
    Status: No record found in internal fraud databases

    Financial Information:
    Monthly Net Salary: 3,500 EUR

    Employment Type: Company Employee

    30% Ruling Check:
    Yes

    Check the customer document for loan acceptance and check if is needed to forward to bank verification team',
    NULL,
    ARRAY(
        'loan_accepted = True',
        'forward_to_bank_verification = True'
    ),
    NULL,
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
        STRUCT('reasoning_hypothesis', 'None'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'loan_accepted = True, forward_to_bank_verification = True')
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
    "loan_processing_no_history_verification",
    'Bank Screening Document

    Customer Information:
    Name: Lisa White
    Customer ID: 888999777

    Loan History (BKR Check):
    Loans:
    - None
    Current Loan Status: No active loans

    Fraud Database Check:
    Status: No record found in internal fraud databases

    Financial Information:
    Monthly Net Salary: 2,800 EUR

    Employment Type: Company Employee

    30% Ruling Check:
    No

    Previous Loans: No
    Ongoing Loans: No

    Check the customer document for loan acceptance and check if is needed to forward to bank verification team',
    NULL,
    ARRAY(
        'loan_accepted = True',
        'forward_to_bank_verification = True'
    ),
    NULL,
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
        STRUCT('reasoning_hypothesis', 'None'),
        STRUCT('engine_status', 'PASSED'),
        STRUCT('reasoned_items', 'loan_accepted = True, forward_to_bank_verification = True')
    ),
    NULL
);
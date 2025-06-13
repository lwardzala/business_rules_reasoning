CREATE OR REPLACE TABLE leasing_document_decision_table (
    unpaid_loans STRING COMMENT "Indicates if there are any open un-paid loans: 'yes' or 'no'",
    fraud_flag STRING COMMENT "Indicates if the fraud database has any records: 'yes' or 'no'",
    employment_type STRING COMMENT "Employment Type option from: [freelancer, company emplyoee, unemployed]",
    monthly_net_salary STRING COMMENT "Monthly Net Salary",
    thirty_percent_ruling STRING COMMENT "30% Ruling - 'yes' if applicable othwerwise 'no'",
    previous_loans STRING COMMENT "Indicates if there were any historical paid loans",
    ongoing_loans STRING COMMENT "Indicates whether there is any open loans",
    loan_accepted BOOLEAN COMMENT "Loan Accepted",
    forward_to_bank_verification BOOLEAN COMMENT "Forward to additional bank verification"
)
COMMENT "Knowledge base for processing leasing documents";

INSERT INTO zenchef_datalake.test.leasing_document_decision_table VALUES
    ('True', NULL, NULL, NULL, NULL, NULL, NULL, False, NULL),
    (NULL, 'True', NULL, NULL, NULL, NULL, NULL, False, NULL),
    (NULL, NULL, 'unemployed', NULL, NULL, NULL, NULL, False, NULL),
    (NULL, NULL, NULL, '<2000', NULL, NULL, NULL, False, NULL),
    ('False', 'False', '!=unemployed', '>=2000', NULL, NULL, NULL, True, NULL),
    (NULL, NULL, 'freelancer', NULL, NULL, NULL, NULL, NULL, True),
    (NULL, NULL, NULL, NULL, 'True', NULL, NULL, NULL, True),
    (NULL, NULL, NULL, NULL, NULL, 'False', 'False', NULL, True);

CREATE OR REPLACE TABLE stock_decision_rules (
  pe_ratio_condition STRING COMMENT "Numeric P/E ratio like 15, 25, etc.",
  sentiment_condition STRING COMMENT "Sentiment analysis result: positive, negative, etc.",
  volatility_condition STRING COMMENT "Stock volatility rules",
  `action` STRING COMMENT "Final decision: BUY, SELL, HOLD"
)
COMMENT "stock action decisions based on a report";

INSERT INTO zenchef_datalake.test.stock_decision_rules VALUES
  ('<15', 'is_in(positive, neutral)', '<=0.2', 'BUY'),
  ('between(15, 25)', 'is_in(positive)', '<=0.3', 'HOLD'),
  ('>25', 'is_in(negative)', '>0.3', 'SELL');
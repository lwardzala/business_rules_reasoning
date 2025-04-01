-- Create the decision table
CREATE TABLE IF NOT EXISTS leasing_document_decision_table (
    rule_id STRING,
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

-- Insert rules into the decision table
INSERT INTO leasing_document_decision_table VALUES
    -- Rule 1: If the client has any unpaid loans, reject the loan
    ('rule1', 'True', NULL, NULL, NULL, NULL, NULL, NULL, False, NULL),

    -- Rule 2: If the client is flagged in the fraud database, reject the loan
    ('rule2', NULL, 'True', NULL, NULL, NULL, NULL, NULL, False, NULL),

    -- Rule 3: If the client is unemployed, reject the loan
    ('rule3', NULL, NULL, 'unemployed', NULL, NULL, NULL, NULL, False, NULL),

    -- Rule 4: If the client's monthly net salary is less than 2000, reject the loan
    ('rule4', NULL, NULL, NULL, '<2000', NULL, NULL, NULL, False, NULL),

    -- Rule 5: If the client meets all conditions, accept the loan
    ('rule5', 'False', 'False', '!=unemployed', '>=2000', NULL, NULL, NULL, True, NULL),

    -- Rule 6: If the client is a freelancer, forward to bank verification
    ('rule6', NULL, NULL, 'freelancer', NULL, NULL, NULL, NULL, NULL, True),

    -- Rule 7: If the client qualifies for the 30% ruling, forward to bank verification
    ('rule7', NULL, NULL, NULL, NULL, 'True', NULL, NULL, NULL, True),

    -- Rule 8: If the client has no previous or ongoing loans, forward to bank verification
    ('rule8', NULL, NULL, NULL, NULL, NULL, 'False', 'False', NULL, True);

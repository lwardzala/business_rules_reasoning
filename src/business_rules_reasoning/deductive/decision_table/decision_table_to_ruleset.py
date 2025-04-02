import pandas as pd
from typing import List
import re
from ..knowledge_builder import RuleBuilder, PredicateBuilder, VariableBuilder
from ...base.operator_enums import OperatorType
from ...base.rule import Rule

def to_snake_case(name: str) -> str:
    return '_'.join(
        re.sub('([A-Z][a-z]+)', r' \1',
        re.sub('([A-Z]+)', r' \1',
        name.replace('-', ' '))).split()).lower()

def parse_value(value):
    if isinstance(value, str):
        return value.strip().lower() in ['true', '1', 'yes'] if value.strip().lower() in ["true", "false", '1', '0', 'yes', 'no'] else float(value.strip()) if value.strip().replace('.', '', 1).isdigit() else value.strip()
    
    return value

def parse_cell_value(cell_value: str):
    """
    Parse a cell value to extract the operator and value.
    If no operator is found, default to EQUAL.
    """
    operator_patterns = {
        OperatorType.EQUAL: r"^=(.+)$",
        OperatorType.NOT_EQUAL: r"^!=(.+)$",
        OperatorType.GREATER_OR_EQUAL: r"^>=(.+)$",
        OperatorType.GREATER_THAN: r"^>(.+)$",
        OperatorType.LESS_OR_EQUAL: r"^<=(.+)$",
        OperatorType.LESS_THAN: r"^<(.+)$",
        OperatorType.IS_IN: r"^is_in\((.+)\)$",
        OperatorType.NOT_IN: r"^not_in\((.+)\)$",
        OperatorType.BETWEEN: r"^between\((.+)\)$",
        OperatorType.NOT_BETWEEN: r"^not_between\((.+)\)$",
        OperatorType.SUBSET: r"^subset\((.+)\)$",
        OperatorType.NOT_SUBSET: r"^not_subset\((.+)\)$",
    }

    for operator, pattern in operator_patterns.items():
        match = re.match(pattern, str(cell_value).strip())
        if match:
            value = match.group(1)
            if operator in [OperatorType.IS_IN, OperatorType.NOT_IN, OperatorType.SUBSET, OperatorType.NOT_SUBSET, OperatorType.BETWEEN, OperatorType.NOT_BETWEEN]:
                value = [
                    parse_value(v) #v.strip().lower() in ['true', '1', 'yes'] if v.strip().lower() in ["true", "false", '1', '0', 'yes', 'no'] else
                    #float(v.strip()) if v.strip().replace('.', '', 1).isdigit() else
                    #v.strip()
                    for v in value.split(",")
                ]
            else:
                value = parse_value(value) #value.strip().lower() in ['true', '1', 'yes'] if value.strip().lower() in ["true", "false", '1', '0', 'yes', 'no'] else float(value.strip()) if value.strip().replace('.', '', 1).isdigit() else value.strip()
            return operator, value

    # Default to EQUAL if no operator is found
    return OperatorType.EQUAL, parse_value(cell_value)

def pandas_to_rules(dataframe: pd.DataFrame, conclusion_index: int | List[int] = -1, features_description: dict = None) -> List[Rule]:
    """
    Convert a pandas DataFrame to a list of Rule objects.

    Args:
        dataframe (pd.DataFrame): The input DataFrame where headers are Variable IDs.
        conclusion_index (int | List[int]): The index or indices of the column(s) that represent the conclusion(s).
        features_description (dict): A dictionary mapping variable IDs to their names.

    Returns:
        List[Rule]: A list of Rule objects.
    """
    rules = []
    headers = dataframe.columns.tolist()

    # Handle multiple conclusion columns
    if isinstance(conclusion_index, list):
        for index in conclusion_index:
            sub_dataframe = dataframe.copy()
            conclusion_header = headers[index]
            sub_dataframe = sub_dataframe.drop(columns=[headers[i] for i in conclusion_index if i != index]).reset_index(drop=True)
            new_conclusion_index = sub_dataframe.columns.tolist().index(conclusion_header)
            rules.extend(pandas_to_rules(sub_dataframe, conclusion_index=new_conclusion_index, features_description=features_description))
        return rules

    # Single conclusion column case
    conclusion_column = to_snake_case(headers[conclusion_index])  # Convert to snake_case
    conclusion_name = features_description.get(conclusion_column, None) if features_description else None

    for _, row in dataframe.iterrows():
        rule_builder = RuleBuilder()
        conclusion_value = row[headers[conclusion_index]]
        if pd.isna(conclusion_value):
            continue
        conclusion_value = parse_value(conclusion_value)
        conclusion_variable = VariableBuilder().set_id(conclusion_column).set_name(conclusion_name).set_value(conclusion_value).unwrap()
        rule_builder.set_conclusion(conclusion_variable)

        for column in headers:
            if column == headers[conclusion_index]:
                continue
            cell_value = row[column]
            if pd.isna(cell_value):  # Skip if the value is NaN
                continue
            column_snake_case = to_snake_case(column)  # Convert to snake_case
            column_name = features_description.get(column_snake_case, column_snake_case) if features_description else column_snake_case
            operator, value = parse_cell_value(cell_value)
            predicate = PredicateBuilder().configure_predicate_with_name(column_snake_case, column_name, operator, value).unwrap()
            rule_builder.add_predicate(predicate)

        rules.append(rule_builder.unwrap())

    return rules

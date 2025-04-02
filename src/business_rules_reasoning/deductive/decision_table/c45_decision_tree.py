import pandas as pd
import numpy as np
from typing import Any, Dict, List

from ..knowledge_builder import RuleBuilder, PredicateBuilder, VariableBuilder
from ...base.operator_enums import OperatorType
from ...base.rule import Rule
import re

def calculate_entropy(data: pd.Series) -> float:
    """
    Calculate the entropy of a dataset.
    """
    probabilities = data.value_counts(normalize=True)
    return -sum(probabilities * np.log2(probabilities))

def calculate_information_gain(data: pd.DataFrame, attribute: str, target: str) -> float:
    """
    Calculate the information gain of splitting on a specific attribute.
    """
    total_entropy = calculate_entropy(data[target])
    values = data[attribute].unique()
    weighted_entropy = 0.0

    for value in values:
        subset = data[data[attribute] == value]
        weighted_entropy += (len(subset) / len(data)) * calculate_entropy(subset[target])

    return total_entropy - weighted_entropy

def find_best_split(data: pd.DataFrame, attributes: list, target: str) -> str:
    """
    Find the best attribute to split on based on information gain.
    """
    information_gains = {attribute: calculate_information_gain(data, attribute, target) for attribute in attributes}
    return max(information_gains, key=information_gains.get)

def build_tree(data: pd.DataFrame, attributes: list, target: str) -> Any:
    """
    Recursively build the decision tree using the C4.5 algorithm.
    """
    # If all target values are the same, return the target value
    if len(data[target].dropna().unique()) == 1:
        return data[target].iloc[0]

    # If no attributes are left to split, return the most common target value
    if not attributes:
        return data[target].mode().iloc[0]

    # Find the best attribute to split on
    best_attribute = find_best_split(data, attributes, target)
    tree = {best_attribute: {}}

    # Split the data on the best attribute and recursively build the tree
    for value in data[best_attribute].dropna().unique():  # Skip NaN values
        subset = data[data[best_attribute] == value]
        subtree = build_tree(subset, [attr for attr in attributes if attr != best_attribute], target)
        tree[best_attribute][value] = subtree

    return tree

def c45_decision_tree(dataframe: pd.DataFrame, conclusion_index: int = -1) -> Dict:
    """
    Create a decision tree using the C4.5 algorithm from a pandas DataFrame.

    Args:
        dataframe (pd.DataFrame): The input DataFrame where headers are attributes.
        conclusion_index (int): The index of the column that represents the target attribute (default is the last column).

    Returns:
        Dict: A nested dictionary representing the decision tree.
    """
    headers = dataframe.columns.tolist()
    target = headers[conclusion_index]
    attributes = [col for col in headers if col != target]

    return build_tree(dataframe, attributes, target)

def parse_value(value):
    if isinstance(value, str):
        return value.strip().lower() in ['true', '1', 'yes'] if value.strip().lower() in ["true", "false", '1', '0', 'yes', 'no'] else float(value.strip()) if value.strip().replace('.', '', 1).isdigit() else value.strip()
    
    return value

def parse_node_value(value: str):
    """
    Parse a node value to extract the operator and right term.
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
        match = re.match(pattern, str(value).strip())
        if match:
            parsed_value = match.group(1)
            if operator in [OperatorType.IS_IN, OperatorType.NOT_IN, OperatorType.SUBSET, OperatorType.NOT_SUBSET, OperatorType.BETWEEN, OperatorType.NOT_BETWEEN]:
                parsed_value = [
                    parse_value(v)
                    for v in parsed_value.split(",")
                ]
            else:
                parsed_value = parse_value(parsed_value)
            return operator, parsed_value

    # Default to EQUAL if no operator is found
    return OperatorType.EQUAL, parse_value(value)

def to_snake_case(name: str) -> str:
    return '_'.join(
        re.sub('([A-Z][a-z]+)', r' \1',
        re.sub('([A-Z]+)', r' \1',
        name.replace('-', ' '))).split()).lower()

def tree_to_rules(tree: dict, target: str, path: list, features_description: dict = None) -> List[Rule]:
    """
    Recursively convert a decision tree to a list of Rule objects.

    Args:
        tree (dict): The decision tree as a nested dictionary or a string.
        target (str): The target variable (conclusion).
        path (list): The current path of predicates.

    Returns:
        List[Rule]: A list of Rule objects.
    """
    rules = []

    target_snake_case = to_snake_case(target)  # Convert target to snake_case

    if isinstance(tree, str):
        # Leaf node: Create a rule with the accumulated path and conclusion
        rule_builder = RuleBuilder()
        for predicate in path:
            rule_builder.add_predicate(predicate)

        conclusion_name = features_description.get(target, None) if features_description else None

        conclusion_variable = VariableBuilder().set_id(target_snake_case).set_name(conclusion_name).set_value(parse_value(tree)).unwrap()
        rule_builder.set_conclusion(conclusion_variable)
        rules.append(rule_builder.unwrap())
        return rules

    for key, value in tree.items():
        key_snake_case = to_snake_case(key)  # Convert key to snake_case
        if isinstance(value, dict):
            # Internal node: Add the current condition to the path and recurse
            for node_value, subtree in value.items():
                operator, right_term = parse_node_value(node_value)
                predicate_name = features_description.get(key, None) if features_description else None
                predicate = PredicateBuilder().configure_predicate_with_name(key_snake_case, predicate_name, operator, right_term).unwrap()
                rules.extend(tree_to_rules(subtree, target, path + [predicate], features_description=features_description))
        else:
            # Leaf node: Create a rule with the accumulated path and conclusion
            rule_builder = RuleBuilder()
            for predicate in path:
                rule_builder.add_predicate(predicate)
            
            conclusion_name = features_description.get(target, None) if features_description else None
            conclusion_variable = VariableBuilder().set_id(target_snake_case).set_name(conclusion_name).set_value(parse_value(value)).unwrap()
            rule_builder.set_conclusion(conclusion_variable)
            rules.append(rule_builder.unwrap())

    return rules

def c45_ruleset(dataframe: pd.DataFrame, conclusion_index: int | List[int] = -1, features_description: dict = None) -> List[Rule]:
    """
    Generate a decision tree using the C4.5 algorithm and convert it to a list of Rule objects.

    Args:
        dataframe (pd.DataFrame): The input DataFrame where headers are attributes.
        conclusion_index (int | List[int]): The index or indices of the column(s) that represent the conclusion(s).
        features_description (dict): A dictionary mapping variable IDs to their names.

    Returns:
        List[Rule]: A list of Rule objects.
    """
    rules = []
    headers = dataframe.columns.tolist()

    if isinstance(conclusion_index, list):
        for index in conclusion_index:
            sub_dataframe = dataframe.copy()
            conclusion_header = headers[index]
            sub_dataframe = sub_dataframe.drop(columns=[headers[i] for i in conclusion_index if i != index]).reset_index(drop=True)
            new_conclusion_index = sub_dataframe.columns.tolist().index(conclusion_header)
            rules.extend(c45_ruleset(sub_dataframe, conclusion_index=new_conclusion_index, features_description=features_description))
        return rules

    tree = c45_decision_tree(dataframe, conclusion_index)
    headers = dataframe.columns.tolist()
    target = headers[conclusion_index]
    return tree_to_rules(tree, target, [], features_description=features_description)

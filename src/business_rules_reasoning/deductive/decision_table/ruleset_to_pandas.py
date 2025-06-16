import pandas as pd
from typing import List
from ...base.rule import Rule
from ...base.operator_enums import OperatorType

def format_predicate(predicate) -> str:
    """
    Format a predicate into a string representation for the DataFrame.
    """
    operator_map = {
        OperatorType.EQUAL: "=",
        OperatorType.NOT_EQUAL: "!=",
        OperatorType.GREATER_THAN: ">",
        OperatorType.GREATER_OR_EQUAL: ">=",
        OperatorType.LESS_THAN: "<",
        OperatorType.LESS_OR_EQUAL: "<=",
        OperatorType.IS_IN: "is_in",
        OperatorType.NOT_IN: "not_in",
        OperatorType.BETWEEN: "between",
        OperatorType.NOT_BETWEEN: "not_between",
        OperatorType.SUBSET: "subset",
        OperatorType.NOT_SUBSET: "not_subset",
    }

    operator = operator_map.get(predicate.operator, "=")
    if operator in ["is_in", "not_in", "between", "not_between", "subset", "not_subset"]:
        value = f"{operator}({','.join(map(str, predicate.right_term.value))})"
    else:
        value = f"{operator}{predicate.right_term.value}"
    return value

def ruleset_to_pandas(rules: List[Rule]) -> pd.DataFrame:
    """
    Convert a list of Rule objects into a pandas DataFrame.

    Args:
        rules (List[Rule]): The list of Rule objects.

    Returns:
        pd.DataFrame: A DataFrame where each row represents a rule, columns are variable IDs, and the last column is the conclusion.
    """
    data = []
    columns = set()

    for rule in rules:
        row = {}
        for predicate in rule.predicates:
            row[predicate.left_term.id] = format_predicate(predicate)
            columns.add(predicate.left_term.id)
        row[rule.conclusion.variable.id] = rule.conclusion.variable.value
        columns.add(rule.conclusion.variable.id)
        data.append(row)

    df = pd.DataFrame(data)
    df = df.reindex(columns=sorted(columns))

    return df

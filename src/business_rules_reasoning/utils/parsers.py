import re
import json
from typing import Any
from ..base import Variable

def parse_variable_value(value: str, variable: Variable) -> Any:
    try:
        # Return None if the value is null or the string "null"
        if value is None or (isinstance(value, str) and value.strip().lower() == "null"):
            return None

        if variable.get_value_type() == 'boolean':
            if isinstance(value, str):
                return value.lower() in ['true', '1', 'yes']
            else:
                return bool(value)
        elif variable.get_value_type() == 'number':
            if isinstance(value, str):
                value = re.sub(r'[^\d.]', '', value)
            return float(value)
        elif variable.get_value_type() == 'list':
            return value.split(',')
        else:
            return value
    except ValueError:
        return value

def extract_json_from_response(response: str) -> dict:
    """
    Extracts a JSON object from a given response string.

    Args:
        response (str): The response string containing a JSON object.

    Returns:
        dict: The extracted JSON object.

    Raises:
        ValueError: If no JSON object is found in the response.
    """
    json_match = re.search(r'\{.*?\}', response, re.DOTALL)
    if not json_match:
        raise ValueError("No JSON object found in the response")
    
    json_str = json_match.group().replace('\n', '').replace('}', '}')
    return json.loads(json_str)

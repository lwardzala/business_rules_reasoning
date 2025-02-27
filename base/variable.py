from .value_types import BaseType, ListType

class Variable:
    _function_escape = "="

    def __init__(self, id=None, name=None, value=None):
        self.id = id
        self.name = name if name is not None else id
        self.value = value
        self.frequency = 0

    def get_value(self):
        try:
            if isinstance(self.value, str):
                if self.value.startswith(self._function_escape):
                    # return FunctionType(self.value)
                    return None
                else:
                    return BaseType(self.value)
            elif isinstance(self.value, (int, float, bool, int)):
                return BaseType(self.value)
            elif isinstance(self.value, (list, tuple, set)):
                return ListType(self.value)
            else:
                raise Exception(f"Unknown variable type at {self.id}")
        except Exception as ex:
            raise Exception(f"Couldn't cast value of {self.name}. Unknown value type") from ex

    def is_empty(self):
        return self.value is None

    def display(self):
        return f"{self.name} = {self.value}"

    def compare_to(self, obj):
        if obj.frequency < self.frequency:
            return 1
        if obj.frequency > self.frequency:
            return -1
        return 0
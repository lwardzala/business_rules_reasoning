from ..value_types import BaseType

class GreaterOrEqual:
    def compare(self, left_term, right_term):
        if not isinstance(left_term, BaseType) or not isinstance(right_term, BaseType):
            return False

        return left_term >= right_term
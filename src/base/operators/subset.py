from ..value_types import BaseType, ListType

class Subset:
    def compare(self, left_term, right_term):
        if isinstance(right_term, ListType):
            return left_term in right_term
        elif isinstance(right_term, BaseType):
            return isinstance(left_term, BaseType) and right_term == left_term
        else:
            return False
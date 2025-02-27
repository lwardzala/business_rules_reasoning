from ..value_types import BaseType, ListType

class NotSubset:
    def compare(self, left_term, right_term):
        if isinstance(right_term, ListType):
            return not right_term.contains(left_term)
        elif isinstance(right_term, BaseType) and isinstance(left_term, BaseType):
            return not right_term == left_term
        elif isinstance(right_term, BaseType):
            return True
        else:
            return True
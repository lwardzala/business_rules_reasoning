from ..value_types import BaseType, ListType

class Between:
    def compare(self, left_term, right_term):
        if not isinstance(left_term, BaseType):
            raise Exception(f"Can't cast {type(left_term).__name__} to BaseType")
        if not isinstance(right_term, ListType):
            raise Exception(f"Can't cast {type(right_term).__name__} to ListType")
        
        return right_term.between(left_term)
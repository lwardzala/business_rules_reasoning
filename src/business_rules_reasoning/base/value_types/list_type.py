from .base_type import BaseType

class ListType:
    def __init__(self, lst):
        self.values = []
        try:
            for item in lst:
                self.values.append(BaseType(item))
        except Exception as ex:
            raise Exception("Couldn't convert object to a list") from ex

    def __eq__(self, other):
        if not isinstance(other, ListType):
            return False
        if len(self.values) != len(other.values):
            return False

        right_term_copy = other.values.copy()
        for value in self.values:
            if value in right_term_copy:
                right_term_copy.remove(value)
            else:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "{" + ";".join(str(value) for value in self.values) + "}"

    def __hash__(self):
        return hash(tuple(self.values))

    def between(self, left_term):
        if len(self.values) != 2:
            raise Exception("Invalid object. Proper range value has to be provided")
        if not isinstance(left_term, BaseType):
            return False

        if not left_term.is_number() or not self.values[0].is_number() or not self.values[1].is_number():
            return False

        return self.values[0] <= left_term <= self.values[1]

    def __contains__(self, other) -> bool:
        if isinstance(other, BaseType):
            return other in self.values
        elif isinstance(other, ListType):
            for item in other.values:
                if item in self.values:
                    continue
                else:
                    return False
            return True
        else:
            return False

    def get_value(self):
        return self.values
    
    def get_type(self):
        return "list"
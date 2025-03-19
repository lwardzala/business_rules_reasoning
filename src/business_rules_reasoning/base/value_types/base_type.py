class BaseType:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, BaseType):
            if self.is_number_or_boolean() and other.is_number_or_boolean():
                return float(self.value) == float(other.value)
            if self.is_string() and other.is_string():
                return str(self.value).lower() == str(other.value).lower()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, BaseType) and self.is_number() and other.is_number():
            return float(self.value) > float(other.value)
        return False

    def __lt__(self, other):
        if isinstance(other, BaseType) and self.is_number() and other.is_number():
            return float(self.value) < float(other.value)
        return False

    def __ge__(self, other):
        if isinstance(other, BaseType) and self.is_number() and other.is_number():
            return not self.__lt__(other)
        return False

    def __le__(self, other):
        if isinstance(other, BaseType) and self.is_number() and other.is_number():
            return not self.__gt__(other)
        return False

    def __contains__(self, left_term):
        if not isinstance(left_term, BaseType):
            return False

        if left_term.is_number_or_boolean():
            return self.__eq__(left_term)
        elif isinstance(self.value, str):
            return str(left_term.value).lower() in str(self.value).lower()

        return False
    
    def get_type(self):
        if self.is_boolean():
            return "boolean"
        if self.is_number():
            return "number"
        if self.is_string():
            return "string"
        return "unknown"

    def is_number(self):
        return isinstance(self.value, (int, float))

    def is_boolean(self):
        return isinstance(self.value, bool)

    def is_string(self):
        return isinstance(self.value, str)

    def is_number_or_boolean(self):
        return self.is_number() or self.is_boolean()

    def get_value(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.value)
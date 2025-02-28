class NotIn:
    def compare(self, left_term, right_term):
        return not right_term.contains(left_term)
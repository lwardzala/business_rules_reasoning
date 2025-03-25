from ..base.conclusion import Conclusion
from ..base.variable import Variable

class DeductiveConclusion(Conclusion):
    def __init__(self, variable: Variable):
        self.variable = variable

    def is_valid(self) -> bool:
        return not self.variable.is_empty()
    
    def validate(self):
        if not self.is_valid():
            raise Exception(f"Invalid conclusion {self.variable.display()}")

    def display(self) -> str:
        return self.variable.display()
    
    def get_value(self):
        return self.variable.value
    
    def get_id(self) -> str:
        return self.variable.id
    
    def get_variable(self):
        return self.variable
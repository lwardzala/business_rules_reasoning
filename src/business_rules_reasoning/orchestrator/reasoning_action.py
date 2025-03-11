from ..base import Variable
from enum import Enum
from typing import Callable

class ActionType(Enum):
    NO_ACTION = "NO_ACTION"
    INVOKE_FUNCTION = "INVOKE_FUNCTION"
    START_REASONING_PROCESS = "START_REASONING_PROCESS"

class ReasoningAction:
    def __init__(self, action_type: ActionType, action_id: str, action_name: str, action_description: str, conclusion: Variable):
        self.action_type = action_type
        self.action_id = action_id
        self.action_name = action_name
        self.action_description = action_description
        self.action_parameters = {}
        self.action_function: Callable = None
        self.conclusion = conclusion

    def add_action_parameter(self, parameter_name: str, parameter_value):
        self.action_parameters[parameter_name] = parameter_value

    def get_action_parameters(self):
        return self.action_parameters

    def get_action_type(self):
        return self.action_type

    def get_action_id(self):
        return self.action_id

    def get_action_name(self):
        return self.action_name

    def get_action_description(self):
        return self.action_description

    def set_action_function(self, func: Callable, parameters: dict):
        self.action_parameters = parameters
        self.action_function = func

    def link_reasoning_topic(self, knowledge_base_id: str):
        self.knowledge_base_id = knowledge_base_id

    def __call_action(self, **kwargs):
        if self.action_function:
            all_parameters = {**self.action_parameters, **kwargs}
            return self.action_function(**all_parameters)
        else:
            raise Exception("Action function is not set")

    def invoke_action(self, **kwargs):
        if self.action_type == ActionType.NO_ACTION:
            return None
        elif self.action_type == ActionType.INVOKE_FUNCTION:
            return self.__call_action(**kwargs)
        elif self.action_type == ActionType.START_REASONING_PROCESS:
            return self.knowledge_base_id

    def __str__(self):
        return f"Action ID: {self.action_id}, Action Name: {self.action_name}, Action Description: {self.action_description}, Action Type: {self.action_type}"
from typing import List
from ..base.reasoning_service import ReasoningService
from ..base.reasoning_process import ReasoningProcess
from ..base.reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod
from ..base import Rule, Variable
from .deductive_predicate import DeductivePredicate

class DeductiveReasoningService(ReasoningService):
    @staticmethod
    def start_reasoning(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        reasoning_process.knowledge_base.validate()
        result = DeductiveReasoningService.clear_reasoning(reasoning_process)
        result.state = ReasoningState.STARTED
        return DeductiveReasoningService.continue_reasoning(result)

    @staticmethod
    def continue_reasoning(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        reasoning_process.knowledge_base.validate()

        if reasoning_process.reasoning_method == ReasoningMethod.DEDUCTION:
            return DeductiveReasoningService.deduction(reasoning_process)
        elif reasoning_process.reasoning_method == ReasoningMethod.HYPOTHESIS_TESTING:
            return DeductiveReasoningService.hypothesis_testing(reasoning_process)
        else:
            return None

    @staticmethod
    def set_values(reasoning_process: ReasoningProcess, variables) -> ReasoningProcess:
        for rule in reasoning_process.knowledge_base.rule_set:
            rule.set_variables(variables)
        return reasoning_process

    @staticmethod
    def reset_reasoning(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        reasoning_process.state = ReasoningState.INITIALIZED
        reasoning_process.reasoned_items = []
        reasoning_process.evaluation_message = EvaluationMessage.NONE
        for rule in reasoning_process.knowledge_base.rule_set:
            rule.reset_evaluation()
        return reasoning_process

    @staticmethod
    def clear_reasoning(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        result = DeductiveReasoningService.reset_reasoning(reasoning_process)
        variables = DeductiveReasoningService.analyze_variables_frequency(reasoning_process)
        for rule in reasoning_process.knowledge_base.rule_set:
            for predicate in rule.predicates:
                if isinstance(predicate, DeductivePredicate):
                    predicate.left_term.frequency = next(variable.frequency for variable in variables if variable.id == predicate.left_term.id)
                    predicate.left_term.value = None
        return result

    @staticmethod
    def get_all_missing_variable_ids(reasoning_process: ReasoningProcess) -> List[str]:
        return [variable.id for variable in DeductiveReasoningService.get_all_missing_variables(reasoning_process)]

    @staticmethod
    def get_all_missing_variables(reasoning_process: ReasoningProcess) -> List[Variable]:
        result = []
        for rule in reasoning_process.knowledge_base.rule_set:
            for predicate in rule.predicates:
                if isinstance(predicate, DeductivePredicate) and predicate.left_term.is_empty() and all(variable.id != predicate.left_term.id for variable in result):
                    result.append(predicate.right_term)
        result.sort(key=lambda var: var.frequency, reverse=True)
        return result

    @staticmethod
    def analyze_variables_frequency(reasoning_process: ReasoningProcess) -> List[Variable]:
        result = []
        for rule in reasoning_process.knowledge_base.rule_set:
            for predicate in rule.predicates:
                if isinstance(predicate, DeductivePredicate) and predicate.left_term not in result:
                    predicate.left_term.frequency = 0
                    result.append(predicate.left_term)
                index = next((i for i, item in enumerate(result) if item.id == predicate.left_term.id), -1)
                if index != -1:
                    result[index].frequency += 1
        return result

    @staticmethod
    def deduction(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        try:
            for rule in reasoning_process.knowledge_base.rule_set:
                if not rule.evaluated:
                    rule.evaluate()
                if rule.evaluated and rule.result:
                    if rule.conclusion.right_term not in reasoning_process.reasoned_items:
                        reasoning_process.reasoned_items.append(rule.conclusion.right_term)
        except Exception as e:
            reasoning_process.evaluation_message = EvaluationMessage.ERROR
            reasoning_process.state = ReasoningState.FINISHED
            reasoning_process.reasoning_error_message = str(e)
            return reasoning_process

        finished = all(rule.evaluated for rule in reasoning_process.knowledge_base.rule_set)
        reasoning_process.state = ReasoningState.FINISHED if finished else ReasoningState.STOPPED
        if finished:
            reasoning_process.evaluation_message = EvaluationMessage.PASSED if reasoning_process.reasoned_items else EvaluationMessage.FAILED
        else:
            reasoning_process.evaluation_message = EvaluationMessage.MISSING_VALUES
        return reasoning_process

    @staticmethod
    def hypothesis_testing(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        if not reasoning_process.options or "hypothesis" not in reasoning_process.options or not isinstance(reasoning_process.options["hypothesis"], Variable):
            raise Exception("[Reasoning Engine]: Hypothesis not provided in reasoning process options.")
        
        hypothesis = reasoning_process.options["hypothesis"]
        rules = [rule for rule in reasoning_process.knowledge_base.rule_set if rule.conclusion.right_term.id == hypothesis.id and rule.conclusion.right_term.value == hypothesis.value]
        try:
            for rule in rules:
                if not rule.evaluated:
                    rule.evaluate()
                if rule.evaluated and rule.result and rule.conclusion.right_term.id == hypothesis.id and rule.conclusion.right_term.value == hypothesis.value:
                    reasoning_process.reasoned_items = [hypothesis]
        except Exception as e:
            reasoning_process.evaluation_message = EvaluationMessage.ERROR
            reasoning_process.state = ReasoningState.FINISHED
            reasoning_process.reasoning_error_message = str(e)
            return reasoning_process

        finished = (all(rule.evaluated for rule in rules) or any(rule.evaluated and rule.result for rule in rules))
        reasoning_process.state = ReasoningState.FINISHED if finished else ReasoningState.STOPPED
        if finished:
            reasoning_process.evaluation_message = EvaluationMessage.PASSED if reasoning_process.reasoned_items else EvaluationMessage.FAILED
        else:
            reasoning_process.evaluation_message = EvaluationMessage.MISSING_VALUES
        return reasoning_process

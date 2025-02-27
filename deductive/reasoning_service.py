from ..base.reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod
from ..base import ReasoningProcess, Rule
from .deductive_predicate import DeductivePremise

class ReasoningService:
    @staticmethod
    def start_reasoning(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        result = ReasoningService.clear_reasoning(reasoning_process)
        result.state = ReasoningState.STARTED
        return ReasoningService.continue_reasoning(result)

    @staticmethod
    def continue_reasoning(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        if reasoning_process.reasoning_method == ReasoningMethod.DEDUCTION:
            return ReasoningService.deduction(reasoning_process)
        elif reasoning_process.reasoning_method == ReasoningMethod.HYPOTHESIS_TESTING:
            return ReasoningService.hypothesis_testing(reasoning_process)
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
        result = ReasoningService.reset_reasoning(reasoning_process)
        variables = ReasoningService.analyze_variables_frequency(reasoning_process)
        for rule in reasoning_process.knowledge_base.rule_set:
            for predicate in rule.predicates:
                if isinstance(predicate, DeductivePremise):
                    predicate.left_term.frequency = next(variable.frequency for variable in variables if variable.id == predicate.left_term.id)
                    predicate.left_term.value = None
        return result

    @staticmethod
    def get_all_missing_variable_ids(reasoning_process: ReasoningProcess) -> list:
        return [variable.id for variable in ReasoningService.get_all_missing_variables(reasoning_process)]

    @staticmethod
    def get_all_missing_variables(reasoning_process: ReasoningProcess) -> list:
        result = []
        for rule in reasoning_process.knowledge_base.rule_set:
            for predicate in rule.predicates:
                if isinstance(predicate, DeductivePremise) and predicate.left_term.is_empty() and all(variable.id != predicate.left_term.id for variable in result):
                    result.append(predicate.left_term)
        result.sort()
        return result

    @staticmethod
    def analyze_variables_frequency(reasoning_process: ReasoningProcess) -> list:
        result = []
        for rule in reasoning_process.knowledge_base.rule_set:
            for predicate in rule.predicates:
                if isinstance(predicate, DeductivePremise) and predicate.left_term not in result:
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
                    reasoning_process.reasoned_items.append(rule.conclusion.right_term)
        except Exception:
            reasoning_process.evaluation_message = EvaluationMessage.ERROR
            reasoning_process.state = ReasoningState.FINISHED
            return reasoning_process

        finished = all(rule.evaluated for rule in reasoning_process.knowledge_base.rule_set)
        reasoning_process.state = ReasoningState.FINISHED if finished else ReasoningState.STOPPED
        reasoning_process.evaluation_message = EvaluationMessage.PASSED if reasoning_process.reasoned_items else (EvaluationMessage.FAILED if finished else EvaluationMessage.MISSING_VALUES)
        return reasoning_process

    @staticmethod
    def hypothesis_testing(reasoning_process: ReasoningProcess) -> ReasoningProcess:
        rules = [rule for rule in reasoning_process.knowledge_base.rule_set if rule.conclusion.right_term.id == reasoning_process.options.hypothesis.id and rule.conclusion.right_term.value == reasoning_process.options.hypothesis.value]
        for rule in rules:
            if not rule.evaluated:
                rule.evaluate()
            if rule.evaluated and rule.result and rule.conclusion.right_term.id == reasoning_process.options.hypothesis.id and rule.conclusion.right_term.value == reasoning_process.options.hypothesis.value:
                reasoning_process.reasoned_items = [reasoning_process.options.hypothesis]

        finished = all(rule.evaluated for rule in rules)
        reasoning_process.state = ReasoningState.FINISHED if finished else ReasoningState.STOPPED
        reasoning_process.evaluation_message = EvaluationMessage.PASSED if reasoning_process.reasoned_items else (EvaluationMessage.FAILED if finished else EvaluationMessage.MISSING_VALUES)
        return reasoning_process
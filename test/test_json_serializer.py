import unittest
from src.business_rules_reasoning.json_serializer import serialize_reasoning_process, serialize_knowledge_base
from src.business_rules_reasoning.base import ReasoningProcess, KnowledgeBase, Rule, Variable, OperatorType
from src.business_rules_reasoning.deductive import DeductivePredicate
from src.business_rules_reasoning.base.reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod, ReasoningType

class TestJsonSerializer(unittest.TestCase):
    def test_serialize_reasoning_process(self):
        # Create variables
        age_variable = Variable(id="1", name="Age", value=25)

        # Create predicates
        adult_predicate = DeductivePredicate(left_term=age_variable, right_term=Variable(value=20), operator=OperatorType.GREATER_OR_EQUAL)

        # Create rules
        adult_rule = Rule(conclusion=adult_predicate, predicates=[adult_predicate])

        # Create knowledge base
        knowledge_base = KnowledgeBase(id="age_classification", name="Age Classification", description="Classify age into categories", reasoning_type=ReasoningType.CRISP)
        knowledge_base.rule_set.append(adult_rule)

        # Create reasoning process
        reasoning_process = ReasoningProcess(reasoning_method=ReasoningMethod.DEDUCTION, knowledge_base=knowledge_base)
        reasoning_process.state = ReasoningState.INITIALIZED
        reasoning_process.reasoned_items = []
        reasoning_process.evaluation_message = EvaluationMessage.NONE

        # Serialize reasoning process
        serialized = serialize_reasoning_process(reasoning_process)
        self.assertIn('"reasoning_method": "DEDUCTION"', serialized)
        self.assertIn('"knowledge_base": {', serialized)
        self.assertIn('"state": "INITIALIZED"', serialized)
        self.assertIn('"evaluation_message": "NONE"', serialized)

    def test_serialize_knowledge_base(self):
        # Create variables
        age_variable = Variable(id="1", name="Age", value=25)

        # Create predicates
        adult_predicate = DeductivePredicate(left_term=age_variable, right_term=Variable(value=20), operator=OperatorType.GREATER_OR_EQUAL)

        # Create rules
        adult_rule = Rule(conclusion=adult_predicate, predicates=[adult_predicate])

        # Create knowledge base
        knowledge_base = KnowledgeBase(id="age_classification", name="Age Classification", description="Classify age into categories", reasoning_type=ReasoningType.CRISP)
        knowledge_base.rule_set.append(adult_rule)

        # Serialize knowledge base
        serialized = serialize_knowledge_base(knowledge_base)
        self.assertIn('"id": "age_classification"', serialized)
        self.assertIn('"name": "Age Classification"', serialized)
        self.assertIn('"description": "Classify age into categories"', serialized)
        self.assertIn('"rule_set": [', serialized)

if __name__ == '__main__':
    unittest.main()

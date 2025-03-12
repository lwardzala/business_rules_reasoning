import unittest
from src.business_rules_reasoning.json_deserializer import deserialize_reasoning_process, deserialize_knowledge_base
from src.business_rules_reasoning.base import ReasoningProcess, KnowledgeBase, Rule, Variable, OperatorType
from src.business_rules_reasoning.deductive import DeductivePredicate
from src.business_rules_reasoning.base.reasoning_enums import ReasoningState, EvaluationMessage, ReasoningMethod, ReasoningType
from src.business_rules_reasoning.json_serializer import serialize_reasoning_process, serialize_knowledge_base

class TestJsonDeserializer(unittest.TestCase):
    def test_deserialize_reasoning_process(self):
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

        # Serialize and deserialize reasoning process
        serialized = serialize_reasoning_process(reasoning_process)
        deserialized = deserialize_reasoning_process(serialized)

        self.assertEqual(deserialized.reasoning_method, ReasoningMethod.DEDUCTION)
        self.assertEqual(deserialized.state, ReasoningState.INITIALIZED)
        self.assertEqual(deserialized.evaluation_message, EvaluationMessage.NONE)
        self.assertEqual(deserialized.knowledge_base.id, "age_classification")
        self.assertEqual(deserialized.knowledge_base.name, "Age Classification")
        self.assertEqual(deserialized.knowledge_base.description, "Classify age into categories")

    def test_deserialize_knowledge_base(self):
        # Create variables
        age_variable = Variable(id="1", name="Age", value=25)

        # Create predicates
        adult_predicate = DeductivePredicate(left_term=age_variable, right_term=Variable(value=20), operator=OperatorType.GREATER_OR_EQUAL)

        # Create rules
        adult_rule = Rule(conclusion=adult_predicate, predicates=[adult_predicate])

        # Create knowledge base
        knowledge_base = KnowledgeBase(id="age_classification", name="Age Classification", description="Classify age into categories", reasoning_type=ReasoningType.CRISP)
        knowledge_base.rule_set.append(adult_rule)

        # Serialize and deserialize knowledge base
        serialized = serialize_knowledge_base(knowledge_base)
        deserialized = deserialize_knowledge_base(serialized)

        self.assertEqual(deserialized.id, "age_classification")
        self.assertEqual(deserialized.name, "Age Classification")
        self.assertEqual(deserialized.description, "Classify age into categories")
        self.assertEqual(len(deserialized.rule_set), 1)
        self.assertEqual(deserialized.rule_set[0].conclusion.left_term.name, "Age")
        self.assertEqual(deserialized.rule_set[0].conclusion.operator, OperatorType.GREATER_OR_EQUAL)

if __name__ == '__main__':
    unittest.main()

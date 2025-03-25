from src.business_rules_reasoning.deductive import KnowledgeBaseBuilder, RuleBuilder, PredicateBuilder, VariableBuilder
from src.business_rules_reasoning import OperatorType

# Create predicates
toddler_predicate = PredicateBuilder().configure_predicate("age", OperatorType.LESS_OR_EQUAL, 3).unwrap()
child_predicate = PredicateBuilder().configure_predicate("age", OperatorType.BETWEEN, [4, 12]).unwrap()
teenager_predicate = PredicateBuilder().configure_predicate("age", OperatorType.BETWEEN, [13, 19]).unwrap()
adult_predicate = PredicateBuilder().configure_predicate("age", OperatorType.GREATER_OR_EQUAL, 20).unwrap()

# Create rules
toddler_rule = RuleBuilder().set_conclusion(VariableBuilder().set_id("age").set_name("Age").set_value("toddler").unwrap()).add_predicate(toddler_predicate).unwrap()
child_rule = RuleBuilder().set_conclusion(VariableBuilder().set_id("age").set_name("Age").set_value("child").unwrap()).add_predicate(child_predicate).unwrap()
teenager_rule = RuleBuilder().set_conclusion(VariableBuilder().set_id("age").set_name("Age").set_value("teenager").unwrap()).add_predicate(teenager_predicate).unwrap()
adult_rule = RuleBuilder().set_conclusion(VariableBuilder().set_id("age").set_name("Age").set_value("adult").unwrap()).add_predicate(adult_predicate).unwrap()

# Build knowledge base
knowledge_base = KnowledgeBaseBuilder() \
    .set_id("age_classification") \
    .set_name("Age Classification") \
    .set_description("Classify age into toddler, child, teenager, and adult") \
    .add_rule(toddler_rule) \
    .add_rule(child_rule) \
    .add_rule(teenager_rule) \
    .add_rule(adult_rule) \
    .unwrap()

# Print knowledge base details
print(f"Knowledge Base ID: {knowledge_base.id}")
print(f"Knowledge Base Name: {knowledge_base.name}")
print(f"Knowledge Base Description: {knowledge_base.description}")
print("Rules:")
for rule in knowledge_base.rule_set:
    print(f"  Rule Conclusion: {rule.conclusion.left_term.name} {rule.conclusion.operator} {rule.conclusion.right_term.value}")
    for predicate in rule.predicates:
        print(f"    Predicate: {predicate.left_term.name} {predicate.operator} {predicate.right_term.value}")

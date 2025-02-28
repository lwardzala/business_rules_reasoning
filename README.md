# Business Rules Reasoning System

It is the Python implementation of the [Business Rules Reasoning System](https://github.com/lwardzala/Business-Rules-Reasoning-System).
It is a simple reasoning tool based on the implication form of the Horn clause.
Provides integration between various systems and supports workflows.

Automate decision processes with the Business Rules Reasoning System!

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](License)

## Features
- Reasoning can be stopped at any time and resumed after collecting more facts;
- Two reasoning methods: Deduction and Hypothesis Testing;
- No need to fill all facts (variables) to finish reasoning. Reasoning finishes when entropy is zero;
- ReasoningResolver tries to obtain facts (variables) automatically by requesting defined APIs;
- ReasoningResolver executes requests to other APIs depending on the reasoning result (support for workflows);

If you are still considering how you would utilize a reasoning system, take a look at the [Use cases](#use-cases) part.

## Table of content

- [Business Rules Reasoning System](#business-rules-reasoning-system)
  - [Features](#features)
  - [Table of content](#table-of-content)
  - [Reasoning.Core](#reasoningcore)
    - [Installation](#installation)
    - [Predicates](#predicates)
    - [Rules](#rules)
    - [Knowledge Base](#knowledge-base)
    - [Variables and supported values](#variables-and-supported-values)
    - [Supported operators](#supported-operators)
    - [Reasoning Process](#reasoning-process)
    - [Reasoning Method](#reasoning-method)
    - [Reasoning Service](#reasoning-service)
  - [Use cases](#use-cases)
  - [Future functionalities](#future-functionalities)
    - [Coming soon](#coming-soon)
    - [Long term plans](#long-term-plans)
  - [Authors](#authors)
  - [References](#references)

## Reasoning.Core

Reasoning.Core library is the engine of the Reasoning System. It's used inside of Reasoning.Host and can be used in an external project as a bridge between your app and the Host or can be used independently to optimize your app.

### Installation

```bash
pip install business_rules_reasoning
```

### Predicates

Predicate is the smallest structure and represents an equation.
They are built from: LeftTerm, Operator, and RightTerm.

So representation of an equation:
```
age >= 18
```

Will be:
```json
{
  "leftTerm": {
    "id": "age",
    "name": "Age",
    "value": null
  },
  "operator": "GreaterOrEqual",
  "rightTerm": {
    "id": "age",
    "name": "Age",
    "value": 18
  }
}
```

With PredicateBuilder:
```python
from business_rules_reasoning.deductive import PredicateBuilder
from business_rules_reasoning import OperatorType

predicate = PredicateBuilder() \
    .configure_predicate("age", OperatorType.GREATER_OR_EQUAL, 18) \
    .set_left_term_value(23)  # optional for left term
    .unwrap()
```

### Rules

Rule is the middle structure in Knowledge Base. Each rule has a set of predicates and a conclusion.
A rule is being evaluated during the reasoning process by evaluating its predicates. If any predicate's evaluation result is false, then the rule's evaluation result is false.

So representation of rule:
```
age >= 18 -> passenger = 'adult'
```

Will be:
```json
{
  "predicates": [
    {
      "leftTerm": {
        "id": "age",
        "name": "Age",
        "value": null
      },
      "operator": "GreaterOrEqual",
      "rightTerm": {
        "id": "age",
        "name": "Age",
        "value": 18
      }
    }
  ],
  "conclusion": {
    "id": "passenger",
    "name": "Passenger type",
    "value": "adult"
  }
}
```

With RuleBuilder:
```python
from business_rules_reasoning.deductive import RuleBuilder, VariableBuilder, PredicateBuilder
from business_rules_reasoning import OperatorType

rule = RuleBuilder() \
    .set_conclusion(VariableBuilder()
        .set_id("passenger")
        .set_name("Passenger type")
        .set_value("adult")  # required for conclusion
        .unwrap()) \
    .add_predicate(PredicateBuilder()
        .configure_predicate("age", OperatorType.GREATER_OR_EQUAL, 18)
        .set_left_term_value(23)  # optional for left term
        .unwrap()) \
    .unwrap()
```

### Knowledge Base

Knowledge base is the biggest unit and it's a representation of a use case. Contains Id, Name, Description, and Rule Set.
The base can be modified or involved at any time by an 'expert' to improve the business process.

Sample of knowledge base rule set:
```
age >= 18 -> passenger = "adult"
age < 18 & age >= 5 -> passenger = "child"
age < 5 -> passenger = "toddler"
```

<details><summary>Json representation</summary>
<p>

```json
[
  {
    "predicates": [
      {
        "leftTerm": {
          "id": "age"
        },
        "operator": "GreaterOrEqual",
        "rightTerm": {
          "id": "age",
          "value": 18
        }
      }
    ],
    "conclusion": {
      "id": "passenger",
      "value": "adult"
    }
  },
  {
    "predicates": [
      {
        "leftTerm": {
          "id": "age"
        },
        "operator": "LessThan",
        "rightTerm": {
          "id": "age",
          "value": 18
        }
      },
      {
        "leftTerm": {
          "id": "age"
        },
        "operator": "GreaterOrEqual",
        "rightTerm": {
          "id": "age",
          "value": 5
        }
      }
    ],
    "conclusion": {
      "id": "passenger",
      "value": "child"
    }
  },
  {
    "predicates": [
      {
        "leftTerm": {
          "id": "age"
        },
        "operator": "LessThan",
        "rightTerm": {
          "id": "age",
          "value": 5
        }
      }
    ],
    "conclusion": {
      "id": "passenger",
      "value": "toddler"
    }
  }
]
```

</p>
</details>

With KnowledgeBaseBuilder:
```python
from business_rules_reasoning.deductive import KnowledgeBaseBuilder, RuleBuilder, VariableBuilder, PredicateBuilder
from business_rules_reasoning import OperatorType

knowledge_base = KnowledgeBaseBuilder() \
    .set_id("knowledgeBase1") \
    .set_name("Knowledge Base 1") \
    .set_description("Passengers type principles") \
    .add_rule(RuleBuilder()
        .set_conclusion(VariableBuilder()
            .set_id("passenger")
            .set_value("adult")
            .unwrap())
        .add_predicate(PredicateBuilder()
            .configure_predicate("age", OperatorType.GREATER_OR_EQUAL, 18)
            .unwrap())
        .unwrap()) \
    .add_rule(RuleBuilder()
        .set_conclusion(VariableBuilder()
            .set_id("passenger")
            .set_value("child")
            .unwrap())
        .add_predicate(PredicateBuilder()
            .configure_predicate("age", OperatorType.LESS_THAN, 18)
            .unwrap())
        .add_predicate(PredicateBuilder()
            .configure_predicate("age", OperatorType.GREATER_OR_EQUAL, 5)
            .unwrap())
        .unwrap()) \
    .add_rule(RuleBuilder()
        .set_conclusion(VariableBuilder()
            .set_id("passenger")
            .set_value("toddler")
            .unwrap())
        .add_predicate(PredicateBuilder()
            .configure_predicate("age", OperatorType.LESS_THAN, 5)
            .unwrap())
        .unwrap()) \
    .unwrap()
```

### Variables and supported values

Variables are the smallest units. Both Terms and Conclusions are instances of a Variable type.

Each Variable has a value. The value is not strongly typed and can be a:

- string;
- number;
- boolean;
- array.

Value types are comparable with each other.

### Supported operators

<u>Available operators:</u>

- Equal;
- NotEqual;
- GreaterThan;
- LessThan;
- GreaterOrEqual;
- LessOrEqual;
- IsIn (inversion of Contains);
- NotIn (negation of IsIn);
- Between (ex. "4 Between [3, 5]" is true);
- NotBetween (negation of Between);
- Subset (Cross type, ex. "4 subset [3, 4, 7]" is true, "[3, 4] subset [3, 4, 7]" is true);
- NotSubset (inversion of Subset).

### Reasoning Process

Reasoning process is a state of reasoning. It contains all necessary data for reasoning like: Reasoning Method, Knowledge Base, State, Reasoned Items, Evaluation Message, and Hypothesis.

<u>Possible State:</u>

- INITIALIZED;
- STARTED;
- STOPPED;
- FINISHED.

<u>Possible Evaluation Message:</u>

- NONE - initialized or started;
- PASSED - at least one rule is true or hypothesis is confirmed;
- FAILED - all rules are false or hypothesis is not confirmed;
- ERROR - an error occurred while reasoning;
- MISSING_VALUES - there are not enough facts to finish reasoning.

When a rule or hypothesis is true, its conclusion is being added to the Reasoned Items parameter.

### Reasoning Method

<u>There are two reasoning modes:</u>

- Deduction - tries to reason as many conclusions as possible;
- HypothesisTesting - checks if any rule can confirm the hypothesis (any rule that is true and its conclusion is the same as the hypothesis).

### Reasoning Service

A service that contains all procedures for reasoning:

- StartReasoning - starts reasoning with resetting all evaluation states and left term values;
- ContinueReasoning - continues reasoning with the current state (without reset);
- SetValues - tries to set appropriate variables to every rule;
- ResetReasoning - resets reasoning evaluation but preserves left term values;
- ClearReasoning - resets reasoning evaluation and variables;
- GetAllMissingVariableIds - tries to get all missing variable ids in the reasoning process.

## Use cases

The Reasoning System can be used whenever you want to automate a decision process:

1. You have a production hall and want to automate production process. You can connect the Host application with production machine's API to avoid any to be idle;

2. You have a complex screening process when customer requests for a loan. There is a need to collect data from various anti-fraud databases and decide whether grant a loan or not;

3. You have a process with several workflows to be executed. The next workflow depends on result of the previous one;

4. You are a software developer and want to improve code of a service that contains multi-level "if" clauses. 

## Authors
- Lukasz Wardzala - [github](https://github.com/lwardzala)

## References
- [Horn clause wiki](https://en.wikipedia.org/wiki/Horn_clause)
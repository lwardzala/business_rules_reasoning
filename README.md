# Business Rules Reasoning System

[![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/lwardzala)

## Introduction

This is a Python implementation of my previous project [Business Rules Reasoning System](https://github.com/lwardzala/Business-Rules-Reasoning-System), enhanced with a reasoning orchestrator that leverages Large Language Models (LLMs) to enable a fully transparent and explainable logical reasoning system for business automation. 

The system is built on the implicational form of Horn clauses, providing a robust logical reasoning framework. It supports seamless integration with various systems, enabling complex workflows and decision-making processes. The addition of LLMs allows for natural language interaction, making it easier to query, trace, and understand the reasoning process.

Turning even small models, such as those with just 3 billion parameters, into a fully logical reasoning system offers the advantage of efficiency and accessibility. Smaller models require significantly less computational power and memory, making them more cost-effective to deploy and run. This enables broader accessibility for businesses and developers, allowing them to integrate advanced reasoning capabilities into their systems without the need for expensive hardware or cloud resources. Additionally, smaller models can achieve faster inference times, which is critical for real-time decision-making in business automation.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](License)

<p align="center">
  <img src="images/dependency_overview.png" alt="Solution" width="600"/>
</p>

### Problem and Solution

The **Business Rules Reasoning System** addresses the challenge of integrating logical reasoning capabilities into Large Language Models (LLMs). While LLMs are powerful tools for natural language understanding and generation, they lack inherent logical reasoning capabilities and often struggle with tasks requiring strict adherence to predefined rules or knowledge bases. This system bridges that gap by combining the structured reasoning of rule-based systems with the flexibility of LLMs. It enables transparent and explainable decision-making processes, making it suitable for business automation and other domains requiring logical consistency.

### Remaining Challenges

One of the key challenges that remains is the potential for **hallucination** in the fact retrieval process. LLMs, when tasked with retrieving facts or generating responses, may produce outputs that are not grounded in the provided knowledge base or context. This can lead to inaccuracies in the reasoning process.

### Mitigating the Risk

Despite this challenge, the system significantly **offloads the risk of hallucination** by anchoring the reasoning process in a structured knowledge base and predefined rules. The LLM is primarily used for interfacing with the user and retrieving facts, while the logical reasoning and decision-making are handled by the rule-based engine. This separation of responsibilities ensures that the core reasoning remains reliable and explainable, even if the LLM introduces some noise in the fact retrieval process.

## Features
- **Interruptible Reasoning**: Reasoning can be stopped at any time and resumed after collecting more facts.
- **Two Reasoning Methods**: Supports both Deduction and Hypothesis Testing for flexible reasoning workflows.
- **Partial Fact Completion**: No need to fill all facts (variables) to finish reasoning. Reasoning concludes when entropy reaches zero or sufficient conclusions are derived.
- **Fact Retrieval Automation**: The orchestrator automatically retrieves facts (variables) from documents or leads a chat conversation to gather missing information.
- **Workflow Integration**: The orchestrator executes functions or triggers actions based on reasoning results, enabling seamless workflow automation.
- **Explainable Reasoning**: Provides detailed logs and explanations for each reasoning step, ensuring transparency and traceability.
- **Knowledge Base Flexibility**: Allows the creation of custom knowledge bases with rules, predicates, and variables tailored to specific domains.
- **LLM Integration**: Leverages Large Language Models (LLMs) for natural language interaction and fact extraction, enhancing usability and accessibility.
- **Error Handling**: Handles incomplete or conflicting data gracefully, ensuring robust reasoning processes.
- **Customizable Options**: Offers configurable options for variable fetching modes, reasoning methods, and workflow behaviors.
- **State Serialization**: The state of the reasoning process is fully serializable to JSON, enabling easy storage, retrieval, and debugging.
- **Multiple knowledge representations**: This library allows to declare the knowledge base using: RuleSet builder, Decision tables defined in Pandas, Decision trees.
- **Knowledge representation converters**: It is possible to use converters to switch between Decision tables, Decision trees and Rules.

# Documentation
## Table of content

- [Business Rules Reasoning System](#business-rules-reasoning-system)
  - [Introduction](#introduction)
    - [Problem and Solution](#problem-and-solution)
    - [Remaining Challenges](#remaining-challenges)
    - [Mitigating the Risk](#mitigating-the-risk)
    - [Features](#features)
- [Documentation](#documentation)
  - [Table of content](#table-of-content)
  - [Reasoning library](#Reasoning-library)
    - [Installation](#installation)
    - [Predicates](#predicates)
    - [Rules](#rules)
    - [Knowledge Base](#knowledge-base)
    - [Variables and supported values](#variables-and-supported-values)
    - [Supported operators](#supported-operators)
    - [Reasoning Process](#reasoning-process)
    - [Reasoning Method](#reasoning-method)
    - [Reasoning Service](#reasoning-service)
  - [Supported knowledge base representations](#supported-knowledge-base-representations)
    - [Business rules](#business-rules)
    - [Decision tables](#decision-tables)
    - [Decision trees](#decision-trees)
  - [LLM Orchestrator](#llm-orchestrator)
    - [LLMOrchestrator](#llmorchestrator)
    - [LLMPipelineBase and HuggingFacePipeline](#llmpipelinebase-and-huggingfacepipeline)
    - [Knowledge Base Retriever](#knowledge-base-retriever)
    - [Orchestrator Options](#orchestrator-options)
  - [Example case-study](#example-case-study)
    - [Building business rules](#building-business-rules)
    - [Displaying business rules](#displaying-business-rules)
    - [Preparing a document example](#preparing-a-document-example)
    - [Initialising the HuggingFace orchestrator](#initialising-the-huggingface-orchestrator)
    - [Querying the orchestrator and tracing the inference log](#querying-the-orchestrator-and-tracing-the-inference-log)
  - [Model evaluation](#model-evaluation)
  - [Authors](#authors)
  - [References](#references)

## Reasoning library

https://pypi.org/project/business-rules-reasoning/

The business-rules-reasoning library contains the engine of the Reasoning System and the LLM orchestrator.

### Installation

```bash
pip install business-rules-reasoning
```

### Predicates

A **Predicate** is the smallest logical structure in the reasoning system and represents an equation or condition that can be evaluated as true or false. Predicates are the building blocks of rules and are used to define the conditions under which a conclusion can be reached.

They are composed of three main components:
- **LeftTerm**: The variable or value being evaluated.
- **Operator**: The comparison or logical operator (e.g., `=`, `>`, `<`, `BETWEEN`) that defines the relationship between the terms.
- **RightTerm**: The variable or value against which the LeftTerm is compared.

Predicates are evaluated during the reasoning process, and their results determine whether the associated rule's conclusion can be applied. For example, a predicate might check if a patient's fever is greater than 38°C or if a loan applicant's salary is less than a specified threshold.

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

It can also be represented as a decision table using Pandas. Each row is a rule, and each column is a variable or conclusion.

**Example:**
```python
import pandas as pd
from business_rules_reasoning.deductive.decision_table import pandas_to_rules

data = {
    "age": [">=18", "<18"],
    "passenger": ["adult", "child"]
}
df = pd.DataFrame(data)
rules = pandas_to_rules(df, conclusion_index=-1)
```

### Rules

A **Rule** is the middle structure in the Knowledge Base, serving as the logical connection between predicates and conclusions. Each rule consists of:
- **Predicates**: A set of conditions that must be evaluated to determine the rule's outcome.
- **Conclusion**: The logical result or action that follows if all predicates are satisfied.

During the reasoning process, a rule is evaluated by sequentially evaluating its predicates:
- If any predicate's evaluation result is `false`, the rule's evaluation result is immediately set to `false`.
- If all predicates are evaluated as `true`, the rule's conclusion is considered valid, and the rule's evaluation result is `true`.

Rules are essential for defining the logical relationships within the Knowledge Base. They allow for complex decision-making by combining multiple conditions into a single logical structure. For example, a rule might state: "If a patient has a fever greater than 38°C and a headache, then prescribe paracetamol." This ensures that conclusions are only reached when all necessary conditions are met.

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

The **Knowledge Base** is the largest and most comprehensive unit in the reasoning system, representing a specific use case or domain of knowledge. It serves as the foundation for logical reasoning and decision-making processes. A Knowledge Base contains the following key components:
- **Id**: A unique identifier for the knowledge base.
- **Name**: A descriptive name that reflects the purpose or domain of the knowledge base.
- **Description**: A detailed explanation of the use case or business process the knowledge base addresses.
- **Rule Set**: A collection of rules, each consisting of predicates and conclusions, that define the logical relationships and decision-making criteria.

The Knowledge Base is designed to be flexible and dynamic. It can be modified or expanded at any time by an "expert" to adapt to changing requirements or improve the business process. This ensures that the system remains relevant and effective as the underlying use case evolves.

For example, in a medical domain, a Knowledge Base might include rules for diagnosing diseases based on symptoms and test results. In a financial domain, it could contain rules for approving loans based on credit scores and income levels. The modular structure of the Knowledge Base allows it to be tailored to virtually any domain or application.

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

Alternatively, it is possible to build the same knowledge base using a decision table and convert it to rules:

```python
import pandas as pd
from business_rules_reasoning.deductive.decision_table import pandas_to_rules
from business_rules_reasoning.deductive import KnowledgeBaseBuilder

# Define the decision table as a DataFrame
data = {
    "age": [">=18", "<18", "<5"],
    "passenger": ["adult", "child", "toddler"]
}
df = pd.DataFrame(data)

# Convert the decision table to rules
rules = pandas_to_rules(df, conclusion_index=-1)

# Build the knowledge base from the rules
knowledge_base = KnowledgeBaseBuilder() \
    .set_id("knowledgeBase1") \
    .set_name("Knowledge Base 1") \
    .set_description("Passengers type principles") \
    .add_rules(rules) \
    .unwrap()
```

This approach allows to define rules in a tabular format and easily convert them into a knowledge base for reasoning.

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

- Deduction - forward reasoning, tries to reason as many conclusions as possible;
- HypothesisTesting - backward reasoning, checks if any rule can confirm the hypothesis (any rule that is true and its conclusion is the same as the hypothesis).

### Reasoning Service

A service that contains all procedures for reasoning:

- **start_reasoning**: Initializes the reasoning process by resetting all evaluation states and clearing left term values. It validates the knowledge base and begins the reasoning process from the initial state.
- **continue_reasoning**: Continues reasoning from the current state without resetting. It evaluates rules based on the current state of variables and predicates.
- **set_values**: Assigns provided variable values to the corresponding rules and predicates in the reasoning process.
- **reset_reasoning**: Resets the evaluation state of all rules and predicates while preserving the current values of left terms.
- **clear_reasoning**: Resets the evaluation state and clears all variable values, effectively starting from a clean slate.
- **get_all_missing_variable_ids**: Retrieves a list of all variable IDs that are required but not yet provided in the reasoning process.
- **get_all_missing_variables**: Retrieves a list of all missing variables (as `Variable` objects) required for the reasoning process.
- **analyze_variables_frequency**: Analyzes the frequency of variables across all rules to prioritize missing variables during reasoning.
- **deduction**: Executes the deduction reasoning method, evaluating rules to derive conclusions based on the provided facts.
- **hypothesis_testing**: Executes the hypothesis testing reasoning method, validating a specific hypothesis against the rules and provided facts.

## Supported knowledge base representations

The Business Rules Reasoning System supports multiple ways to represent and construct knowledge bases, making it flexible for different user needs and integration scenarios.

### Business rules (Rule Builder)

The most expressive and programmatic way to define a knowledge base is using the Rule Builder API. This approach allows you to construct rules using Python code, chaining together predicates and conclusions. Each rule is built from predicates (conditions) and a conclusion, and you can use the builder pattern to fluently define complex logic.

**Example:**
```python
from business_rules_reasoning.deductive import RuleBuilder, VariableBuilder, PredicateBuilder
from business_rules_reasoning import OperatorType

rule = RuleBuilder() \
    .set_conclusion(VariableBuilder().set_id("loan_approved").set_value(True).unwrap()) \
    .add_predicate(PredicateBuilder().configure_predicate("age", OperatorType.GREATER_OR_EQUAL, 18).unwrap()) \
    .unwrap()
```
This approach is ideal for developers who want full control and flexibility in defining business logic.

### Decision tables (Python/Pandas)

Decision tables provide a tabular way to represent rules, where each row is a rule and each column is a variable (predicate or conclusion). It is possible to define a decision table as a Pandas DataFrame, and then use the `pandas_to_rules` converter to automatically generate a list of rules from the table.

**Example:**
```python
import pandas as pd
from business_rules_reasoning.deductive.decision_table import pandas_to_rules

data = {
    "age": ["<18", ">=18", "between(30,40)"],
    "income": [">5000", "<=5000", "is_in(3000,4000,5000)"],
    "loan_approved": [False, True, True]
}
df = pd.DataFrame(data)
rules = pandas_to_rules(df, conclusion_index=[-1])
```
This method is especially useful for business analysts or domain experts who prefer working with spreadsheets or tabular data.

### Decision trees (C4.5 algorithm)

The system also supports generating rules from decision trees using the C4.5 algorithm. It is possible to build a decision tree from a Pandas DataFrame using the `c45_decision_tree` function, and then convert the tree to a set of rules with `tree_to_rules`.
The C4.5 alghoritm builds decision trees from a set of training data. The training data does not need to be optimized. The optimized rules are being generated.

**Example:**
```python
from business_rules_reasoning.deductive.decision_table.c45_decision_tree import c45_decision_tree, tree_to_rules

tree = c45_decision_tree(df, conclusion_index=[-1])
rules = tree_to_rules(tree, target="loan_approved", path=[])
```
This approach is useful for scenarios where it is mopre efficient to extract interpretable rules from data-driven decision trees, combining the strengths of machine learning and symbolic reasoning.

## LLM Orchestrator

The LLM Orchestrator is a flexible reasoning tool that integrates with large language models (LLMs) to facilitate automated decision-making and inference processes. It uses knowledge bases, rules, and reasoning methods (e.g., deduction, hypothesis testing) to derive conclusions or ask for additional information when required. The orchestrator supports step-by-step or batch variable fetching and can handle complex reasoning workflows with customizable options.

Unlike popular LLM agents, the large language model is not responsible for controlling the reasoning flow. It functions solely as a fact retrieval agent, while the orchestrator and reasoning engine algorithms manage the entire reasoning process.

### LLMOrchestrator

The `LLMOrchestrator` is the core component that manages the reasoning process. It interacts with the knowledge base, retrieves missing facts, and evaluates rules using the reasoning engine. The orchestrator also integrates with an LLM to handle natural language queries and fact extraction. Key features include:
- Managing the reasoning state and orchestrating the workflow.
- Fetching missing variables through LLM-based prompts or user interactions.
- Supporting both deduction and hypothesis testing reasoning methods.
- Providing detailed inference logs for transparency and debugging.

### LLMPipelineBase and HuggingFacePipeline

The `LLMPipelineBase` is an abstract base class that defines the interface for integrating LLMs into the orchestrator. It includes methods for text generation, summarization, question answering, and more. The `HuggingFacePipeline` is a concrete implementation of this interface using Hugging Face's `transformers` library. It provides:
- Text generation for creating prompts and responses.
- Question answering for extracting facts from documents or user queries.
- Summarization and classification for processing and interpreting input data.

### Knowledge Base Retriever

The knowledge base retriever is a callable function provided to the orchestrator to dynamically load knowledge bases. It allows the orchestrator to access domain-specific rules and predicates tailored to the use case. The retriever can fetch knowledge bases from various sources, such as databases, files, or predefined configurations.

### Orchestrator Options

The orchestrator supports customizable options through the `OrchestratorOptions` class. These options allow fine-tuning of the reasoning process and include:
- **Variables Fetching Mode**: Determines whether variables are fetched step-by-step (`STEP_BY_STEP`) for chat purpose or all at once (`ALL_POSSIBLE`).
- **Conclusion as Fact**: Allows conclusions to be treated as facts for subsequent reasoning steps.
- **Pass Conclusions as Arguments**: Enables passing conclusions as arguments to external functions or workflows.
- **Pass Facts as Arguments**: Enables passing facts as arguments to external functions or workflows.

These options provide flexibility in configuring the orchestrator to meet specific requirements and optimize its behavior for different use cases.

## Example case-study

Let's build a simple yet practical example of automating loan document processing decisions. This case study demonstrates how to use the reasoning system to evaluate loan applications based on predefined business rules, such as checking for unpaid loans, fraud flags, and income thresholds. By leveraging the orchestrator and knowledge base, we can automate decision-making while ensuring transparency and consistency.

### Building business rules

Business rules are constructed using the `KnowledgeBaseBuilder`, `RuleBuilder`, `PredicateBuilder`, and `VariableBuilder` classes. These builders allow you to define variables, predicates, and rules that form the foundation of your knowledge base. For example, you can create rules to evaluate conditions and derive conclusions based on input data.

The orchestrator is able to retrieve more than one knowledge base and evaluate which one should be used based on the provided information.
For the example purpose lets wrap the knowledge base in a retriever function

```python
from typing import List, Callable
from business_rules_reasoning import serialize_knowledge_base
from business_rules_reasoning.base import ReasoningType, OperatorType
from business_rules_reasoning.deductive import KnowledgeBaseBuilder, RuleBuilder, PredicateBuilder, VariableBuilder

def knowledge_base_retriever():
    kb_builder = KnowledgeBaseBuilder().set_id("kb1").set_name("Leasing Document Processing KB").set_description("Knowledge base for processing leasing documents")

    unpaid_loans = VariableBuilder() \
        .set_id("unpaid_loans") \
        .set_name("Indicates if there are any open un-paid loans: 'yes' or 'no'") \
        .unwrap()
    fraud_flag = VariableBuilder() \
        .set_id("fraud_database") \
        .set_name("Indicates if the fraud database has any records: 'yes' or 'no'") \
        .unwrap()
    monthly_net_salary = VariableBuilder() \
        .set_id("monthly_net_salary") \
        .set_name("Monthly Net Salary") \
        .unwrap()
    employment_type = VariableBuilder() \
        .set_id("employment_type") \
        .set_name("Employment Type option from: [freelancer, company emplyoee, unemployed]") \
        .unwrap()
    thirty_percent_ruling = VariableBuilder() \
        .set_id("thirty_percent_ruling") \
        .set_name("30% Ruling - 'yes' if applicable othwerwise 'no'") \
        .unwrap()
    previous_loans = VariableBuilder() \
        .set_id("previous_loans") \
        .set_name("Indicates if there were any historical paid loans") \
        .unwrap()
    ongoing_loans = VariableBuilder() \
        .set_id("ongoing_loans") \
        .set_name("Indicates whether there is any open loans") \
        .unwrap()

    rule1 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(unpaid_loans, OperatorType.EQUAL, True).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule1)

    rule2 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(fraud_flag, OperatorType.EQUAL, True).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule2)

    rule3 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(employment_type, OperatorType.EQUAL, 'unemployed').unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule3)

    rule4 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(monthly_net_salary, OperatorType.LESS_THAN, 2000).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule4)

    rule5 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("loan_accepted").set_name("Loan Accepted").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(employment_type, OperatorType.NOT_EQUAL, "unemployed").unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(monthly_net_salary, OperatorType.GREATER_OR_EQUAL, 2000).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(fraud_flag, OperatorType.EQUAL, False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(unpaid_loans, OperatorType.EQUAL, False).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule5)

    rule6 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("forward_to_bank_verification").set_name("Forward to additional bank verification").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(employment_type, OperatorType.EQUAL, "freelancer").unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule6)

    rule7 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("forward_to_bank_verification").set_name("Forward to additional bank verification").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(thirty_percent_ruling, OperatorType.EQUAL, True).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule7)

    rule8 = RuleBuilder() \
        .set_conclusion(VariableBuilder().set_id("forward_to_bank_verification").set_name("Forward to additional bank verification").set_value(True).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(previous_loans, OperatorType.EQUAL, False).unwrap()) \
        .add_predicate(PredicateBuilder().configure_predicate_with_variable(ongoing_loans, OperatorType.EQUAL, False).unwrap()) \
        .unwrap()
    
    kb_builder.add_rule(rule8)

    knowledge_base = kb_builder.unwrap()
    return [knowledge_base]

def inference_state_retriever(inference_id: str) -> dict:
    # Return an empty inference state for simplicity
    return {}
```

*** OR alternatively (Example in ApacheSpark) ***

```sql
CREATE OR REPLACE TABLE leasing_document_decision_table (
    unpaid_loans STRING COMMENT "Indicates if there are any open un-paid loans: 'yes' or 'no'",
    fraud_flag STRING COMMENT "Indicates if the fraud database has any records: 'yes' or 'no'",
    employment_type STRING COMMENT "Employment Type option from: [freelancer, company emplyoee, unemployed]",
    monthly_net_salary STRING COMMENT "Monthly Net Salary",
    thirty_percent_ruling STRING COMMENT "30% Ruling - 'yes' if applicable othwerwise 'no'",
    previous_loans STRING COMMENT "Indicates if there were any historical paid loans",
    ongoing_loans STRING COMMENT "Indicates whether there is any open loans",
    loan_accepted BOOLEAN COMMENT "Loan Accepted",
    forward_to_bank_verification BOOLEAN COMMENT "Forward to additional bank verification"
)
COMMENT "Knowledge base for processing leasing documents";

INSERT INTO leasing_document_decision_table VALUES
    ('True', NULL, NULL, NULL, NULL, NULL, NULL, False, NULL),
    (NULL, 'True', NULL, NULL, NULL, NULL, NULL, False, NULL),
    (NULL, NULL, 'unemployed', NULL, NULL, NULL, NULL, False, NULL),
    (NULL, NULL, NULL, '<2000', NULL, NULL, NULL, False, NULL),
    ('False', 'False', '!=unemployed', '>=2000', NULL, NULL, NULL, True, NULL),
    (NULL, NULL, 'freelancer', NULL, NULL, NULL, NULL, NULL, True),
    (NULL, NULL, NULL, NULL, 'True', NULL, NULL, NULL, True),
    (NULL, NULL, NULL, NULL, NULL, 'False', 'False', NULL, True);
```

```python
from business_rules_reasoning.base import KnowledgeBase
from business_rules_reasoning.deductive import KnowledgeBaseBuilder
from business_rules_reasoning.deductive.decision_table import pandas_to_rules
from business_rules_reasoning.orchestrator import OrchestratorOptions
from business_rules_reasoning.orchestrator.llm import HuggingFacePipeline, LLMOrchestrator

def knowledge_base_retriever_from_tables() -> list[KnowledgeBase]:
    # Define the decision tables and determine conclusion column indexes
    tables = [
        { "name": 'leasing_document_decision_table', "conclusions": [-2, -1] }
    ]
    knowledge_bases = []

    for table in tables:
        table_name = table["name"]
        query = f"SELECT * FROM {table_name}"
        df = spark.sql(query)

        pandas_df = df.toPandas()

        # Extract column names and comments into a dictionary
        columns_query = f"DESCRIBE TABLE {table_name}"
        columns_df = spark.sql(columns_query)
        features_description = {row['col_name']: row['comment'] for row in columns_df.collect() if row['comment']}

        # Extract table comment
        table_comment_query = f"DESCRIBE TABLE EXTENDED {table_name}"
        table_comment_df = spark.sql(table_comment_query)
        table_comment = table_comment_df.filter(table_comment_df.col_name == "Comment").select("data_type").collect()
        table_description = table_comment[0]["data_type"] if table_comment else f"Knowledge base for {table_name}"

        # Generate rule sets from the Pandas DataFrame
        rules = pandas_to_rules(pandas_df, conclusion_index=table["conclusions"], features_description=features_description)

        # Pass the rules to the KnowledgeBase
        kb_builder = KnowledgeBaseBuilder().set_id(table_name).set_name(f"Knowledge Base for {table_name}").set_description(table_description)
        for rule in rules:
            kb_builder.add_rule(rule)
        knowledge_bases.append(kb_builder.unwrap())

    return knowledge_bases
```

### Displaying business rules

Once the knowledge base is built, you can display the rules and their structure using the `display()` method of the `KnowledgeBase` class. This provides a human-readable representation of the rules, including their predicates and conclusions, which is useful for debugging and validation.

```python
kb = knowledge_base_retriever()[0]
print(kb.display())
```

Result:
```
(unpaid_loans = True) → loan_accepted = False
(fraud_database = True) → loan_accepted = False
(employment_type = unemployed) → loan_accepted = False
(monthly_net_salary < 2000) → loan_accepted = False
(employment_type != unemployed ∧ monthly_net_salary >= 2000 ∧ fraud_database = False ∧ unpaid_loans = False) → loan_accepted = True
(employment_type = freelancer) → forward_to_bank_verification = True
(thirty_percent_ruling = True) → forward_to_bank_verification = True
(previous_loans = False ∧ ongoing_loans = False) → forward_to_bank_verification = True
```

### Preparing a document example

To demonstrate the reasoning process, you can prepare a document example by defining variables and their values. These variables are then used as input to the orchestrator or reasoning engine to evaluate the rules and derive conclusions.

```python
case1_success_with_bank_verification = """
Bank Screening Document

Customer Information:
Name: John Doe
Customer ID: 123456789

Loan History (BKR Check):
Loans:
- Personal Loan (Paid, closed)
- Private car leasing (Paid, closed)
Current Loan Status: No active loans

Fraud Database Check:
Status: No record found in internal fraud databases

Financial Information:
Monthly Net Salary: 3,000 EUR

Employment Type: Freelancer

30% Ruling Check:
No

Check the customer document for loan acceptance and check if is needed to forward to bank verification team
"""
```

### Initialising the HuggingFace orchestrator

The HuggingFace orchestrator is initialized by providing a knowledge base retriever, inference state retriever, and an LLM pipeline (e.g., HuggingFace's text-generation model). The orchestrator integrates the reasoning engine with the LLM to handle complex queries and reasoning workflows.

First lets download a model from HuggingFace. Let if be the Llama 3.2 3B Instruct. There is a instruction fine tune version needed to proceed.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "meta-llama/Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
```

Lets set the model kwargs so to a level the model is more deterministic.

```python
model_kwargs={
    "max_new_tokens": 100,
    "temperature": 0.2,
    "top_k": 1,
    "top_p": 0.4
}
```

The orchestrator needs knowledge base retriever and inference state retriever in case of loading existing and stopped reasoning processes.
Also the donloaded model and tokenizer needs to be provided via HuggingFacePipeline to be compatible with the orchestrator.

```python
from business_rules_reasoning.orchestrator.llm import LLMOrchestrator, HuggingFacePipeline

orchestrator = LLMOrchestrator(
    model_name=model_name,
    knowledge_base_retriever=knowledge_base_retriever,
    inference_state_retriever=inference_state_retriever,
    llm = HuggingFacePipeline(model_name=model_name, tokenizer=tokenizer, model=model, **model_kwargs)
)
```

### Querying the orchestrator and tracing the inference log

You can query the orchestrator by providing a natural language query. The orchestrator processes the query, evaluates the rules, and returns the results. Additionally, you can trace the inference log to understand the reasoning steps, including the variables fetched, rules evaluated, and conclusions derived.

Lets start deduction by executing the document and question before:

```python
response = orchestrator.query(case1_success_with_bank_verification)

print("Response:\n", response)
```

Result:
```
Response:
 The loan has been accepted and is moving forward to bank verification.
```

The answer seems to be correct as it is the expected conclusion but it is possible to display all resaoning process state to see what heppened during the inference.

```python
print(orchestrator.reasoning_process.display_state())
```

Result:
```
(unpaid_loans = True (Provided: False, Status: Evaluated, Result: False)) → loan_accepted = False
Rule Status: Evaluated, Rule Result: False

(fraud_database = True (Provided: False, Status: Evaluated, Result: False)) → loan_accepted = False
Rule Status: Evaluated, Rule Result: False

(employment_type = unemployed (Provided: freelancer, Status: Evaluated, Result: False)) → loan_accepted = False
Rule Status: Evaluated, Rule Result: False

(monthly_net_salary < 2000 (Provided: 3000.0, Status: Evaluated, Result: False)) → loan_accepted = False
Rule Status: Evaluated, Rule Result: False

(employment_type != unemployed (Provided: freelancer, Status: Evaluated, Result: True) ∧ monthly_net_salary >= 2000 (Provided: 3000.0, Status: Evaluated, Result: True) ∧ fraud_database = False (Provided: False, Status: Evaluated, Result: True) ∧ unpaid_loans = False (Provided: False, Status: Evaluated, Result: True)) → loan_accepted = True
Rule Status: Evaluated, Rule Result: True

(employment_type = freelancer (Provided: freelancer, Status: Evaluated, Result: True)) → forward_to_bank_verification = True
Rule Status: Evaluated, Rule Result: True

(thirty_percent_ruling = True (Provided: False, Status: Evaluated, Result: False)) → forward_to_bank_verification = True
Rule Status: Evaluated, Rule Result: False

(previous_loans = False (Provided: True, Status: Evaluated, Result: False) ∧ ongoing_loans = False (Provided: False, Status: Not Evaluated, Result: False)) → forward_to_bank_verification = True
Rule Status: Evaluated, Rule Result: False

State: FINISHED
Evaluation Message: PASSED
Reasoned Items: loan_accepted = True, forward_to_bank_verification = True

Reasoning Method: DEDUCTION
Knowledge Base Type: CRISP
```

It's visble now the rules and the values provided together with information which rule was evaluated and what was the evaluation result. All predicates with result 'True' should imply the conclusion is valid.

And the inference log to track the logic:

```python
print('\n'.join(orchestrator.inference_logger.get_log()))
```

Response:
```
[Orchestrator]: Retrieved knwledge bases: kb1
[Orchestrator]: Status set to: OrchestratorStatus.INITIALIZED
[Orchestrator]: Prompting for inference instructions...
[Orchestrator]: Retrieved JSON from prompt: {"knowledge_base_id": "kb1", "reasoning_method": "deduction"}
[Orchestrator]: Reasoning process was set with method: DEDUCTION and knowledge base: kb1
[Orchestrator]: Changing status from OrchestratorStatus.INITIALIZED to OrchestratorStatus.STARTED.
[Engine]: Starting reasoning process from status: ReasoningState.INITIALIZED
[Engine]: Reasoning process was started. Resulting status: ReasoningState.STOPPED
[Orchestrator]: Changing status from OrchestratorStatus.STARTED to OrchestratorStatus.ENGINE_WAITING_FOR_VARIABLES.
[Engine]: Status: ReasoningState.STOPPED Retrieving missing variables.
[Orchestrator]: Prompting for variables...
[Orchestrator]: Retrieved JSON from prompt: {"unpaid_loans": "no", "fraud_database": "no", "employment_type": "freelancer", "monthly_net_salary": 3000, "thirty_percent_ruling": "no", "previous_loans": "yes", "ongoing_loans": "no"}
[Orchestrator]: Parsed variables from prompt: {"unpaid_loans": false, "fraud_database": false, "employment_type": "freelancer", "monthly_net_salary": 3000.0, "thirty_percent_ruling": false, "previous_loans": true, "ongoing_loans": false}
[Engine]: Providing variables to engine: unpaid_loans, fraud_database, employment_type, monthly_net_salary, thirty_percent_ruling, previous_loans, ongoing_loans.
[Engine]: Reasoning continued. Resulting status: ReasoningState.FINISHED.
[Orchestrator]: Changing status from OrchestratorStatus.ENGINE_WAITING_FOR_VARIABLES to OrchestratorStatus.INFERENCE_FINISHED.
[Orchestrator]: Prompting for answer generation...
```

## Model evaluation

Model evaluation for this reasoning system was performed using Databricks model evaluation workflows. All test cases were executed as internal agent requests, ensuring that the reasoning engine and orchestrator were thoroughly validated in a controlled environment. The evaluation code, including batch prompt execution and dataset initialization, can be found in the `model_evaluation` folder of this repository.

All test cases passed successfully, demonstrating the robustness and correctness of the reasoning process and LLM orchestration. Please note that the examples and test cases provided in this repository are abstract and intended solely for demonstration and educational purposes. They do not represent any real company business logic or production decision rules.

<p align="center">
  <img src="images/test_case_correctness.png" alt="Test Case Correctness" width="600"/>
</p>

<p align="center">
  <img src="images/internal_conversation_relevance_tests.png" alt="Internal Conversation Relevance Tests" width="600"/>
</p>

## Authors
- Lukasz Wardzala - [github](https://github.com/lwardzala)

## References
- [Horn clause wiki](https://en.wikipedia.org/wiki/Horn_clause)
import unittest
from unittest.mock import MagicMock, patch
from transformers import AutoTokenizer, AutoModelForCausalLM
from src.business_rules_reasoning.orchestrator.llm.huggingface_orchestrator import HuggingFaceOrchestrator, PromptTemplates
from src.business_rules_reasoning.base import KnowledgeBase, ReasoningProcess, ReasoningMethod, Variable

class TestHuggingFaceOrchestrator(unittest.TestCase):
    def setUp(self):
        self.mock_tokenizer = MagicMock(spec=AutoTokenizer)
        self.mock_model = MagicMock(spec=AutoModelForCausalLM)
        self.knowledge_base_retriever = MagicMock()
        self.inference_state_retriever = MagicMock()
        self.orchestrator = HuggingFaceOrchestrator(
            model_name="mock-model",
            knowledge_base_retriever=self.knowledge_base_retriever,
            inference_state_retriever=self.inference_state_retriever,
            tokenizer=self.mock_tokenizer,
            model=self.mock_model
        )

    @patch.object(HuggingFaceOrchestrator, '_prompt_llm')
    def test_fetch_inference_instructions(self, mock_prompt_llm):
        mock_prompt_llm.return_value = "knowledge_base: kb1\nreasoning_method: deduction"
        self.orchestrator.knowledge_bases = [KnowledgeBase(id="kb1", name="KB1", description="Test KB")]
        knowledge_base_id, reasoning_method = self.orchestrator._fetch_inference_instructions("test query")
        self.assertEqual(knowledge_base_id, "kb1")
        self.assertEqual(reasoning_method, ReasoningMethod.DEDUCTION)

    @patch.object(HuggingFaceOrchestrator, '_prompt_llm')
    def test_fetch_variables(self, mock_prompt_llm):
        mock_prompt_llm.return_value = "var1 = value1\nvar2 = value2"
        variables = [Variable(id="var1", name="Variable 1"), Variable(id="var2", name="Variable 2")]
        variables_dict = self.orchestrator._fetch_variables("test query", variables)
        self.assertEqual(variables_dict["var1"], "value1")
        self.assertEqual(variables_dict["var2"], "value2")

    @patch.object(HuggingFaceOrchestrator, '_prompt_llm')
    def test_ask_for_more_information(self, mock_prompt_llm):
        mock_prompt_llm.return_value = "question: Can you provide more details about var1?"
        self.orchestrator.query_history = [
            {"role": "user", "text": "Initial query"},
            {"role": "agent", "text": "Response from agent"}
        ]
        question = self.orchestrator._ask_for_more_information("var1")
        self.assertEqual(question, "Can you provide more details about var1?")

    @patch.object(HuggingFaceOrchestrator, '_prompt_llm')
    def test_ask_for_reasoning_clarification(self, mock_prompt_llm):
        mock_prompt_llm.return_value = "question: Can you clarify the reasoning needed?"
        self.orchestrator.knowledge_bases = [KnowledgeBase(name="KB1", description="Test KB")]
        question = self.orchestrator._ask_for_reasoning_clarification()
        self.assertEqual(question, "Can you clarify the reasoning needed?")

if __name__ == '__main__':
    unittest.main()

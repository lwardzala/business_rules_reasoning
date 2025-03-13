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

    @patch('src.business_rules_reasoning.orchestrator.llm.huggingface_pipeline.HuggingFacePipeline.prompt_text_generation')
    def test_fetch_inference_instructions(self, mock_prompt_text_gen):
        mock_prompt_text_gen.return_value = ' { "knowledge_base_id": "kb1", "reasoning_method": "deduction" }\nreasoning_method: deduction'
        self.orchestrator.knowledge_bases = [KnowledgeBase(id="kb1", name="KB1", description="Test KB")]
        knowledge_base_id, reasoning_method = self.orchestrator._fetch_inference_instructions("test query")
        self.assertEqual(knowledge_base_id, "kb1")
        self.assertEqual(reasoning_method, ReasoningMethod.DEDUCTION)

    @patch('src.business_rules_reasoning.orchestrator.llm.huggingface_pipeline.HuggingFacePipeline.prompt_text_generation')
    def test_fetch_variables(self, mock_prompt_text_gen):
        mock_prompt_text_gen.return_value = '{"var1": 39,\n     "var2": "true"}'
        variables = [
            Variable(id="var1", name="Variable 1", value=0),
            Variable(id="var2", name="Variable 2", value=False)
        ]
        variables_dict = self.orchestrator._fetch_variables("test query", variables)
        self.assertEqual(variables_dict["var1"], 39)
        self.assertEqual(variables_dict["var2"], True)

    @patch('src.business_rules_reasoning.orchestrator.llm.huggingface_pipeline.HuggingFacePipeline.prompt_text_generation')
    def test_ask_for_more_information(self, mock_prompt_text_gen):
        mock_prompt_text_gen.return_value = "question: Can you provide more details about var1?"
        self.orchestrator.query_history = [
            {"role": "user", "text": "Initial query"},
            {"role": "agent", "text": "Response from agent"}
        ]
        question = self.orchestrator._ask_for_more_information("var1")
        self.assertEqual(question, "Can you provide more details about var1?")

    @patch('src.business_rules_reasoning.orchestrator.llm.huggingface_pipeline.HuggingFacePipeline.prompt_text_generation')
    def test_ask_for_reasoning_clarification(self, mock_prompt_text_gen):
        mock_prompt_text_gen.return_value = "question: Can you clarify the reasoning needed?"
        self.orchestrator.knowledge_bases = [KnowledgeBase(name="KB1", description="Test KB")]
        question = self.orchestrator._ask_for_reasoning_clarification()
        self.assertEqual(question, "Can you clarify the reasoning needed?")

    def test_set_reasoning_process(self):
        knowledge_base = KnowledgeBase(id="kb1", name="KBbb1", description="Test KB")
        self.orchestrator.knowledge_bases = [knowledge_base]
        result = self.orchestrator._set_reasoning_process("kb1", ReasoningMethod.DEDUCTION)
        self.assertTrue(result)
        self.assertIsNotNone(self.orchestrator.reasoning_process)
        self.assertEqual(self.orchestrator.reasoning_process.knowledge_base.id, "kb1")
        self.assertEqual(self.orchestrator.reasoning_process.reasoning_method, ReasoningMethod.DEDUCTION)

if __name__ == '__main__':
    unittest.main()

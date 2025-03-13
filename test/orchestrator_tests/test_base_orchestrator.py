import unittest
from unittest.mock import MagicMock
from src.business_rules_reasoning.orchestrator.base_orchestrator import BaseOrchestrator, OrchestratorStatus
from src.business_rules_reasoning.base import KnowledgeBase, ReasoningProcess, ReasoningMethod

class TestBaseOrchestrator(BaseOrchestrator):
    def _next_step(self):
        pass

    def set_session_id(self):
        self.inference_session_id = "test_session_id"

class TestBaseOrchestratorMethods(unittest.TestCase):
    def setUp(self):
        self.knowledge_base_retriever = MagicMock()
        self.inference_state_retriever = MagicMock()
        self.orchestrator = TestBaseOrchestrator(
            knowledge_base_retriever=self.knowledge_base_retriever,
            inference_state_retriever=self.inference_state_retriever
        )

    def test_start_orchestration(self):
        self.orchestrator.start_orchestration()
        self.assertEqual(self.orchestrator.status, OrchestratorStatus.INITIALIZED)

    def test_reset_orchestration(self):
        self.orchestrator.reset_orchestration()
        self.assertEqual(self.orchestrator.status, OrchestratorStatus.INITIALIZED)
        self.assertEqual(self.orchestrator.inference_session_id, 'test_session_id')
        self.assertIsNone(self.orchestrator.reasoning_process)

    # def test_retrieve_knowledge_base(self):
    #     self.knowledge_base_retriever.return_value = [{"id": "kb1", "name": "KB1", "description": "Test KB"}]
    #     self.orchestrator.retrieve_knowledge_base()
    #     self.assertEqual(len(self.orchestrator.knowledge_bases), 1)
    #     self.assertEqual(self.orchestrator.knowledge_bases[0].id, "kb1")

    # def test_retrieve_inference_state(self):
    #     self.inference_state_retriever.return_value = {"state": "INITIALIZED"}
    #     self.orchestrator.retrieve_inference_state("test_id")
    #     self.assertEqual(self.orchestrator.reasoning_process.state, "INITIALIZED")

if __name__ == '__main__':
    unittest.main()

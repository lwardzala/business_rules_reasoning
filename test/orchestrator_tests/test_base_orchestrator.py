from typing import Callable
import unittest
from unittest.mock import Mock
from src.business_rules_reasoning.orchestrator.base_orchestrator import BaseOrchestrator, OrchestratorStatus
from src.business_rules_reasoning.base import KnowledgeBase, ReasoningProcess, ReasoningState, ReasoningType
from src.business_rules_reasoning.deductive import DeductiveReasoningService

class TestBaseOrchestrator(BaseOrchestrator):
    def next_step(self):
        pass

    def set_session_id(self):
        self.inference_session_id = "test_session_id"

class TestBaseOrchestratorMethods(unittest.TestCase):
    def setUp(self):
        self.knowledge_base_retriever = Mock(return_value=[{"id": "kb1", "name": "Knowledge Base 1", "description": "Test KB", "rule_set": [], "properties": {}, "reasoning_type": "CRISP"}])
        self.inference_state_retriever = Mock(return_value={"reasoning_method": "DEDUCTION", "knowledge_base": {"id": "kb1", "name": "Knowledge Base 1", "description": "Test KB", "rule_set": [], "properties": {}, "reasoning_type": "CRISP"}, "state": "INITIALIZED", "reasoned_items": [], "evaluation_message": "NONE", "options": {}, "reasoning_error_message": ""})
        self.orchestrator = TestBaseOrchestrator(self.knowledge_base_retriever, self.inference_state_retriever)

    def test_start_orchestration(self):
        self.orchestrator.start_orchestration()
        self.assertEqual(self.orchestrator.status, OrchestratorStatus.INITIALIZED)
        self.assertEqual(self.orchestrator.inference_session_id, "test_session_id")
        self.assertEqual(len(self.orchestrator.knowledge_bases), 1)
        self.assertEqual(self.orchestrator.knowledge_bases[0].id, "kb1")

    def test_reset_orchestration(self):
        self.orchestrator.start_orchestration()
        self.orchestrator.reset_orchestration()
        self.assertEqual(self.orchestrator.status, OrchestratorStatus.INITIALIZED)
        self.assertEqual(self.orchestrator.inference_session_id, "test_session_id")
        self.assertEqual(len(self.orchestrator.knowledge_bases), 1)
        self.assertEqual(self.orchestrator.knowledge_bases[0].id, "kb1")

    def test_retrieve_knowledge_base(self):
        self.orchestrator.retrieve_knowledge_base()
        self.assertEqual(len(self.orchestrator.knowledge_bases), 1)
        self.assertEqual(self.orchestrator.knowledge_bases[0].id, "kb1")

    def test_retrieve_inference_state(self):
        self.orchestrator.retrieve_inference_state("test_session_id")
        self.assertEqual(self.orchestrator.reasoning_process.state, ReasoningState.INITIALIZED)
        self.assertEqual(self.orchestrator.reasoning_process.knowledge_base.id, "kb1")

    def test_get_reasoning_service(self):
        self.orchestrator.retrieve_inference_state("test_session_id")
        reasoning_service = self.orchestrator.get_reasoning_service()

        reasoning_process = self.orchestrator.reasoning_process
        self.assertEqual(reasoning_process.state, ReasoningState.INITIALIZED)
        started_reasoning_process = reasoning_service.start_reasoning(reasoning_process)
        self.assertEqual(started_reasoning_process.state, ReasoningState.FINISHED)

        self.orchestrator.reasoning_process.knowledge_base.reasoning_type = ReasoningType.FUZZY
        with self.assertRaises(NotImplementedError):
            self.orchestrator.get_reasoning_service()

if __name__ == '__main__':
    unittest.main()

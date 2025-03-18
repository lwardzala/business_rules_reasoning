import unittest
from src.business_rules_reasoning.orchestrator.llm.huggingface_pipeline import HuggingFacePipeline

class TestMergeKwargs(unittest.TestCase):
    def setUp(self):
        self.pipeline = HuggingFacePipeline(model_name="mock-model", tokenizer=None, model=None)

    def test_merge_kwargs(self):
        kwargs1 = {'a': 1, 'b': 2}
        kwargs2 = {'b': 3, 'c': 4}
        result = self.pipeline.merge_kwargs(kwargs1, kwargs2)
        expected_result = {'a': 1, 'b': 2, 'c': 4}
        self.assertEqual(result, expected_result)

    def test_merge_kwargs_with_empty_kwargs1(self):
        kwargs1 = {}
        kwargs2 = {'b': 3, 'c': 4}
        result = self.pipeline.merge_kwargs(kwargs1, kwargs2)
        expected_result = {'b': 3, 'c': 4}
        self.assertEqual(result, expected_result)

    def test_merge_kwargs_with_empty_kwargs2(self):
        kwargs1 = {'a': 1, 'b': 2}
        kwargs2 = {}
        result = self.pipeline.merge_kwargs(kwargs1, kwargs2)
        expected_result = {'a': 1, 'b': 2}
        self.assertEqual(result, expected_result)

    def test_merge_kwargs_with_both_empty(self):
        kwargs1 = {}
        kwargs2 = {}
        result = self.pipeline.merge_kwargs(kwargs1, kwargs2)
        expected_result = {}
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
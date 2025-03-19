import unittest
from src.business_rules_reasoning.utils.kwargs_utils import merge_kwargs

class TestKwargsUtils(unittest.TestCase):
    def test_merge_kwargs(self):
        kwargs1 = {"a": 1, "b": 2}
        kwargs2 = {"b": 3, "c": 4}
        result = merge_kwargs(kwargs1, kwargs2)
        expected = {"a": 1, "b": 2, "c": 4}
        self.assertEqual(result, expected)

    def test_merge_kwargs_with_empty_first(self):
        kwargs1 = {}
        kwargs2 = {"b": 3, "c": 4}
        result = merge_kwargs(kwargs1, kwargs2)
        expected = {"b": 3, "c": 4}
        self.assertEqual(result, expected)

    def test_merge_kwargs_with_empty_second(self):
        kwargs1 = {"a": 1, "b": 2}
        kwargs2 = {}
        result = merge_kwargs(kwargs1, kwargs2)
        expected = {"a": 1, "b": 2}
        self.assertEqual(result, expected)

    def test_merge_kwargs_with_overlapping_keys(self):
        kwargs1 = {"a": 1, "b": 2}
        kwargs2 = {"a": 3, "b": 4}
        result = merge_kwargs(kwargs1, kwargs2)
        expected = {"a": 1, "b": 2}
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

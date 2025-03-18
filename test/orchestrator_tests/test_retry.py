import unittest
from src.business_rules_reasoning.orchestrator.llm.retry import retry

class TestRetry(unittest.TestCase):
    def test_retry_success_on_first_attempt(self):
        def func():
            return "success"
        
        result = retry(func, retries=3, validation_func=lambda x: x == "success")
        self.assertEqual(result, "success")

    def test_retry_success_on_second_attempt(self):
        attempts = [0]

        def func():
            if attempts[0] < 1:
                attempts[0] += 1
                return "fail"
            return "success"
        
        result = retry(func, retries=3, validation_func=lambda x: x == "success")
        self.assertEqual(result, "success")

    def test_retry_failure(self):
        def func():
            raise Exception("fail")
        
        with self.assertRaises(Exception):
            retry(func, retries=3, validation_func=lambda x: x == "success")

    def test_retry_with_exception(self):
        attempts = [0]

        def func():
            if attempts[0] < 2:
                attempts[0] += 1
                raise ValueError("error")
            return "success"
        
        result = retry(func, retries=3, validation_func=lambda x: x == "success")
        self.assertEqual(result, "success")

    def test_retry_with_exception_failure(self):
        def func():
            raise ValueError("error")
        
        with self.assertRaises(ValueError):
            retry(func, retries=3, validation_func=lambda x: x == "success")

if __name__ == '__main__':
    unittest.main()

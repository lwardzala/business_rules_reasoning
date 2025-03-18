from typing import Callable, Any

def retry(func: Callable, retries: int, validation_func: Callable[[Any], bool] = None) -> Any:
    for attempt in range(retries):
        try:
            result = func()
            if validation_func is None or validation_func(result):
                return result
        except Exception as e:
            if attempt == retries - 1:
                raise e
    return result

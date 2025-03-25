from typing import List


class InferenceLogger:
    def __init__(self, log: List[str] = None):
        self._log = log.copy() if log is not None else []

    def log(self, message: str):
        self._log.append(message)

    def get_log(self):
        return self._log

    def clear_log(self):
        self._log = []

    def __len__(self):
        return len(self._log)

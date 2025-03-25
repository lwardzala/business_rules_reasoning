from typing import List


class InferenceLogger:
    def __init__(self):
        self._log =  []

    def log(self, message: str):
        if not self._log or self._log[-1] != message:
            self._log.append(message)

    def get_log(self):
        return self._log

    def clear_log(self):
        self._log = []

    def __len__(self):
        return len(self._log)

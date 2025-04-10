from typing import List

class ChatHistory:
    def __init__(self):
        self.history: List[tuple[str, str]] = []

    def append(self, query: str, response: str):
        self.history.append((query, response))

    def get(self) -> List[tuple[str, str]]:
        return self.history
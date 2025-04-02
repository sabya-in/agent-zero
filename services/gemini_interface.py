from abc import ABC, abstractmethod

class GeminiService(ABC):
    @abstractmethod
    def get_analysis(self, prompt: str) -> str:
        pass

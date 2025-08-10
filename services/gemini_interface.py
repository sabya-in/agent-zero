from abc import ABC, abstractmethod

class GeminiService(ABC):
    @abstractmethod
    def get_analysis(self, prompt: str, prompt_type: str) -> str:
        pass

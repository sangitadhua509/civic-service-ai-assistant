from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Base interface for all LLM providers.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate an answer from the given prompt.
        """
        pass
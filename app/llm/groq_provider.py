from app.llm.base import LLMProvider


class GroqProvider(LLMProvider):
    """
    LLM provider using Groq.
    """

    def __init__(self, client):
        self.client = client

    def generate(self, prompt: str) -> str:
        """
        Generate an answer using the Groq API.
        """

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content
from app.llm.base import LLMProvider


class RetrievalOnlyProvider(LLMProvider):
    """
    Provider that returns retrieved guideline content
    without calling an external language model.
    """

    def generate(self, prompt: str) -> str: 
        """
        Return the approved guideline context as the answer.
        """

        marker = "Approved guideline context:"

        if marker in prompt:
         context = prompt.split(
            marker,
            1
          )[1]

         if "Answer clearly and concisely." in context:
            context = context.split(
                "Answer clearly and concisely.",
                1
            )[0]

         return context.strip()

        return prompt 
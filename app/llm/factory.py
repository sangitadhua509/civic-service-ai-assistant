from app.llm.retrieval_only import RetrievalOnlyProvider
from app.llm.groq_provider import GroqProvider


def get_llm_provider(
    mode: str = "retrieval_only",
    client=None
):
    """
    Return the configured LLM provider.
    """

    if mode == "retrieval_only":
        return RetrievalOnlyProvider()

    if mode == "groq":
        if client is None:
            raise ValueError(
                "Groq client is required for Groq mode."
            )

        return GroqProvider(client)

    raise ValueError(
        f"Unsupported LLM mode: {mode}"
    )
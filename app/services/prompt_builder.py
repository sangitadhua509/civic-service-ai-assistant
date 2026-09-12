def build_context(results: list[dict]) -> str:
    """
    Convert retrieved results into a text context
    that can be provided to the AI.
    """

    context_parts = []

    for result in results:
        context_parts.append(
            result["chunk_text"]
        )

    return "\n\n".join(context_parts)

def build_sources(results: list[dict]) -> str:
    """
    Convert retrieved metadata into human-readable
    source references.
    """

    sources = []

    for result in results:
        metadata = result.get("metadata", {})

        source = metadata.get(
            "source",
            "Unknown source"
        )

        page = metadata.get(
            "page",
            "Unknown page"
        )

        sources.append(
            f"Source: {source} | Page: {page}"
        )

    return "\n".join(sources)


def build_prompt(
    query: str,
    context: str
) -> str:
    """
    Build the prompt used by the AI to answer
    using the retrieved guideline context.
    """

    prompt = f"""
You are a civic service assistant.

Answer the citizen's question using ONLY the
information provided in the approved guideline context.

If the answer cannot be found in the provided context,
clearly say that the information is not available in
the indexed guidelines.

Do not invent requirements, documents, fees, eligibility
conditions, deadlines, or procedures.

Citizen's question:
{query}

Approved guideline context:
{context}

Answer clearly and concisely.
"""

    return prompt.strip()


def format_response(
    answer: str,
    sources: str
) -> str:
    """
    Format the final answer with source references
    and the required disclaimer.
    """

    disclaimer = (
        "This information is based on the indexed "
        "guidelines and does not guarantee eligibility "
        "or approval."
    )

    response = f"""
{answer}

Source References:
{sources}

Disclaimer:
{disclaimer}
"""

    return response.strip()

if __name__ == "__main__":

    from app.services.retriever import retrieve

    query = "What documents are required?"

    results = retrieve(
        query,
        top_k=3
    )

    print("=== CONTEXT ===")
    print(build_context(results))

    print("\n=== SOURCES ===")
    print(build_sources(results))

    context = build_context(results)

    prompt = build_prompt(
        query=query,
        context=context
    )

    print("\n=== PROMPT ===")
    print(prompt)\

    answer = "You need to submit the application form, proof of address, and supporting documents."

    sources = build_sources(results)

    formatted_response = format_response(
        answer=answer,
        sources=sources
    )

    print("\n=== FINAL RESPONSE ===")
    print(formatted_response)
from app.services.retriever import retrieve
from app.services.prompt_builder import (
    build_context,
    build_prompt,
    build_sources,
    format_response
)
from app.llm.factory import get_llm_provider


def prepare_rag(
    query: str,
    top_k: int = 3
) -> dict:
    """
    Retrieve relevant guideline content and prepare
    the context and prompt for the AI.
    """

    results = retrieve(
        query=query,
        top_k=top_k
    )

    if not results:
     return {
        "query": query,
        "results": [],
        "context": "",
        "prompt": "",
        "answer": "The information is not available in the indexed guidelines."
    }

    provider = get_llm_provider()
    context = build_context(results)

    prompt = build_prompt(
        query=query,
        context=context
    )
    answer = provider.generate(prompt)
    sources = build_sources(results)

    formatted_response = format_response(
    answer=answer,
    sources=sources
)

    return {
    "query": query,
    "results": results,
    "context": context,
    "prompt": prompt,
    "answer": formatted_response,
    "sources": sources
}


if __name__ == "__main__":

    query = "What documents are required?"

    rag_data = prepare_rag(
        query=query,
        top_k=3
    )

    print("=== QUERY ===")
    print(rag_data["query"])

    print("\n=== RESULTS ===")
    print(f"Results found: {len(rag_data['results'])}")

    print("\n=== CONTEXT ===")
    print(rag_data["context"])

    print("\n=== PROMPT ===")
    print(rag_data["prompt"])
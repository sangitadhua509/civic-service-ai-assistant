import math
import re

from app.services.embedding import embed_text
from app.services.vector_store import get_all_vectors

def get_keywords(text: str) -> set[str]:
    """
    Extract meaningful words from text.
    """

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

    stop_words = {
        "the",
        "and",
        "for",
        "are",
        "what",
        "how",
        "can",
        "does",
        "with",
        "from",
        "this",
        "that",
        "you",
        "need"
    }

    return {
        word
        for word in words
        if word not in stop_words
    }

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    """

    dot_product = sum(
        x * y for x, y in zip(a, b)
    )

    magnitude_a = math.sqrt(
        sum(x * x for x in a)
    )

    magnitude_b = math.sqrt(
        sum(x * x for x in b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )

def retrieve(
    query: str,
    top_k: int = 3,
    similarity_threshold: float = 0.20
) -> list[dict]:
    """
    Retrieve the most relevant stored chunks for a query.
    """

    query_vector = embed_text(query)

    query_keywords = get_keywords(query)

    stored_vectors = get_all_vectors()

    results = []

    for record in stored_vectors:

      chunk_keywords = get_keywords(
        record["chunk_text"]
      )

      keyword_overlap = query_keywords & chunk_keywords

      if len(keyword_overlap) < 2:
       continue

      score = cosine_similarity(
        query_vector,
        record["vector"]
       )
      print(
              f"Similarity score: {score:.4f}"
        )

      results.append({
            "score": score,
            "chunk_text": record["chunk_text"],
            "document_id": record["document_id"],
            "department_id": record["department_id"],
            "service_id": record["service_id"],
            "metadata": record["metadata"]
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    results = [
    result
    for result in results
    if result["score"] >= similarity_threshold
]

    return results[:top_k]



if __name__ == "__main__":

    query = "What documents are required?"

    results = retrieve(
        query,
        top_k=3
    )

    print(f"Query: {query}")
    print(f"Results found: {len(results)}")

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print(f"Score: {result['score']:.4f}")
        print(f"Chunk: {result['chunk_text']}")
        print(f"Metadata: {result['metadata']}")
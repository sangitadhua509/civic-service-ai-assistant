import json
from pathlib import Path


VECTOR_INDEX_DIR = Path("data/vector_index")
VECTOR_INDEX_FILE = VECTOR_INDEX_DIR / "vectors.json"


def save_vectors(vectors: list[dict]) -> None:
    """
    Save vector records to the vector index file.
    """

    VECTOR_INDEX_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        VECTOR_INDEX_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            vectors,
            file,
            indent=2
        )


def load_vectors() -> list[dict]:
    """
    Load vector records from the vector index file.
    """

    if not VECTOR_INDEX_FILE.exists():
        return []

    with open(
        VECTOR_INDEX_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)




def add_vector(
    chunk_text: str,
    vector: list[float],
    document_id: int,
    department_id: int | None = None,
    service_id: int | None = None,
    metadata: dict | None = None
) -> dict:
    """
    Add one chunk and its vector to the vector store.
    """

    vectors = load_vectors()

    record = {
        "chunk_text": chunk_text,
        "vector": vector,
        "document_id": document_id,
        "department_id": department_id,
        "service_id": service_id,
        "metadata": metadata or {}
    }

    vectors.append(record)

    save_vectors(vectors)

    return record

def add_vectors(records: list[dict]) -> None:
    """
    Add multiple vector records to the vector store.
    """

    vectors = load_vectors()

    vectors.extend(records)

    save_vectors(vectors)


def get_all_vectors() -> list[dict]:
    """
    Return all stored vector records.
    """

    return load_vectors()

def clear_vectors() -> None:
    """
    Delete all stored vectors.
    """

    save_vectors([])


if __name__ == "__main__":

    from app.services.chunking import chunk_text
    from app.services.embedding import embed_text

    sample_text = """
    Citizens must submit the application form.
    Proof of address is required.
    The citizen must also provide supporting documents.
    Applications should be submitted to the appropriate department.
    """

    chunks = chunk_text(sample_text)

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):

        vector = embed_text(chunk)

        add_vector(
            chunk_text=chunk,
            vector=vector,
            document_id=1,
            department_id=1,
            service_id=1,
            metadata={
                "page": 1,
                "source": "sample_guideline.txt",
                "chunk_number": i
            }
        )

        print(f"Stored chunk {i}")
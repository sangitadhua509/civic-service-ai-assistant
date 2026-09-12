def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:
    """
    Split extracted document text into smaller overlapping chunks.

    chunk_size = maximum number of words in one chunk
    overlap = number of words shared between consecutive chunks
    """

    words = text.split()

    if not words:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks



if __name__ == "__main__":

    sample_text = """
    Citizens must submit the application form.
    Proof of address is required.
    The citizen must also provide supporting documents.
    Applications should be submitted to the appropriate department.
    """

    chunks = chunk_text(
        sample_text,
        chunk_size=10,
        overlap=3
    )

    for i, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {i}:")
        print(chunk)
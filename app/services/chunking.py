def chunk_text(text: str, chunk_size: int = 500, overlap:     int = 50) -> list[str]:
    words = text.split()

    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1

        if current_length + word_length > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))

            overlap_words = []
            overlap_length = 0

            for previous_word in reversed(current_chunk):
                if overlap_length + len(previous_word) + 1 > overlap:
                    break

                overlap_words.insert(0, previous_word)
                overlap_length += len(previous_word) + 1

            current_chunk = overlap_words
            current_length = sum(len(w) + 1 for w in current_chunk)

        current_chunk.append(word)
        current_length += word_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

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
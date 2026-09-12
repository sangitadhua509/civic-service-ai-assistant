import hashlib
import re
from collections import Counter


VECTOR_SIZE = 128


def tokenize(text: str) -> list[str]:
    """
    Convert text into lowercase words.
    """

    return re.findall(r"\b\w+\b", text.lower())


def embed_text(text: str) -> list[float]:
    """
    Create a lightweight fixed-size embedding.

    This is a simple hashing-based embedding:
    1. Tokenize text
    2. Count word frequencies
    3. Hash each word into a fixed vector position

    Note:
    This is used for this student project as a lightweight,
    explainable alternative to a neural embedding API.
    It can later be replaced with a real embedding model.
    """

    tokens = tokenize(text)

    frequencies = Counter(tokens)

    vector = [0.0] * VECTOR_SIZE

    for word, frequency in frequencies.items():

        hash_value = int(
            hashlib.md5(word.encode("utf-8")).hexdigest(),
            16
        )

        index = hash_value % VECTOR_SIZE

        vector[index] += frequency

    return vector




if __name__ == "__main__":

    sample_text = """
    Birth certificate application requires proof of address.
    Birth certificate documents must be submitted.
    """

    vector = embed_text(sample_text)

    print("Vector size:", len(vector))
    print("Vector:", vector)
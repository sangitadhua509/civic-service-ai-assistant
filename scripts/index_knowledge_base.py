import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path

from app.services.document_loader import extract_text
from app.services.chunking import chunk_text
from app.services.embedding import embed_text
from app.services.vector_store import add_vectors, clear_vectors


KNOWLEDGE_BASE_DIR = Path("data/knowledge_base")


def index_knowledge_base():
    clear_vectors()

    records = []

    for file_path in KNOWLEDGE_BASE_DIR.iterdir():
        if file_path.suffix.lower() not in {".pdf", ".docx", ".txt", ".md"}:
            continue

        file_type = file_path.suffix.lower().lstrip(".")
        text = extract_text(str(file_path), file_type)

        chunks = chunk_text(text)

        for chunk_number, chunk in enumerate(chunks, start=1):
            vector = embed_text(chunk)

            records.append({
                "chunk_text": chunk,
                "vector": vector,
                "document_id": 1,
                "department_id": 1,
                "service_id": 1,
                "metadata": {
                    "source": file_path.name,
                    "page": "N/A",
                    "chunk_number": chunk_number
                }
            })

    add_vectors(records)

    print(f"Indexed {len(records)} chunks.")


if __name__ == "__main__":
    index_knowledge_base()
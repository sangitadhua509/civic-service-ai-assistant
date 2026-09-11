"""
Each file type needs a completely different approach to get plain
text out of it:

  PDF  -> pypdf reads the file page by page; we join every page's
          text together with a blank line between them.
  DOCX -> python-docx reads Word's internal XML structure and gives
          us a list of paragraph objects; we join their text.
  TXT / MD -> these are ALREADY plain text — "extraction" is just
          reading the file with the right encoding. Markdown's
          symbols (#, *, etc.) are left in as-is; they don't hurt
          embeddings later and stripping them isn't necessary here.

`extract_text()` is the single entry point the upload endpoint calls
— it looks at the file extension and picks the right function, so the
endpoint code doesn't need to know these details at all.
"""

from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages_text = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages_text).strip()


def extract_text_from_docx(file_path: str) -> str:
    document = Document(file_path)
    paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs).strip()


def extract_text_from_plain_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read().strip()


def extract_text(file_path: str, file_type: str) -> str:
    """
    Raises whatever exception the underlying library raises (a
    corrupted PDF, an unreadable file, etc.) — the caller in
    app/api/documents.py catches this and records it as a "failed"
    processing_status instead of crashing the whole request.
    """
    extractors = {
        "pdf": extract_text_from_pdf,
        "docx": extract_text_from_docx,
        "txt": extract_text_from_plain_file,
        "md": extract_text_from_plain_file,
    }
    extractor = extractors[file_type]
    return extractor(file_path)

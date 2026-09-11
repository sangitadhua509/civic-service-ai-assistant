"""
  POST   /documents/upload   -> admin/officer uploads a file, we extract its text
  GET    /documents           -> admin/officer lists all documents (optional filters)
  GET    /documents/{id}      -> admin/officer sees full extracted text
  DELETE /documents/{id}      -> admin only, removes both the DB row and the file

File uploads in FastAPI use `UploadFile` (the file itself) alongside
`Form(...)` fields (any other regular form data sent in the same
request) — this is different from JSON endpoints because browsers
send files as "multipart/form-data", not JSON.
"""

import os
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.db.models.user import User
from app.db.models.knowledge_document import KnowledgeDocument
from app.schemas.document import DocumentOut, DocumentDetailOut
from app.api.deps import get_current_user, require_roles
from app.services.document_loader import extract_text

router = APIRouter(prefix="/documents", tags=["Documents"])

ALLOWED_FILE_TYPES = {"pdf", "docx", "txt", "md"}
STORAGE_DIR = "data/storage"
PREVIEW_LENGTH = 300


def _to_document_out(doc: KnowledgeDocument) -> DocumentOut:
    preview = doc.extracted_text[:PREVIEW_LENGTH] if doc.extracted_text else None
    return DocumentOut(
        id=doc.id,
        title=doc.title,
        original_filename=doc.original_filename,
        file_type=doc.file_type,
        department_id=doc.department_id,
        service_id=doc.service_id,
        uploaded_by=doc.uploaded_by,
        processing_status=doc.processing_status,
        processing_error=doc.processing_error,
        created_at=doc.created_at,
        text_preview=preview,
    )


@router.post(
    "/upload",
    response_model=DocumentOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin", "officer"))],
)
def upload_document(
    title: str = Form(...),
    department_id: int | None = Form(default=None),
    service_id: int | None = Form(default=None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    original_filename = file.filename or "upload"
    extension = original_filename.rsplit(".", 1)[-1].lower() if "." in original_filename else ""

    if extension not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '.{extension}'. Allowed: {sorted(ALLOWED_FILE_TYPES)}",
        )

    # Save with a random filename on disk (never trust the original
    # filename for the actual storage path — two people could upload
    # files named "guidelines.pdf" and we'd overwrite one with the other).
    os.makedirs(STORAGE_DIR, exist_ok=True)
    stored_filename = f"{uuid.uuid4().hex}.{extension}"
    stored_path = os.path.join(STORAGE_DIR, stored_filename)

    contents = file.file.read()
    with open(stored_path, "wb") as f:
        f.write(contents)

    document = KnowledgeDocument(
        title=title,
        original_filename=original_filename,
        stored_path=stored_path,
        file_type=extension,
        department_id=department_id,
        service_id=service_id,
        uploaded_by=current_user.id,
        processing_status="uploaded",
    )
    db.add(document)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        os.remove(stored_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid department_id or service_id",
        )
    db.refresh(document)

    # Extraction happens right after upload, synchronously. A larger
    # production system might do this in a background job — for this
    # project's scale (small fictional sample documents), doing it
    # immediately keeps the code simple and the result is instant.
    try:
        text = extract_text(stored_path, extension)
        document.extracted_text = text
        document.processing_status = "extracted"
    except Exception as e:
        document.processing_status = "failed"
        document.processing_error = str(e)[:500]

    db.commit()
    db.refresh(document)
    return _to_document_out(document)


@router.get("", response_model=list[DocumentOut], dependencies=[Depends(require_roles("admin", "officer"))])
def list_documents(
    department_id: int | None = None,
    service_id: int | None = None,
    status_filter: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(KnowledgeDocument)
    if department_id is not None:
        query = query.filter(KnowledgeDocument.department_id == department_id)
    if service_id is not None:
        query = query.filter(KnowledgeDocument.service_id == service_id)
    if status_filter is not None:
        query = query.filter(KnowledgeDocument.processing_status == status_filter)
    return [_to_document_out(doc) for doc in query.all()]


@router.get(
    "/{document_id}",
    response_model=DocumentDetailOut,
    dependencies=[Depends(require_roles("admin", "officer"))],
)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.get(KnowledgeDocument, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    base = _to_document_out(document)
    return DocumentDetailOut(**base.model_dump(), extracted_text=document.extracted_text)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles("admin"))],
)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = db.get(KnowledgeDocument, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    if os.path.exists(document.stored_path):
        os.remove(document.stored_path)

    db.delete(document)
    db.commit()
    return None

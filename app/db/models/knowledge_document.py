"""
KnowledgeDocument = one uploaded guideline/FAQ/notice file, plus
everything we know about it: where it's stored, what type it is,
whether text extraction succeeded, and the extracted text itself.

`extracted_text` holds the FULL text pulled from the file — this is
what Phase 7's chunking step will read and split into pieces for the
vector store. We store it here rather than re-reading the file every
time, since extraction (especially PDF parsing) is slower than a
database read.

`processing_status` tracks the file's lifecycle:
  "uploaded"  -> file saved, extraction not attempted yet (transient)
  "extracted" -> text pulled out successfully, ready for Phase 7 indexing
  "failed"    -> extraction failed (see processing_error for why)

department_id/service_id are OPTIONAL — some documents are
department-wide (general FAQs), others apply to one specific service.
"""

from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(10), nullable=False)  # pdf / docx / txt / md

    department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id"), nullable=True)
    service_id: Mapped[int | None] = mapped_column(ForeignKey("services.id"), nullable=True)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    processing_status: Mapped[str] = mapped_column(String(20), default="uploaded", nullable=False)
    processing_error: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    department: Mapped["Department"] = relationship()
    service: Mapped["Service"] = relationship()
    uploader: Mapped["User"] = relationship()

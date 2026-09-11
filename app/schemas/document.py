"""
DocumentOut is deliberately LIGHTWEIGHT — it includes only a short
`text_preview` (first 300 characters), not the full extracted text.
A guideline PDF could have tens of thousands of characters; returning
that in every list item would make GET /documents slow and the
response huge. Use GET /documents/{id} to see the full extracted text
for one specific document when you actually need it.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    original_filename: str
    file_type: str
    department_id: Optional[int] = None
    service_id: Optional[int] = None
    uploaded_by: int
    processing_status: str
    processing_error: Optional[str] = None
    created_at: datetime
    text_preview: Optional[str] = None


class DocumentDetailOut(DocumentOut):
    extracted_text: Optional[str] = None

"""
Service = one item in a department's catalogue (e.g. "New Water Connection").

`requirements` is a free-form dictionary (JSON) because different services
need different things — some need 2 documents, some need 5, some have
extra eligibility rules. Instead of hard-coding fixed columns for every
possible requirement, we store it as flexible JSON. This is what the
brief calls a "JSONB required-document list."
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ServiceCreate(BaseModel):
    department_id: int
    name: str = Field(..., min_length=2, max_length=150, examples=["New Water Connection"])
    code: str = Field(..., min_length=2, max_length=30, examples=["WSD-NWC-01"])
    requirements: Dict[str, Any] = Field(
        default_factory=dict,
        examples=[{
            "documents": ["ID proof", "Address proof", "Property tax receipt"],
            "eligibility": "Applicant must be the property owner or a registered tenant",
        }],
    )
    status: str = Field(default="active", examples=["active"])


class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    requirements: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class ServiceOut(BaseModel):
    id: int
    department_id: int
    name: str
    code: str
    requirements: Dict[str, Any]
    status: str

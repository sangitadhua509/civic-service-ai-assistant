"""
ApplicationCreate -> what a citizen sends: which service, and their
answers to that service's required fields (payload). No citizen_id
here — same pattern as CitizenCreate, it's derived from the logged-in
user, never trusted from client input.

ApplicationStatusUpdate -> the ONLY way an officer changes an
application afterwards. Notice citizens can't use this endpoint at
all (enforced in the router) — they can view their application's
status, never set it themselves.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ApplicationCreate(BaseModel):
    service_id: int
    payload: Dict[str, Any] = Field(
        default_factory=dict,
        examples=[{"applicant_name": "Sangita Dhua", "property_id": "PROP-2201"}],
    )


class ApplicationStatusUpdate(BaseModel):
    status: str = Field(..., examples=["under_review"])


class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    citizen_id: int
    service_id: int
    reference_no: str
    payload: Dict[str, Any]
    status: str

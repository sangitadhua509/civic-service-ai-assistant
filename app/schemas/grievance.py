"""
GrievanceCreate -> what a citizen sends to file a complaint.

GrievanceRespond -> what an OFFICER sends: their written response AND
optionally a new status in the same request (e.g. respond + mark
resolved in one action). `status` is optional so an officer can leave
a response without necessarily changing status, or vice versa.
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class GrievanceCreate(BaseModel):
    department_id: int
    subject: str = Field(..., min_length=3, max_length=150, examples=["No water supply for 3 days"])
    details: str = Field(..., min_length=10, examples=["Our street has had no water since Monday morning."])


class GrievanceRespond(BaseModel):
    response: Optional[str] = Field(default=None, examples=["A technician has been dispatched to inspect the pipeline."])
    status: Optional[str] = Field(default=None, examples=["in_progress"])


class GrievanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    citizen_id: int
    department_id: int
    subject: str
    details: str
    status: str
    response: Optional[str] = None

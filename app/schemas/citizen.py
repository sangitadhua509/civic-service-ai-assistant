"""
Citizen = a profile belonging to a citizen-role user.

CitizenCreate no longer accepts `user_id` from the client. Before
Phase 4, anyone could create a citizen profile pointing at ANY user_id
— now that we have real logins, a citizen's profile is always linked
to WHOEVER IS LOGGED IN when they create it (see app/api/citizens.py).
This is what "ownership" means at the data level: the link is decided
by the server from the verified token, never trusted from client input.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class CitizenCreate(BaseModel):
    phone: str = Field(..., min_length=8, max_length=15, examples=["9876543210"])
    address: Dict[str, Any] = Field(
        default_factory=dict,
        examples=[{"line1": "12 MG Road", "city": "Kolkata", "pincode": "700001"}],
    )


class CitizenUpdate(BaseModel):
    phone: Optional[str] = Field(default=None, min_length=8, max_length=15)
    address: Optional[Dict[str, Any]] = None


class CitizenOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    phone: str
    address: Dict[str, Any]

"""
Citizen = a profile belonging to a citizen-role user.
`user_id` will really matter starting Phase 4 (auth) — a real citizen's
profile is tied to their logged-in account. For now we just accept it
as plain input.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class CitizenCreate(BaseModel):
    user_id: int
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

"""
What we send back describing a user. Notice `hashed_password` is
NOT here — even though it's on the database model, we must never let
it leak out in an API response, not even the hash.
"""

from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str
    is_active: bool

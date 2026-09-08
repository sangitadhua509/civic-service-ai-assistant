"""
UserRegister -> what a new citizen sends to sign up. Note there's no
"role" field here on purpose: self-registration always creates a
CITIZEN account. Admin and officer accounts are created separately
(for now, via the seed script) — a real system wouldn't let anyone
sign themselves up as an admin.

Token -> what we hand back after a successful login. `token_type` is
always "bearer" — that's just the standard name for "attach this
token in an Authorization: Bearer <token> header."
"""

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

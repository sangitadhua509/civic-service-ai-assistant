"""
Two separate jobs live in this file:

1. PASSWORD HASHING (hash_password / verify_password)
   We NEVER store a user's real password anywhere. Instead we run it
   through bcrypt, a one-way scrambling algorithm: easy to compute
   forward (turn a password into a hash), practically impossible to
   reverse (turn a hash back into the password). To check a login
   attempt, we hash the ATTEMPT and compare hashes — we never need to
   "unscramble" the stored one.

2. JWT ACCESS TOKENS (create_access_token / decode_access_token)
   After a successful login, instead of asking for the password again
   on every request, we hand the user a signed token containing their
   user id, role, and an expiry time. The token is signed with our
   secret key (JWT_SECRET_KEY in .env) — anyone can READ a JWT's
   contents (it's not encrypted), but nobody can FORGE or ALTER one
   without knowing our secret key, because the signature would no
   longer match.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(subject: str, role: str) -> str:
    """
    `subject` is the user's id (as a string) — the JWT standard calls
    this claim "sub". `role` gets embedded too, so every protected
    endpoint can check permissions WITHOUT hitting the database again
    just to find out who's asking.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Raises jwt.PyJWTError (caught by the caller) if the token is
    expired, malformed, or signed with a different secret key than
    ours (i.e. someone tried to fake one).
    """
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

"""
FastAPI "dependencies" are just functions that run automatically
before your endpoint code, and hand their return value to it as a
parameter. This file defines TWO dependencies every protected
endpoint will use:

1. get_current_user  -> reads the JWT from the request's
   Authorization header, verifies its signature, looks up the
   matching User row in the database, and returns it. If the token
   is missing, expired, or invalid, it raises 401 Unauthorized
   automatically — the endpoint code never even runs.

2. require_roles(...)  -> a "dependency factory": you call it with
   the roles you want to allow (e.g. require_roles("admin")), and it
   returns a NEW dependency that checks the current user's role and
   raises 403 Forbidden if they're not allowed. This is what turns
   "I know who you are" into "and here's what you're allowed to do."
"""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.user import User
from app.core.security import decode_access_token

# tokenUrl tells Swagger UI's "Authorize" button which endpoint to
# send username/password to, in order to fetch a token automatically.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_error
    except jwt.PyJWTError:
        raise credentials_error

    user = db.get(User, int(user_id))
    if user is None or not user.is_active:
        raise credentials_error
    return user


def require_roles(*allowed_roles: str):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of these roles: {', '.join(allowed_roles)}",
            )
        return current_user

    return role_checker


def get_current_citizen_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Applications and grievances belong to a CITIZEN profile, not
    directly to a User — so before a citizen can submit either one,
    they need to already have created their profile (Phase 4's
    POST /citizens). This dependency fetches that profile or raises a
    clear error telling them what to do instead of a confusing 500.
    """
    from app.db.models.citizen import Citizen  # local import avoids a circular import

    citizen = db.query(Citizen).filter(Citizen.user_id == current_user.id).first()
    if citizen is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Create your citizen profile first (POST /citizens) before applying for services.",
        )
    return citizen

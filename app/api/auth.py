"""
Three endpoints:

  POST /auth/register  -> create a new CITIZEN account (public, no login needed)
  POST /auth/login      -> exchange email+password for a JWT access token
  GET  /auth/me         -> "who am I?" — proves a token actually works

Login uses OAuth2PasswordRequestForm, which is FastAPI's standard
helper for "username + password" form data — we treat the "username"
field as the user's email. This exact shape is what makes Swagger
UI's green "Authorize" button work: paste in an email/password there,
and Swagger calls this endpoint for you and stores the resulting
token for every subsequent "Try it out" call.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.db.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import UserRegister, Token
from app.schemas.user import UserOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="citizen",  # self-registration is always a citizen account
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with that email already exists",
        )
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    # Deliberately vague error message — we don't tell an attacker
    # WHICH part was wrong (email not found vs wrong password). That
    # would let someone probe for which emails are registered.
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise invalid_credentials
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")

    access_token = create_access_token(subject=str(user.id), role=user.role)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

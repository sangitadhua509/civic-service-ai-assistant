"""
Citizen CRUD, now with real ownership enforcement — this is the
"citizen-only ownership checks" requirement from the brief, in its
simplest form.

The rule: a CITIZEN can only ever see/edit/delete THEIR OWN profile.
An ADMIN or OFFICER can see/manage any citizen's profile (they need
this to process applications and grievances). We enforce this with a
small helper, `ensure_can_access_citizen`, used in every endpoint that
takes a specific citizen_id.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.db.models.user import User
from app.db.models.citizen import Citizen
from app.schemas.citizen import CitizenCreate, CitizenUpdate, CitizenOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/citizens", tags=["Citizens"])


def ensure_can_access_citizen(citizen: Citizen, current_user: User) -> None:
    is_owner = citizen.user_id == current_user.id
    is_staff = current_user.role in ("admin", "officer")
    if not (is_owner or is_staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own citizen profile",
        )


@router.post("", response_model=CitizenOut, status_code=status.HTTP_201_CREATED)
def create_citizen(
    payload: CitizenCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # user_id is taken from the verified token, never from the request
    # body — this is what makes it impossible to create a profile
    # pretending to be someone else.
    citizen = Citizen(user_id=current_user.id, **payload.model_dump())
    db.add(citizen)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a citizen profile",
        )
    db.refresh(citizen)
    return citizen


@router.get("", response_model=list[CitizenOut])
def list_citizens(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Admin/officer see every citizen. A citizen sees only themselves —
    in practice this means the list has at most one item for them.
    """
    query = db.query(Citizen)
    if current_user.role == "citizen":
        query = query.filter(Citizen.user_id == current_user.id)
    return query.all()


@router.get("/{citizen_id}", response_model=CitizenOut)
def get_citizen(
    citizen_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    citizen = db.get(Citizen, citizen_id)
    if citizen is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Citizen not found")
    ensure_can_access_citizen(citizen, current_user)
    return citizen


@router.put("/{citizen_id}", response_model=CitizenOut)
def update_citizen(
    citizen_id: int,
    payload: CitizenUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    citizen = db.get(Citizen, citizen_id)
    if citizen is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Citizen not found")
    ensure_can_access_citizen(citizen, current_user)

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(citizen, field, value)

    db.commit()
    db.refresh(citizen)
    return citizen


@router.delete("/{citizen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_citizen(
    citizen_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    citizen = db.get(Citizen, citizen_id)
    if citizen is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Citizen not found")
    ensure_can_access_citizen(citizen, current_user)
    db.delete(citizen)
    db.commit()
    return None

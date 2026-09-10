"""
Endpoints for grievances. Same ownership shape as applications:
citizens submit and view their own; officers/admins see everything
and are the only ones who can respond or change status.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.db.models.user import User
from app.db.models.citizen import Citizen
from app.db.models.grievance import Grievance
from app.schemas.grievance import GrievanceCreate, GrievanceRespond, GrievanceOut
from app.api.deps import get_current_user, get_current_citizen_profile, require_roles
from app.services.workflow import validate_transition, GRIEVANCE_TRANSITIONS

router = APIRouter(prefix="/grievances", tags=["Grievances"])


def ensure_can_access_grievance(grievance: Grievance, citizen: Citizen | None, current_user: User) -> None:
    is_owner = citizen is not None and grievance.citizen_id == citizen.id
    is_staff = current_user.role in ("admin", "officer")
    if not (is_owner or is_staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own grievances",
        )


@router.post("", response_model=GrievanceOut, status_code=status.HTTP_201_CREATED)
def create_grievance(
    payload: GrievanceCreate,
    db: Session = Depends(get_db),
    citizen: Citizen = Depends(get_current_citizen_profile),
):
    grievance = Grievance(citizen_id=citizen.id, status="open", **payload.model_dump())
    db.add(grievance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid department_id")
    db.refresh(grievance)
    return grievance


@router.get("", response_model=list[GrievanceOut])
def list_grievances(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Grievance)
    if current_user.role == "citizen":
        citizen = db.query(Citizen).filter(Citizen.user_id == current_user.id).first()
        if citizen is None:
            return []
        query = query.filter(Grievance.citizen_id == citizen.id)
    return query.all()


@router.get("/{grievance_id}", response_model=GrievanceOut)
def get_grievance(
    grievance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    grievance = db.get(Grievance, grievance_id)
    if grievance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grievance not found")

    citizen = db.query(Citizen).filter(Citizen.user_id == current_user.id).first()
    ensure_can_access_grievance(grievance, citizen, current_user)
    return grievance


@router.patch(
    "/{grievance_id}/respond",
    response_model=GrievanceOut,
    dependencies=[Depends(require_roles("admin", "officer"))],
)
def respond_to_grievance(
    grievance_id: int,
    payload: GrievanceRespond,
    db: Session = Depends(get_db),
):
    grievance = db.get(Grievance, grievance_id)
    if grievance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grievance not found")

    if payload.status is not None:
        validate_transition(grievance.status, payload.status, GRIEVANCE_TRANSITIONS)
        grievance.status = payload.status
    if payload.response is not None:
        grievance.response = payload.response

    db.commit()
    db.refresh(grievance)
    return grievance

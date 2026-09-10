"""
Endpoints for service applications. Deliberately NO PUT (edit) or
DELETE — once submitted, an application isn't something a citizen
edits or removes; it only moves forward through status. That's why
there's a dedicated PATCH /status endpoint instead of a general
update endpoint.

  POST /applications           -> citizen submits (own profile only)
  GET  /applications           -> citizen sees own; staff sees all
  GET  /applications/{id}      -> ownership enforced
  PATCH /applications/{id}/status -> officer/admin only, controlled transitions
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.db.models.user import User
from app.db.models.citizen import Citizen
from app.db.models.service_application import ServiceApplication
from app.schemas.service_application import ApplicationCreate, ApplicationStatusUpdate, ApplicationOut
from app.api.deps import get_current_user, get_current_citizen_profile, require_roles
from app.services.reference_service import generate_reference_no
from app.services.workflow import validate_transition, APPLICATION_TRANSITIONS

router = APIRouter(prefix="/applications", tags=["Applications"])


def ensure_can_access_application(application: ServiceApplication, citizen: Citizen | None, current_user: User) -> None:
    is_owner = citizen is not None and application.citizen_id == citizen.id
    is_staff = current_user.role in ("admin", "officer")
    if not (is_owner or is_staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own applications",
        )


@router.post("", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    citizen: Citizen = Depends(get_current_citizen_profile),
):
    application = ServiceApplication(
        citizen_id=citizen.id,
        service_id=payload.service_id,
        payload=payload.payload,
        status="submitted",
        reference_no="PENDING",  # placeholder, replaced right after insert gives us a real id
    )
    db.add(application)
    try:
        db.flush()  # assigns application.id without fully committing yet
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid service_id")

    application.reference_no = generate_reference_no(application.id)
    db.commit()
    db.refresh(application)
    return application


@router.get("", response_model=list[ApplicationOut])
def list_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(ServiceApplication)
    if current_user.role == "citizen":
        citizen = db.query(Citizen).filter(Citizen.user_id == current_user.id).first()
        # No profile yet -> no applications possible; return an empty list
        # rather than an error, since this is a normal (not exceptional) state.
        if citizen is None:
            return []
        query = query.filter(ServiceApplication.citizen_id == citizen.id)
    return query.all()


@router.get("/reference/{reference_no}", response_model=ApplicationOut)
def get_application_by_reference(
    reference_no: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lets a citizen (or officer) look up an application by its
    human-readable reference number instead of the internal database
    id — this is what the brief calls "reference lookup" in the
    /applications module description.
    """
    application = db.query(ServiceApplication).filter(ServiceApplication.reference_no == reference_no).first()
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    citizen = db.query(Citizen).filter(Citizen.user_id == current_user.id).first()
    ensure_can_access_application(application, citizen, current_user)
    return application


@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = db.get(ServiceApplication, application_id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    citizen = db.query(Citizen).filter(Citizen.user_id == current_user.id).first()
    ensure_can_access_application(application, citizen, current_user)
    return application


@router.patch(
    "/{application_id}/status",
    response_model=ApplicationOut,
    dependencies=[Depends(require_roles("admin", "officer"))],
)
def update_application_status(
    application_id: int,
    payload: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
):
    application = db.get(ServiceApplication, application_id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    validate_transition(application.status, payload.status, APPLICATION_TRANSITIONS)
    application.status = payload.status
    db.commit()
    db.refresh(application)
    return application

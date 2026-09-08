"""
Same endpoints as Phase 3, now with role protection added:
GET endpoints (list/get one) stay PUBLIC — anyone browsing the civic
portal should be able to see what departments exist, even before
logging in. POST/PUT/DELETE now require an admin token, via
`Depends(require_roles("admin"))`. Notice we don't even need to USE
the returned user in most of these — just requiring the dependency to
succeed (or raise 403) is enough to protect the route.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.db.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentOut
from app.api.deps import require_roles

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post(
    "",
    response_model=DepartmentOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    department = Department(**payload.model_dump())
    db.add(department)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A department with that code already exists",
        )
    db.refresh(department)
    return department


@router.get("", response_model=list[DepartmentOut])
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()


@router.get("/{department_id}", response_model=DepartmentOut)
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = db.get(Department, department_id)
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return department


@router.put(
    "/{department_id}",
    response_model=DepartmentOut,
    dependencies=[Depends(require_roles("admin"))],
)
def update_department(department_id: int, payload: DepartmentUpdate, db: Session = Depends(get_db)):
    department = db.get(Department, department_id)
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(department, field, value)

    db.commit()
    db.refresh(department)
    return department


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles("admin"))],
)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = db.get(Department, department_id)
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    db.delete(department)
    db.commit()
    return None

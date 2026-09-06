"""
CRUD endpoints for Service (the service catalogue).

The one new idea here: a Service always belongs to a Department, so on
create we check that `department_id` actually exists first. This is a
simple version of what a real foreign key constraint in PostgreSQL will
enforce automatically starting Phase 3.
"""

from fastapi import APIRouter, HTTPException, status

from app.core import fake_db
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceOut

router = APIRouter(prefix="/services", tags=["Services"])


@router.post("", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
def create_service(payload: ServiceCreate):
    if payload.department_id not in fake_db.departments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department {payload.department_id} does not exist",
        )
    new_id = fake_db.next_service_id()
    record = {"id": new_id, **payload.model_dump()}
    fake_db.services[new_id] = record
    return record


@router.get("", response_model=list[ServiceOut])
def list_services(department_id: int | None = None):
    """
    Optional filter: GET /services?department_id=1
    This is the "search/filter services by department" extra feature
    from the brief, in its simplest possible form.
    """
    values = list(fake_db.services.values())
    if department_id is not None:
        values = [s for s in values if s["department_id"] == department_id]
    return values


@router.get("/{service_id}", response_model=ServiceOut)
def get_service(service_id: int):
    record = fake_db.services.get(service_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return record


@router.put("/{service_id}", response_model=ServiceOut)
def update_service(service_id: int, payload: ServiceUpdate):
    record = fake_db.services.get(service_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    updates = payload.model_dump(exclude_unset=True)
    record.update(updates)
    return record


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: int):
    if service_id not in fake_db.services:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    del fake_db.services[service_id]
    return None

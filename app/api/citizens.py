"""
CRUD endpoints for Citizen profiles.

Right now anyone can create/view/edit any citizen record — there's no
login system yet. From Phase 4 onwards, we'll lock this down so a
citizen can only ever see and edit THEIR OWN profile (the "ownership
check" the brief requires). For now, focus on the shape of the API.
"""

from fastapi import APIRouter, HTTPException, status

from app.core import fake_db
from app.schemas.citizen import CitizenCreate, CitizenUpdate, CitizenOut

router = APIRouter(prefix="/citizens", tags=["Citizens"])


@router.post("", response_model=CitizenOut, status_code=status.HTTP_201_CREATED)
def create_citizen(payload: CitizenCreate):
    new_id = fake_db.next_citizen_id()
    record = {"id": new_id, **payload.model_dump()}
    fake_db.citizens[new_id] = record
    return record


@router.get("", response_model=list[CitizenOut])
def list_citizens():
    return list(fake_db.citizens.values())


@router.get("/{citizen_id}", response_model=CitizenOut)
def get_citizen(citizen_id: int):
    record = fake_db.citizens.get(citizen_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Citizen not found")
    return record


@router.put("/{citizen_id}", response_model=CitizenOut)
def update_citizen(citizen_id: int, payload: CitizenUpdate):
    record = fake_db.citizens.get(citizen_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Citizen not found")
    updates = payload.model_dump(exclude_unset=True)
    record.update(updates)
    return record


@router.delete("/{citizen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_citizen(citizen_id: int):
    if citizen_id not in fake_db.citizens:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Citizen not found")
    del fake_db.citizens[citizen_id]
    return None

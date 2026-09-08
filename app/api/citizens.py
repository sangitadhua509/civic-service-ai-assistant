"""
Citizen CRUD, now backed by PostgreSQL.

Heads up: `user_id` is a real foreign key to the `users` table now.
Since we haven't built the register/login endpoints yet (that's
Phase 4), there won't be any real users to attach a citizen to unless
you run the seed script (scripts/seed_sample_data.py) first, which
creates a couple of placeholder users for testing.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.db.models.citizen import Citizen
from app.schemas.citizen import CitizenCreate, CitizenUpdate, CitizenOut

router = APIRouter(prefix="/citizens", tags=["Citizens"])


@router.post("", response_model=CitizenOut, status_code=status.HTTP_201_CREATED)
def create_citizen(payload: CitizenCreate, db: Session = Depends(get_db)):
    citizen = Citizen(**payload.model_dump())
    db.add(citizen)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id, or that user already has a citizen profile",
        )
    db.refresh(citizen)
    return citizen


@router.get("", response_model=list[CitizenOut])
def list_citizens(db: Session = Depends(get_db)):
    return db.query(Citizen).all()


@router.get("/{citizen_id}", response_model=CitizenOut)
def get_citizen(citizen_id: int, db: Session = Depends(get_db)):
    citizen = db.get(Citizen, citizen_id)
    if citizen is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Citizen not found")
    return citizen


@router.put("/{citizen_id}", response_model=CitizenOut)
def update_citizen(citizen_id: int, payload: CitizenUpdate, db: Session = Depends(get_db)):
    citizen = db.get(Citizen, citizen_id)
    if citizen is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Citizen not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(citizen, field, value)

    db.commit()
    db.refresh(citizen)
    return citizen


@router.delete("/{citizen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_citizen(citizen_id: int, db: Session = Depends(get_db)):
    citizen = db.get(Citizen, citizen_id)
    if citizen is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Citizen not found")
    db.delete(citizen)
    db.commit()
    return None

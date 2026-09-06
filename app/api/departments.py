"""
CRUD endpoints for Department.

Notice the pattern — every resource in this project will follow this
same shape:

  POST   /departments        -> create one
  GET    /departments        -> list all
  GET    /departments/{id}   -> get one specific one
  PUT    /departments/{id}   -> update one
  DELETE /departments/{id}   -> delete one

HTTP status codes we use on purpose (not random choices):
  200 OK           -> normal successful GET/PUT
  201 Created      -> successful POST (something new now exists)
  204 No Content   -> successful DELETE (nothing to return)
  404 Not Found    -> you asked for an id that doesn't exist
"""

from fastapi import APIRouter, HTTPException, status

from app.core import fake_db
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentOut

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(payload: DepartmentCreate):
    new_id = fake_db.next_department_id()
    record = {"id": new_id, **payload.model_dump()}
    fake_db.departments[new_id] = record
    return record


@router.get("", response_model=list[DepartmentOut])
def list_departments():
    return list(fake_db.departments.values())


@router.get("/{department_id}", response_model=DepartmentOut)
def get_department(department_id: int):
    record = fake_db.departments.get(department_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return record


@router.put("/{department_id}", response_model=DepartmentOut)
def update_department(department_id: int, payload: DepartmentUpdate):
    record = fake_db.departments.get(department_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    # Only overwrite fields the client actually sent (exclude_unset=True).
    # This is what makes PUT/PATCH-style partial updates work correctly.
    updates = payload.model_dump(exclude_unset=True)
    record.update(updates)
    return record


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int):
    if department_id not in fake_db.departments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    del fake_db.departments[department_id]
    return None

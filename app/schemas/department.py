"""
A "schema" is just a Python class that describes the SHAPE of data:
which fields exist, and what type each one must be.

We define THREE versions for Department, and you'll see this pattern
repeat for every entity in this project:

1. DepartmentCreate  -> what the CLIENT sends us when creating one
                         (no "id" yet, because we generate that)
2. DepartmentUpdate  -> what the client sends when editing one
                         (every field optional, since they might only
                         want to change one thing)
3. DepartmentOut     -> what WE send back to the client
                         (includes the generated "id")

Why not just use one schema for everything? Because the client should
never be allowed to invent their own "id" — that has to come from our
side. Separating "in" shapes from "out" shapes prevents that.
"""

from typing import Optional
from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120, examples=["Water Supply Department"])
    code: str = Field(..., min_length=2, max_length=20, examples=["WSD"])
    description: Optional[str] = Field(default=None, examples=["Handles water connections and complaints"])


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    code: Optional[str] = Field(default=None, min_length=2, max_length=20)
    description: Optional[str] = None


class DepartmentOut(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None

"""
Department = one public-service department (e.g. "Water Supply").
Straightforward table — the interesting part is the `relationship()`
at the bottom: it lets us write `some_department.services` in Python
and get a list of every Service that belongs to it, without writing
any SQL ourselves.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    services: Mapped[list["Service"]] = relationship(back_populates="department")

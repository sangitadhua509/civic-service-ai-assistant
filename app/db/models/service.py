"""
Service = one entry in a department's catalogue.

`requirements` uses PostgreSQL's JSONB column type — this is what the
brief specifically asks for ("JSONB required-document list"). JSONB
lets us store flexible, nested data (a list of documents, eligibility
notes, whatever a given service needs) in ONE column instead of
inventing a rigid fixed set of columns that wouldn't fit every service.

`department_id` is a FOREIGN KEY — PostgreSQL itself will now REFUSE
to let you create a Service pointing at a department_id that doesn't
exist. This replaces the manual "if department not in fake_db..."
check we wrote by hand in Phase 2 — the database enforces it for us.
"""

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    requirements: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(20), default="active")

    department: Mapped["Department"] = relationship(back_populates="services")

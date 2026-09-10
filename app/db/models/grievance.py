"""
Grievance = a citizen's complaint against a department. Simpler than
ServiceApplication — no reference number required by the brief, just
a subject/details from the citizen and, eventually, a response and
status update from an officer.
"""

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Grievance(Base):
    __tablename__ = "grievances"

    id: Mapped[int] = mapped_column(primary_key=True)
    citizen_id: Mapped[int] = mapped_column(ForeignKey("citizens.id"), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    subject: Mapped[str] = mapped_column(String(150), nullable=False)
    details: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False)
    response: Mapped[str | None] = mapped_column(Text, nullable=True)

    citizen: Mapped["Citizen"] = relationship()
    department: Mapped["Department"] = relationship()

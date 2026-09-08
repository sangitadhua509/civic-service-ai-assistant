"""
Citizen = the profile data for a citizen-role user. Linked 1-to-1 with
a User row via `user_id`. `address` is JSONB for the same reason as
Service.requirements — addresses have variable structure (line1,
line2, city, pincode, etc.) and JSONB stores that flexibly.
"""

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Citizen(Base):
    __tablename__ = "citizens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    address: Mapped[dict] = mapped_column(JSONB, default=dict)

    user: Mapped["User"] = relationship(back_populates="citizen_profile")

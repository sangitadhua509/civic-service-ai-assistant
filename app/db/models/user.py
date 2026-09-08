"""
User = one login account. Every person who can log in (admin,
department officer, or citizen) has exactly one row here.

We're defining the TABLE now, but we won't build the actual
register/login endpoints until Phase 4 — this just makes sure the
table (and its `id`) exists so Citizen can reference it.

`role` is a plain string for now ("admin" / "officer" / "citizen").
Phase 4 will use this field to decide what each user is allowed to do.
"""

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="citizen")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # This lets us write `some_user.citizen_profile` in Python and get
    # their linked Citizen row automatically — SQLAlchemy handles the
    # JOIN behind the scenes.
    citizen_profile: Mapped["Citizen"] = relationship(back_populates="user", uselist=False)

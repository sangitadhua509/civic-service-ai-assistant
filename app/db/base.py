"""
`Base` is the parent class every table model inherits from — it's what
lets SQLAlchemy turn a Python class into a real database table.

WHY THIS FILE IMPORTS EVERY MODEL:
Alembic (our migration tool) looks at `Base.metadata` to figure out
what tables SHOULD exist, then compares that to what tables ACTUALLY
exist in the database, and generates the SQL to fix the difference.
But that only works if every model file has actually been imported
somewhere — Python doesn't know a class exists until its file is
executed at least once. So every time we add a new model file, we add
one import line here.
"""

from app.db.base_class import Base  # noqa: F401

# Import every model below so Alembic (and SQLAlchemy) knows about it.
from app.db.models.user import User  # noqa: F401
from app.db.models.department import Department  # noqa: F401
from app.db.models.service import Service  # noqa: F401
from app.db.models.citizen import Citizen  # noqa: F401
from app.db.models.service_application import ServiceApplication  # noqa: F401
from app.db.models.grievance import Grievance  # noqa: F401

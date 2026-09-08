"""
Separate tiny file just for the `Base` class itself, kept apart from
base.py's imports. This avoids a "circular import" problem: model
files need to import `Base` from somewhere, but base.py imports the
model files — if Base lived in base.py too, that would be a loop.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

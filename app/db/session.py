"""
This file sets up the connection between your Python code and the
actual PostgreSQL database running on your machine.

Three key ideas:

1. `engine` — the actual connection pool to PostgreSQL, built from
   your DATABASE_URL in .env.

2. `SessionLocal` — a "session" is one conversation with the database:
   you open it, do some queries/inserts, then close it. We create a
   NEW session for every single API request (see get_db() below) so
   requests never interfere with each other.

3. `get_db()` — a FastAPI "dependency". Any endpoint that needs
   database access will declare `db: Session = Depends(get_db)` as a
   parameter, and FastAPI will automatically: open a session, hand it
   to your function, then close it afterwards — even if your function
   raises an error. You never have to manually open/close a session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

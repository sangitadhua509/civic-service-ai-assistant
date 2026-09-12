"""
This is the entry point of the whole backend.
Running `uvicorn app.main:app --reload` starts this file.

Each feature area (auth, departments, services, citizens,
applications, grievances) lives in its own router file under
app/api/, and gets plugged in below with one line each.
"""
from app.api.chat import router as chat_router
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging

# Import every SQLAlchemy model together, exactly once, before anything
# else touches the database. This guarantees relationships that refer
# to each other by name (e.g. User.citizen_profile -> "Citizen") can
# always be resolved, no matter which router file happens to run first.
import app.db.base  # noqa: F401

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.departments import router as departments_router
from app.api.services import router as services_router
from app.api.citizens import router as citizens_router
from app.api.applications import router as applications_router
from app.api.grievances import router as grievances_router
from app.api.documents import router as documents_router

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Civic Service, Application and Grievance Assistant (student capstone project)",
    version="0.6.0",
)

# Every router we add gets included here, one line each.
app.include_router(health_router, tags=["Health"])
app.include_router(auth_router)
app.include_router(departments_router)
app.include_router(services_router)
app.include_router(citizens_router)
app.include_router(applications_router)
app.include_router(grievances_router)
app.include_router(documents_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Civic Service AI Assistant API",
        "docs": "/docs",
    }

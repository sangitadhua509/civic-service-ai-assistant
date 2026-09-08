"""
This is the entry point of the whole backend.
Running `uvicorn app.main:app --reload` starts this file.

Right now it only wires up the health check. In later phases we will
add: /auth, /departments, /services, /citizens, /applications,
/grievances, /documents, /chat — each as its own router file, plugged
in here the same way health.router is plugged in below.
"""

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging

# Import every SQLAlchemy model together, exactly once, before anything
# else touches the database. This guarantees relationships that refer
# to each other by name (e.g. User.citizen_profile -> "Citizen") can
# always be resolved, no matter which router file happens to run first.
import app.db.base  # noqa: F401

from app.api.health import router as health_router
from app.api.departments import router as departments_router
from app.api.services import router as services_router
from app.api.citizens import router as citizens_router

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Civic Service, Application and Grievance Assistant (student capstone project)",
    version="0.2.0",
)

# Every router we add gets included here, one line each.
app.include_router(health_router, tags=["Health"])
app.include_router(departments_router)
app.include_router(services_router)
app.include_router(citizens_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Civic Service AI Assistant API",
        "docs": "/docs",
    }

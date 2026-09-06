"""
A "health check" endpoint. It doesn't do anything business-related —
its only job is to answer "yes, I am alive" so that:
- you can quickly confirm the server started correctly, and
- later (Docker, deployment tools) can automatically check if the
  app is still running.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok", "message": "Civic Service AI Assistant is running"}

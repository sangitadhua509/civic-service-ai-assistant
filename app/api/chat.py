from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import prepare_rag

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    query: str


@router.post("/")
def chat(request: ChatRequest):
    return prepare_rag(request.query)
from fastapi import APIRouter
from app.services.ollama_service import ollama_service
from app.core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health_check():
    return {
        "status": "healthy",
        "service": "Angkor Verse AI API",
        "ai_mode": settings.AI_MODE,
        "ollama_available": ollama_service.is_available()
    }

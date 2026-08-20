from fastapi import APIRouter
from app.services.ollama_service import ollama_service
from app.services.online.gemini_service import gemini_online_service
from app.core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health_check():
    gemini_ok = gemini_online_service.is_available()
    ollama_ok = ollama_service.is_available()
    active_mode = "online" if gemini_ok else ("offline" if ollama_ok else "degraded")
    return {
        "status": "healthy",
        "service": "Angkor Verse AI API",
        "ai_mode": settings.AI_MODE,
        "active_mode": active_mode,
        "gemini_available": gemini_ok,
        "ollama_available": ollama_ok
    }

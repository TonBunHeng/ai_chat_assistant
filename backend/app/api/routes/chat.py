from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.models.chat import ChatRequest
from app.models.response import StandardResponse, ChatResponseData
from app.services.rag_service import rag_service
from app.services.memory_service import memory_service
from app.utils.validators import validate_chat_message

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=StandardResponse[ChatResponseData])
def handle_chat_message(request: ChatRequest):
    validate_chat_message(request.message)
    try:
        result = rag_service.process_chat_message(
            message=request.message,
            session_id=request.session_id,
            preferred_language=request.language
        )
        return StandardResponse(
            success=True,
            data=ChatResponseData(**result)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions")
def get_chat_sessions():
    """List all active chat sessions."""
    sessions = memory_service.get_all_sessions()
    return {"success": True, "data": sessions}

@router.get("/sessions/{session_id}")
def get_chat_session(session_id: str):
    """Get message history for a specific session."""
    history = memory_service.get_history(session_id, limit=50)
    meta = memory_service.get_session_metadata(session_id)
    return {
        "success": True,
        "data": {
            "session_id": session_id,
            "messages": history,
            "metadata": meta
        }
    }

@router.delete("/sessions")
@router.delete("/sessions/all")
def clear_all_sessions():
    """Clear all chat sessions."""
    memory_service.delete_all_sessions()
    return {"success": True, "message": "All chat sessions cleared"}

@router.delete("/sessions/{session_id:path}")
@router.delete("/{session_id:path}")
def delete_chat_session(session_id: str):
    """Delete a specific chat session."""
    clean_id = session_id.strip()
    deleted = memory_service.delete_session(clean_id)
    return {"success": True, "deleted": deleted, "session_id": clean_id}

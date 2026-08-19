from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.models.chat import ChatRequest
from app.models.response import StandardResponse, ChatResponseData
from app.services.rag_service import rag_service
from app.services.memory_service import memory_service
from app.utils.validators import validate_chat_message

router = APIRouter(tags=["Chat"])

class TourismChatMessageRequest(BaseModel):
    message: Optional[str] = None
    message_text: Optional[str] = None
    language: Optional[str] = "en"
    session_id: Optional[str] = None

class TourismCreateChatRequest(BaseModel):
    category: Optional[str] = "General Inquiry"
    priority: Optional[str] = "medium"
    message: Optional[str] = ""
    message_text: Optional[str] = ""

@router.post("/chat", response_model=StandardResponse[ChatResponseData])
def handle_chat_message(request: ChatRequest):
    validate_chat_message(request.message)
    try:
        result = rag_service.process_chat_message(
            message=request.message,
            session_id=request.session_id,
            preferred_language=request.language,
            client_history=request.history
        )
        return StandardResponse(
            success=True,
            message="Message processed successfully.",
            data=ChatResponseData(**result)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/sessions")
@router.get("/chats")
@router.get("/travel/chats")
def get_chat_sessions():
    """List all active chat conversations."""
    sessions = memory_service.get_all_sessions()
    return {
        "success": True,
        "message": "Chat sessions retrieved successfully.",
        "data": sessions
    }

@router.post("/chats")
@router.post("/travel/chats")
def create_chat(payload: TourismCreateChatRequest):
    """Create new chat conversation matching tourism-backend-api format."""
    text = payload.message or payload.message_text or "New Conversation"
    result = rag_service.process_chat_message(
        message=text,
        preferred_language="en",
    )
    sid = result.get("session_id")
    return {
        "success": True,
        "message": "Support conversation started successfully.",
        "data": {
            "id": sid,
            "session_id": sid,
            "category": payload.category,
            "priority": payload.priority,
            "status": "active",
            "last_message": result.get("answer", ""),
            "answer": result.get("answer", "")
        }
    }

@router.get("/chat/sessions/{session_id}")
@router.get("/chats/{session_id}")
@router.get("/travel/chats/{session_id}")
def get_chat_session(session_id: str):
    """Get message history for a specific session."""
    history = memory_service.get_history(session_id, limit=50)
    meta = memory_service.get_session_metadata(session_id)
    return {
        "success": True,
        "message": "Chat conversation retrieved successfully.",
        "data": {
            "id": session_id,
            "session_id": session_id,
            "messages": history,
            "metadata": meta
        }
    }

@router.post("/chats/{session_id}/messages")
@router.post("/travel/chats/{session_id}/messages")
def send_chat_message_to_session(session_id: str, payload: TourismChatMessageRequest):
    """Send message to a specific conversation matching tourism-backend-api format."""
    text = payload.message or payload.message_text or ""
    validate_chat_message(text)
    try:
        result = rag_service.process_chat_message(
            message=text,
            session_id=session_id,
            preferred_language=payload.language or "en",
        )
        return {
            "success": True,
            "message": "Message sent successfully.",
            "data": {
                "id": session_id,
                "session_id": session_id,
                "sender_type": "ai",
                "message_text": result.get("answer", ""),
                "answer": result.get("answer", ""),
                "sources": result.get("sources", []),
                "suggestions": result.get("suggestions", []),
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/chat/sessions")
@router.delete("/chat/sessions/all")
@router.delete("/chats")
def clear_all_sessions():
    """Clear all chat sessions."""
    memory_service.delete_all_sessions()
    return {
        "success": True,
        "message": "All chat sessions cleared successfully.",
        "data": []
    }

@router.delete("/chat/sessions/{session_id:path}")
@router.delete("/chats/{session_id:path}")
def delete_chat_session(session_id: str):
    """Delete a specific chat session."""
    clean_id = session_id.strip()
    if clean_id.startswith("sessions/"):
        clean_id = clean_id.replace("sessions/", "", 1).strip()
    deleted = memory_service.delete_session(clean_id)
    return {
        "success": True,
        "message": "Chat session deleted successfully.",
        "deleted": deleted,
        "session_id": clean_id
    }

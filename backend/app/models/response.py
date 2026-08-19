from typing import Optional, List, Dict, Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class ChatResponseData(BaseModel):
    answer: str
    language: str = "km"
    intent: str = "general_tourism"
    confidence: float = 0.95
    sources: List[Dict[str, Any]] = []
    related_places: List[Dict[str, Any]] = []
    suggestions: List[str] = []
    session_id: Optional[str] = None
    is_matched: Optional[bool] = False
    similarity_score: Optional[float] = 0.0


class StandardResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Operation successful."
    data: Optional[T] = None
    error: Optional[str] = None
    errors: Optional[Any] = None

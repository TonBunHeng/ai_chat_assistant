from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of message sender: 'user' or 'assistant'")
    content: str = Field(..., description="Message text content")

class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None, description="Unique conversation session ID")
    message: str = Field(..., min_length=1, max_length=4000, description="User question or prompt")
    language: Optional[str] = Field(None, description="Preferred language code ('km', 'en', or 'km_en')")
    history: Optional[List[Dict[str, Any]]] = Field(None, description="Optional list of prior conversation messages")

class SearchQuery(BaseModel):
    query: str = Field(..., description="Search keyword or question")
    category: Optional[str] = Field(None, description="Filter category (e.g. 'Heritage', 'Beach', 'Food')")
    province: Optional[str] = Field(None, description="Filter province (e.g. 'Siem Reap')")
    limit: Optional[int] = Field(5, description="Number of results to return")

class SummaryRequest(BaseModel):
    topic: str = Field(..., description="Destination or topic to summarize")
    language: Optional[str] = Field("km", description="Target language ('km' or 'en')")

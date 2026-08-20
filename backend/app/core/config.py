import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # AI Mode & Orchestration ("auto", "online", "offline", "degraded")
    AI_MODE: str = "auto"
    
    # Online AI Provider Configuration (Gemini Only)
    ONLINE_AI_PROVIDER: str = "gemini"
    ONLINE_AI_MODEL: str = "gemini-2.5-flash"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    ONLINE_API_KEY: str = ""
    ONLINE_MODEL: str = "gemini-2.5-flash"
    
    # Offline AI Provider Configuration (Ollama)
    OFFLINE_AI_PROVIDER: str = "ollama"
    OFFLINE_AI_MODEL: str = "CamTour-On-Mistral-Ai:latest"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "CamTour-On-Mistral-Ai:latest"
    
    # External APIs (Optional - fallbacks always available)
    WEATHER_API_KEY: str = ""
    MAPS_API_KEY: str = ""
    
    # Matching Similarity Threshold (80%-90% match)
    SIMILARITY_THRESHOLD: float = 0.80
    
    # Recommendation Scoring Weights
    REC_WEIGHT_INTEREST: float = 0.30
    REC_WEIGHT_LOCATION: float = 0.15
    REC_WEIGHT_BUDGET: float = 0.15
    REC_WEIGHT_DURATION: float = 0.15
    REC_WEIGHT_WEATHER: float = 0.10
    REC_WEIGHT_POPULARITY: float = 0.10
    REC_WEIGHT_ACCESSIBILITY: float = 0.05
    
    # Cache TTL (in seconds)
    CACHE_TTL_WEATHER: int = 3600       # 1 hour
    CACHE_TTL_CURRENCY: int = 43200     # 12 hours
    CACHE_TTL_EVENTS: int = 86400       # 24 hours
    CACHE_TTL_RECOMMENDATIONS: int = 1800 # 30 mins
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://ai-chatbot-psi-sepia.vercel.app"
    ]
    
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    SQLITE_DB_PATH: str = "/tmp/conversations.db" if os.environ.get("VERCEL") else os.path.join(BASE_DIR, "storage/conversations/conversations.db")
    DATA_DIR: str = os.path.join(BASE_DIR, "data/tourism")
    VECTOR_DB_DIR: str = "/tmp/vector_db" if os.environ.get("VERCEL") else os.path.join(BASE_DIR, "storage/vector_db")
    
    MAX_HISTORY_MESSAGES: int = 10
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def effective_gemini_api_key(self) -> str:
        return self.GEMINI_API_KEY or self.ONLINE_API_KEY or os.environ.get("GEMINI_API_KEY", "") or os.environ.get("GOOGLE_API_KEY", "")

    @property
    def effective_online_model(self) -> str:
        return self.ONLINE_AI_MODEL or self.GEMINI_MODEL or "gemini-flash-latest"

    @property
    def effective_offline_model(self) -> str:
        return self.OFFLINE_AI_MODEL or self.OLLAMA_MODEL or "CamTour-On-Mistral-Ai:latest"

settings = Settings()



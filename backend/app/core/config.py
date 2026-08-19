import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    AI_MODE: str = "online"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "Camtour-On-Mistral-Ai:latest"
    ONLINE_API_KEY: str = ""
    ONLINE_MODEL: str = "gpt-3.5-turbo"
    
    # Google Gemini AI Configuration
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.6-flash"
    
    # Matching Similarity Threshold (80%-90% match)
    SIMILARITY_THRESHOLD: float = 0.80

    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000"
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

settings = Settings()



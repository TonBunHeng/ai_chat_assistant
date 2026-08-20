import requests
import json
from typing import List, Dict, Any, Optional
from app.core.config import settings

class OllamaOfflineService:
    def __init__(self, base_url: str = settings.OLLAMA_BASE_URL, model: str = settings.OLLAMA_MODEL):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def is_available(self) -> bool:
        """Check if local Ollama server is running."""
        try:
            res = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return res.status_code == 200
        except Exception:
            return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Optional[str]:
        """Generate response from Ollama using generate endpoint."""
        url = f"{self.base_url}/api/generate"
        model_name = settings.effective_offline_model
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        if system_prompt:
            payload["system"] = system_prompt
            
        try:
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            return None
        except Exception as e:
            print(f"OllamaOfflineService generate error: {e}")
            return None

    def chat(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> Optional[str]:
        """Generate response from Ollama using chat endpoint."""
        url = f"{self.base_url}/api/chat"
        model_name = settings.effective_offline_model
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
            
        for msg in messages:
            formatted_messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
            
        payload = {
            "model": model_name,
            "messages": formatted_messages,
            "stream": False,
            "options": {"num_predict": 1024}
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "")
            return None
        except Exception as e:
            print(f"OllamaOfflineService chat error: {e}")
            return None

ollama_offline_service = OllamaOfflineService()

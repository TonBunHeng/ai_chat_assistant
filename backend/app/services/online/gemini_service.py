import os
import requests
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.prompts import GEMINI_SYSTEM_INSTRUCTION

try:
    # pyrefly: ignore [missing-import]
    import google.genai as genai
    # pyrefly: ignore [missing-import]
    from google.genai import types
    HAS_GOOGLE_GENAI = True
except ImportError:
    HAS_GOOGLE_GENAI = False

class GeminiOnlineService:
    def __init__(self):
        self.client = None
        self._init_gemini_client()

    def _init_gemini_client(self):
        api_key = settings.effective_gemini_api_key
        if HAS_GOOGLE_GENAI and api_key:
            try:
                self.client = genai.Client(api_key=api_key)
            except Exception as e:
                print(f"GeminiOnlineService: Client init note: {e}")
                self.client = None

    def is_available(self) -> bool:
        """Check if Gemini API is configured with an API key."""
        return bool(settings.effective_gemini_api_key)

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
        """
        Generate response from Google Gemini API.
        Tries active models with fast failover on quota (429) or auth errors.
        """
        api_key = settings.effective_gemini_api_key.strip()
        if not api_key:
            return None

        sys_inst = system_instruction or GEMINI_SYSTEM_INSTRUCTION

        # Active Gemini models
        models_to_try = [
            settings.effective_online_model,
            "gemini-3.6-flash",
            "gemini-flash-latest"
        ]
        models_to_try = [m for m in list(dict.fromkeys(models_to_try)) if m]

        # 1. Direct REST API (Fastest and resilient with zero blocking sleep)
        for model in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "systemInstruction": {"parts": [{"text": sys_inst}]},
                    "generationConfig": {"temperature": 0.3, "maxOutputTokens": 800}
                }
                res = requests.post(url, json=payload, timeout=settings.GEMINI_TIMEOUT_SECONDS or 4)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        non_thought = [p.get("text", "") for p in parts if p.get("text") and not p.get("thought")]
                        texts = non_thought if non_thought else [p.get("text", "") for p in parts if p.get("text")]
                        if texts:
                            return "".join(texts).strip()
                elif res.status_code in [429, 401, 403]:
                    # Quota exhausted or invalid key: immediately return to trigger local fallback without sleeping
                    print(f"GeminiOnlineService: Quota/Auth issue ({res.status_code}), switching immediately to fallback.")
                    return None
            except Exception as ex:
                print(f"GeminiOnlineService REST note ({model}): {ex}")

        # 2. SDK Call fallback (only if not quota limited)
        if HAS_GOOGLE_GENAI and self.client:
            try:
                response = self.client.models.generate_content(
                    model=settings.effective_online_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=sys_inst,
                        temperature=0.3,
                        max_output_tokens=800,
                    )
                )
                if response and hasattr(response, 'text') and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"GeminiOnlineService SDK note: {e}")

        return None

gemini_online_service = GeminiOnlineService()

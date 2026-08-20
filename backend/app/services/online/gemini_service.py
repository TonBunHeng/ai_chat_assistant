import os
import requests
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.prompts import GEMINI_SYSTEM_INSTRUCTION

try:
    # pyrefly: ignore [missing-import]
    from google import genai
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
        Tries multiple active models in order of priority to ensure 100% online availability.
        """
        api_key = settings.effective_gemini_api_key.strip()
        if not api_key:
            return None

        sys_inst = system_instruction or GEMINI_SYSTEM_INSTRUCTION

        # Active Gemini models in order of priority
        models_to_try = [
            settings.effective_online_model,
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-2.5-pro",
            "gemini-1.5-pro",
            "gemini-flash-latest"
        ]
        models_to_try = [m for m in list(dict.fromkeys(models_to_try)) if m]

        # 1. Try SDK Call
        if HAS_GOOGLE_GENAI:
            for model_name in models_to_try:
                try:
                    if not self.client:
                        self._init_gemini_client()
                    if self.client:
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=sys_inst,
                                temperature=0.3,
                                max_output_tokens=600,
                            )
                        )
                        if response:
                            if hasattr(response, 'text') and response.text:
                                return response.text.strip()
                            if hasattr(response, 'candidates') and response.candidates:
                                parts_text = [
                                    part.text for part in response.candidates[0].content.parts
                                    if hasattr(part, 'text') and part.text
                                ]
                                if parts_text:
                                    return "".join(parts_text).strip()
                except Exception as e:
                    print(f"GeminiOnlineService SDK note ({model_name}): {e}")

        # 2. REST API Fallback
        for model in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "systemInstruction": {"parts": [{"text": sys_inst}]},
                    "generationConfig": {"temperature": 0.3, "maxOutputTokens": 600}
                }
                res = requests.post(url, json=payload, timeout=6)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        texts = [p.get("text", "") for p in parts if p.get("text")]
                        if texts:
                            return "".join(texts).strip()
            except Exception as ex:
                print(f"GeminiOnlineService REST note ({model}): {ex}")

        return None

gemini_online_service = GeminiOnlineService()

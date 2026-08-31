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
        self.last_used_model = settings.effective_online_model
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

    def generate_with_model(self, prompt: str, system_instruction: Optional[str] = None) -> Optional[Dict[str, str]]:
        """
        Generate response from Google Gemini API and return {'text': str, 'model': str}.
        Tries high-speed active models with fast failover across all candidate models.
        """
        api_key = settings.effective_gemini_api_key.strip()
        if not api_key:
            return None

        sys_inst = system_instruction or GEMINI_SYSTEM_INSTRUCTION

        # Active high-availability Gemini models ordered for speed & quota resilience
        models_to_try = [
            settings.effective_online_model,
            "gemini-flash-lite-latest",
            "gemini-3.5-flash-lite",
            "gemini-3.6-flash",
            "gemini-3.5-flash",
            "gemini-flash-latest",
            "gemini-3.7-flash",
            "gemini-2.5-flash",
        ]
        # Deduplicate while preserving priority order
        seen = set()
        models_to_try = [m for m in models_to_try if m and not (m in seen or seen.add(m))]

        per_model_timeout = min(max(settings.GEMINI_TIMEOUT_SECONDS, 4), 8)

        # 1. Direct REST API (Fastest with seamless model failover)
        for model in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "systemInstruction": {"parts": [{"text": sys_inst}]},
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 800
                    }
                }
                res = requests.post(url, json=payload, timeout=per_model_timeout)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        non_thought = [p.get("text", "") for p in parts if p.get("text") and not p.get("thought")]
                        texts = non_thought if non_thought else [p.get("text", "") for p in parts if p.get("text")]
                        if texts:
                            ans = "".join(texts).strip()
                            if len(ans) > 5:
                                self.last_used_model = model
                                return {"text": ans, "model": model}
                elif res.status_code in [429, 404, 400]:
                    # Model quota exhausted or not found for this version: proceed to next candidate
                    print(f"GeminiOnlineService: Model {model} status {res.status_code}, trying next model...")
                    continue
                elif res.status_code in [401, 403]:
                    print(f"GeminiOnlineService: Auth error ({res.status_code}) on key.")
                    return None
            except Exception as ex:
                print(f"GeminiOnlineService REST note ({model}): {ex}")
                continue

        # 2. SDK Call fallback
        if HAS_GOOGLE_GENAI and self.client:
            for sdk_model in ["gemini-flash-lite-latest", "gemini-3.5-flash-lite", settings.effective_online_model]:
                try:
                    response = self.client.models.generate_content(
                        model=sdk_model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=sys_inst,
                            temperature=0.3,
                            max_output_tokens=800,
                        )
                    )
                    if response and hasattr(response, 'text') and response.text:
                        self.last_used_model = sdk_model
                        return {"text": response.text.strip(), "model": sdk_model}
                except Exception as e:
                    print(f"GeminiOnlineService SDK note ({sdk_model}): {e}")
                    continue

        return None

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
        """Backwards-compatible generate method returning plain text."""
        res = self.generate_with_model(prompt, system_instruction)
        return res["text"] if res else None

gemini_online_service = GeminiOnlineService()

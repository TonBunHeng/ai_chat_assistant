import os
import requests
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.prompts import GEMINI_SYSTEM_INSTRUCTION
from app.services.ollama_service import ollama_service
from app.utils.text_utils import is_khmer_text

try:
    # pyrefly: ignore [missing-import]
    from google import genai
    # pyrefly: ignore [missing-import]
    from google.genai import types
    HAS_GOOGLE_GENAI = True
except ImportError:
    HAS_GOOGLE_GENAI = False

class AIService:
    def __init__(self):
        self.client = None
        self._init_gemini_client()

    def _init_gemini_client(self):
        api_key = settings.effective_gemini_api_key
        if HAS_GOOGLE_GENAI and api_key:
            try:
                self.client = genai.Client(api_key=api_key)
            except Exception as e:
                print(f"AIService: Failed to initialize Gemini client: {e}")
                self.client = None

    def generate_response(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        context: Optional[str] = None,
        is_matched: bool = False
    ) -> str:
        """
        Generate natural, conversational AI response using Google Gemini AI model.
        - If is_matched=True (80-90%+ similarity match), instructs Gemini to use context as absolute ground truth.
        - If is_matched=False (no match), instructs Gemini to answer dynamically using general knowledge.
        """
        system_instruction = GEMINI_SYSTEM_INSTRUCTION

        # Construct prompt content with conversation history & context
        prompt_parts = []

        if is_matched and context:
            prompt_parts.append(
                f"[MATCHED TOURISM DATASET CONTEXT (ABSOLUTE GROUND TRUTH - DO NOT DUMP RAW JSON)]:\n"
                f"{context}\n\n"
                f"Instruction: The user's question matched our local tourism record. "
                f"Use the above factual context as the absolute source of truth to formulate a natural, friendly, conversational response. "
                f"Do not output raw JSON or code keys."
            )
        else:
            prompt_parts.append(
                f"[DYNAMIC GENERAL KNOWLEDGE MODE]:\n"
                f"No exact match was found in our local database for this query. "
                f"Please answer dynamically using your comprehensive AI knowledge in a natural, helpful, conversational tone."
            )

        if conversation_history:
            history_str = "Conversation History:\n"
            for msg in conversation_history[-6:]:
                role = "User" if msg["role"] == "user" else "Assistant"
                history_str += f"{role}: {msg['content']}\n"
            prompt_parts.append(history_str)

        prompt_parts.append(f"Current User Question: {message}")
        user_prompt = "\n\n".join(prompt_parts)

        # 1. Try Primary: Google Gemini API via official SDK
        gemini_response = self._call_gemini_api(user_prompt, system_instruction)
        if gemini_response:
            return gemini_response

        # 2. Try Fallback: Ollama local model if active
        if ollama_service.is_available():
            formatted_messages = [{"role": msg["role"], "content": msg["content"]} for msg in conversation_history]
            formatted_messages.append({"role": "user", "content": user_prompt})
            ollama_resp = ollama_service.chat(formatted_messages, system_prompt=system_instruction)
            if ollama_resp:
                return ollama_resp

        # 3. Handle missing key / service unreachable gracefully (NO raw JSON dump)
        return self._generate_fallback_response(message, context, is_matched)

    def _call_gemini_api(self, prompt: str, system_instruction: str) -> Optional[str]:
        """Call Google Gemini API using google-genai SDK or HTTP endpoint."""
        api_key = settings.effective_gemini_api_key.strip()
        if not api_key:
            return None

        # Try SDK call
        if HAS_GOOGLE_GENAI:
            try:
                if not self.client:
                    self._init_gemini_client()
                if self.client:
                    model_name = settings.GEMINI_MODEL
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.3,
                            max_output_tokens=1024,
                        )
                    )
                    if response and response.text:
                        return response.text.strip()
            except Exception as e:
                print(f"Gemini SDK Call Note: {e}")

        # REST API fallback for Gemini if SDK fails or alternative model name
        for model in [settings.GEMINI_MODEL, "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "systemInstruction": {"parts": [{"text": system_instruction}]},
                    "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1024}
                }
                res = requests.post(url, json=payload, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "").strip()
                elif res.status_code in [400, 401, 403]:
                    # Auth or Invalid key error - don't retry all models
                    print(f"Gemini API returned status {res.status_code}: {res.text[:100]}")
                    break
            except Exception as ex:
                print(f"Gemini REST call failed for model {model}: {ex}")
                break

        return None

    def _generate_fallback_response(self, message: str, context: Optional[str], is_matched: bool) -> str:
        """Graceful conversational fallback if LLM service is offline or API key is not yet provided."""
        is_km = is_khmer_text(message)

        if context and context.strip():
            context_excerpt = "\n".join(context.splitlines()[:6])
            if is_km:
                return f"ព័ត៌មានទេសចរណ៍ដែលបានស្វែងរកឃើញ៖\n\n{context_excerpt}\n\nតើអ្នកមានសំណួរអ្វីបន្ថែមទៀតទេ?"
            else:
                return f"Here is the key Cambodia tourism information:\n\n{context_excerpt}\n\nDo you have any follow-up questions?"

        if is_km:
            return (
                "សូមអភ័យទោស! ប្រព័ន្ធ AI Gemini មិនទាន់ត្រូវបានភ្ជាប់ API Key ទេ។ "
                "សូមបំពេញ GEMINI_API_KEY នៅក្នុង backend/.env ដើម្បីប្រើប្រាស់ Gemini AI ពេញលេញ។"
            )
        else:
            return (
                "Welcome to Cambodia AI Tourism Assistant! "
                "Please configure your GEMINI_API_KEY in backend/.env to unlock full Google Gemini AI capabilities."
            )


ai_service = AIService()

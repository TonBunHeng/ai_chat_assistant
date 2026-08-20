from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.prompts import GEMINI_SYSTEM_INSTRUCTION
from app.services.online.gemini_service import gemini_online_service
from app.services.offline.ollama_service import ollama_offline_service
from app.services.offline.offline_knowledge_service import offline_knowledge_service
from app.utils.text_utils import is_khmer_text

class AIService:
    def generate_response(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        context: Optional[str] = None,
        is_matched: bool = False,
        real_time_data_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Orchestrate natural, conversational response across:
        1. Online Mode -> app.services.online.gemini_service
        2. Offline Mode -> app.services.offline.ollama_service
        3. Degraded Mode -> app.services.offline.offline_knowledge_service
        with strict language alignment (100% Khmer / 100% English).
        """
        is_km = is_khmer_text(message)
        system_instruction = GEMINI_SYSTEM_INSTRUCTION

        # Construct prompt content with conversation history & real-time context
        prompt_parts = []

        if real_time_data_text:
            prompt_parts.append(
                f"[VERIFIED REAL-TIME DATA / TOOL OUTPUT - ABSOLUTE GROUND TRUTH]:\n"
                f"{real_time_data_text}\n\n"
                f"Instruction: Use the above real-time data to answer accurately without inventing details."
            )

        if is_matched and context:
            prompt_parts.append(
                f"[MATCHED TOURISM DATASET CONTEXT (ABSOLUTE GROUND TRUTH)]:\n"
                f"{context}\n\n"
                f"Instruction: Formulate a natural, friendly, conversational response based on this verified record."
            )
        elif not real_time_data_text:
            prompt_parts.append(
                f"[GENERAL TOURISM KNOWLEDGE MODE]:\n"
                f"Answer concisely in a natural, helpful, conversational tone grounded in Cambodian geography and culture."
            )

        if is_km:
            prompt_parts.append("[LANGUAGE MANDATE: Respond 100% in Khmer (ភាសាខ្មែរ). Do not mix English prose.]")
        else:
            prompt_parts.append("[LANGUAGE MANDATE: Respond 100% in English.]")

        if conversation_history:
            history_str = "Conversation History:\n"
            for msg in conversation_history[-6:]:
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_str += f"{role}: {msg.get('content', '')}\n"
            prompt_parts.append(history_str)

        prompt_parts.append(f"Current User Question: {message}")
        user_prompt = "\n\n".join(prompt_parts)

        # 1. ONLINE MODE: Try Online Gemini Service (app.services.online.gemini_service)
        if settings.AI_MODE in ["online", "auto"] and gemini_online_service.is_available():
            gemini_response = gemini_online_service.generate(user_prompt, system_instruction)
            if gemini_response:
                return {
                    "answer": gemini_response,
                    "mode": "online",
                    "model": settings.effective_online_model,
                    "data_sources": ["gemini_api", "tourism_database"]
                }

        # 2. OFFLINE MODE: Try Local Ollama Service (app.services.offline.ollama_service)
        if ollama_offline_service.is_available():
            formatted_messages = [{"role": msg.get("role", "user"), "content": msg.get("content", "")} for msg in conversation_history]
            formatted_messages.append({"role": "user", "content": user_prompt})
            ollama_resp = ollama_offline_service.chat(formatted_messages, system_prompt=system_instruction)
            if ollama_resp:
                return {
                    "answer": ollama_resp,
                    "mode": "offline",
                    "model": settings.effective_offline_model,
                    "data_sources": ["local_ollama_model", "local_tourism_database"]
                }

        # 3. DEGRADED MODE: Offline Local Knowledge Synthesizer (app.services.offline.offline_knowledge_service)
        fallback_answer = offline_knowledge_service.synthesize_response(message, context or real_time_data_text, is_matched)
        return {
            "answer": fallback_answer,
            "mode": "degraded",
            "model": "local_knowledge_engine",
            "data_sources": ["cached_tourism_database", "local_knowledge_engine"]
        }

ai_service = AIService()

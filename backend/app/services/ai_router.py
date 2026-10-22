from typing import Dict, Any, List, Optional, Iterator
from app.core.config import settings
from app.services.online.gemini_service import gemini_online_service
from app.services.offline.ollama_service import ollama_offline_service
from app.services.offline.offline_knowledge_service import offline_knowledge_service

class AIRouter:
    def route_request(
        self,
        user_prompt: str,
        system_instruction: str,
        conversation_history: List[Dict[str, str]],
        intent: str = "general_qa",
        requires_real_time: bool = False,
        local_knowledge_sufficient: bool = False,
        raw_message: str = "",
        context_snippet: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Intelligent multi-criteria AI provider router:
        Evaluates availability, intent, real-time necessity, timeouts, and multi-tier fallback.
        1. Online: Google Gemini (gemini-2.5-flash / gemini-3.6-flash / gemini-flash)
        2. Offline: Ollama (Camtour-On-Mistral-Ai:latest)
        3. Degraded: Local Grounded Knowledge Engine
        """
        gemini_ready = gemini_online_service.is_available()
        ollama_ready = ollama_offline_service.is_available()

        # Preferred Mode Evaluation
        should_try_gemini = (settings.AI_MODE in ["online", "auto"]) and gemini_ready
        should_try_ollama = (settings.AI_MODE in ["offline", "auto"] or not gemini_ready) and ollama_ready

        # 1. Tier 1: Try Gemini Online Service
        if should_try_gemini:
            try:
                gemini_res = gemini_online_service.generate_with_model(
                    prompt=user_prompt,
                    system_instruction=system_instruction,
                    attachments=attachments
                )
                if gemini_res and gemini_res.get("text") and len(gemini_res["text"].strip()) > 3:
                    return {
                        "answer": gemini_res["text"].strip(),
                        "mode": "online",
                        "provider": "gemini",
                        "model": gemini_res.get("model", settings.effective_online_model),
                        "fallback_used": False
                    }
            except Exception as e:
                print(f"AIRouter: Gemini call failed ({e}), falling back to Ollama.")

        # 2. Tier 2: Try Ollama Offline LLM
        if should_try_ollama:
            try:
                formatted_messages = [
                    {"role": msg.get("role", "user"), "content": msg.get("content", "")}
                    for msg in conversation_history
                ]
                formatted_messages.append({"role": "user", "content": user_prompt})

                ollama_text = ollama_offline_service.chat(
                    messages=formatted_messages,
                    system_prompt=system_instruction
                )
                if ollama_text and len(ollama_text.strip()) > 5:
                    return {
                        "answer": ollama_text.strip(),
                        "mode": "offline",
                        "provider": "ollama",
                        "model": settings.effective_offline_model,
                        "fallback_used": True
                    }
            except Exception as e:
                print(f"AIRouter: Ollama call failed ({e}), falling back to Local Knowledge Engine.")

        # 3. Tier 3: Deterministic Local Grounded Knowledge Engine Fallback
        fallback_text = offline_knowledge_service.synthesize_response(
            message=raw_message,
            context=context_snippet,
            is_matched=bool(context_snippet)
        )
        return {
            "answer": fallback_text,
            "mode": "offline",
            "provider": "local_fallback",
            "model": "local_knowledge_engine",
            "fallback_used": True
        }

    def route_stream(
        self,
        user_prompt: str,
        system_instruction: str,
        conversation_history: List[Dict[str, str]],
        intent: str = "general_qa",
        raw_message: str = "",
        context_snippet: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Iterator[str]:
        """
        Yield streaming tokens/chunks for SSE streaming endpoint.
        """
        gemini_ready = gemini_online_service.is_available()
        should_try_gemini = (settings.AI_MODE in ["online", "auto"]) and gemini_ready

        if should_try_gemini:
            stream_gen = gemini_online_service.generate_stream(
                prompt=user_prompt,
                system_instruction=system_instruction,
                attachments=attachments
            )
            streamed_anything = False
            for chunk in stream_gen:
                if chunk:
                    streamed_anything = True
                    yield chunk
            if streamed_anything:
                return

        # Fallback to route_request and yield as single block
        res = self.route_request(
            user_prompt=user_prompt,
            system_instruction=system_instruction,
            conversation_history=conversation_history,
            intent=intent,
            raw_message=raw_message,
            context_snippet=context_snippet,
            attachments=attachments
        )
        yield res.get("answer", "")

ai_router = AIRouter()

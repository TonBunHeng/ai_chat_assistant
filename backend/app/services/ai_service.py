from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.prompts import GEMINI_SYSTEM_INSTRUCTION
from app.services.ai_router import ai_router
from app.services.language_service import language_service
from app.services.response_validation_service import response_validation_service
from app.services.confidence_service import confidence_service

class AIService:
    def generate_response(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        context: Optional[str] = None,
        is_matched: bool = False,
        real_time_data_text: Optional[str] = None,
        intent: str = "general_qa",
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate grounded, strictly bilingual AI response:
        1. Assembles structured ground truth prompts with real-time & RAG context.
        2. Routes to AI Router (Gemini -> Ollama -> Local Knowledge).
        3. Validates language and content via ResponseValidationService.
        4. Calculates multi-factor confidence via ConfidenceService.
        """
        detected_lang = language or language_service.detect_language(message)
        is_km = "km" in detected_lang or language_service.is_khmer(message)
        system_instruction = GEMINI_SYSTEM_INSTRUCTION

        # Construct prompt content with strict grounding
        prompt_parts = []

        if real_time_data_text:
            prompt_parts.append(
                f"[VERIFIED REAL-TIME DATA / TOOL OUTPUT - ABSOLUTE GROUND TRUTH]:\n"
                f"{real_time_data_text}\n\n"
                f"Instruction: Use the above real-time data to answer accurately without fabricating any details."
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

        # Language Mandate
        prompt_parts.append(language_service.get_system_language_mandate("km" if is_km else "en"))

        # Conversation History
        if conversation_history:
            history_str = "Conversation History:\n"
            for msg in conversation_history[-6:]:
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_str += f"{role}: {msg.get('content', '')}\n"
            prompt_parts.append(history_str)

        prompt_parts.append(f"Current User Question: {message}")
        user_prompt = "\n\n".join(prompt_parts)

        # Execute through AI Router
        route_result = ai_router.route_request(
            user_prompt=user_prompt,
            system_instruction=system_instruction,
            conversation_history=conversation_history,
            intent=intent,
            requires_real_time=bool(real_time_data_text),
            local_knowledge_sufficient=bool(is_matched and context),
            raw_message=message,
            context_snippet=context or real_time_data_text
        )

        raw_answer = route_result["answer"]

        # Validate response
        validation = response_validation_service.validate_response(
            answer=raw_answer,
            expected_language="km" if is_km else "en",
            intent=intent
        )
        final_answer = validation["sanitized_answer"]

        # Calculate confidence
        conf_eval = confidence_service.calculate_confidence(
            intent_confidence=0.95 if is_matched or real_time_data_text else 0.80,
            rag_similarity_score=0.90 if is_matched else 0.70,
            tool_executed=bool(real_time_data_text),
            tool_success=True,
            is_matched=is_matched,
            ai_provider_mode=route_result["mode"],
            has_entities=True
        )

        return {
            "answer": final_answer,
            "mode": route_result["mode"],
            "provider": route_result.get("provider", "gemini"),
            "model": route_result["model"],
            "confidence": conf_eval["overall_score"],
            "confidence_level": conf_eval["level"],
            "fallback_used": route_result.get("fallback_used", False),
            "data_sources": [f"{route_result['provider']}_ai", "cambodia_tourism_dataset"]
        }

ai_service = AIService()

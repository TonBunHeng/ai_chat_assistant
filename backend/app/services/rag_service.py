import json
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.services.language_service import language_service
from app.services.intent_service import intent_service
from app.services.memory_service import memory_service
from app.services.matching_service import matching_service
from app.services.ai_service import ai_service
from app.services.summary_service import summary_service

class RAGService:
    def process_chat_message(
        self,
        message: str,
        session_id: Optional[str] = None,
        preferred_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process Chat Message through Similarity Matching Layer + Google Gemini AI."""
        # 1. Session Setup
        sid = memory_service.get_or_create_session_id(session_id)
        
        # 2. Language Detection
        detected_lang = preferred_language or language_service.detect_language(message)
        
        # 3. Retrieve Conversation History & Metadata
        history = memory_service.get_history(sid)
        session_meta = memory_service.get_session_metadata(sid)
        
        # 4. Intent & Entity Understanding
        intent_info = intent_service.detect_intent(message, history)
        intent = intent_info["intent"]
        entities = intent_info["entities"]
        
        # Contextual resolution if follow-up
        active_destination = entities.get("destination") or session_meta.get("destination")
        if entities.get("destination"):
            memory_service.update_session_metadata(sid, destination=entities["destination"], language=detected_lang)
            
        # 5. Smart Similarity Matching Layer (80%-90%+ match threshold)
        match_result = matching_service.find_best_match(
            query=message,
            threshold=settings.SIMILARITY_THRESHOLD
        )
        
        is_matched = match_result["match_found"]
        similarity_score = match_result["similarity_score"]
        matched_item = match_result["matched_item"]
        context_snippet = match_result["formatted_snippet"]
        
        # 6. Special Itinerary Handling if intent is itinerary_planning
        if intent == "itinerary_planning" and active_destination:
            days = 3
            if entities.get("duration"):
                try:
                    num = [int(s) for s in entities["duration"].split() if s.isdigit()]
                    if num:
                        days = num[0]
                except Exception:
                    pass
            
            # Generate contextual prompt for the LLM to build a dynamic itinerary
            from app.services.tourism_service import tourism_service
            dest_items = tourism_service.find_items_by_province(active_destination)
            if not dest_items:
                dest_items = tourism_service.search_keyword(active_destination, limit=5)
                
            attraction_names = []
            for item in dest_items:
                name = item.get("name_km") if "km" in detected_lang and item.get("name_km") else item.get("name")
                if name and name not in attraction_names:
                    attraction_names.append(name)
                # Also add popular attractions if it's a destination summary
                if item.get("popular_attractions"):
                    attraction_names.extend(item["popular_attractions"])
            
            unique_attractions = list(dict.fromkeys(attraction_names))
            attractions_str = ", ".join(unique_attractions[:15]) if unique_attractions else active_destination
            
            itinerary_context = (
                f"User requested a {days}-day itinerary for {active_destination}. "
                f"Available attractions/places to include: {attractions_str}. "
                f"Please create a dynamic, day-by-day travel itinerary using these places."
            )
            
            answer = ai_service.generate_response(
                message=message,
                conversation_history=history,
                context=itinerary_context,
                is_matched=True
            )
        else:
            # 7. AI Generation using Google Gemini AI
            answer = ai_service.generate_response(
                message=message,
                conversation_history=history,
                context=context_snippet if is_matched else None,
                is_matched=is_matched
            )
            
        # 8. Save Conversation Memory
        memory_service.add_message(sid, "user", message, metadata={"intent": intent, "language": detected_lang})
        memory_service.add_message(sid, "assistant", answer, metadata={"is_matched": is_matched, "similarity_score": similarity_score})
        
        # 9. Related Places & Suggestions & Sources
        related_places = []
        sources = []
        if is_matched and matched_item:
            related_places = [
                {
                    "id": matched_item.get("id", "1"),
                    "name": matched_item.get("name") or matched_item.get("title"),
                    "name_km": matched_item.get("name_km"),
                    "province": matched_item.get("province") or matched_item.get("location"),
                    "category": matched_item.get("category")
                }
            ]
            sources = [
                {
                    "id": matched_item.get("id", "src_1"),
                    "name": matched_item.get("name") or matched_item.get("title"),
                    "category": matched_item.get("category", "Tourism Knowledge Base"),
                    "location": matched_item.get("province") or matched_item.get("location", ""),
                    "description": matched_item.get("description", ""),
                    "source_file": matched_item.get("_source_file", "local_json_dataset"),
                    "similarity_score": similarity_score
                }
            ]
        
        suggestions = self._generate_suggestions(intent, active_destination, detected_lang)

        return {
            "answer": answer,
            "language": detected_lang,
            "intent": intent,
            "confidence": intent_info.get("confidence", 0.9),
            "is_matched": is_matched,
            "similarity_score": similarity_score,
            "sources": sources,
            "related_places": related_places,
            "suggestions": suggestions,
            "session_id": sid
        }

    def _generate_suggestions(self, intent: str, destination: Optional[str], lang: str) -> List[str]:
        """Generate smart follow-up suggestions for the UI."""
        is_km = "km" in lang
        dest = destination or "សៀមរាប" if is_km else destination or "Siem Reap"
        
        if is_km:
            return [
                f"តើទៅ {dest} គួររៀបចំដំណើរកម្សាន្តប៉ុន្មានថ្ងៃ?",
                f"តើម្ហូបអាហារល្បីៗនៅ {dest} មានអ្វីខ្លះ?",
                "តើមធ្យោបាយធ្វើដំណើរណាដែលងាយស្រួលបំផុត?"
            ]
        else:
            return [
                f"What is the best 3-day itinerary for {dest}?",
                f"What local dishes should I try in {dest}?",
                "What is the best way to get around?"
            ]

rag_service = RAGService()

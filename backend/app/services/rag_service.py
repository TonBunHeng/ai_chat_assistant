import json
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.services.language_service import language_service
from app.services.intent_service import intent_service
from app.services.memory_service import memory_service
from app.services.matching_service import matching_service
from app.services.ai_service import ai_service
from app.services.weather_service import weather_service
from app.services.currency_service import currency_service
from app.services.events_service import events_service
from app.services.places_service import places_service
from app.services.recommendation_engine import recommendation_engine
from app.services.itinerary_engine import itinerary_engine

class RAGService:
    def process_chat_message(
        self,
        message: str,
        session_id: Optional[str] = None,
        preferred_language: Optional[str] = None,
        client_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Master AI Orchestrator:
        1. Language detection (Strict Khmer vs English).
        2. Intent & entity understanding.
        3. Real-Time Tool Execution (Weather, Currency, Events, Itinerary, Recommendations, Places).
        4. Grounded Context Construction (Zero hallucination).
        5. AI Generation via Gemini (Online) / Ollama (Offline) / Degraded Engine.
        6. Structured response synthesis without cluttered duplication.
        """
        # 1. Session Setup
        sid = memory_service.get_or_create_session_id(session_id)
        
        # 2. Strict Language Detection
        detected_lang = preferred_language or language_service.detect_language(message)
        is_km = "km" in detected_lang or any("\u1780" <= c <= "\u17ff" for c in message)
        
        # 3. Retrieve Conversation History & Sync Client History
        history = memory_service.get_history(sid)
        if (not history or len(history) < (len(client_history) if client_history else 0)) and client_history:
            formatted_history = []
            for item in client_history[-10:]:
                role = item.get("role") or item.get("sender") or "user"
                role = "assistant" if role in ["ai", "assistant", "bot"] else "user"
                content = item.get("content") or item.get("message") or ""
                if content:
                    formatted_history.append({"role": role, "content": str(content)})
            if formatted_history:
                history = formatted_history
        session_meta = memory_service.get_session_metadata(sid)
        
        # 4. Intent & Entity Understanding
        intent_info = intent_service.detect_intent(message, history)
        intent = intent_info["intent"]
        entities = intent_info["entities"]
        
        active_destination = entities.get("destination") or session_meta.get("destination") or "Siem Reap"
        if entities.get("destination"):
            memory_service.update_session_metadata(sid, destination=entities["destination"], language=detected_lang)

        # 5. Real-Time Tools Execution & Focused Context Assembly
        real_time_blocks = []
        data_sources_used = ["tourism_database"]
        
        weather_payload = None
        currency_payload = None
        events_payload = None
        itinerary_payload = None
        recommendations_payload = None
        sources = []
        related_places = []

        # Tool Selection Priority (Mutually exclusive primary widgets to avoid visual clutter)
        is_itinerary_query = (
            intent == "itinerary_planning" or 
            any(w in message.lower() for w in ["itinerary", "plan", "day 1", "day 2", "3-day", "4-day", "5-day", "គម្រោង", "ដំណើរកម្សាន្ត"])
        )
        is_weather_query = (
            intent == "weather_travel" or 
            any(w in message.lower() for w in ["weather", "rain", "temperature", "forecast", "អាកាសធាតុ", "ភ្លៀង"])
        )
        is_currency_query = (
            intent == "currency_conversion" or 
            any(c in message.lower() for c in ["riel", "khr", "exchange", "convert", "ប្តូរលុយ", "រៀល", "ដុល្លារ"])
        )
        is_recommend_query = (
            not is_itinerary_query and (
                intent == "recommendation" or 
                any(r in message.lower() for r in ["recommend", "where to go", "best places", "top places", "attractions", "គួរទៅណា", "កន្លែងណា"])
            )
        )

        # Tool A: Itinerary Planning Tool
        if is_itinerary_query:
            days = entities.get("duration_days", 3)
            budget = entities.get("budget_usd")
            itinerary_payload = itinerary_engine.generate_itinerary(
                destination=active_destination,
                days=days,
                budget_usd=budget,
                interests=entities.get("interests", ["culture", "history"]),
                language=detected_lang
            )
            data_sources_used.append("itinerary_engine")
            real_time_blocks.append(
                f"[OPTIMIZED ITINERARY PLAN: {itinerary_payload['title']}]:\n"
                f"- Destination: {itinerary_payload['destination']}\n"
                f"- Duration: {itinerary_payload['duration_days']} Days\n"
                f"- Estimated Budget: {itinerary_payload['formatted_total_budget']}"
            )

        # Tool B: Weather Tool
        if is_weather_query:
            weather_payload = weather_service.get_weather(active_destination, days=3)
            data_sources_used.append("weather_service")
            w_curr = weather_payload["current"]
            real_time_blocks.append(
                f"[REAL-TIME WEATHER FOR {weather_payload['province'].upper()}]:\n"
                f"- Temperature: {w_curr['temperature_c']}°C ({w_curr['temperature_f']}°F)\n"
                f"- Condition: {w_curr['condition']} ({w_curr['condition_km']})\n"
                f"- Rain Probability: {w_curr['rain_probability']}%\n"
                f"- Travel Suitability: {weather_payload['travel_suitability']}\n"
                f"- Travel Advice: {weather_payload['travel_advice_km'] if is_km else weather_payload['travel_advice_en']}"
            )

        # Tool C: Currency / Budget Tool
        if is_currency_query:
            currency_payload = currency_service.get_exchange_rate()
            data_sources_used.append("currency_service")
            real_time_blocks.append(
                f"[LIVE EXCHANGE RATE]:\n"
                f"- Base Rate: {currency_payload['formatted_rate']}\n"
                f"- Source: {currency_payload['source']}"
            )

        # Tool D: Recommendation Scoring Tool (Only if not already an itinerary query)
        if is_recommend_query:
            recommendations_payload = recommendation_engine.recommend(
                interests=entities.get("interests"),
                province=active_destination if active_destination != "Cambodia" else None,
                budget_usd=entities.get("budget_usd"),
                duration_days=entities.get("duration_days"),
                limit=3
            )
            if recommendations_payload:
                data_sources_used.append("recommendation_engine")
                rec_lines = [f"- {r['name']} ({r.get('province', '')}) [Match: {r['match_score']}%]: {r.get('description', '')} | Fee: {r.get('price', '')}" for r in recommendations_payload]
                real_time_blocks.append("[VERIFIED RECOMMENDATION ENGINE SUGGESTIONS]:\n" + "\n".join(rec_lines))

        # Tool E: Events & Festivals Tool
        if intent == "events_festivals" or any(e in message.lower() for e in ["event", "festival", "marathon", "បុណ្យ", "ពិធីបុណ្យ", "អុំទូក"]):
            events_data = events_service.search_events(query=message, province=active_destination)
            if events_data.get("events"):
                events_payload = events_data["events"]
                data_sources_used.append("events_service")
                evt_lines = [f"- {evt['name']}: {evt.get('typical_period', '')} in {evt.get('location', '')}. {evt.get('description', '')}" for evt in events_payload[:2]]
                real_time_blocks.append("[VERIFIED CAMBODIAN EVENTS & FESTIVALS]:\n" + "\n".join(evt_lines))

        # 6. Similarity Search against Local Database (only if no dedicated structured tool is active)
        match_result = matching_service.find_best_match(
            query=message,
            threshold=settings.SIMILARITY_THRESHOLD
        )
        is_matched = match_result["match_found"]
        similarity_score = match_result["similarity_score"]
        matched_item = match_result["matched_item"]
        context_snippet = match_result["formatted_snippet"]

        if matched_item and not itinerary_payload and not recommendations_payload:
            sources.append({
                "id": matched_item.get("id", "src_1"),
                "name": matched_item.get("name") or matched_item.get("title"),
                "category": matched_item.get("category", "Cambodia Tourism Record"),
                "location": matched_item.get("province") or matched_item.get("location", ""),
                "description": matched_item.get("description", ""),
                "entrance_fee": matched_item.get("price") or matched_item.get("entrance_fee"),
                "google_maps_url": f"https://www.google.com/maps/search/?api=1&query={matched_item.get('latitude')},{matched_item.get('longitude')}" if matched_item.get("latitude") else None,
                "verified_source": matched_item.get("verified_source", "Ministry of Tourism Cambodia")
            })

        # 7. Greeting Short-circuit
        if intent == "greeting":
            answer = (
                "សួស្តី! 🖐️ ខ្ញុំជា Angkor Verse AI ជំនួយការទេសចរណ៍ AI នៅកម្ពុជា។ តើខ្ញុំអាចជួយផ្ដល់ព័ត៌មានអំពីកន្លែងកម្សាន្ត ហាងអាហារ សណ្ឋាគារ ពិនិត្យអាកាសធាតុ ឬរៀបចំគម្រោងដើរលេងដល់អ្នកយ៉ាងដូចម្តេចដែរ?"
                if is_km
                else "Hello! 👋 Welcome to Cambodia! I'm Angkor Verse AI, your Smart Tourism Assistant. How can I help you explore attractions, local food, check live weather, or plan an itinerary today?"
            )
            ai_meta = {
                "mode": "online" if settings.effective_gemini_api_key else "offline",
                "model": settings.effective_online_model if settings.effective_gemini_api_key else settings.effective_offline_model,
                "data_sources": ["system_greeting"]
            }
        else:
            # 8. Run Central AI Orchestrator
            combined_real_time = "\n\n".join(real_time_blocks) if real_time_blocks else None
            ai_resp = ai_service.generate_response(
                message=message,
                conversation_history=history,
                context=context_snippet if is_matched else None,
                is_matched=is_matched,
                real_time_data_text=combined_real_time
            )
            answer = ai_resp["answer"]
            ai_meta = ai_resp

        # 9. Save Conversation Memory
        memory_service.add_message(sid, "user", message, metadata={"intent": intent, "language": detected_lang})
        memory_service.add_message(sid, "assistant", answer, metadata={"mode": ai_meta.get("mode"), "model": ai_meta.get("model")})

        # 10. Generate Smart Contextual Suggestions
        suggestions = self._generate_suggestions(intent, active_destination, detected_lang)

        # Merge data sources
        final_sources = list(dict.fromkeys(data_sources_used + ai_meta.get("data_sources", [])))

        return {
            "answer": answer,
            "mode": ai_meta.get("mode", "online"),
            "model": ai_meta.get("model", "gemini-flash-latest"),
            "data_sources": final_sources,
            "language": "km" if is_km else "en",
            "intent": intent,
            "confidence": intent_info.get("confidence", 0.95),
            "is_matched": is_matched,
            "similarity_score": similarity_score,
            "sources": sources,
            "related_places": related_places,
            "suggestions": suggestions,
            "weather": weather_payload,
            "currency": currency_payload,
            "itinerary": itinerary_payload,
            "recommendations": recommendations_payload,
            "session_id": sid
        }

    def _generate_suggestions(self, intent: str, destination: Optional[str], lang: str) -> List[str]:
        """Generate smart follow-up suggestions for the UI."""
        is_km = "km" in lang
        dest = destination or ("សៀមរាប" if is_km else "Siem Reap")
        
        if intent == "greeting":
            if is_km:
                return [
                    "តើកន្លែងណាខ្លះគួរទៅកម្សាន្តនៅសៀមរាប?",
                    "តើអាកាសធាតុនៅសៀមរាបថ្ងៃនេះយ៉ាងម៉េចដែរ?",
                    "រៀបចំគម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប"
                ]
            else:
                return [
                    "What are the top places to visit in Siem Reap?",
                    "What is the weather like in Siem Reap today?",
                    "Create a 3-day Siem Reap cultural itinerary"
                ]

        if intent == "weather_travel":
            if is_km:
                return [
                    f"តើទៅ {dest} គួររៀបចំដំណើរកម្សាន្តប៉ុន្មានថ្ងៃ?",
                    "តើម្ហូបអាហារល្បីៗនៅទីនោះមានអ្វីខ្លះ?",
                    "ណែនាំមធ្យោបាយធ្វើដំណើរដែលល្អបំផុត"
                ]
            else:
                return [
                    f"Create a 3-day itinerary for {dest}",
                    f"What local dishes should I try in {dest}?",
                    "What are the best transportation options?"
                ]

        if is_km:
            return [
                f"តើអាកាសធាតុនៅ {dest} យ៉ាងណាដែរ?",
                f"តើម្ហូបអាហារល្បីៗនៅ {dest} មានអ្វីខ្លះ?",
                f"រៀបចំគម្រោងដើរលេង ៣ ថ្ងៃនៅ {dest}"
            ]
        else:
            return [
                f"What is the weather like in {dest}?",
                f"What local food should I try in {dest}?",
                f"Create a 3-day itinerary for {dest}"
            ]

rag_service = RAGService()

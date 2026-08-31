import uuid
import time
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.logging import structured_logger
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
        Master AI Orchestration Pipeline:
        1. Request ID & Session Setup
        2. Strict Language Detection (Khmer vs English)
        3. Intent Detection & Entity Extraction
        4. Smart Intent-Driven Tool Execution
        5. Grounded RAG Retrieval (all-MiniLM / Vector cosine + fuzzy)
        6. AI Router Execution (Gemini -> Ollama -> Fallback Engine)
        7. Response Validation & Multi-Factor Confidence Scoring
        8. Standard JSON Payload Formulation (React Cards & Android XML)
        9. Structured Observability Logging
        """
        start_time = time.time()
        request_id = f"req_{uuid.uuid4().hex[:12]}"
        timestamp_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # 1. Session Setup
        sid = memory_service.get_or_create_session_id(session_id)
        
        # 2. Strict Language Detection & Normalization
        raw_lang = preferred_language or language_service.detect_language(message)
        detected_lang = language_service.normalize_language_code(raw_lang)
        is_km = detected_lang == "km" or language_service.is_khmer(message)
        effective_lang = "km" if is_km else "en"

        # 3. Retrieve & Sync Conversation History
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
            memory_service.update_session_metadata(
                sid,
                destination=entities["destination"],
                duration=str(entities.get("duration", "")),
                budget=entities.get("budget"),
                travel_style=entities.get("travel_style"),
                language=effective_lang
            )

        # 5. Smart Tool Selection & Focused Real-Time Execution
        real_time_blocks = []
        data_sources_used = ["tourism_knowledge_base"]
        
        weather_payload = None
        currency_payload = None
        events_payload = None
        itinerary_payload = None
        recommendations_payload = None
        sources = []
        data_type = "general"
        data_content: Dict[str, Any] = {}

        # Tool 1: Itinerary Planning Engine
        if intent == "itinerary":
            data_type = "itinerary"
            days = entities.get("duration_days") or entities.get("duration") or 3
            budget = entities.get("budget_usd") or entities.get("budget")
            itinerary_payload = itinerary_engine.generate_itinerary(
                destination=active_destination,
                days=days,
                budget_usd=budget,
                travel_style=entities.get("travel_style", "culture"),
                interests=entities.get("interests", ["culture", "history"]),
                travelers=entities.get("number_of_people", 2),
                language=effective_lang
            )
            data_sources_used.append("itinerary_engine")
            data_content = itinerary_payload
            real_time_blocks.append(
                f"[OPTIMIZED ITINERARY PLAN: {itinerary_payload['title']}]:\n"
                f"- Destination: {itinerary_payload['destination']}\n"
                f"- Duration: {itinerary_payload['duration_days']} Days\n"
                f"- Estimated Budget: {itinerary_payload['formatted_total_budget']}"
            )

        # Tool 2: Weather Service
        elif intent == "weather":
            data_type = "weather"
            weather_payload = weather_service.get_weather(active_destination, days=3)
            data_sources_used.append("weather_service")
            w_curr = weather_payload["current"]
            data_content = {
                "type": "weather",
                "location": weather_payload["province"],
                "temperature": w_curr["temperature_c"],
                "condition": w_curr["condition_km"] if is_km else w_curr["condition"],
                "humidity": w_curr["humidity_percent"],
                "rain_probability": w_curr["rain_probability"],
                "travel_advice": weather_payload["travel_advice_km"] if is_km else weather_payload["travel_advice_en"]
            }
            real_time_blocks.append(
                f"[REAL-TIME WEATHER FOR {weather_payload['province'].upper()}]:\n"
                f"- Temperature: {w_curr['temperature_c']}°C ({w_curr['temperature_f']}°F)\n"
                f"- Condition: {w_curr['condition']} ({w_curr['condition_km']})\n"
                f"- Rain Probability: {w_curr['rain_probability']}%\n"
                f"- Travel Suitability: {weather_payload['travel_suitability']}\n"
                f"- Travel Advice: {weather_payload['travel_advice_km'] if is_km else weather_payload['travel_advice_en']}"
            )

        # Tool 3: Currency & Budget Conversion Engine
        elif intent == "currency":
            data_type = "currency"
            budget_amount = entities.get("budget") or 100.0
            currency_payload = currency_service.convert(amount=budget_amount, from_curr="USD", to_curr="KHR")
            data_sources_used.append("currency_service")
            data_content = currency_payload
            real_time_blocks.append(
                f"[LIVE EXCHANGE RATE & CONVERSION]:\n"
                f"- Conversion: {currency_payload['formatted']}\n"
                f"- Reference Rate: 1 USD = {currency_payload['rate']:,.0f} KHR\n"
                f"- Source: {currency_payload['source']}"
            )

        # Tool 4: Recommendations Engine
        elif intent == "recommendation":
            data_type = "recommendation"
            recommendations_payload = recommendation_engine.recommend(
                interests=entities.get("interests"),
                province=active_destination if active_destination != "Cambodia" else None,
                budget_usd=entities.get("budget"),
                duration_days=entities.get("duration"),
                travel_style=entities.get("travel_style"),
                limit=4
            )
            if recommendations_payload:
                data_sources_used.append("recommendation_engine")
                data_content = {"recommendations": recommendations_payload}
                rec_lines = [
                    f"- {r['name']} ({r.get('province', '')}) [Match: {r['match_score']}%]: {r.get('description', '')} | Fee: {r.get('price', '')}"
                    for r in recommendations_payload[:3]
                ]
                real_time_blocks.append("[VERIFIED RECOMMENDATIONS]:\n" + "\n".join(rec_lines))

        # Tool 5: Festivals & Events Service
        elif intent == "events":
            data_type = "event"
            events_data = events_service.search_events(query=message, province=active_destination)
            if events_data.get("events"):
                events_payload = events_data["events"]
                data_sources_used.append("events_service")
                data_content = {"events": events_payload}
                evt_lines = [
                    f"- {evt['name']} ({evt.get('name_km', '')}): {evt.get('typical_period', '')} in {evt.get('location', '')}. {evt.get('description', '')}"
                    for evt in events_payload[:2]
                ]
                real_time_blocks.append("[VERIFIED CAMBODIAN FESTIVALS]:\n" + "\n".join(evt_lines))

        # 6. RAG Retrieval from Tourism Knowledge Base
        rag_context_text, retrieved_sources = matching_service.build_rag_context(
            query=message,
            top_k=settings.TOP_K,
            threshold=settings.SIMILARITY_THRESHOLD,
            max_length=settings.MAX_CONTEXT_LENGTH
        )
        
        is_matched = bool(retrieved_sources)
        top_sim_score = retrieved_sources[0]["relevance_score"] if retrieved_sources else 0.0

        if retrieved_sources and not itinerary_payload and not recommendations_payload:
            sources = retrieved_sources
            if data_type == "general":
                data_type = "place"
                data_content = {
                    "place": retrieved_sources[0]["name"],
                    "province": retrieved_sources[0].get("province"),
                    "category": retrieved_sources[0].get("category"),
                    "price": retrieved_sources[0].get("price")
                }

        # 7. Fast-Path Greeting, Time, & Identity
        if intent == "greeting":
            answer = (
                "សួស្តី! 🖐️ ខ្ញុំជា Angkor Verse AI ជំនួយការទេសចរណ៍ AI នៅកម្ពុជា។ "
                "តើខ្ញុំអាចជួយផ្ដល់ព័ត៌មានអំពីកន្លែងកម្សាន្ត ម្ហូបអាហារ សណ្ឋាគារ ពិនិត្យអាកាសធាតុ ឬរៀបចំគម្រោងដើរលេងដល់អ្នកយ៉ាងដូចម្តេចដែរ?"
                if is_km
                else "Hello! 👋 Welcome to Cambodia! I'm Angkor Verse AI, your intelligent Tourism Assistant. "
                     "How can I help you explore temple attractions, authentic cuisine, check live weather, or plan an itinerary today?"
            )
            ai_meta = {
                "mode": "online" if settings.effective_gemini_api_key else "offline",
                "provider": "gemini" if settings.effective_gemini_api_key else "ollama",
                "model": settings.effective_online_model if settings.effective_gemini_api_key else settings.effective_offline_model,
                "confidence": 0.98,
                "fallback_used": False,
                "data_sources": ["system_greeting"]
            }
        elif intent == "time":
            from datetime import datetime, timezone, timedelta
            cambodia_tz = timezone(timedelta(hours=7))
            now_cambodia = datetime.now(cambodia_tz)
            time_12h = now_cambodia.strftime("%I:%M %p")
            time_24h = now_cambodia.strftime("%H:%M")
            date_en = now_cambodia.strftime("%A, %B %d, %Y")
            
            kh_digits = {'0': '០', '1': '១', '2': '២', '3': '៣', '4': '៤', '5': '៥', '6': '៦', '7': '៧', '8': '៨', '9': '៩'}
            time_km_digits = "".join(kh_digits.get(c, c) for c in time_12h)
            
            if is_km:
                answer = f"🕒 ពេលនេះនៅប្រទេសកម្ពុជា (ម៉ោងឥណ្ឌូចិន Indochina Time, UTC+7) គឺម៉ោង **{time_12h}** ({time_24h}) នា **{date_en}**។"
            else:
                answer = f"🕒 The current time in Cambodia (Indochina Time, UTC+7) is **{time_12h}** ({time_24h}), **{date_en}**."
                
            ai_meta = {
                "mode": "online" if settings.effective_gemini_api_key else "offline",
                "provider": "system_clock",
                "model": "system_realtime",
                "confidence": 1.0,
                "fallback_used": False,
                "data_sources": ["system_time_service"]
            }
        elif intent == "identity":
            if is_km:
                answer = (
                    "ខ្ញុំជា **Angkor Verse AI** 🇰🇭 ជំនួយការទេសចរណ៍ឆ្លាតវៃសម្រាប់ប្រទេសកម្ពុជា។ "
                    "ខ្ញុំអាចជួយផ្ដល់ព័ត៌មានលម្អិតអំពីប្រាសាទបុរាណ ឆ្នេរកោះ ម្ហូបអាហារខ្មែរ ប្តូរប្រាក់រៀល-ដុល្លារ ពិនិត្យអាកាសធាតុផ្ទាល់ និងរៀបចំគម្រោងដើរលេង ១ ដល់ ៥ ថ្ងៃឡើងទៅ។"
                )
            else:
                answer = (
                    "I am **Angkor Verse AI** 🇰🇭, your intelligent travel assistant dedicated to the Kingdom of Cambodia. "
                    "I can provide verified insights on ancient temples, tropical islands, Khmer cuisine, live weather forecasts, USD/KHR exchange rates, and customized 1-5+ day travel itineraries."
                )
            ai_meta = {
                "mode": "online" if settings.effective_gemini_api_key else "offline",
                "provider": "system_identity",
                "model": "system_core",
                "confidence": 1.0,
                "fallback_used": False,
                "data_sources": ["system_identity"]
            }
        else:
            # 8. Central AI Orchestration
            combined_real_time = "\n\n".join(real_time_blocks) if real_time_blocks else None
            ai_resp = ai_service.generate_response(
                message=message,
                conversation_history=history,
                context=rag_context_text if is_matched else None,
                is_matched=is_matched,
                real_time_data_text=combined_real_time,
                intent=intent,
                language=effective_lang
            )
            answer = ai_resp["answer"]
            ai_meta = ai_resp

        # 9. Save Conversation Memory
        memory_service.add_message(sid, "user", message, metadata={"intent": intent, "language": effective_lang})
        memory_service.add_message(sid, "assistant", answer, metadata={"mode": ai_meta.get("mode"), "model": ai_meta.get("model")})

        # 10. Generate Contextual Suggestions
        suggestions = self._generate_suggestions(intent, active_destination, effective_lang)

        # Merge data sources
        final_sources = list(dict.fromkeys(data_sources_used + ai_meta.get("data_sources", [])))
        latency_ms = (time.time() - start_time) * 1000

        # 11. Structured Observability Logging
        structured_logger.log_request(
            request_id=request_id,
            session_id=sid,
            intent=intent,
            language=effective_lang,
            provider=ai_meta.get("provider", "gemini"),
            mode=ai_meta.get("mode", "online"),
            latency_ms=latency_ms,
            confidence=ai_meta.get("confidence", 0.95),
            fallback_used=ai_meta.get("fallback_used", False)
        )

        return {
            "success": True,
            "request_id": request_id,
            "session_id": sid,
            "language": effective_lang,
            "mode": ai_meta.get("mode", "online"),
            "provider": ai_meta.get("provider", "gemini"),
            "intent": intent,
            "confidence": ai_meta.get("confidence", 0.95),
            "message": answer,
            "answer": answer,  # React compatibility field
            "model": ai_meta.get("model", "gemini-flash-latest"),
            "data": {
                "type": data_type,
                "location": active_destination,
                "content": data_content or answer,
                **data_content
            },
            "sources": sources,
            "timestamp": timestamp_str,
            
            # Backwards Compatibility Fields
            "data_sources": final_sources,
            "related_places": [],
            "suggestions": suggestions,
            "weather": weather_payload,
            "currency": currency_payload,
            "itinerary": itinerary_payload,
            "recommendations": recommendations_payload,
            "is_matched": is_matched,
            "similarity_score": top_sim_score
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

        if intent == "weather":
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

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

        # Tool 6: Verified Cambodian Restaurant & Food Search
        elif intent == "food" or any(w in message.lower() for w in ["amok", "restaurant", "food", "eat", "lok lak", "dining", "ហាងបាយ", "ម្ហូប", "អាហារ"]):
            verified_rests = places_service.search_restaurants(query=message, province=active_destination, limit=3)
            if verified_rests:
                data_type = "place"
                data_sources_used.append("verified_restaurants_registry")
                data_content = {
                    "type": "restaurant",
                    "restaurants": verified_rests,
                    "top_match": verified_rests[0]
                }
                rest_lines = []
                for vr in verified_rests:
                    desc_display = vr.get('description_km') if is_km else vr.get('description')
                    dishes_str = ", ".join(vr.get('specialty_dishes', []))
                    rest_lines.append(
                        f"- {vr.get('name')} ({vr.get('name_km', '')}) in {vr.get('province', '')}: {desc_display} | Specialties: {dishes_str} | Price: {vr.get('price', '')} | Hours: {vr.get('opening_hours', '')}"
                    )
                real_time_blocks.append(
                    "[VERIFIED CAMBODIAN RESTAURANTS - ABSOLUTE GROUND TRUTH]:\n" + "\n".join(rest_lines) +
                    "\n\nInstruction: Recommend ONLY these verified restaurants with their exact verified details. Do not invent any restaurant names or prices."
                )

        # Tool 7: Conversation Summary
        elif intent == "conversation_summary":
            summary_info = memory_service.get_structured_conversation_summary(sid, effective_lang)
            data_type = "conversation_summary"
            data_content = summary_info
            data_sources_used.append("conversation_memory")
            real_time_blocks.append(
                f"[CONVERSATION SUMMARY RECAP]:\n"
                f"- Active Destination: {summary_info['active_destination']}\n"
                f"- Topics Discussed: {', '.join(summary_info['topics'])}\n"
                f"- Total Messages: {summary_info['message_count']}\n"
                f"- Summary Content: {summary_info['summary_text']}"
            )

        # 6. RAG Retrieval from Tourism Knowledge Base
        rag_context_text, retrieved_sources = matching_service.build_rag_context(
            query=message,
            top_k=settings.TOP_K,
            threshold=settings.SIMILARITY_THRESHOLD,
            max_length=settings.MAX_CONTEXT_LENGTH
        )
        
        is_matched = bool(retrieved_sources)
        top_sim_score = retrieved_sources[0]["relevance_score"] if retrieved_sources else 0.0

        if retrieved_sources and not itinerary_payload and not recommendations_payload and data_type == "general":
            sources = retrieved_sources
            data_type = "place"
            data_content = {
                "place": retrieved_sources[0]["name"],
                "province": retrieved_sources[0].get("province"),
                "category": retrieved_sources[0].get("category"),
                "price": retrieved_sources[0].get("price")
            }

        # 7. Fast-Path Greeting, Time, Identity, & Conversation Summary
        if intent == "conversation_summary":
            summary_info = memory_service.get_structured_conversation_summary(sid, effective_lang)
            answer = summary_info["summary_text"]
            data_type = "conversation_summary"
            data_content = summary_info
            ai_meta = {
                "mode": "online" if settings.effective_gemini_api_key else "offline",
                "provider": "conversation_memory",
                "model": "system_memory",
                "confidence": 1.0,
                "fallback_used": False,
                "data_sources": ["conversation_memory"]
            }
        elif intent == "greeting":
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
            "model": ai_meta.get("model", settings.effective_online_model),
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
        """Generate 3 to 4 smart randomized follow-up suggestions for the UI."""
        import random
        is_km = "km" in lang
        dest_en = destination or "Siem Reap"
        dest_km = "សៀមរាប" if (not destination or destination == "Siem Reap") else (
            "ភ្នំពេញ" if destination == "Phnom Penh" else (
                "កំពត" if destination == "Kampot" else (
                    "កោះរ៉ុង" if destination == "Koh Rong" else (
                        "ព្រះសីហនុ" if destination == "Sihanoukville" else destination
                    )
                )
            )
        )
        
        # Candidate question pools categorized by domain
        if is_km:
            itinerary_pool = [
                f"រៀបចំគម្រោងដើរលេង ៣ ថ្ងៃនៅ {dest_km}",
                "រៀបចំដំណើរកម្សាន្ត ៥ ថ្ងៃ ភ្នំពេញ និង សៀមរាប",
                f"តើទៅ {dest_km} គួររៀបចំដំណើរកម្សាន្តប៉ុន្មានថ្ងៃ?",
                "រៀបចំគម្រោងលំហែកាយ ២ ថ្ងៃនៅកោះរ៉ុង"
            ]
            attractions_pool = [
                f"តើកន្លែងណាខ្លះគួរទៅកម្សាន្តនៅ {dest_km}?",
                "តើប្រាសាទល្បីៗណាខ្លះដែលគួរទៅទស្សនាក្រៅពីអង្គរវត្ត?",
                "តើពេលវេលាណាដែលល្អបំផុតសម្រាប់មើលថ្ងៃរះនៅប្រាសាទអង្គរវត្ត?",
                "តើឆ្នេរខ្សាច់ណាខ្លះដែលស្អាតបំផុតនៅកោះរ៉ុង?",
                "តើនៅឧទ្យានជាតិភ្នំបូកគោមានកន្លែងកម្សាន្តអ្វីខ្លះ?",
                "តើព្រះបរមរាជវាំងនៅភ្នំពេញមានអ្វីពិសេសខ្លះ?"
            ]
            food_pool = [
                f"តើម្ហូបអាហារល្បីៗនៅ {dest_km} មានអ្វីខ្លះ?",
                "តើម្ហូបខ្មែរប្រពៃណីណាខ្លះដែលមិនគួររំលង?",
                "តើអាចរកញ៉ាំអាម៉ុកត្រី និងឡុកឡាក់ឆ្ងាញ់នៅឯណា?",
                "តើក្តាមឆាម្រេចខ្ចីនៅកែបមានរសជាតិយ៉ាងណា?"
            ]
            practical_pool = [
                f"តើអាកាសធាតុនៅ {dest_km} យ៉ាងណាដែរ?",
                "តើអត្រាប្តូរប្រាក់ ១ ដុល្លារស្មើនឹងប៉ុន្មានរៀលថ្ងៃនេះ?",
                "តើតម្លៃសំបុត្រចូលទស្សនាអង្គរវត្តប៉ុន្មានដែរ?",
                "តើត្រូវស្លៀកពាក់បែបណាពេលចូលទស្សនាប្រាសាទបុរាណ?",
                "តើធ្វើដំណើរពីភ្នំពេញទៅសៀមរាបតាមមធ្យោបាយណាស្រួលជាងគេ?",
                "តើពិធីបុណ្យប្រពៃណីខ្មែរល្បីៗមានអ្វីខ្លះ?"
            ]
        else:
            itinerary_pool = [
                f"Create a 3-day {dest_en} cultural itinerary",
                "Plan a 5-day Cambodia highlights trip (Phnom Penh & Siem Reap)",
                f"How many days are ideal to visit {dest_en}?",
                "Plan a relaxing 2-day beach getaway to Koh Rong island"
            ]
            attractions_pool = [
                f"What are the top attractions to visit in {dest_en}?",
                "What must-see temples in Siem Reap should I visit besides Angkor Wat?",
                "What is the best time and spot for Angkor Wat sunrise?",
                "What are the most beautiful beaches on Koh Rong?",
                "What can I explore at Bokor National Park in Kampot?",
                "What are the highlights of the Royal Palace in Phnom Penh?"
            ]
            food_pool = [
                f"What local dishes should I try in {dest_en}?",
                "What authentic Khmer dishes are must-try in Cambodia?",
                "Where can I find the best Fish Amok and Beef Lok Lak?",
                "Tell me about fresh Kampot pepper crab in Kep"
            ]
            practical_pool = [
                f"What is the weather like in {dest_en} today?",
                "What is the current USD to Cambodian Riel exchange rate?",
                "How much does an Angkor Wat temple pass cost?",
                "What is the dress code for visiting ancient temples in Cambodia?",
                "How do I travel comfortably between Phnom Penh and Siem Reap?",
                "What traditional Cambodian festivals happen throughout the year?"
            ]

        # Assemble diverse mix from categories
        candidates = [
            random.choice(attractions_pool),
            random.choice(itinerary_pool),
            random.choice(food_pool),
            random.choice(practical_pool)
        ]

        # De-duplicate while preserving order
        unique_selected = list(dict.fromkeys(candidates))
        random.shuffle(unique_selected)
        target_count = random.choice([3, 4])
        return unique_selected[:target_count]

rag_service = RAGService()

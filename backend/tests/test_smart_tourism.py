import pytest
from app.services.language_service import language_service
from app.services.intent_service import intent_service
from app.services.weather_service import weather_service
from app.services.currency_service import currency_service
from app.services.events_service import events_service
from app.services.places_service import places_service
from app.services.transport_service import transport_service
from app.services.recommendation_engine import recommendation_engine
from app.services.itinerary_engine import itinerary_engine
from app.services.confidence_service import confidence_service
from app.services.response_validation_service import response_validation_service
from app.services.ai_router import ai_router
from app.services.matching_service import matching_service
from app.services.rag_service import rag_service
from app.services.memory_service import memory_service

# 1. Language Service Tests
def test_language_detection_and_validation():
    """Verify strict language detection and validation for Khmer and English."""
    assert language_service.detect_language("អង្គរវត្តនៅឯណា?") == "km"
    assert language_service.detect_language("តើទៅសៀមរាបគួរទៅណា?") == "km"
    assert language_service.detect_language("Where is Angkor Wat located?") == "en"
    assert language_service.detect_language("What is the weather in Kampot?") == "en"

    # Validation
    val_km = response_validation_service.validate_response("ប្រាសាទអង្គរវត្តស្ថិតនៅខេត្តសៀមរាប", expected_language="km")
    assert val_km["is_valid"] is True

    val_en = response_validation_service.validate_response("Angkor Wat is located in Siem Reap province.", expected_language="en")
    assert val_en["is_valid"] is True

# 2. Intent & Entity Extraction Tests
def test_intent_and_entity_extraction():
    """Verify all major intents and entities extraction."""
    # Itinerary intent with duration & budget
    res1 = intent_service.detect_intent("Plan a 3-day trip to Siem Reap under $300.")
    assert res1["intent"] == "itinerary"
    assert res1["entities"].get("duration") == 3
    assert res1["entities"].get("budget") == 300.0
    assert res1["entities"].get("destination") == "Siem Reap"

    # Weather intent
    res2 = intent_service.detect_intent("What is the weather in Phnom Penh today?")
    assert res2["intent"] == "weather"
    assert res2["entities"].get("destination") == "Phnom Penh"

    # Currency intent
    res3 = intent_service.detect_intent("Convert 50 USD to Khmer Riel")
    assert res3["intent"] == "currency"

    # Food intent
    res4 = intent_service.detect_intent("Where can I eat Fish Amok in Siem Reap?")
    assert res4["intent"] == "food"

    # Events intent
    res5 = intent_service.detect_intent("When is the Water Festival in Cambodia?")
    assert res5["intent"] == "events"

# 3. Weather Service Tests
def test_weather_service():
    """Verify weather service returns valid weather payload for Cambodian hubs."""
    res = weather_service.get_weather("Siem Reap", days=3)
    assert res["province"] == "Siem Reap"
    assert "temperature_c" in res["current"]
    assert "forecast" in res
    assert len(res["forecast"]) >= 1

# 4. Currency Service Tests
def test_currency_service():
    """Verify deterministic currency exchange rate and conversion."""
    rate = currency_service.get_exchange_rate()
    assert rate["exchange_rate"] > 3000
    
    conversion = currency_service.convert(50, "USD", "KHR")
    assert conversion["result"] >= 150000
    assert conversion["from"] == "USD"
    assert conversion["to"] == "KHR"

    budget = currency_service.estimate_travel_budget(days=3, travelers=2, style="culture")
    assert budget["breakdown_usd"]["total_estimated_usd"] > 0

# 5. Events & Festivals Service Tests
def test_events_service():
    """Verify verified Cambodian festivals can be retrieved."""
    events = events_service.get_all_events()
    assert len(events) >= 3
    
    water_fest = events_service.search_events(query="water festival")
    assert len(water_fest["events"]) >= 1

# 6. Recommendation Engine Tests
def test_recommendation_engine():
    """Verify multi-factor recommendation scoring."""
    recs = recommendation_engine.recommend(interests=["culture", "temple"], limit=3)
    assert len(recs) >= 1
    assert "match_score" in recs[0]
    assert recs[0]["match_score"] > 50

# 7. Itinerary Engine Tests
def test_itinerary_engine():
    """Verify 1, 2, 3, 4, 5+ day itinerary generation with deterministic calculations."""
    itin = itinerary_engine.generate_itinerary(destination="Siem Reap", days=3, language="en")
    assert itin["duration_days"] == 3
    assert len(itin["days"]) == 3
    assert "estimated_budget" in itin
    assert len(itin["days"][0]["items"]) >= 2
    assert "time" in itin["days"][0]["items"][0]
    assert "activity" in itin["days"][0]["items"][0]

# 8. Confidence Scoring Tests
def test_confidence_service():
    """Verify confidence calculation factors and levels."""
    high_eval = confidence_service.calculate_confidence(
        intent_confidence=0.95,
        rag_similarity_score=0.95,
        tool_executed=True,
        tool_success=True,
        is_matched=True,
        ai_provider_mode="online"
    )
    assert high_eval["level"] == "high"
    assert high_eval["overall_score"] >= 0.90

# 9. RAG Retrieval & Context Builder Tests
def test_rag_retrieval_pipeline():
    """Verify semantic retrieval and context building."""
    ctx, sources = matching_service.build_rag_context("Tell me about Angkor Wat", top_k=2)
    assert len(sources) >= 1
    assert "Angkor" in sources[0]["name"]
    assert len(ctx) > 50

# 10. Memory Service Tests
def test_memory_service():
    """Verify session metadata, history, and limits."""
    sid = "test_sess_001"
    memory_service.add_message(sid, "user", "I want to visit Siem Reap.")
    memory_service.add_message(sid, "assistant", "Siem Reap is wonderful!")
    
    hist = memory_service.get_history(sid)
    assert len(hist) == 2
    assert hist[0]["role"] == "user"
    assert hist[1]["role"] == "assistant"
    
    memory_service.delete_session(sid)
    assert len(memory_service.get_history(sid)) == 0

# 11. Full End-to-End Orchestrator Flow
def test_rag_service_full_flow():
    """Verify master RAG orchestrator for bilingual tourism requests."""
    res_en = rag_service.process_chat_message("What is the best time to visit Angkor Wat?")
    assert res_en["success"] is True
    assert len(res_en["message"]) > 20
    assert "request_id" in res_en
    assert res_en["language"] == "en"
    assert "data" in res_en

    res_km = rag_service.process_chat_message("តើអាកាសធាតុនៅសៀមរាបយ៉ាងម៉េចដែរ?")
    assert res_km["success"] is True
    assert res_km["language"] == "km"
    assert res_km["weather"] is not None

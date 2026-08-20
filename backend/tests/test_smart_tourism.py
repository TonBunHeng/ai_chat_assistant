import pytest
from app.services.language_service import language_service
from app.services.weather_service import weather_service
from app.services.currency_service import currency_service
from app.services.events_service import events_service
from app.services.places_service import places_service
from app.services.transport_service import transport_service
from app.services.recommendation_engine import recommendation_engine
from app.services.itinerary_engine import itinerary_engine
from app.services.rag_service import rag_service

def test_language_detection():
    """Verify strict language detection for Khmer and English."""
    assert language_service.detect_language("អង្គរវត្តនៅឯណា?") == "km"
    assert language_service.detect_language("តើទៅសៀមរាបគួរទៅណា?") == "km"
    assert language_service.detect_language("Where is Angkor Wat located?") == "en"
    assert language_service.detect_language("What is the weather in Kampot?") == "en"

def test_weather_service():
    """Verify weather service returns valid weather payload for Siem Reap."""
    res = weather_service.get_weather("Siem Reap", days=3)
    assert res["province"] == "Siem Reap"
    assert "temperature_c" in res["current"]
    assert "forecast" in res
    assert len(res["forecast"]) >= 1

def test_currency_service():
    """Verify currency exchange rate and travel budget breakdown."""
    rate = currency_service.get_exchange_rate()
    assert rate["exchange_rate"] > 3000
    
    conversion = currency_service.convert(50, "USD", "KHR")
    assert conversion["converted_amount"] >= 150000

    budget = currency_service.estimate_travel_budget(days=3, travelers=2, style="culture")
    assert budget["breakdown_usd"]["total_estimated_usd"] > 0

def test_events_service():
    """Verify verified Cambodian festivals can be retrieved."""
    events = events_service.get_all_events()
    assert len(events) >= 3
    
    water_fest = events_service.search_events(query="water festival")
    assert len(water_fest["events"]) >= 1

def test_recommendation_engine():
    """Verify multi-factor recommendation scoring."""
    recs = recommendation_engine.recommend(interests=["history", "temples"], limit=3)
    assert len(recs) >= 1
    assert "match_score" in recs[0]
    assert recs[0]["match_score"] > 50

def test_itinerary_engine():
    """Verify 3-day itinerary generation with day slots and budget."""
    itin = itinerary_engine.generate_itinerary(destination="Siem Reap", days=3, language="en")
    assert itin["duration_days"] == 3
    assert len(itin["days"]) == 3
    assert "estimated_budget" in itin
    assert len(itin["days"][0]["activities"]) >= 2

def test_rag_service_full_flow():
    """Verify end-to-end RAG orchestrator for general tourism and real-time questions."""
    res = rag_service.process_chat_message("What is the best time to visit Angkor Wat?")
    assert res["answer"] is not None
    assert len(res["answer"]) > 50
    assert "mode" in res
    assert "data_sources" in res
    assert res["language"] == "en"

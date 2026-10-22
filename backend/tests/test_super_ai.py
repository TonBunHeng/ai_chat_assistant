import pytest
from app.services.tourism_service import tourism_service
from app.services.intent_service import intent_service
from app.services.memory_service import memory_service
from app.services.offline.offline_knowledge_service import offline_knowledge_service
from app.services.rag_service import rag_service

def test_25_provinces_coverage():
    """Verify all 25 first-level administrative units of Cambodia are loaded with full details."""
    provinces_data = tourism_service.get_dataset("provinces")
    assert len(provinces_data) == 25, f"Expected 25 provinces, found {len(provinces_data)}"
    
    expected_provinces = [
        "Phnom Penh", "Siem Reap", "Preah Sihanouk", "Kampot", "Battambang",
        "Banteay Meanchey", "Kampong Cham", "Kampong Chhnang", "Kampong Speu", "Kampong Thom",
        "Kandal", "Kep", "Koh Kong", "Kratié", "Mondulkiri",
        "Oddar Meanchey", "Pailin", "Preah Vihear", "Pursat", "Prey Veng",
        "Ratanakiri", "Stung Treng", "Svay Rieng", "Takéo", "Tboung Khmum"
    ]
    
    found_names = {p["name"] for p in provinces_data}
    for prov in expected_provinces:
        assert prov in found_names, f"Province '{prov}' missing from dataset"
        
    for p in provinces_data:
        assert "name_km" in p and p["name_km"], f"Missing name_km in {p['name']}"
        assert "capital" in p and p["capital"], f"Missing capital in {p['name']}"
        assert "description" in p and p["description"], f"Missing description in {p['name']}"
        assert "top_attractions" in p and len(p["top_attractions"]) > 0, f"Missing attractions in {p['name']}"

def test_broad_ai_intents():
    """Verify intent extraction supports coding, translation, mathematics, business, and provinces."""
    # Coding intent
    r_code = intent_service.detect_intent("Write a Python script to sort an array using quicksort.")
    assert r_code["intent"] == "coding"
    
    # Translation intent
    r_trans = intent_service.detect_intent("How to say 'Thank you very much' in Khmer?")
    assert r_trans["intent"] == "translation"
    
    # Math & science intent
    r_math = intent_service.detect_intent("Calculate the derivative of x^2 + 3x.")
    assert r_math["intent"] == "math_science"
    
    # Business & finance intent
    r_biz = intent_service.detect_intent("Explain the Bakong digital payment system in Cambodia.")
    assert r_biz["intent"] == "business_finance"
    
    # 25 Provinces extraction
    r_prov1 = intent_service.detect_intent("What are the best ecotourism places in Mondulkiri?")
    assert r_prov1["entities"].get("destination") == "Mondulkiri"
    
    r_prov2 = intent_service.detect_intent("Tell me about the marble carvings in Pursat.")
    assert r_prov2["entities"].get("destination") == "Pursat"

def test_session_rename_and_search():
    """Verify session renaming and keyword search in memory service."""
    test_sid = "test_super_ai_session_123"
    memory_service.add_message(test_sid, "user", "How to write a fast API endpoint in Python?")
    memory_service.add_message(test_sid, "assistant", "Here is how to create a fast endpoint with FastAPI...")
    
    # Rename session
    success = memory_service.rename_session(test_sid, "FastAPI Python Guide")
    assert success is True
    
    # Verify title in sessions list
    all_sessions = memory_service.get_all_sessions()
    matching = [s for s in all_sessions if s["session_id"] == test_sid]
    assert len(matching) == 1
    assert matching[0]["title"] == "FastAPI Python Guide"
    
    # Search session
    search_res = memory_service.search_sessions("FastAPI")
    assert any(s["session_id"] == test_sid for s in search_res)
    
    # Cleanup
    memory_service.delete_session(test_sid)

def test_offline_safe_math():
    """Verify offline knowledge service evaluates simple arithmetic expressions safely."""
    res1 = offline_knowledge_service.synthesize_response("25 * 4")
    assert "100" in res1
    
    res2 = offline_knowledge_service.synthesize_response("120 + 380")
    assert "500" in res2

def test_api_chat_stream_and_sessions():
    """Verify streaming endpoint, session rename, and search over HTTP API."""
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    
    # Test streaming endpoint
    stream_payload = {
        "message": "Calculate 50 + 50 and explain Cambodia's capital.",
        "session_id": "test_stream_sid_888",
        "language": "en"
    }
    resp = client.post("/api/chat/stream", json=stream_payload)
    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers.get("content-type", "")
    assert "data:" in resp.text
    assert "[DONE]" in resp.text
    
    # Test session rename endpoint
    rename_resp = client.patch(
        "/api/chat/sessions/test_stream_sid_888",
        json={"title": "Stream & Math Test Session"}
    )
    assert rename_resp.status_code == 200
    assert rename_resp.json()["success"] is True
    
    # Test session search endpoint
    search_resp = client.get("/api/chat/sessions/search?q=Stream")
    assert search_resp.status_code == 200
    assert search_resp.json()["success"] is True
    assert any(s["session_id"] == "test_stream_sid_888" for s in search_resp.json()["data"])
    
    # Test chat with attachments
    att_payload = {
        "message": "Here is an attached data snippet.",
        "session_id": "test_stream_sid_888",
        "attachments": [
            {
                "name": "sample.txt",
                "type": "text/plain",
                "base64": "data:text/plain;base64,SGVsbG8gQ2FtYm9kaWEgU3VwZXIgQUkh"
            }
        ]
    }
    chat_resp = client.post("/api/chat", json=att_payload)
    assert chat_resp.status_code == 200
    assert chat_resp.json()["success"] is True
    
    # Cleanup session
    memory_service.delete_session("test_stream_sid_888")


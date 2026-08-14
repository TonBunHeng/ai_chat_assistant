import re
from typing import Dict, Any, List, Optional

class IntentService:
    def __init__(self):
        # Keyword patterns for Khmer and English intents
        self.intent_patterns = {
            "greeting": [
                r"\b(hello|hi|hey|good\s+morning|good\s+afternoon|good\s+evening)\b",
                r"(សួស្តី|ជំរាបសួរ)"
            ],
            "itinerary_planning": [
                r"រៀបចំ", r"ដំណើរកំសាន្ត", r"កម្សាន្ត.*ថ្ងៃ", r"ថ្ងៃ", r"itinerary", r"plan", r"days", r"schedule", r"trip plan"
            ],
            "destination_recommendation": [
                r"គួរទៅណា", r"កន្លែងណាខ្លះ", r"ណែនាំ", r"ល្អបំផុត", r"recommend", r"where to go", r"best places", r"should i visit"
            ],
            "destination_information": [
                r"នៅឯណា", r"ព័ត៌មាន", r"ស្ថិតនៅ", r"where is", r"tell me about", r"information", r"located"
            ],
            "food": [
                r"ម្ហូប", r"ហូប", r"ញ៉ាំ", r"អត្ថបទម្ហូប", r"អាហារ", r"food", r"restaurant", r"eat", r"dish", r"amok", r"lok lak", r"kuy teav"
            ],
            "transportation": [
                r"ជិះ", r"រថយន្ត", r"រថភ្លើង", r"តុលតុល", r"ឡាន", r"កប៉ាល់", r"bus", r"taxi", r"tuk tuk", r"flight", r"ferry", r"transport"
            ],
            "weather_travel": [
                r"អាកាសធាតុ", r"រដូវ", r"ភ្លៀង", r"weather", r"season", r"rain", r"best time"
            ],
            "travel_tips": [
                r"ណែនាំ", r"ទិដ្ឋាការ", r"លុយ", r"រៀល", r"ដុល្លារ", r"visa", r"tips", r"currency", r"pass", r"ticket"
            ],
            "nearby_places": [
                r"ជិត", r"ក្បែរ", r"near", r"nearby", r"around"
            ],
            "culture": [
                r"វប្បធម៌", r"ប្រពៃណី", r"របាំ", r"ក្រមា", r" festival", r"culture", r"tradition", r"dance", r"apsara"
            ]
        }
        
        # Province and destination entities
        self.provinces = {
            "siem reap": ["siem reap", "សៀមរាប", "angkor", "អង្គរ"],
            "phnom penh": ["phnom penh", "ភ្នំពេញ"],
            "kampot": ["kampot", "កំពត", "bokor", "បូកគោ"],
            "preah sihanouk": ["sihanoukville", "sihanouk", "ព្រះសីហនុ", "koh rong", "កោះរ៉ុង"],
            "battambang": ["battambang", "បាត់ដំបង"],
            "mondulkiri": ["mondulkiri", "មណ្ឌលគិរី"],
            "kep": ["kep", "កែប"],
            "preah vihear": ["preah vihear", "ព្រះវិហារ"]
        }

    def detect_intent(self, text: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """Detect intent and extract entities from prompt text."""
        lowered = text.lower()
        
        # Check follow-up indicators
        is_short_followup = len(text.strip().split()) <= 4 and ("នៅឯណា" in text or "where" in lowered or "ប៉ុន្មាន" in text or "how much" in lowered)
        
        detected_intent = "general_tourism"
        for intent, patterns in self.intent_patterns.items():
            if any(re.search(p, lowered) for p in patterns):
                detected_intent = intent
                break
                
        if is_short_followup and conversation_history:
            detected_intent = "follow_up_question"
            
        entities = self.extract_entities(text)
        
        return {
            "intent": detected_intent,
            "entities": entities,
            "confidence": 0.92 if detected_intent != "general_tourism" else 0.75
        }

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract destination, duration, and numerical entities."""
        lowered = text.lower()
        entities = {}
        
        # Extract province / destination
        for key, aliases in self.provinces.items():
            if any(alias in lowered for alias in aliases):
                entities["destination"] = key
                break
                
        # Extract duration (e.g. 3 days / ៣ ថ្ងៃ)
        duration_match = re.search(r'(\d+|១|២|៣|៤|៥|៦|៧|៨|៩|១០)\s*(day|days|ថ្ងៃ)', lowered)
        if duration_match:
            entities["duration"] = duration_match.group(0)
            
        return entities

intent_service = IntentService()

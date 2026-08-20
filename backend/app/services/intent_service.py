import re
from typing import Dict, Any, List, Optional

class IntentService:
    def __init__(self):
        self.provinces = {
            "Siem Reap": ["siem reap", "angkor", "សៀមរាប", "អង្គរ", "បាយ័ន", "តាព្រហ្ម"],
            "Phnom Penh": ["phnom penh", "capital", "ភ្នំពេញ", "រាជធានី", "វាំង"],
            "Preah Sihanouk": ["sihanoukville", "sihanouk", "koh rong", "ព្រះសីហនុ", "កំពង់សោម", "កោះរ៉ុង"],
            "Kampot": ["kampot", "bokor", "កំពត", "បូកគោ"],
            "Battambang": ["battambang", "បាត់ដំបង", "រថភ្លើងឫស្សី"],
            "Kep": ["kep", "crab market", "កែប", "ផ្សារក្តាម"],
            "Mondulkiri": ["mondulkiri", "bousra", "មណ្ឌលគិរី", "ប៊ូស្រា"],
            "Ratanakiri": ["ratanakiri", "yeak laom", "រតនគិរី", "យក្សឡោម"],
            "Koh Kong": ["koh kong", "cardamom", "កោះកុង", "ក្រវាញ"],
            "Preah Vihear": ["preah vihear", "ព្រះវិហារ"],
            "Siem Pang": ["stung treng", "ស្ទឹងត្រែង"]
        }
        
        self.intent_patterns = {
            "greeting": [r"^\s*(hi|hello|hey|greetings|good\s+morning|good\s+afternoon|សួស្តី|ជំរាបសួរ)\b"],
            "weather_travel": [r"\b(weather|rain|temperature|forecast|climate|temp|អាកាសធាតុ|ភ្លៀង|ក្តៅ|រងា)\b"],
            "currency_conversion": [r"\b(riel|khr|exchange|convert|currency|rate|usd\s+to\s+khr|khr\s+to\s+usd|ប្តូរលុយ|រៀល|ដុល្លារ)\b"],
            "itinerary_planning": [r"\b(itinerary|plan|trip\s+plan|day\s+1|day\s+2|day\s+3|day\s+4|day\s+5|3\s*day|4\s*day|5\s*day|schedule|tour|route|គម្រោង|ដំណើរកម្សាន្ត|ដើរលេង)\b"],
            "recommendation": [r"\b(recommend|recommendation|where\s+to\s+go|best\s+places|must\s+visit|top\s+attractions|things\s+to\s+do|suggest|ណែនាំ|កន្លែងណា|គួរទៅណា)\b"],
            "events_festivals": [r"\b(event|events|festival|festivals|holiday|water\s+festival|bon\s+om\s+touk|marathon|ពិធីបុណ្យ|បុណ្យ|អុំទូក|ចូលឆ្នាំ)\b"],
            "food_dining": [r"\b(food|eat|restaurant|dish|dishes|amok|lok\s+lak|kuy\s+teav|noodles|ម្ហូប|អាហារ|ញ៉ាំ|ហាងបាយ|អាម៉ុក|ឡុកឡាក់)\b"],
            "transportation": [r"\b(transport|how\s+to\s+get|taxi|bus|train|flight|ferry|tuk\s*tuk|passapp|grab|ធ្វើដំណើរ|ជិះអី|ឡានក្រុង|តាក់ស៊ី|ទូក)\b"],
            "budget_estimation": [r"\b(cost|price|budget|how\s+much|entrance\s+fee|ticket|តម្លៃ|ថ្លៃ|សំបុត្រ|លុយ)\b"]
        }

    def detect_intent(self, text: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """Detect intent and extract entities from prompt text."""
        lowered = text.lower().strip()
        
        detected_intent = "general_tourism"
        for intent, patterns in self.intent_patterns.items():
            if any(re.search(p, lowered) for p in patterns):
                detected_intent = intent
                break
                
        entities = self.extract_entities(text)
        
        # If duration is mentioned with itinerary keywords, prioritize itinerary
        if entities.get("duration_days") and any(w in lowered for w in ["in", "to", "for", "visit", "trip", "plan", "itinerary", "places", "travel", "ដើរលេង"]):
            detected_intent = "itinerary_planning"

        return {
            "intent": detected_intent,
            "entities": entities,
            "confidence": 0.95 if detected_intent != "general_tourism" else 0.75
        }

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract destination, duration, budget, and interest entities."""
        lowered = text.lower()
        entities = {}
        
        # 1. Extract province / destination
        for key, aliases in self.provinces.items():
            if any(alias in lowered for alias in aliases):
                entities["destination"] = key
                break
                
        # 2. Extract duration (e.g. 4day, 4 days, 3-day, ៤ ថ្ងៃ)
        duration_match = re.search(r'(\d+|១|២|៣|៤|៥|៦|៧|៨|៩|១០)\s*(?:-|–)?\s*(?:day|days|ថ្ងៃ)', lowered)
        if duration_match:
            raw_num = duration_match.group(1)
            kh_digits = {'១':'1', '២':'2', '៣':'3', '៤':'4', '៥':'5', '៦':'6', '៧':'7', '៨':'8', '៩':'9', '១០':'10'}
            num_str = kh_digits.get(raw_num, raw_num)
            try:
                entities["duration_days"] = int(num_str)
                entities["duration"] = f"{num_str} days"
            except Exception:
                pass

        # 3. Extract explicit budget (e.g. $50, 50$, 100 USD, 500 dollars, ៥០ ដុល្លារ)
        budget_match = (
            re.search(r'\$\s*(\d+(?:\.\d+)?)', lowered) or
            re.search(r'(\d+(?:\.\d+)?)\s*\$', lowered) or
            re.search(r'(\d+(?:\.\d+)?)\s*(?:usd|dollars?|ដុល្លារ)', lowered)
        )
        if budget_match:
            try:
                entities["budget_usd"] = float(budget_match.group(1))
            except Exception:
                pass

        # 4. Extract interests
        interests = []
        interest_keywords = {
            "history": ["history", "ancient", "temple", "temples", "ប្រវត្តិ", "ប្រាសាទ"],
            "culture": ["culture", "traditional", "heritage", "វប្បធម៌", "ប្រពៃណី"],
            "beach": ["beach", "island", "sea", "snorkeling", "ឆ្នេរ", "កោះ", "សមុទ្រ"],
            "food": ["food", "culinary", "dishes", "restaurant", "ម្ហូប", "អាហារ"],
            "nature": ["nature", "waterfall", "wildlife", "elephants", "hiking", "ធម្មជាតិ", "ទឹកធ្លាក់", "ព្រៃ"],
            "relaxation": ["relax", "peaceful", "quiet", "resort", "សម្រាក", "លំហែ"],
            "adventure": ["adventure", "kayak", "trekking", "ម៉ូតូ", "ផ្សងព្រេង"]
        }
        for category, kws in interest_keywords.items():
            if any(kw in lowered for kw in kws):
                interests.append(category)
        if interests:
            entities["interests"] = interests

        return entities

intent_service = IntentService()

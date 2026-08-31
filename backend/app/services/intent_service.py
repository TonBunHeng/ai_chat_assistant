import re
from typing import Dict, Any, List, Optional
from app.services.language_service import language_service

class IntentService:
    def __init__(self):
        self.provinces = {
            "Siem Reap": ["siem reap", "angkor", "សៀមរាប", "អង្គរ", "បាយ័ន", "តាព្រហ្ម", "បន្ទាយស្រី"],
            "Phnom Penh": ["phnom penh", "capital", "ភ្នំពេញ", "រាជធានី", "វាំង", "សារមន្ទីរជាតិ"],
            "Preah Sihanouk": ["sihanoukville", "sihanouk", "koh rong", "preah sihanouk", "ព្រះសីហនុ", "កំពង់សោម", "កោះរ៉ុង", "កោះរ៉ុងសន្លឹម"],
            "Kampot": ["kampot", "bokor", "កំពត", "បូកគោ", "ម្រេចកំពត"],
            "Battambang": ["battambang", "បាត់ដំបង", "រថភ្លើងឫស្សី", "ភ្នំសំពៅ"],
            "Kep": ["kep", "crab market", "កែប", "ផ្សារក្តាម"],
            "Mondulkiri": ["mondulkiri", "bousra", "មណ្ឌលគិរី", "ប៊ូស្រា", "ដំរី"],
            "Ratanakiri": ["ratanakiri", "yeak laom", "រតនគិរី", "យក្សឡោម"],
            "Koh Kong": ["koh kong", "cardamom", "កោះកុង", "ក្រវាញ"],
            "Preah Vihear": ["preah vihear", "ព្រះវិហារ"],
            "Kampong Thom": ["kampong thom", "sambor prei kuk", "កំពង់ធំ", "សំបូរព្រៃគុក"],
            "Kandal": ["kandal", "oudong", "koh dach", "កណ្តាល", "ឧដុង្គ", "កោះដាច់"]
        }
        
        self.intent_patterns = {
            "greeting": [
                r"^\s*(hi|hello|hey|greetings|good\s+morning|good\s+afternoon|good\s+evening|សួស្តី|ជំរាបសួរ)\b"
            ],
            "weather": [
                r"\b(weather|rain|temperature|forecast|climate|temp|degrees|humidity|sunny|storm|អាកាសធាតុ|ភ្លៀង|ក្តៅ|រងា|ព្យុះ|ពពក)\b"
            ],
            "currency": [
                r"\b(riel|khr|exchange|convert|currency|rate|usd\s+to\s+khr|khr\s+to\s+usd|dollar|riel\s+rate|money|cash|ប្តូរលុយ|រៀល|ដុល្លារ|អត្រាប្តូរប្រាក់|រូបិយប័ណ្ណ)\b"
            ],
            "itinerary": [
                r"\b(itinerary|plan|trip\s+plan|schedule|tour|route|day\s+1|day\s+2|day\s+3|day\s+4|day\s+5|3\s*day|4\s*day|5\s*day|multi-day|គម្រោង|ដំណើរកម្សាន្ត|ដើរលេង|គម្រោងដើរលេង)\b"
            ],
            "recommendation": [
                r"\b(recommend|recommendation|where\s+to\s+go|best\s+places|must\s+visit|top\s+attractions|things\s+to\s+do|suggest|highlight|suggested|ណែនាំ|កន្លែងណា|គួរទៅណា|កន្លែងល្បី|កន្លែងស្អាត)\b"
            ],
            "events": [
                r"\b(event|events|festival|festivals|holiday|water\s+festival|bon\s+om\s+touk|marathon|new\s+year|sankranta|pchum\s+ben|ពិធីបុណ្យ|បុណ្យ|អុំទូក|ចូលឆ្នាំ|ភ្ជុំបិណ្ឌ|ព្រឹត្តិការណ៍)\b"
            ],
            "culture": [
                r"\b(culture|tradition|heritage|history|apsara|shadow\s+theatre|sbek\s+thom|chapei|buddhism|monk|dress\s+code|pagoda|temple\s+rule|វប្បធម៌|ប្រពៃណី|ប្រវត្តិ|របាំ|អប្សរា|ចាប៉ី|ព្រះពុទ្ធសាសនា|វត្ត)\b"
            ],
            "food": [
                r"\b(food|eat|restaurant|dish|dishes|amok|lok\s+lak|kuy\s+teav|noodles|crab|seafood|street\s+food|dining|cuisine|ម្ហូប|អាហារ|ញ៉ាំ|ហាងបាយ|អាម៉ុក|ឡុកឡាក់|គុយទាវ|នំបញ្ចុក|ក្តាម)\b"
            ],
            "transportation": [
                r"\b(transport|transportation|how\s+to\s+get|taxi|bus|train|flight|ferry|speed\s+boat|tuk\s*tuk|passapp|grab|rent|drive|airport|ធ្វើដំណើរ|ជិះអី|ឡានក្រុង|តាក់ស៊ី|ទូក|កាណូត|យន្តហោះ)\b"
            ],
            "safety": [
                r"\b(safety|safe|emergency|police|hospital|doctor|clinic|scam|sim\s*card|internet|vaccine|tap\s*water|សុវត្ថិភាព|អាសន្ន|ប៉ូលិស|មន្ទីរពេទ្យ|ស៊ីមកាត|ទឹកស្អាត|គ្រោះថ្នាក់)\b"
            ],
            "place_search": [
                r"\b(where\s+is|location\s+of|tell\s+me\s+about|information\s+about|find|opening\s+hours|ticket|price\s+of|entrance\s+fee|នៅឯណា|ទីតាំង|តម្លៃសំបុត្រ|ម៉ោងបើក)\b"
            ]
        }

    def detect_intent(self, text: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Detect intent and extract all relevant entities from user message.
        Supports: general_qa, place_search, recommendation, itinerary, weather,
                  currency, events, culture, food, transportation, safety.
        """
        lowered = text.lower().strip()
        detected_lang = language_service.detect_language(text)
        entities = self.extract_entities(text)
        
        detected_intent = "general_qa"
        matched_pattern = False
        
        for intent_name, patterns in self.intent_patterns.items():
            if any(re.search(p, lowered) for p in patterns):
                detected_intent = intent_name
                matched_pattern = True
                break

        # Priority Rule: If duration or budget is extracted along with travel words, map to itinerary
        if entities.get("duration") and any(w in lowered for w in ["trip", "plan", "itinerary", "visit", "to", "in", "day", "days", "ថ្ងៃ", "ដើរលេង"]):
            detected_intent = "itinerary"
        elif entities.get("budget") and any(w in lowered for w in ["trip", "plan", "itinerary", "days", "visit"]):
            detected_intent = "itinerary"

        confidence = 0.95 if matched_pattern else 0.75
        if detected_intent == "general_qa" and (entities.get("destination") or entities.get("category")):
            confidence = 0.85

        entities["language"] = detected_lang

        return {
            "intent": detected_intent,
            "confidence": confidence,
            "entities": entities
        }

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extract entities:
        - destination
        - province
        - duration (int)
        - budget (float)
        - category
        - travel_style
        - date
        - time
        - number_of_people (int)
        - language
        """
        lowered = text.lower()
        entities = {}
        
        # 1. Destination / Province Extraction
        for prov_name, aliases in self.provinces.items():
            if any(alias in lowered for alias in aliases):
                entities["destination"] = prov_name
                entities["province"] = prov_name
                break

        # 2. Duration Extraction (e.g., 3-day, 4 days, 5 days, ៣ ថ្ងៃ)
        duration_match = re.search(r'(\d+|១|២|៣|៤|៥|៦|៧|៨|៩|១០)\s*(?:-|–)?\s*(?:day|days|night|nights|ថ្ងៃ|យប់)', lowered)
        if duration_match:
            raw_num = duration_match.group(1)
            kh_digits = {'១': '1', '២': '2', '៣': '3', '៤': '4', '៥': '5', '៦': '6', '៧': '7', '៨': '8', '៩': '9', '១០': '10'}
            num_str = kh_digits.get(raw_num, raw_num)
            try:
                days_int = int(num_str)
                entities["duration"] = days_int
                entities["duration_days"] = days_int
            except Exception:
                pass

        # 3. Budget Extraction (e.g., $300, 300$, under $300, 300 USD, 300 dollars, ៣០០ ដុល្លារ)
        budget_match = (
            re.search(r'(?:under|below|less\s+than|max|budget\s+of)?\s*\$\s*(\d+(?:\.\d+)?)', lowered) or
            re.search(r'(\d+(?:\.\d+)?)\s*\$', lowered) or
            re.search(r'(\d+(?:\.\d+)?)\s*(?:usd|dollars?|ដុល្លារ)', lowered)
        )
        if budget_match:
            try:
                entities["budget"] = float(budget_match.group(1))
                entities["budget_usd"] = float(budget_match.group(1))
            except Exception:
                pass

        # 4. Category Extraction
        category_keywords = {
            "temple": ["temple", "temples", "angkor", "ancient", "ruins", "ប្រាសាទ", "អង្គរ"],
            "beach": ["beach", "island", "sea", "snorkeling", "diving", "ឆ្នេរ", "កោះ", "សមុទ្រ"],
            "museum": ["museum", "gallery", "exhibit", "history", "សារមន្ទីរ"],
            "restaurant": ["restaurant", "food", "dining", "cafe", "meal", "breakfast", "lunch", "dinner", "ហាងបាយ", "ភោជនីយដ្ឋាន"],
            "activity": ["activity", "tour", "circus", "bamboo train", "kayak", "trekking", "ស្ទូចត្រី", "សៀក"],
            "culture": ["culture", "dance", "apsara", "puppet", "heritage", "វប្បធម៌", "របាំ"],
            "festival": ["festival", "event", "water festival", "new year", "បុណ្យ"]
        }
        for cat_name, kws in category_keywords.items():
            if any(kw in lowered for kw in kws):
                entities["category"] = cat_name
                break

        # 5. Travel Style
        if any(w in lowered for w in ["luxury", "resort", "fine dining", "5 star", "high-end", "ប្រណីត"]):
            entities["travel_style"] = "luxury"
        elif any(w in lowered for w in ["budget", "backpacker", "cheap", "hostel", "low cost", "សន្សំសំចៃ"]):
            entities["travel_style"] = "budget"
        elif any(w in lowered for w in ["culture", "heritage", "history", "temples", "វប្បធម៌"]):
            entities["travel_style"] = "culture"
        elif any(w in lowered for w in ["adventure", "trekking", "nature", "jungle", "kayak", "ផ្សងព្រេង"]):
            entities["travel_style"] = "adventure"
        elif any(w in lowered for w in ["relax", "chill", "peaceful", "quiet", "beach", "លំហែ"]):
            entities["travel_style"] = "relaxation"

        # 6. Number of people
        people_match = re.search(r'(\d+)\s*(?:people|persons?|travelers?|adults?|guests?|នាក់)', lowered)
        if people_match:
            try:
                entities["number_of_people"] = int(people_match.group(1))
            except Exception:
                pass

        # 7. Time / Date extraction
        if "tomorrow" in lowered or "ថ្ងៃស្អែក" in lowered:
            entities["date"] = "tomorrow"
        elif "today" in lowered or "ថ្ងៃនេះ" in lowered:
            entities["date"] = "today"
        elif "this weekend" in lowered or "ចុងសប្តាហ៍នេះ" in lowered:
            entities["date"] = "this_weekend"

        return entities

intent_service = IntentService()

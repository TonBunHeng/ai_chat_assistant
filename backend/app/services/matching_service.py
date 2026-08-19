import json
import threading
from typing import Dict, Any, List, Optional, Tuple
from app.core.config import settings
from app.services.tourism_service import tourism_service
from app.services.embedding_service import embedding_service

try:
    # pyrefly: ignore [missing-import]
    from rapidfuzz import fuzz
    HAS_RAPIDFUZZ = True
except ImportError:
    HAS_RAPIDFUZZ = False

class SimilarityMatchingService:
    def __init__(self):
        self._item_embeddings: List[Tuple[Dict[str, Any], Any, str]] = []
        self._is_indexed = False
        self._lock = threading.Lock()

    def index_datasets(self, force: bool = False):
        """Index all JSON items for semantic and fuzzy similarity matching."""
        with self._lock:
            if self._is_indexed and not force:
                return

            all_items = tourism_service.get_all_items()
            self._item_embeddings = []

        for item in all_items:
            # Build comprehensive text profile for semantic indexing
            text_profile = self._build_item_profile_text(item)
            vec = embedding_service.encode(text_profile)
            self._item_embeddings.append((item, vec, text_profile))

        self._is_indexed = True

    def _build_item_profile_text(self, item: Dict[str, Any]) -> str:
        """Create rich searchable text for semantic embedding."""
        parts = []
        if item.get("name"):
            parts.append(str(item["name"]))
        if item.get("name_km"):
            parts.append(str(item["name_km"]))
        if item.get("category"):
            parts.append(f"Category: {item['category']}")
        if item.get("province"):
            parts.append(f"Province: {item['province']}")
        if item.get("province_km"):
            parts.append(f"Province: {item['province_km']}")
        if item.get("description"):
            parts.append(str(item["description"]))
        if item.get("description_km"):
            parts.append(str(item["description_km"]))
        if item.get("tags") and isinstance(item["tags"], list):
            parts.append("Tags: " + ", ".join(item["tags"]))
        if item.get("travel_tips") and isinstance(item["travel_tips"], list):
            parts.append("Tips: " + ", ".join(item["travel_tips"]))

        return " | ".join(parts)

    NON_PLACE_QUERIES = {
        "hi", "hello", "hey", "good morning", "good afternoon", "good evening", "greetings",
        "what is cambodia", "tell me about cambodia", "about cambodia", "cambodia", "cambodia country",
        "who are you", "what can you do", "help", "thanks", "thank you", "bye", "goodbye",
        "what is cambodia ?", "tell me about cambodia ?", "about cambodia ?",
        "សួស្តី", "ជំរាបសួរ", "កម្ពុជា", "តើអ្វីទៅជាកម្ពុជា", "ប្រាប់អំពីកម្ពុជា"
    }

    def compute_fuzzy_score(self, query: str, item: Dict[str, Any]) -> float:
        """Compute fuzzy similarity score (0.0 to 1.0) with exact word and token matching."""
        import re
        import difflib
        
        clean_q = re.sub(r'[^\w\s\u1780-\u17FF]', '', query.lower()).strip()
        if not clean_q or len(clean_q) < 3 or clean_q in self.NON_PLACE_QUERIES:
            return 0.0

        name_en = str(item.get("name") or "").lower().strip()
        name_km = str(item.get("name_km") or "").lower().strip()
        
        scores = []
        
        # 1. Check exact or clean full name match
        for name in [name_en, name_km]:
            if not name:
                continue
            if clean_q == name:
                return 1.0
            # If place name is contained with word boundaries in query (e.g. "tell me about Angkor Wat")
            if len(name) >= 4 and (f" {name} " in f" {clean_q} " or clean_q.startswith(name) or clean_q.endswith(name)):
                scores.append(0.95)
            # If query is contained in place name (e.g. "angkor wat" in "angkor wat temple")
            elif len(clean_q) >= 4 and (f" {clean_q} " in f" {name} " or name.startswith(clean_q)):
                len_ratio = len(clean_q) / len(name)
                scores.append(0.80 + 0.18 * len_ratio)
            else:
                # Sequence matcher on whole name
                ratio = difflib.SequenceMatcher(None, clean_q, name).ratio()
                if ratio >= 0.75:
                    scores.append(ratio)

        # 2. Token overlap on significant words
        q_tokens = set(clean_q.split())
        for name in [name_en, name_km]:
            if not name:
                continue
            n_tokens = set(name.split())
            if n_tokens and n_tokens.issubset(q_tokens):
                scores.append(0.90)
            elif q_tokens and n_tokens and len(q_tokens & n_tokens) >= 2:
                overlap = len(q_tokens & n_tokens) / len(n_tokens)
                if overlap >= 0.66:
                    scores.append(0.75 + 0.20 * overlap)

        return max(scores) if scores else 0.0

    def find_best_match(
        self,
        query: str,
        threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Check query against local JSON files using semantic vector similarity + fuzzy matching.
        If top match similarity >= threshold (default 80-90%), return match_found=True and JSON snippet.
        """
        import re
        clean_q = re.sub(r'[^\w\s\u1780-\u17FF]', '', query.lower()).strip()
        if not clean_q or len(clean_q) < 3 or clean_q in self.NON_PLACE_QUERIES:
            return {
                "match_found": False,
                "similarity_score": 0.0,
                "matched_item": None,
                "formatted_snippet": ""
            }

        if not self._is_indexed:
            self.index_datasets()

        if not self._item_embeddings:
            return {
                "match_found": False,
                "similarity_score": 0.0,
                "matched_item": None,
                "formatted_snippet": ""
            }

        effective_threshold = threshold if threshold is not None else settings.SIMILARITY_THRESHOLD

        # Encode user query
        query_vec = embedding_service.encode(query)

        best_score = 0.0
        best_item = None

        for item, item_vec, text_profile in self._item_embeddings:
            # 1. Fuzzy String Similarity Score (0.0 to 1.0)
            fuz_score = self.compute_fuzzy_score(query, item)

            # 2. Semantic Embedding Cosine Similarity Score (0.0 to 1.0)
            sem_score = embedding_service.compute_similarity(query_vec, item_vec)

            # Only trust semantic score if there is some token/fuzzy relevance
            if fuz_score >= 0.75:
                score = max(sem_score, fuz_score)
            else:
                score = fuz_score

            if score > best_score:
                best_score = score
                best_item = item

        match_found = best_score >= effective_threshold

        formatted_snippet = ""
        if match_found and best_item:
            formatted_snippet = self._format_snippet(best_item)

        return {
            "match_found": match_found,
            "similarity_score": round(best_score, 4),
            "matched_item": best_item if match_found else None,
            "formatted_snippet": formatted_snippet
        }

    def _format_snippet(self, item: Dict[str, Any]) -> str:
        """Format the matched JSON item into a structured clean text block for Gemini AI."""
        lines = []
        name = item.get("name")
        name_km = item.get("name_km")
        title = f"{name} ({name_km})" if name_km else name
        lines.append(f"NAME: {title}")

        if item.get("category"):
            lines.append(f"CATEGORY: {item['category']}")
        if item.get("province"):
            prov = item.get("province")
            if item.get("province_km"):
                prov += f" ({item['province_km']})"
            lines.append(f"PROVINCE/LOCATION: {prov}")
        if item.get("description"):
            lines.append(f"DESCRIPTION (EN): {item['description']}")
        if item.get("description_km"):
            lines.append(f"DESCRIPTION (KM): {item['description_km']}")
        if item.get("opening_hours"):
            lines.append(f"OPENING HOURS: {item['opening_hours']}")
        if item.get("entrance_fee"):
            lines.append(f"ENTRANCE FEE: {item['entrance_fee']}")
        if item.get("best_time_to_visit"):
            lines.append(f"BEST TIME TO VISIT: {item['best_time_to_visit']}")
        if item.get("travel_tips"):
            tips = item["travel_tips"]
            lines.append(f"TRAVEL TIPS: {', '.join(tips) if isinstance(tips, list) else tips}")

        return "\n".join(lines)

matching_service = SimilarityMatchingService()

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

    def compute_fuzzy_score(self, query: str, item: Dict[str, Any]) -> float:
        """Compute fuzzy similarity score (0.0 to 1.0) using rapidfuzz or string matching."""
        query_lower = query.lower().strip()
        name_en = str(item.get("name") or "").lower()
        name_km = str(item.get("name_km") or "").lower()
        desc_en = str(item.get("description") or "").lower()
        desc_km = str(item.get("description_km") or "").lower()

        scores = []

        if HAS_RAPIDFUZZ:
            # Direct title matching
            if name_en:
                scores.append(fuzz.ratio(query_lower, name_en) / 100.0)
                scores.append(fuzz.partial_ratio(query_lower, name_en) / 100.0)
                scores.append(fuzz.token_set_ratio(query_lower, name_en) / 100.0)
            if name_km:
                scores.append(fuzz.ratio(query_lower, name_km) / 100.0)
                scores.append(fuzz.partial_ratio(query_lower, name_km) / 100.0)
                scores.append(fuzz.token_set_ratio(query_lower, name_km) / 100.0)
            if desc_en:
                scores.append(fuzz.partial_ratio(query_lower, desc_en) / 100.0 * 0.85)
            if desc_km:
                scores.append(fuzz.partial_ratio(query_lower, desc_km) / 100.0 * 0.85)
        else:
            # Fallback string matching if rapidfuzz is missing
            for target in [name_en, name_km]:
                if target and (query_lower in target or target in query_lower):
                    len_ratio = min(len(query_lower), len(target)) / max(len(query_lower), len(target))
                    scores.append(0.8 + 0.2 * len_ratio)

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
            # 1. Semantic Embedding Cosine Similarity Score (0.0 to 1.0)
            sem_score = embedding_service.compute_similarity(query_vec, item_vec)

            # 2. Fuzzy String Similarity Score (0.0 to 1.0)
            fuz_score = self.compute_fuzzy_score(query, item)

            # Hybrid score
            hybrid_score = max(sem_score, fuz_score)

            if fuz_score >= 0.85:
                hybrid_score = max(hybrid_score, fuz_score)

            if hybrid_score > best_score:
                best_score = hybrid_score
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

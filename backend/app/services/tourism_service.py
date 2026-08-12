import os
import json
from typing import List, Dict, Any, Optional
from app.core.config import settings

class TourismService:
    def __init__(self, data_dir: str = settings.DATA_DIR):
        self.data_dir = data_dir
        self.datasets: Dict[str, List[Dict[str, Any]]] = {}
        self.all_items: List[Dict[str, Any]] = []
        self.load_all_datasets()

    def load_all_datasets(self):
        """Load all 16 JSON datasets into memory."""
        self.datasets = {}
        self.all_items = []
        
        if not os.path.exists(self.data_dir):
            return
            
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                category_name = filename[:-5]
                filepath = os.path.join(self.data_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            self.datasets[category_name] = data
                            for item in data:
                                # Ensure dataset category tag
                                item["_source_file"] = category_name
                                self.all_items.append(item)
                except Exception as e:
                    print(f"Error loading tourism dataset {filename}: {e}")

    def get_dataset(self, name: str) -> List[Dict[str, Any]]:
        return self.datasets.get(name, [])

    def get_all_items(self) -> List[Dict[str, Any]]:
        return self.all_items

    def find_items_by_province(self, province_name: str) -> List[Dict[str, Any]]:
        """Filter tourism items by province name (English or Khmer)."""
        target = province_name.lower()
        results = []
        for item in self.all_items:
            prov_en = (item.get("province") or "").lower()
            prov_km = (item.get("province_km") or "").lower()
            if target in prov_en or target in prov_km or prov_en in target:
                results.append(item)
        return results

    def find_items_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Filter items by category (e.g. 'Heritage', 'Beach', 'Food', 'Temple')."""
        target = category.lower()
        results = []
        for item in self.all_items:
            cat = (item.get("category") or "").lower()
            if target in cat:
                results.append(item)
        return results

    def search_keyword(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Keyword matching across name, description, tags, province, and tips."""
        query_lower = query.lower()
        tokens = [t for t in query_lower.split() if len(t) > 1]
        
        scored_items = []
        for item in self.all_items:
            score = 0
            name_en = (item.get("name") or "").lower()
            name_km = (item.get("name_km") or "").lower()
            desc_en = (item.get("description") or "").lower()
            desc_km = (item.get("description_km") or "").lower()
            prov_en = (item.get("province") or "").lower()
            prov_km = (item.get("province_km") or "").lower()
            tags = [t.lower() for t in item.get("tags", [])]
            
            # Exact or substring match in name (both directions for Khmer unspaced text)
            if (name_en and (query_lower in name_en or name_en in query_lower)) or \
               (name_km and (query_lower in name_km or name_km in query_lower)):
                score += 15
            if (prov_en and (query_lower in prov_en or prov_en in query_lower)) or \
               (prov_km and (query_lower in prov_km or prov_km in query_lower)):
                score += 8
            if (desc_en and query_lower in desc_en) or (desc_km and query_lower in desc_km):
                score += 5
                
            # Token & Tag match
            for token in tokens:
                if (name_en and token in name_en) or (name_km and (token in name_km or name_km in token)):
                    score += 5
                if (prov_en and token in prov_en) or (prov_km and (token in prov_km or prov_km in token)):
                    score += 3
                if any(token in tag or tag in token for tag in tags):
                    score += 4
                if (desc_en and token in desc_en) or (desc_km and token in desc_km):
                    score += 2
                    
            if score > 0:
                scored_items.append((score, item))
                
        scored_items.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in scored_items[:limit]]

tourism_service = TourismService()

import math
from typing import List, Dict, Any, Optional
from app.services.tourism_service import tourism_service

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points in kilometers."""
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

class PlacesService:
    def get_all_places(self, category: Optional[str] = None, province: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve places with coordinates and Google Maps links."""
        items = tourism_service.get_all_items()
        results = []
        for item in items:
            cat = str(item.get("category", "")).lower()
            prov = str(item.get("province", "")).lower()
            tags = [str(t).lower() for t in item.get("tags", [])]
            
            if category and category.lower() not in cat and not any(category.lower() in t for t in tags):
                continue
            if province and province.lower() not in prov and province.lower() not in str(item.get("province_km", "")).lower():
                continue
            
            enhanced = dict(item)
            lat = item.get("latitude")
            lon = item.get("longitude")
            name = item.get("name", "Cambodia")
            
            if lat and lon:
                enhanced["google_maps_url"] = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            else:
                enhanced["google_maps_url"] = f"https://www.google.com/maps/search/?api=1&query={name.replace(' ', '+')}+Cambodia"
                
            results.append(enhanced)
        return results

    def get_place_by_id(self, place_id: str) -> Optional[Dict[str, Any]]:
        """Get single place by ID with enriched details."""
        item = tourism_service.get_item_by_id(place_id)
        if not item:
            return None
        enhanced = dict(item)
        lat = item.get("latitude")
        lon = item.get("longitude")
        name = item.get("name", "Cambodia")
        if lat and lon:
            enhanced["google_maps_url"] = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        else:
            enhanced["google_maps_url"] = f"https://www.google.com/maps/search/?api=1&query={name.replace(' ', '+')}+Cambodia"
            
        enhanced["related_places"] = self.get_related_places(place_id, limit=3)
        return enhanced

    def get_popular_places(self, limit: int = 6) -> List[Dict[str, Any]]:
        """Get top popular Cambodian attractions."""
        all_places = self.get_all_places()
        # Prioritize UNESCO, world heritage, and famous temples
        scored = []
        for p in all_places:
            score = 10
            tags = [t.lower() for t in p.get("tags", [])]
            name = p.get("name", "").lower()
            if "unesco" in tags:
                score += 20
            if "angkor" in name or "wat" in name:
                score += 15
            if "palace" in name or "museum" in name:
                score += 10
            scored.append((score, p))
            
        scored.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in scored[:limit]]

    def get_related_places(self, place_id: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Get related places in the same province or category."""
        target = tourism_service.get_item_by_id(place_id)
        if not target:
            return []
            
        target_prov = (target.get("province") or "").lower()
        target_cat = (target.get("category") or "").lower()
        
        all_places = self.get_all_places()
        related = []
        
        for p in all_places:
            if str(p.get("id")) == str(place_id):
                continue
            prov = (p.get("province") or "").lower()
            cat = (p.get("category") or "").lower()
            
            score = 0
            if target_prov and target_prov in prov:
                score += 10
            if target_cat and target_cat in cat:
                score += 8
                
            if score > 0:
                related.append((score, p))
                
        related.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in related[:limit]]

    def find_nearby_places(self, lat: float, lon: float, max_distance_km: float = 25.0, limit: int = 6) -> List[Dict[str, Any]]:
        """Find places closest to specified coordinates."""
        places = self.get_all_places()
        scored = []
        for p in places:
            p_lat = p.get("latitude")
            p_lon = p.get("longitude")
            if p_lat is not None and p_lon is not None:
                dist = haversine_distance(lat, lon, p_lat, p_lon)
                if dist <= max_distance_km:
                    p_copy = dict(p)
                    p_copy["distance_km"] = dist
                    p_copy["estimated_travel_time_tuk_tuk"] = f"{int(dist * 2.5 + 5)} mins"
                    scored.append((dist, p_copy))

        scored.sort(key=lambda x: x[0])
        return [p for _, p in scored[:limit]]

places_service = PlacesService()

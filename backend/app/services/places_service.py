import math
from typing import List, Dict, Any, Optional
from app.services.tourism_service import tourism_service

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points in kilometers."""
    R = 6371.0  # Earth radius in kilometers
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
            cat = item.get("category", "")
            prov = item.get("province", "")
            if category and category.lower() not in cat.lower():
                continue
            if province and province.lower() not in prov.lower():
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
        """Get single place by ID."""
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
        return enhanced

    def find_nearby_places(self, lat: float, lon: float, max_distance_km: float = 25.0, limit: int = 6) -> List[Dict[str, Any]]:
        """Find places in Cambodia closest to the specified coordinates."""
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

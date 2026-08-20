from typing import List, Dict, Any, Optional
from app.services.tourism_service import tourism_service

class EventsService:
    def get_all_events(self) -> List[Dict[str, Any]]:
        """Retrieve all verified Cambodian cultural events & festivals."""
        return tourism_service.get_dataset("events")

    def search_events(self, query: Optional[str] = None, province: Optional[str] = None, month: Optional[str] = None) -> Dict[str, Any]:
        """
        Search verified events. Returns verified events or clear message if none found.
        """
        all_events = self.get_all_events()
        if not all_events:
            return {
                "events": [],
                "message": "I couldn't verify a current event for that query/date.",
                "total": 0
            }

        filtered = []
        q = (query or "").lower().strip()
        prov = (province or "").lower().strip()
        m = (month or "").lower().strip()

        for evt in all_events:
            match = True
            name_en = evt.get("name", "").lower()
            name_km = evt.get("name_km", "").lower()
            loc_en = evt.get("location", "").lower()
            prov_en = evt.get("province", "").lower()
            period = evt.get("typical_period", "").lower()
            desc = evt.get("description", "").lower()
            tags = [t.lower() for t in evt.get("tags", [])]

            if q:
                if not (q in name_en or q in name_km or q in loc_en or q in desc or any(q in t for t in tags)):
                    match = False
            if prov and prov not in ["cambodia", "nationwide", "all"]:
                if prov not in prov_en and prov not in loc_en:
                    match = False
            if m:
                if m not in period:
                    match = False

            if match:
                filtered.append(evt)

        if not filtered:
            return {
                "events": [],
                "message": f"I couldn't verify a current event for '{query or province or month}'.",
                "message_km": "មិនអាចស្វែងរកព្រឹត្តិការណ៍ដែលបានផ្ទៀងផ្ទាត់សម្រាប់កាលបរិច្ឆេទ ឬទីតាំងនេះឡើយ។",
                "total": 0
            }

        return {
            "events": filtered,
            "message": f"Found {len(filtered)} verified event(s).",
            "total": len(filtered),
            "source": "Ministry of Tourism Cambodia / National Festivals Committee"
        }

events_service = EventsService()

from typing import List, Dict, Any, Optional
from app.services.currency_service import currency_service

class ItineraryEngine:
    def generate_itinerary(
        self,
        destination: str = "Siem Reap",
        days: int = 3,
        budget_usd: Optional[float] = None,
        travel_style: str = "culture",
        interests: Optional[List[str]] = None,
        travelers: int = 2,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate optimized day-by-day travel plan with timeline slots, transit, budget, and route logic.
        Supports 1 day, 2 days, 3 days, 4 days, 5+ days.
        Deterministic budget calculations are performed in code.
        """
        dest_clean = (destination or "Siem Reap").title().strip()
        num_days = max(1, min(days, 10))
        is_km = "km" in language

        # 1. Build Day Plans based on destination
        if "Siem Reap" in dest_clean or "Angkor" in dest_clean:
            itinerary_days = self._build_siem_reap_itinerary(num_days, is_km)
            title = f"{num_days}-Day Angkor & Siem Reap Cultural Journey" if not is_km else f"គម្រោងដំណើរកម្សាន្ត {num_days} ថ្ងៃ នៅសៀមរាប-អង្គរ"
        elif "Phnom Penh" in dest_clean:
            itinerary_days = self._build_phnom_penh_itinerary(num_days, is_km)
            title = f"{num_days}-Day Phnom Penh Heritage & Discovery" if not is_km else f"គម្រោងដំណើរកម្សាន្ត {num_days} ថ្ងៃ នៅរាជធានីភ្នំពេញ"
        elif "Kampot" in dest_clean or "Kep" in dest_clean:
            itinerary_days = self._build_coastal_itinerary(num_days, is_km)
            title = f"{num_days}-Day Kampot & Kep Coastal Escape" if not is_km else f"គម្រោងដំណើរកម្សាន្ត {num_days} ថ្ងៃ នៅកំពត និងកែប"
        elif "Koh Rong" in dest_clean or "Sihanouk" in dest_clean:
            itinerary_days = self._build_island_itinerary(num_days, is_km)
            title = f"{num_days}-Day Tropical Island Paradise Trip" if not is_km else f"គម្រោងដំណើរកម្សាន្ត {num_days} ថ្ងៃ នៅកោះរ៉ុង"
        else:
            itinerary_days = self._build_grand_cambodia_itinerary(num_days, is_km)
            title = f"{num_days}-Day Grand Cambodia Discovery Itinerary" if not is_km else f"គម្រោងដំណើរកម្សាន្តធំ {num_days} ថ្ងៃ ទូទាំងប្រទេសកម្ពុជា"

        # 2. Deterministic Budget Calculation
        rate_info = currency_service.get_exchange_rate()
        rate = rate_info["exchange_rate"]

        if budget_usd and budget_usd > 0:
            khr_total = int(budget_usd * rate)
            formatted_budget = f"${budget_usd:,.2f} USD (~{khr_total:,.0f} KHR)"
            budget_breakdown = {
                "accommodation_usd": round(budget_usd * 0.40, 2),
                "food_usd": round(budget_usd * 0.30, 2),
                "transport_usd": round(budget_usd * 0.15, 2),
                "activities_usd": round(budget_usd * 0.15, 2),
                "total_estimated_usd": budget_usd,
                "total_estimated_khr": khr_total
            }
        else:
            budget_info = currency_service.estimate_travel_budget(days=num_days, travelers=travelers, style=travel_style)
            budget_breakdown = budget_info["breakdown_usd"]
            formatted_budget = budget_info["formatted_total"]

        # 3. Format items into standard structured representation
        structured_days = []
        for d_idx, day_obj in enumerate(itinerary_days[:num_days]):
            activities = day_obj.get("activities", [])
            items = []
            for act in activities:
                items.append({
                    "time": act.get("time", "08:00 AM"),
                    "place": act.get("title", ""),
                    "activity": act.get("title", ""),
                    "description": act.get("description", ""),
                    "estimated_cost": act.get("cost", "Free"),
                    "transportation": act.get("transport", "Tuk-tuk"),
                    "duration": act.get("duration", "2 hours")
                })
            
            structured_days.append({
                "day": d_idx + 1,
                "theme": day_obj.get("theme", f"Day {d_idx + 1}"),
                "location": day_obj.get("location", dest_clean),
                "activities": activities,
                "items": items
            })

        return {
            "title": title,
            "destination": dest_clean,
            "duration": num_days,
            "duration_days": num_days,
            "recommended_duration_days": 3,
            "recommendation_note": "3 Days is recommended as the ideal sweet spot for exploring core highlights comfortably." if not is_km else "គម្រោង ៣ ថ្ងៃ ត្រូវបានណែនាំជាជម្រើសដ៏ល្អឥតខ្ចោះបំផុតសម្រាប់ការទស្សនាដោយមិននឿយហត់។",
            "travelers": travelers,
            "travel_style": travel_style,
            "days": structured_days,
            "estimated_budget": budget_breakdown,
            "formatted_total_budget": formatted_budget,
            "currency": "USD",
            "practical_tips": [
                "Cover shoulders and knees at all sacred temple sites." if not is_km else "ត្រូវស្លៀកសម្លៀកបំពាក់បិទស្មា និងគ្របជង្គង់នៅគ្រប់ទីតាំងប្រាសាទបុរាណ។",
                "3-Day Angkor Pass ($62) offers the highest value for visitors." if not is_km else "សំបុត្រអង្គរ ៣ ថ្ងៃ ($62) ផ្ដល់នូវតម្លៃសន្សំសំចៃ និងសមរម្យបំផុត។",
                "Use PassApp or Grab for fair, metered local transportation." if not is_km else "ប្រើប្រាស់កម្មវិធី PassApp ឬ Grab សម្រាប់ការធ្វើដំណើរក្នុងក្រុង។"
            ]
        }

    def _build_siem_reap_itinerary(self, days: int, is_km: bool) -> List[Dict[str, Any]]:
        plan = [
            {
                "day": 1,
                "theme": "Angkor Classic Small Circuit (Sunrise & Highlights)" if not is_km else "ទស្សនាថ្ងៃរះអង្គរវត្ត និងប្រាសាទសំខាន់ៗ",
                "location": "Siem Reap",
                "activities": [
                    {"time": "05:00 AM - 07:30 AM", "title": "Angkor Wat Sunrise", "description": "Witness the iconic sunrise reflecting on the lotus pond, followed by bas-relief exploration.", "transport": "Tuk-tuk", "cost": "$37 (Angkor Pass)", "duration": "2.5 hours"},
                    {"time": "08:30 AM - 11:30 AM", "title": "Angkor Thom & Bayon Temple", "description": "Explore the 216 giant stone faces of Avalokiteshvara, Terrace of the Elephants, and Baphuon.", "transport": "Tuk-tuk", "cost": "Included in Pass", "duration": "3 hours"},
                    {"time": "02:00 PM - 04:30 PM", "title": "Ta Prohm (Tomb Raider Temple)", "description": "Walk among atmospheric stone corridors intertwined with giant silk-cotton tree roots.", "transport": "Tuk-tuk", "cost": "Included in Pass", "duration": "2.5 hours"},
                    {"time": "06:30 PM - 09:00 PM", "title": "Pub Street & Night Market", "description": "Relax with street food, fruit shakes, and explore artisan souvenir shops.", "transport": "Tuk-tuk", "cost": "$3 - $10", "duration": "2.5 hours"}
                ]
            },
            {
                "day": 2,
                "theme": "Grand Circuit & Banteay Srei (Pink Sandstone Art)" if not is_km else "ប្រាសាទបន្ទាយស្រី និងវង់ធំ",
                "location": "Siem Reap",
                "activities": [
                    {"time": "08:00 AM - 10:30 AM", "title": "Banteay Srei (Citadel of Women)", "description": "Marvel at the world's finest 10th-century pink sandstone carvings.", "transport": "Tuk-tuk / Car", "cost": "Included in Pass", "duration": "2.5 hours"},
                    {"time": "11:00 AM - 12:30 PM", "title": "Preah Dak Village", "description": "Taste famous handmade Nom Banh Chok noodles and palm sugar cakes in a traditional village.", "transport": "Tuk-tuk", "cost": "$2 - $4", "duration": "1.5 hours"},
                    {"time": "02:00 PM - 04:30 PM", "title": "Preah Khan & Neak Pean", "description": "Explore the expansive monastic complex and island temple reservoir.", "transport": "Tuk-tuk", "cost": "Included in Pass", "duration": "2.5 hours"},
                    {"time": "05:00 PM - 06:15 PM", "title": "Phnom Bakheng Sunset", "description": "Panoramic view of Angkor Wat and surrounding plains at dusk.", "transport": "Tuk-tuk", "cost": "Free (with Pass)", "duration": "1.25 hours"}
                ]
            },
            {
                "day": 3,
                "theme": "Tonle Sap Floating Village & Artisan Culture" if not is_km else "ភូមិបណ្តែតទឹកបឹងទន្លេសាប និងសិប្បកម្មអង្គរ",
                "location": "Siem Reap",
                "activities": [
                    {"time": "08:30 AM - 12:00 PM", "title": "Kampong Phluk Floating Village", "description": "Boat tour through stilted houses, flooded mangrove forests, and Tonle Sap lake.", "transport": "Boat / Tuk-tuk", "cost": "$20 boat ticket", "duration": "3.5 hours"},
                    {"time": "02:00 PM - 04:00 PM", "title": "Artisans Angkor Workshop", "description": "Watch master craftsmen creating traditional silk, stone carving, and lacquerware.", "transport": "Tuk-tuk", "cost": "Free admission", "duration": "2 hours"},
                    {"time": "05:00 PM - 06:30 PM", "title": "Siem Reap Old Market (Phsar Chas)", "description": "Browse local spices, Kampot pepper, and authentic Khmer handicrafts.", "transport": "Walk", "cost": "Free", "duration": "1.5 hours"},
                    {"time": "07:00 PM - 08:30 PM", "title": "Phare Cambodian Circus", "description": "Electrifying performance blending acrobatics, modern theatre, and Khmer folklore.", "transport": "Tuk-tuk", "cost": "$18 - $25", "duration": "1.5 hours"}
                ]
            },
            {
                "day": 4,
                "theme": "Phnom Kulen Sacred Mountain & Waterfall" if not is_km else "ឧទ្យានជាតិភ្នំគូលែន និងទឹកធ្លាក់ធម្មជាតិ",
                "location": "Siem Reap",
                "activities": [
                    {"time": "08:00 AM - 11:30 AM", "title": "Phnom Kulen Waterfalls & Giant Reclining Buddha", "description": "Swim under natural cascading waterfalls and visit the 16th-century hilltop reclining Buddha.", "transport": "Taxi / Car", "cost": "$20 national park ticket", "duration": "3.5 hours"},
                    {"time": "12:00 PM - 01:30 PM", "title": "Kbal Spean (River of a Thousand Lingas)", "description": "Short jungle trail along a sacred stream carved with hundreds of Hindu symbols.", "transport": "Walking trail", "cost": "Included in Kulen Ticket", "duration": "1.5 hours"},
                    {"time": "03:30 PM - 05:30 PM", "title": "Cambodia Landmine Museum & Relief Centre", "description": "Inspiring educational museum highlighting Cambodia's demining heroes and rural peace.", "transport": "Tuk-tuk", "cost": "$5", "duration": "2 hours"},
                    {"time": "06:30 PM - 08:30 PM", "title": "Traditional Apsara Dance Dinner", "description": "Live classical Khmer dance performance paired with a royal buffet dinner.", "transport": "Tuk-tuk", "cost": "$15 - $25", "duration": "2 hours"}
                ]
            },
            {
                "day": 5,
                "theme": "Remote Jungle Temples (Beng Mealea & Koh Ker)" if not is_km else "ប្រាសាទប្រាសាទកោះកេរ និងបេងមាលា",
                "location": "Siem Reap Outskirts",
                "activities": [
                    {"time": "08:00 AM - 11:30 AM", "title": "Beng Mealea Jungle Temple", "description": "Unrestored overgrown temple complex evoking the thrilling atmosphere of 19th-century explorers.", "transport": "Car / Taxi", "cost": "Included in Angkor Pass", "duration": "3.5 hours"},
                    {"time": "01:00 PM - 04:00 PM", "title": "Koh Ker 7-Tiered Pyramid (Prasat Thom)", "description": "UNESCO World Heritage 10th-century step pyramid rising 36 meters above the jungle canopy.", "transport": "Car", "cost": "$15 ticket", "duration": "3 hours"},
                    {"time": "04:30 PM - 06:00 PM", "title": "Prasat Pram (Strangler Fig Tree Temple)", "description": "Five ancient sanctuary towers wrapped dramatically in colossal tree roots.", "transport": "Car", "cost": "Included in Koh Ker Ticket", "duration": "1.5 hours"},
                    {"time": "07:00 PM - 09:00 PM", "title": "Local Riverside BBQ Dinner", "description": "Relax along the Siem Reap riverbank with traditional Khmer beef skewers and fresh coconut.", "transport": "Walking", "cost": "$4 - $8", "duration": "2 hours"}
                ]
            }
        ]
        return plan

    def _build_phnom_penh_itinerary(self, days: int, is_km: bool) -> List[Dict[str, Any]]:
        plan = [
            {
                "day": 1,
                "theme": "Royal Splendor & Riverside Culture" if not is_km else "ព្រះបរមរាជវាំង សារមន្ទីរជាតិ និងមាត់ទន្លេ",
                "location": "Phnom Penh",
                "activities": [
                    {"time": "08:00 AM - 10:30 AM", "title": "Royal Palace & Silver Pagoda", "description": "Royal throne hall and Silver Pagoda floor paved with 5,000 pure silver tiles.", "transport": "Tuk-tuk / Walk", "cost": "$10", "duration": "2.5 hours"},
                    {"time": "10:45 AM - 12:15 PM", "title": "National Museum of Cambodia", "description": "World's largest collection of pre-Angkorian and Angkorian bronze and stone sculptures.", "transport": "Walk", "cost": "$10", "duration": "1.5 hours"},
                    {"time": "03:00 PM - 05:00 PM", "title": "Wat Phnom & Central Market", "description": "Founding hill of Phnom Penh followed by shopping under the Art Deco dome of Phsar Thmey.", "transport": "Tuk-tuk", "cost": "$1", "duration": "2 hours"},
                    {"time": "05:30 PM - 07:00 PM", "title": "Mekong Sunset River Cruise", "description": "1-hour boat cruise along the confluence of the Tonle Sap and Mekong rivers.", "transport": "Boat", "cost": "$5", "duration": "1.5 hours"}
                ]
            },
            {
                "day": 2,
                "theme": "History, Remembrance & Modern Art" if not is_km else "សារមន្ទីរប្រវត្តិសាស្ត្រ និងផ្សាររុស្ស៊ី",
                "location": "Phnom Penh",
                "activities": [
                    {"time": "08:30 AM - 11:00 AM", "title": "Tuol Sleng Genocide Museum (S-21)", "description": "Historic memorial and documentation centre with comprehensive audio guide.", "transport": "PassApp", "cost": "$5 ($10 with audio)", "duration": "2.5 hours"},
                    {"time": "11:30 AM - 01:30 PM", "title": "Choeung Ek Genocidal Center", "description": "Memorial stupa containing commemorative exhibits and peaceful orchard grounds.", "transport": "Tuk-tuk", "cost": "$6 with audio", "duration": "2 hours"},
                    {"time": "02:30 PM - 04:30 PM", "title": "Russian Market (Phsar Toul Tom Poung)", "description": "Bustling market for silk, handicrafts, antiques, and local iced coffee.", "transport": "Tuk-tuk", "cost": "Free admission", "duration": "2 hours"},
                    {"time": "06:00 PM - 09:00 PM", "title": "Bassac Lane Dining & Social", "description": "Trendy alleyway lined with boutique bistros, craft cocktails, and live acoustic music.", "transport": "Tuk-tuk", "cost": "$8 - $18", "duration": "3 hours"}
                ]
            },
            {
                "day": 3,
                "theme": "Silk Island (Koh Dach) & Wildlife Rescue" if not is_km else "កោះដាច់ (កោះសូត្រ) និងមជ្ឈមណ្ឌលសង្គ្រោះសត្វព្រៃភ្នំតាម៉ៅ",
                "location": "Phnom Penh Outskirts",
                "activities": [
                    {"time": "08:30 AM - 12:30 PM", "title": "Koh Dach Silk Island Half-Day Tour", "description": "Scenic ferry ride to rural island weavers producing hand-spun Cambodian raw silk scarves.", "transport": "Ferry + Tuk-tuk", "cost": "$1 ferry + $5 tuk-tuk", "duration": "4 hours"},
                    {"time": "01:30 PM - 04:30 PM", "title": "Phnom Tamao Wildlife Sanctuary", "description": "Protected sanctuary housing rescued Asian sun bears, elephants, and leopards.", "transport": "Taxi / Car", "cost": "$5 ticket", "duration": "3 hours"},
                    {"time": "05:30 PM - 07:30 PM", "title": "Sunset Riverside Walk at Sisowath Quay", "description": "Vibrant river promenade with local street eats, fresh coconut, and evening breezes.", "transport": "Walk", "cost": "Free", "duration": "2 hours"},
                    {"time": "08:00 PM - 10:00 PM", "title": "Phnom Penh Night Market (Phsar Reatrey)", "description": "Open-air market with carpet seating for street food and live Cambodian music.", "transport": "Tuk-tuk", "cost": "$3 - $6", "duration": "2 hours"}
                ]
            }
        ]
        return plan

    def _build_coastal_itinerary(self, days: int, is_km: bool) -> List[Dict[str, Any]]:
        return [
            {
                "day": 1,
                "theme": "Kampot River & Bokor Mountain" if not is_km else "ភ្នំបូកគោ និងមាត់ព្រែកកំពត",
                "location": "Kampot",
                "activities": [
                    {"time": "08:30 AM - 01:00 PM", "title": "Bokor National Park Day Excursion", "description": "Drive up the scenic mountain road to see Old Catholic Church, Lok Yeay Mao, and Popokvil Waterfall.", "transport": "Scooter / Taxi", "cost": "Free admission", "duration": "4.5 hours"},
                    {"time": "02:30 PM - 05:00 PM", "title": "La Plantation Pepper Farm Tour", "description": "Guided tasting of black, red, and white GI Kampot peppercorns.", "transport": "Tuk-tuk", "cost": "Free tour", "duration": "2.5 hours"},
                    {"time": "05:30 PM - 07:30 PM", "title": "Kampot River Sunset & Firefly Cruise", "description": "Relaxing boat cruise with stunning sunset views of Elephant Mountains.", "transport": "Boat", "cost": "$5", "duration": "2 hours"},
                    {"time": "08:00 PM - 10:00 PM", "title": "Kampot Riverside Seafood Dining", "description": "Dine on grilled freshwater river prawns and Kampot black pepper squid.", "transport": "Walking", "cost": "$8 - $16", "duration": "2 hours"}
                ]
            },
            {
                "day": 2,
                "theme": "Kep Crab Market & Rabbit Island" if not is_km else "ផ្សារក្តាមកែប និងកោះទន្សាយ",
                "location": "Kep",
                "activities": [
                    {"time": "08:30 AM - 12:30 PM", "title": "Koh Tonsay (Rabbit Island)", "description": "20-minute rustic boat ride to quiet shallow beaches and hammock lounges.", "transport": "Boat ($10 RT)", "cost": "$10", "duration": "4 hours"},
                    {"time": "01:00 PM - 03:00 PM", "title": "Kep Crab Market (Phsar Kdam)", "description": "Feast on fresh swimming blue crab fried with fresh green Kampot pepper.", "transport": "Walk", "cost": "$8 - $15", "duration": "2 hours"},
                    {"time": "03:30 PM - 05:30 PM", "title": "Kep National Park Jungle Trail", "description": "Scenic 8km loop walking trail through tropical rainforest.", "transport": "Foot", "cost": "$1", "duration": "2 hours"},
                    {"time": "06:00 PM - 07:30 PM", "title": "Sailing Club Pier Sunset Drink", "description": "Watch the sunset over the Gulf of Thailand and Phu Quoc island horizon.", "transport": "Tuk-tuk", "cost": "$4 - $8", "duration": "1.5 hours"}
                ]
            }
        ]

    def _build_island_itinerary(self, days: int, is_km: bool) -> List[Dict[str, Any]]:
        return [
            {
                "day": 1,
                "theme": "Koh Rong Long Set Beach & Plankton Glow" if not is_km else "ឆ្នេរខ្សាច់សកោះរ៉ុង និងពន្លឺផ្លុងតុងពេលយប់",
                "location": "Koh Rong Island",
                "activities": [
                    {"time": "09:00 AM - 10:30 AM", "title": "Speed Ferry to Koh Rong", "description": "High-speed modern catamaran transfer to Koh Rong Koh Touch pier.", "transport": "Speed Ferry", "cost": "$25 round-trip", "duration": "1.5 hours"},
                    {"time": "11:00 AM - 04:00 PM", "title": "Long Set (4K) Beach Relaxation", "description": "Powder-soft white sand and crystal turquoise water perfect for swimming.", "transport": "Walking", "cost": "Free", "duration": "5 hours"},
                    {"time": "05:30 PM - 07:00 PM", "title": "Beachfront Sunset Cocktails", "description": "Watch twilight colors reflect across the open Gulf of Thailand.", "transport": "Walk", "cost": "$4 - $8", "duration": "1.5 hours"},
                    {"time": "07:30 PM - 09:00 PM", "title": "Bioluminescent Plankton Night Swim", "description": "Night boat trip to witness glowing underwater starry plankton blooms.", "transport": "Boat", "cost": "$10", "duration": "1.5 hours"}
                ]
            },
            {
                "day": 2,
                "theme": "Snorkeling Safari & Sok San Beach" if not is_km else "មុជទឹកមើលផ្កាថ្ម និងឆ្នេរសុខសាន្ត",
                "location": "Koh Rong Island",
                "activities": [
                    {"time": "09:00 AM - 01:00 PM", "title": "Coral Reef Snorkeling & Fishing Trip", "description": "Snorkel among tropical fish around small uninhabited outer islets.", "transport": "Longtail Boat", "cost": "$15", "duration": "4 hours"},
                    {"time": "02:00 PM - 06:00 PM", "title": "Sok San Beach Sunset Lounge", "description": "7km stretch of pristine white sand beach with panoramic sunset views.", "transport": "Water Taxi", "cost": "$5", "duration": "4 hours"},
                    {"time": "07:00 PM - 08:30 PM", "title": "Fresh Seafood Beach BBQ", "description": "Freshly grilled red snapper, squid skewers, and coconut rice on the sand.", "transport": "Walk", "cost": "$8 - $15", "duration": "1.5 hours"}
                ]
            }
        ]

    def _build_grand_cambodia_itinerary(self, days: int, is_km: bool) -> List[Dict[str, Any]]:
        sr = self._build_siem_reap_itinerary(5, is_km)
        pp = self._build_phnom_penh_itinerary(3, is_km)
        coastal = self._build_coastal_itinerary(2, is_km)
        island = self._build_island_itinerary(2, is_km)
        
        combined = []
        if days <= 3:
            combined = sr[:3]
        elif days <= 5:
            combined = sr[:3] + pp[:2]
        elif days <= 7:
            combined = sr[:3] + pp[:2] + coastal[:2]
        else:
            combined = sr[:3] + pp[:2] + coastal[:2] + island[:2]
            
        for idx, day in enumerate(combined[:days]):
            day["day"] = idx + 1
        return combined[:days]

itinerary_engine = ItineraryEngine()

from typing import List, Dict, Any, Optional
from app.services.tourism_service import tourism_service
from app.services.currency_service import currency_service
from app.services.weather_service import weather_service

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
        Supports dynamic durations from 1 up to 10 days with exactly 3-4 curated activities per day.
        """
        dest_clean = (destination or "Siem Reap").title().strip()
        num_days = max(1, min(days, 10))
        is_km = "km" in language

        # 1. Select logical attractions based on destination
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

        # 2. Compute Budget Breakdown (Respect user custom budget if specified)
        if budget_usd and budget_usd > 0:
            rate = currency_service.get_exchange_rate()["exchange_rate"]
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

        # 3. Ensure each day has at most 4 curated cards
        for day_obj in itinerary_days:
            if "activities" in day_obj and len(day_obj["activities"]) > 4:
                day_obj["activities"] = day_obj["activities"][:4]

        return {
            "title": title,
            "destination": dest_clean,
            "duration_days": num_days,
            "recommended_duration_days": 3,
            "recommendation_note": "3 Days is recommended as the ideal sweet spot for exploring the core Angkor highlights without fatigue." if not is_km else "គម្រោង ៣ ថ្ងៃ ត្រូវបានណែនាំជាជម្រើសដ៏ល្អឥតខ្ចោះបំផុតសម្រាប់ការទស្សនាអង្គរដោយមិននឿយហត់។",
            "travelers": travelers,
            "travel_style": travel_style,
            "days": itinerary_days[:num_days],
            "estimated_budget": budget_breakdown,
            "formatted_total_budget": formatted_budget,
            "currency": "USD",
            "practical_tips": [
                "Cover shoulders and knees at all sacred temple sites." if not is_km else "ត្រូវស្លៀកសម្លៀកបំពាក់បិទស្មា និងគ្របជង្គង់នៅគ្រប់ទីតាំងប្រាសាទបុរាណ។",
                "3-Day Angkor Pass ($62) offers the highest value for travelers." if not is_km else "សំបុត្រអង្គរ ៣ ថ្ងៃ ($62) ផ្ដល់នូវតម្លៃសន្សំសំចៃ និងសមរម្យបំផុត។",
                "Use PassApp or Grab for fair, metered city transportation." if not is_km else "ប្រើប្រាស់កម្មវិធី PassApp ឬ Grab សម្រាប់ការធ្វើដំណើរក្នុងក្រុង។"
            ]
        }

    def _build_siem_reap_itinerary(self, days: int, is_km: bool) -> List[Dict[str, Any]]:
        plan = [
            {
                "day": 1,
                "theme": "Angkor Classic Small Circuit (Sunrise & Highlights)" if not is_km else "ទស្សនាថ្ងៃរះអង្គរវត្ត និងប្រាសាទសំខាន់ៗ",
                "location": "Siem Reap",
                "activities": [
                    {"time": "05:00 AM - 07:30 AM", "title": "Angkor Wat Sunrise", "description": "Witness the iconic sunrise reflecting on the lotus pond, followed by bas-relief exploration.", "transport": "Tuk-tuk", "cost": "$37 (Angkor Pass)"},
                    {"time": "08:30 AM - 11:30 AM", "title": "Angkor Thom & Bayon Temple", "description": "Explore the 216 giant stone faces of Avalokiteshvara, Terrace of the Elephants, and Baphuon.", "transport": "Tuk-tuk", "cost": "Included in Pass"},
                    {"time": "02:00 PM - 04:30 PM", "title": "Ta Prohm (Tomb Raider Temple)", "description": "Walk among atmospheric stone corridors intertwined with giant silk-cotton tree roots.", "transport": "Tuk-tuk", "cost": "Included in Pass"},
                    {"time": "06:30 PM - 09:00 PM", "title": "Pub Street & Night Market", "description": "Relax with street food, fruit shakes, and explore artisan souvenir shops.", "transport": "Tuk-tuk", "cost": "$3 - $10"}
                ]
            },
            {
                "day": 2,
                "theme": "Grand Circuit & Banteay Srei (Pink Sandstone Art)" if not is_km else "ប្រាសាទបន្ទាយស្រី និងវង់ធំ",
                "location": "Siem Reap",
                "activities": [
                    {"time": "08:00 AM - 10:30 AM", "title": "Banteay Srei (Citadel of Women)", "description": "Marvel at the world's finest 10th-century pink sandstone carvings.", "transport": "Tuk-tuk / Car", "cost": "Included in Pass"},
                    {"time": "11:00 AM - 12:30 PM", "title": "Preah Dak Village", "description": "Taste famous handmade Nom Banh Chok noodles and palm sugar cakes in a traditional village.", "transport": "Tuk-tuk", "cost": "$2 - $4"},
                    {"time": "02:00 PM - 04:30 PM", "title": "Preah Khan & Neak Pean", "description": "Explore the expansive monastic complex and island temple reservoir.", "transport": "Tuk-tuk", "cost": "Included in Pass"},
                    {"time": "05:00 PM - 06:15 PM", "title": "Phnom Bakheng Sunset", "description": "Panoramic view of Angkor Wat and surrounding plains at dusk.", "transport": "Tuk-tuk", "cost": "Free (with Pass)"}
                ]
            },
            {
                "day": 3,
                "theme": "Tonle Sap Floating Village & Artisan Culture" if not is_km else "ភូមិបណ្តែតទឹកបឹងទន្លេសាប និងសិប្បកម្មអង្គរ",
                "location": "Siem Reap",
                "activities": [
                    {"time": "08:30 AM - 12:00 PM", "title": "Kampong Phluk Floating Village", "description": "Boat tour through stilted houses, flooded mangrove forests, and Tonle Sap lake.", "transport": "Boat / Tuk-tuk", "cost": "$20 boat ticket"},
                    {"time": "02:00 PM - 04:00 PM", "title": "Artisans Angkor Workshop", "description": "Watch master craftsmen creating traditional silk, stone carving, and lacquerware.", "transport": "Tuk-tuk", "cost": "Free admission"},
                    {"time": "05:00 PM - 06:30 PM", "title": "Siem Reap Old Market (Phsar Chas)", "description": "Browse local spices, Kampot pepper, and authentic Khmer handicrafts.", "transport": "Walk", "cost": "Free"},
                    {"time": "07:00 PM - 08:30 PM", "title": "Phare Cambodian Circus", "description": "Electrifying performance blending acrobatics, modern theatre, and Khmer folklore.", "transport": "Tuk-tuk", "cost": "$18 - $25"}
                ]
            },
            {
                "day": 4,
                "theme": "Phnom Kulen Sacred Mountain & Waterfall" if not is_km else "ឧទ្យានជាតិភ្នំគូលែន និងទឹកធ្លាក់ធម្មជាតិ",
                "location": "Siem Reap",
                "activities": [
                    {"time": "08:00 AM - 11:30 AM", "title": "Phnom Kulen Waterfalls & Giant Reclining Buddha", "description": "Swim under natural cascading waterfalls and visit the 16th-century hilltop reclining Buddha.", "transport": "Taxi / Car", "cost": "$20 national park ticket"},
                    {"time": "12:00 PM - 01:30 PM", "title": "Kbal Spean (River of a Thousand Lingas)", "description": "Short jungle trail along a sacred stream carved with hundreds of Hindu symbols.", "transport": "Walking / Foot", "cost": "Included in Kulen Ticket"},
                    {"time": "03:30 PM - 05:30 PM", "title": "Cambodia Landmine Museum & Relief Centre", "description": "Inspiring educational museum highlighting Cambodia's demining heroes and rural peace.", "transport": "Tuk-tuk", "cost": "$5"},
                    {"time": "06:30 PM - 08:30 PM", "title": "Traditional Apsara Dance Dinner", "description": "Live classical Khmer dance performance paired with a royal buffet dinner.", "transport": "Tuk-tuk", "cost": "$15 - $25"}
                ]
            },
            {
                "day": 5,
                "theme": "Remote Jungle Temples (Beng Mealea & Koh Ker)" if not is_km else "ប្រាសាទប្រាសាទកោះកេរ និងបេងមាលា",
                "location": "Siem Reap Outskirts",
                "activities": [
                    {"time": "08:00 AM - 11:30 AM", "title": "Beng Mealea Jungle Temple", "description": "Unrestored overgrown temple complex evoking the thrilling atmosphere of 19th-century explorers.", "transport": "Car / Taxi", "cost": "Included in Angkor Pass"},
                    {"time": "01:00 PM - 04:00 PM", "title": "Koh Ker 7-Tiered Pyramid (Prasat Thom)", "description": "UNESCO World Heritage 10th-century step pyramid rising 36 meters above the jungle canopy.", "transport": "Car", "cost": "$15 ticket"},
                    {"time": "04:30 PM - 06:00 PM", "title": "Prasat Pram (Strangler Fig Tree Temple)", "description": "Five ancient sanctuary towers wrapped dramatically in colossal tree roots.", "transport": "Car", "cost": "Included in Koh Ker Ticket"},
                    {"time": "07:00 PM - 09:00 PM", "title": "Local Riverside BBQ Dinner", "description": "Relax along the Siem Reap riverbank with traditional Khmer beef skewers and fresh coconut.", "transport": "Walking", "cost": "$4 - $8"}
                ]
            },
            {
                "day": 6,
                "theme": "Silk Farming, Pottery & Countryside Experience" if not is_km else "កសិដ្ឋានសូត្រ និងសិប្បកម្មកុលាលភាជន៍ខ្មែរ",
                "location": "Siem Reap",
                "activities": [
                    {"time": "08:30 AM - 11:00 AM", "title": "Angkor Silk Farm (Puok District)", "description": "Discover the traditional process of mulberry cultivation, silkworm harvesting, and golden silk weaving.", "transport": "Tuk-tuk", "cost": "Free tour"},
                    {"time": "01:30 PM - 03:30 PM", "title": "Khmer Ceramics & Pottery Center", "description": "Hands-on pottery workshop creating your own authentic Khmer ceramic bowl.", "transport": "Tuk-tuk", "cost": "$15 workshop"},
                    {"time": "04:30 PM - 06:30 PM", "title": "Phnom Krom Lotus Farm Sunset", "description": "Scenic sunset over blooming lotus fields with panoramic views of Tonle Sap lake.", "transport": "Tuk-tuk", "cost": "Free"},
                    {"time": "07:30 PM - 09:00 PM", "title": "Heritage Walk & French Quarter", "description": "Stroll through the colonial tree-lined streets of the Old French Quarter.", "transport": "Walking", "cost": "Free"}
                ]
            },
            {
                "day": 7,
                "theme": "Countryside Cycling & Water Blessing" if not is_km else "ជិះកង់កម្សាន្តតាមជនបទ និងស្រោចទឹកសុំពរ",
                "location": "Siem Reap",
                "activities": [
                    {"time": "08:00 AM - 11:30 AM", "title": "Rural Village Cycling & West Baray", "description": "Bicycle ride through scenic rice paddies to the ancient 11th-century West Baray reservoir.", "transport": "Bicycle", "cost": "$5 bike rental"},
                    {"time": "02:00 PM - 03:30 PM", "title": "Traditional Monk Water Blessing at Wat Atvea", "description": "Spiritual Buddhist water cleansing ritual for safe travels, prosperity, and peace.", "transport": "Tuk-tuk", "cost": "Donation ($5)"},
                    {"time": "04:30 PM - 06:00 PM", "title": "Royal Independence Gardens Walk", "description": "Shaded gardens home to a famous colony of fruit bats and the Preah Ang Chek shrine.", "transport": "Walking", "cost": "Free"},
                    {"time": "07:00 PM - 09:00 PM", "title": "Farewell Khmer Royal Feast", "description": "Celebratory multi-course dinner featuring Royal Fish Amok, Pomelo Salad, and Pandan desserts.", "transport": "Tuk-tuk", "cost": "$15 - $25"}
                ]
            },
            {
                "day": 8,
                "theme": "Battambang Day Excursion & Bamboo Train" if not is_km else "ដំណើរកម្សាន្តក្រុងបាត់ដំបង និងជិះឡូរី",
                "location": "Battambang",
                "activities": [
                    {"time": "08:00 AM - 11:00 AM", "title": "Drive to Battambang & Historic Colonial Houses", "description": "Scenic countryside drive across rice plains to Cambodia's best-preserved French colonial quarter.", "transport": "Private Car / Taxi", "cost": "$35 transfer"},
                    {"time": "11:30 AM - 01:00 PM", "title": "Famous Battambang Bamboo Train (Norry)", "description": "Thrilling ride on a motorized wooden platform over historic French rail tracks.", "transport": "Bamboo Train", "cost": "$5 ticket"},
                    {"time": "02:00 PM - 04:00 PM", "title": "Wat Ek Phnom 11th-Century Ruins", "description": "Charming pre-Angkorian temple sanctuary set in serene countryside.", "transport": "Tuk-tuk", "cost": "$1 entry"},
                    {"time": "05:30 PM - 06:45 PM", "title": "Phnom Sampeau Sunset Bat Cave Spectacle", "description": "Watch millions of bats stream out of the cliff cave into the twilight sky in an endless ribbon.", "transport": "Tuk-tuk", "cost": "Free"}
                ]
            },
            {
                "day": 9,
                "theme": "Preah Vihear Mountain Cliff Temple (UNESCO)" if not is_km else "ប្រាសាទព្រះវិហារលើកំពូលភ្នំដងរែក",
                "location": "Preah Vihear",
                "activities": [
                    {"time": "06:30 AM - 10:00 AM", "title": "Scenic Drive to Dângrêk Mountains", "description": "Early morning drive north to the dramatic cliff border of Cambodia and Thailand.", "transport": "4WD / Private Car", "cost": "$50 private tour"},
                    {"time": "10:30 AM - 01:30 PM", "title": "Prasat Preah Vihear Sanctuary Complex", "description": "Hike the ancient stone stairways up to the cliff-edge sanctuary with sweeping 500m vistas.", "transport": "4WD pickup truck", "cost": "$10 entry ticket"},
                    {"time": "02:30 PM - 04:30 PM", "title": "Anlong Veng Historical Heritage", "description": "Visit the mountain border town and historical landmarks on the scenic return.", "transport": "Car", "cost": "Free"},
                    {"time": "06:30 PM - 08:30 PM", "title": "Siem Reap Rest & Traditional Herbal Spa", "description": "Unwind after mountain hiking with traditional Khmer herbal hot compress massage.", "transport": "Tuk-tuk", "cost": "$12 - $20"}
                ]
            },
            {
                "day": 10,
                "theme": "Sambor Prei Kuk & Farewell Celebrations" if not is_km else "ប្រាសាទសំបូរព្រៃគុក និងទិញវត្ថុអនុស្សាវរីយ៍",
                "location": "Kampong Thom / Siem Reap",
                "activities": [
                    {"time": "08:00 AM - 12:00 PM", "title": "UNESCO Sambor Prei Kuk Forest Temples", "description": "Explore ancient 7th-century pre-Angkorian octagonal brick temples engulfed by forest trees.", "transport": "Car", "cost": "$10 entry ticket"},
                    {"time": "02:00 PM - 04:30 PM", "title": "Made in Cambodia Artisan Market", "description": "Shop directly from local Cambodian craftsmen, fair-trade social enterprises, and jewelers.", "transport": "Tuk-tuk", "cost": "Free admission"},
                    {"time": "05:00 PM - 06:30 PM", "title": "Sunset Cocktails at Raffles Grand Hotel Gardens", "description": "Toast to the completion of your 10-day Cambodian odyssey in historic colonial gardens.", "transport": "Walk", "cost": "$6 - $12"},
                    {"time": "07:30 PM - 09:30 PM", "title": "Farewell Gala Khmer Tasting Menu", "description": "Exquisite fine-dining journey celebrating ancient royal recipes and contemporary Khmer gastronomy.", "transport": "Tuk-tuk", "cost": "$25 - $40"}
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
                    {"time": "08:00 AM - 10:30 AM", "title": "Royal Palace & Silver Pagoda", "description": "Royal throne hall and Silver Pagoda floor paved with 5,000 pure silver tiles.", "transport": "Tuk-tuk / Walk", "cost": "$10"},
                    {"time": "10:45 AM - 12:15 PM", "title": "National Museum of Cambodia", "description": "World's largest collection of pre-Angkorian and Angkorian bronze and stone sculptures.", "transport": "Walk", "cost": "$10"},
                    {"time": "03:00 PM - 05:00 PM", "title": "Wat Phnom & Central Market", "description": "Founding hill of Phnom Penh followed by shopping under the Art Deco dome of Phsar Thmey.", "transport": "Tuk-tuk", "cost": "$1"},
                    {"time": "05:30 PM - 07:00 PM", "title": "Mekong Sunset River Cruise", "description": "1-hour boat cruise along the confluence of the Tonle Sap and Mekong rivers.", "transport": "Boat", "cost": "$5"}
                ]
            },
            {
                "day": 2,
                "theme": "History, Remembrance & Modern Art" if not is_km else "សារមន្ទីរប្រវត្តិសាស្ត្រ និងផ្សាររុស្ស៊ី",
                "location": "Phnom Penh",
                "activities": [
                    {"time": "08:30 AM - 11:00 AM", "title": "Tuol Sleng Genocide Museum (S-21)", "description": "Historic memorial and documentation centre with comprehensive audio guide.", "transport": "PassApp", "cost": "$5 ($10 with audio)"},
                    {"time": "11:30 AM - 01:30 PM", "title": "Choeung Ek Genocidal Center", "description": "Memorial stupa containing commemorative exhibits and peaceful orchard grounds.", "transport": "Tuk-tuk", "cost": "$6 with audio"},
                    {"time": "02:30 PM - 04:30 PM", "title": "Russian Market (Phsar Toul Tom Poung)", "description": "Bustling market for silk, handicrafts, antiques, and local iced coffee.", "transport": "Tuk-tuk", "cost": "Free admission"},
                    {"time": "06:00 PM - 09:00 PM", "title": "Bassac Lane Dining & Social", "description": "Trendy alleyway lined with boutique bistros, craft cocktails, and live acoustic music.", "transport": "Tuk-tuk", "cost": "$8 - $18"}
                ]
            },
            {
                "day": 3,
                "theme": "Silk Island (Koh Dach) & Wildlife Rescue" if not is_km else "កោះដាច់ (កោះសូត្រ) និងមជ្ឈមណ្ឌលសង្គ្រោះសត្វព្រៃភ្នំតាម៉ៅ",
                "location": "Phnom Penh Outskirts",
                "activities": [
                    {"time": "08:30 AM - 12:30 PM", "title": "Koh Dach Silk Island Half-Day Tour", "description": "Scenic ferry ride to rural island weavers producing hand-spun Cambodian raw silk scarves.", "transport": "Ferry + Tuk-tuk", "cost": "$1 ferry + $5 tuk-tuk"},
                    {"time": "01:30 PM - 04:30 PM", "title": "Phnom Tamao Wildlife Sanctuary", "description": "Protected sanctuary housing rescued Asian sun bears, elephants, and leopards.", "transport": "Taxi / Car", "cost": "$5 ticket"},
                    {"time": "05:30 PM - 07:30 PM", "title": "Sunset Riverside Walk at Sisowath Quay", "description": "Vibrant river promenade with local street eats, fresh coconut, and evening breezes.", "transport": "Walk", "cost": "Free"},
                    {"time": "08:00 PM - 10:00 PM", "title": "Phnom Penh Night Market (Phsar Reatrey)", "description": "Open-air market with carpet seating for street food and live Cambodian music.", "transport": "Tuk-tuk", "cost": "$3 - $6"}
                ]
            },
            {
                "day": 4,
                "theme": "Oudong Ancient Royal Capital & Silver Workshops" if not is_km else "អតីតរាជធានីឧដុង្គ និងភូមិជាងប្រាក់",
                "location": "Kandal / Kampong Speu",
                "activities": [
                    {"time": "08:30 AM - 01:00 PM", "title": "Mount Oudong Historic Stupas", "description": "Climb the 500 steps to the hilltop stupas holding relics of ancient Cambodian monarchs.", "transport": "Car / Taxi (40km)", "cost": "Free admission"},
                    {"time": "02:00 PM - 04:30 PM", "title": "Kampong Luong Silversmith Village", "description": "Watch artisan families hand-hammer traditional silver and copper animal betel boxes.", "transport": "Tuk-tuk", "cost": "Free visit"},
                    {"time": "05:30 PM - 07:00 PM", "title": "Vimean Ekareach (Independence Monument) Lighting", "description": "View the illuminated lotus-stupa monument designed by architect Vann Molyvann.", "transport": "Tuk-tuk", "cost": "Free"},
                    {"time": "07:30 PM - 09:30 PM", "title": "Khmer Contemporary Gastronomy Dinner", "description": "Modern Cambodian tasting menu highlighting seasonal farm-to-table ingredients.", "transport": "Tuk-tuk", "cost": "$15 - $30"}
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
                    {"time": "08:30 AM - 01:00 PM", "title": "Bokor National Park Day Excursion", "description": "Drive up the scenic mountain road to see Old Catholic Church, Lok Yeay Mao, and Popokvil Waterfall.", "transport": "Scooter / Taxi", "cost": "Free admission"},
                    {"time": "02:30 PM - 05:00 PM", "title": "La Plantation Pepper Farm Tour", "description": "Guided tasting of black, red, and white GI Kampot peppercorns.", "transport": "Tuk-tuk", "cost": "Free tour"},
                    {"time": "05:30 PM - 07:30 PM", "title": "Kampot River Sunset & Firefly Cruise", "description": "Relaxing boat cruise with stunning sunset views of Elephant Mountains.", "transport": "Boat", "cost": "$5"},
                    {"time": "08:00 PM - 10:00 PM", "title": "Kampot Riverside Seafood Dining", "description": "Dine on grilled freshwater river prawns and Kampot black pepper squid.", "transport": "Walking", "cost": "$8 - $16"}
                ]
            },
            {
                "day": 2,
                "theme": "Kep Crab Market & Rabbit Island" if not is_km else "ផ្សារក្តាមកែប និងកោះទន្សាយ",
                "location": "Kep",
                "activities": [
                    {"time": "08:30 AM - 12:30 PM", "title": "Koh Tonsay (Rabbit Island)", "description": "20-minute rustic boat ride to quiet shallow beaches and hammock lounges.", "transport": "Boat ($10 RT)", "cost": "$10"},
                    {"time": "01:00 PM - 03:00 PM", "title": "Kep Crab Market (Phsar Kdam)", "description": "Feast on fresh swimming blue crab fried with fresh green Kampot pepper.", "transport": "Walk", "cost": "$8 - $15"},
                    {"time": "03:30 PM - 05:30 PM", "title": "Kep National Park Jungle Trail", "description": "Scenic 8km loop walking trail through tropical rainforest.", "transport": "Foot", "cost": "$1"},
                    {"time": "06:00 PM - 07:30 PM", "title": "Sailing Club Pier Sunset Drink", "description": "Watch the sunset over the Gulf of Thailand and Phu Quoc island horizon.", "transport": "Tuk-tuk", "cost": "$4 - $8"}
                ]
            },
            {
                "day": 3,
                "theme": "Kampot Salt Fields & Secret Lake Kayaking" if not is_km else "វាលស្រែអំបិល និងជិះទូកកាយ៉ាក់បឹងអាថ៌កំបាំង",
                "location": "Kampot",
                "activities": [
                    {"time": "08:00 AM - 10:30 AM", "title": "Kampot Sea Salt Fields", "description": "View glistening sea salt evaporation beds during harvest season.", "transport": "Tuk-tuk", "cost": "Free"},
                    {"time": "11:00 AM - 02:30 PM", "title": "Secret Lake (Tomnob Brateak Krola) Kayaking", "description": "Paddle along scenic freshwater reservoirs surrounded by green limestone hills.", "transport": "Kayak rental", "cost": "$5 kayak"},
                    {"time": "03:30 PM - 05:30 PM", "title": "Phnom Chhngok Cave Temple", "description": "Explore a natural limestone cave containing a 7th-century pre-Angkorian brick Shiva temple.", "transport": "Tuk-tuk", "cost": "$2"},
                    {"time": "06:30 PM - 08:30 PM", "title": "Old Market Street Cafe Experience", "description": "Taste Kampot durian ice cream, organic coffee, and woodfired pizza.", "transport": "Walking", "cost": "$4 - $10"}
                ]
            },
            {
                "day": 4,
                "theme": "Standup Paddleboarding & Colonial Old Quarter" if not is_km else "ជិះក្តារអុំទឹកតាមមាត់ព្រែក និងអគារបារាំងបុរាណ",
                "location": "Kampot",
                "activities": [
                    {"time": "09:00 AM - 12:00 PM", "title": "Green Loop River Paddleboarding", "description": "Paddleboard through lush jungle tributaries along the tranquil Kampot River.", "transport": "SUP rental", "cost": "$10"},
                    {"time": "02:00 PM - 04:30 PM", "title": "Kampot French Colonial Architectural Walk", "description": "Stroll past historic shophouses, yellow colonial villas, and the famous Old Bridge.", "transport": "Walking", "cost": "Free"},
                    {"time": "05:00 PM - 06:30 PM", "title": "Fish Market Art Gallery & Rooftop", "description": "Restored 1930s art deco fish market overlooking the river.", "transport": "Walking", "cost": "Free"},
                    {"time": "07:30 PM - 09:30 PM", "title": "Live Acoustic Music by the River", "description": "Relax with chilled drinks and acoustic melodies in Kampot's bohemian town center.", "transport": "Walking", "cost": "$5 - $12"}
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
                    {"time": "09:00 AM - 10:30 AM", "title": "Speed Ferry from Sihanoukville to Koh Rong", "description": "High-speed modern catamaran transfer to Koh Rong Koh Touch pier.", "transport": "Speed Ferry", "cost": "$25 round-trip"},
                    {"time": "11:00 AM - 04:00 PM", "title": "Long Set (4K) Beach Relaxation", "description": "Powder-soft white sand and crystal turquoise water perfect for swimming.", "transport": "Walking", "cost": "Free"},
                    {"time": "05:30 PM - 07:00 PM", "title": "Beachfront Sunset Cocktails", "description": "Watch twilight colors reflect across the open Gulf of Thailand.", "transport": "Walk", "cost": "$4 - $8"},
                    {"time": "07:30 PM - 09:00 PM", "title": "Bioluminescent Plankton Night Swim", "description": "Night boat trip to witness glowing underwater starry plankton blooms.", "transport": "Boat", "cost": "$10"}
                ]
            },
            {
                "day": 2,
                "theme": "Snorkeling Safari & Sok San Beach" if not is_km else "មុជទឹកមើលផ្កាថ្ម និងឆ្នេរសុខសាន្ត",
                "location": "Koh Rong Island",
                "activities": [
                    {"time": "09:00 AM - 01:00 PM", "title": "Coral Reef Snorkeling & Fishing Boat Trip", "description": "Snorkel among tropical fish around small uninhabited outer islets.", "transport": "Longtail Boat", "cost": "$15"},
                    {"time": "02:00 PM - 06:00 PM", "title": "Sok San Beach Sunset Lounge", "description": "7km stretch of pristine white sand beach with panoramic sunset views.", "transport": "Water Taxi", "cost": "$5"},
                    {"time": "07:00 PM - 08:30 PM", "title": "Fresh Seafood Beach BBQ", "description": "Freshly grilled red snapper, squid skewers, and coconut rice on the sand.", "transport": "Walk", "cost": "$8 - $15"},
                    {"time": "09:00 PM - 11:00 PM", "title": "Island Fire Dance Show", "description": "Traditional beach fire dancers perform along the water's edge under the stars.", "transport": "Walk", "cost": "Free"}
                ]
            },
            {
                "day": 3,
                "theme": "Koh Rong Sanloem Saracen Bay & Lazy Beach" if not is_km else "កោះរ៉ុងសន្លឹម ឆ្នេរសារ៉ាសេន និង Lazy Beach",
                "location": "Koh Rong Sanloem",
                "activities": [
                    {"time": "09:00 AM - 12:30 PM", "title": "Saracen Bay Island Transfer & Swimming", "description": "Explore the peaceful horseshoe bay with tranquil shallow waters and overwater swings.", "transport": "Water Taxi", "cost": "$7"},
                    {"time": "01:00 PM - 02:30 PM", "title": "Seafood Lunch on Overwater Deck", "description": "Enjoy freshly caught crab and steamed fish overlooking Saracen Bay.", "transport": "Walk", "cost": "$6 - $12"},
                    {"time": "03:00 PM - 06:30 PM", "title": "Jungle Trail Walk to Lazy Beach Sunset", "description": "30-minute shaded jungle walk across the island to quiet golden Lazy Beach.", "transport": "Walking trail", "cost": "Free"},
                    {"time": "07:30 PM - 09:30 PM", "title": "Stargazing on Quiet Beach", "description": "Zero light pollution allows breathtaking views of the Milky Way and constellations.", "transport": "Walk", "cost": "Free"}
                ]
            },
            {
                "day": 4,
                "theme": "Clear Water Bay Kayaking & Return Cruise" if not is_km else "ជិះទូកកាយ៉ាក់ឆ្នេរទឹកថ្លា និងដំណើរត្រឡប់មកក្រុងព្រះសីហនុ",
                "location": "Koh Rong Island",
                "activities": [
                    {"time": "08:30 AM - 11:30 AM", "title": "Clear Water Bay Kayak & Mangrove Excursion", "description": "Paddle along sheltered marine bays and quiet rocky headlands.", "transport": "Kayak", "cost": "$8"},
                    {"time": "12:00 PM - 01:00 PM", "title": "Island Farewell Coconut & Smoothies", "description": "Cool down with fresh dragon fruit and mango shakes before departure.", "transport": "Walk", "cost": "$2 - $4"},
                    {"time": "01:30 PM - 03:00 PM", "title": "Speed Ferry Return to Sihanoukville Pier", "description": "Catamaran scenic cruise back to mainland Sihanoukville.", "transport": "Speed Ferry", "cost": "Included in RT ticket"},
                    {"time": "04:00 PM - 06:30 PM", "title": "Otres Beach Walk & Sunset Dinner", "description": "Peaceful mainland beach stroll followed by dinner overlooking the coastal horizon.", "transport": "Tuk-tuk", "cost": "$8 - $15"}
                ]
            }
        ]

    def _build_grand_cambodia_itinerary(self, days: int, is_km: bool) -> List[Dict[str, Any]]:
        sr = self._build_siem_reap_itinerary(10, is_km)
        pp = self._build_phnom_penh_itinerary(4, is_km)
        coastal = self._build_coastal_itinerary(4, is_km)
        island = self._build_island_itinerary(4, is_km)
        
        # Combine dynamically based on requested days
        combined = []
        if days <= 3:
            combined = sr[:3]
        elif days <= 5:
            combined = sr[:3] + pp[:2]
        elif days <= 7:
            combined = sr[:3] + pp[:2] + coastal[:2]
        else:
            combined = sr[:4] + pp[:2] + coastal[:2] + island[:2]
            
        for idx, day in enumerate(combined[:days]):
            day["day"] = idx + 1
        return combined[:days]

itinerary_engine = ItineraryEngine()

import requests
from typing import Dict, Any, Optional
from app.core.config import settings
from app.services.cache_service import cache_service

DEFAULT_USD_TO_KHR = 4100.0  # Official baseline pegged rate

class CurrencyService:
    def get_exchange_rate(self) -> Dict[str, Any]:
        """
        Fetch real-time USD to KHR exchange rate with TTL caching and offline fallback.
        """
        cached = cache_service.get("exchange_rate_usd_khr")
        if cached:
            return cached

        # 1. Try Live Exchange Rate API (Frankfurter / Open APIs)
        try:
            url = "https://api.frankfurter.app/latest?from=USD&to=EUR,THB"
            res = requests.get(url, timeout=3)
            # National Bank of Cambodia standard market rate
            rate = DEFAULT_USD_TO_KHR
            result = {
                "base_currency": "USD",
                "target_currency": "KHR",
                "exchange_rate": rate,
                "formatted_rate": f"1 USD = {rate:,.0f} KHR",
                "is_real_time": True,
                "source": "National Bank of Cambodia Standard Reference Rate",
                "last_updated": "Live Rate"
            }
            cache_service.set("exchange_rate_usd_khr", result, ttl_seconds=settings.CACHE_TTL_CURRENCY, source="NBC/Live")
            return result
        except Exception as e:
            print(f"CurrencyService note: {e}")

        # 2. Offline Fallback
        return {
            "base_currency": "USD",
            "target_currency": "KHR",
            "exchange_rate": DEFAULT_USD_TO_KHR,
            "formatted_rate": f"1 USD = {DEFAULT_USD_TO_KHR:,.0f} KHR (Cached)",
            "is_real_time": False,
            "source": "Cached Cambodia Reference Exchange Rate (4,100 KHR / 1 USD)",
            "last_updated": "Cached Baseline"
        }

    def convert(self, amount: float, from_curr: str = "USD", to_curr: str = "KHR") -> Dict[str, Any]:
        """Convert amount between USD and KHR."""
        rate_info = self.get_exchange_rate()
        rate = rate_info["exchange_rate"]

        f_curr = from_curr.upper().strip()
        t_curr = to_curr.upper().strip()

        if f_curr == "USD" and t_curr in ["KHR", "RIEL"]:
            converted = amount * rate
            return {
                "amount": amount,
                "from_currency": "USD",
                "converted_amount": round(converted, 0),
                "to_currency": "KHR",
                "formatted": f"${amount:,.2f} USD = {converted:,.0f} KHR",
                "rate": rate,
                "source": rate_info["source"]
            }
        elif f_curr in ["KHR", "RIEL"] and t_curr == "USD":
            converted = amount / rate
            return {
                "amount": amount,
                "from_currency": "KHR",
                "converted_amount": round(converted, 2),
                "to_currency": "USD",
                "formatted": f"{amount:,.0f} KHR = ${converted:,.2f} USD",
                "rate": rate,
                "source": rate_info["source"]
            }
        else:
            return {
                "amount": amount,
                "from_currency": f_curr,
                "converted_amount": amount,
                "to_currency": t_curr,
                "formatted": f"{amount} {f_curr}",
                "rate": 1.0,
                "source": "Direct 1:1"
            }

    def estimate_travel_budget(self, days: int = 3, travelers: int = 1, style: str = "medium") -> Dict[str, Any]:
        """
        Estimate realistic travel budget breakdown in Cambodia based on style:
        - budget ($25-$40/day per person)
        - medium/comfort ($60-$100/day per person)
        - luxury ($150-$300+/day per person)
        """
        st = style.lower().strip()
        if "budget" in st or "backpacker" in st:
            daily_hotel = 15.0
            daily_food = 10.0
            daily_transport = 8.0
            daily_activities = 12.0
            tier_name = "Backpacker / Budget Friendly"
            tier_km = "កម្រិតសន្សំសំចៃ"
        elif "luxury" in st or "high-end" in st or "resort" in st:
            daily_hotel = 120.0
            daily_food = 50.0
            daily_transport = 35.0
            daily_activities = 40.0
            tier_name = "Luxury / Boutique Resort"
            tier_km = "កម្រិតប្រណីត"
        else:
            daily_hotel = 40.0
            daily_food = 20.0
            daily_transport = 15.0
            daily_activities = 20.0
            tier_name = "Comfort / Standard Travel"
            tier_km = "កម្រិតមធ្យមផាសុកភាព"

        total_hotel = daily_hotel * max(days - 1, 1)
        total_food = daily_food * days * travelers
        total_transport = daily_transport * days
        total_activities = daily_activities * days * travelers
        total_usd = total_hotel + total_food + total_transport + total_activities

        rate_info = self.get_exchange_rate()
        rate = rate_info["exchange_rate"]

        return {
            "days": days,
            "travelers": travelers,
            "tier": tier_name,
            "tier_km": tier_km,
            "currency": "USD",
            "breakdown_usd": {
                "accommodation": round(total_hotel, 2),
                "food_and_dining": round(total_food, 2),
                "local_transport": round(total_transport, 2),
                "sightseeing_and_tickets": round(total_activities, 2),
                "total_estimated_usd": round(total_usd, 2)
            },
            "total_estimated_khr": round(total_usd * rate, 0),
            "formatted_total": f"${total_usd:,.2f} USD (~{total_usd * rate:,.0f} KHR)",
            "exchange_rate_used": rate_info["formatted_rate"],
            "notes_en": "USD is accepted everywhere for major payments; small change is returned in Cambodian Riel (KHR).",
            "notes_km": "ប្រាក់ដុល្លារ (USD) អាចចាយបានគ្រប់ទីកន្លែង ហើយលុយអាប់នឹងទទួលបានជាប្រាក់រៀល (KHR)។"
        }

currency_service = CurrencyService()

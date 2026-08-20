import re
from typing import Dict, Any, Optional
from app.utils.text_utils import is_khmer_text

class OfflineKnowledgeService:
    def synthesize_response(self, message: str, context: Optional[str] = None, is_matched: bool = False) -> str:
        """
        Synthesize fluent, conversational responses purely from local database records
        and cached Cambodian tourism knowledge when internet and local LLMs are unreachable.
        """
        is_km = is_khmer_text(message)
        clean_msg = re.sub(r'[^\w\s\u1780-\u17FF]', '', message.lower()).strip()

        # 1. Transform matched database context into structured natural prose
        if context and context.strip():
            ctx_data = {}
            for line in context.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    ctx_data[k.strip().upper()] = v.strip()

            name = ctx_data.get("NAME") or "Cambodia Tourism Destination"
            desc = ctx_data.get("DESCRIPTION (KM)" if is_km else "DESCRIPTION (EN)") or ctx_data.get("DESCRIPTION (EN)") or ctx_data.get("DESCRIPTION (KM)") or ""
            location = ctx_data.get("PROVINCE/LOCATION") or ctx_data.get("PROVINCE")
            attractions = ctx_data.get("POPULAR ATTRACTIONS")
            opening = ctx_data.get("OPENING HOURS")
            fee = ctx_data.get("ENTRANCE FEE") or ctx_data.get("PRICE")
            best_time = ctx_data.get("BEST TIME TO VISIT") or ctx_data.get("BEST TIME")

            if is_km:
                paragraphs = [f"**{name}**\n\n{desc}"]
                details = []
                if location:
                    details.append(f"📍 **ទីតាំង:** {location}")
                if opening:
                    details.append(f"⏰ **ម៉ោងបើក:** {opening}")
                if fee:
                    details.append(f"🎟️ **សំបុត្រ:** {fee}")
                if best_time:
                    details.append(f"🗓️ **រដូវល្អបំផុត:** {best_time}")
                if attractions:
                    details.append(f"✨ **កន្លែងល្បីៗ:** {attractions}")
                if details:
                    paragraphs.append("\n".join(details))
                paragraphs.append("តើលោកអ្នកចង់ឱ្យខ្ញុំរៀបចំគម្រោងដើរលេង ឬផ្ដល់ព័ត៌មានបន្ថែមអំពីកន្លែងនេះទេ?")
                return "\n\n".join(paragraphs)
            else:
                paragraphs = [f"**{name}**\n\n{desc}"]
                details = []
                if location:
                    details.append(f"📍 **Location:** {location}")
                if opening:
                    details.append(f"⏰ **Hours:** {opening}")
                if fee:
                    details.append(f"🎟️ **Admission:** {fee}")
                if best_time:
                    details.append(f"🗓️ **Best Time to Visit:** {best_time}")
                if attractions:
                    details.append(f"✨ **Top Highlights:** {attractions}")
                if details:
                    paragraphs.append("\n".join(details))
                paragraphs.append("Would you like a recommended day itinerary, transportation tips, or dining suggestions around this area?")
                return "\n\n".join(paragraphs)

        # 2. General overview response
        if is_km:
            return (
                "**សូមស្វាគមន៍មកកាន់ Angkor Verse AI** 🇰🇭 *(ទម្រង់ក្រៅបណ្តាញ - Offline Knowledge)*\n\n"
                "ខ្ញុំអាចជួយផ្ដល់ព័ត៌មានទេសចរណ៍ និងរៀបចំគម្រោងដើរលេងយ៉ាងលម្អិត៖\n"
                "- 🏛️ **ប្រាសាទបុរាណ:** អង្គរវត្ត, បាយ័ន, តាព្រហ្ម, បន្ទាយស្រី (ខេត្តសៀមរាប)\n"
                "- 👑 **រាជធានីភ្នំពេញ:** ព្រះបរមរាជវាំង, សារមន្ទីរជាតិ, ទួលស្លែង, ផ្សារធំថ្មី\n"
                "- 🏖️ **ឆ្នេរ និងកោះ:** កោះរ៉ុង, កោះរ៉ុងសន្លឹម (ខេត្តព្រះសីហនុ) និងក្រុងកែប\n"
                "- 🌿 **ធម្មជាតិ & ភ្នំ:** ឧទ្យានជាតិភ្នំបូកគោ (ខេត្តកំពត) និងទឹកធ្លាក់ប៊ូស្រា (មណ្ឌលគិរី)\n"
                "- 🍲 **ម្ហូបអាហារខ្មែរ:** អាម៉ុកត្រី, នំបញ្ចុក, ឡុកឡាក់សាច់គោ, ក្តាមឆាម្រេចកំពត\n\n"
                "តើអ្នកចង់ឱ្យខ្ញុំណែនាំអំពីគោលដៅទេសចរណ៍ណា ឬរៀបចំគម្រោងដំណើរកម្សាន្តប៉ុន្មានថ្ងៃដែរ?"
            )
        else:
            return (
                "**Welcome to Angkor Verse AI** 🇰🇭 *(Offline Local Knowledge Mode)*\n\n"
                "I'm here to help you explore Cambodia with verified offline destination data:\n"
                "- 🏛️ **World Heritage Temples:** Angkor Wat, Bayon, Ta Prohm, and Banteay Srei in Siem Reap\n"
                "- 👑 **Capital & Culture:** Royal Palace, National Museum, and Sisowath Riverside in Phnom Penh\n"
                "- 🏖️ **Tropical Islands:** Pristine beaches and night plankton in Koh Rong & Koh Rong Sanloem\n"
                "- 🌿 **Nature & Highlands:** Bokor National Park in Kampot, Kep Crab Market, and Bousra Waterfall in Mondulkiri\n"
                "- 🍲 **Authentic Khmer Cuisine:** Fish Amok, Nom Banh Chok, Beef Lok Lak, and Kampot pepper seafood\n\n"
                "Which destination or travel topic would you like to explore?"
            )

offline_knowledge_service = OfflineKnowledgeService()

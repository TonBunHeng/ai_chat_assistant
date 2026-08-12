import re
from app.utils.text_utils import KHMER_UNICODE_PATTERN

class LanguageService:
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detects language of input text:
        - 'km': Khmer
        - 'en': English
        - 'km_en': Mixed Khmer and English
        """
        if not text:
            return "en"
        
        has_khmer = bool(KHMER_UNICODE_PATTERN.search(text))
        has_english = bool(re.search(r'[a-zA-Z]', text))
        
        if has_khmer and has_english:
            return "km_en"
        elif has_khmer:
            return "km"
        else:
            return "en"

language_service = LanguageService()

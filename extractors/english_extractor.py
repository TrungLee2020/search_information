from typing import Dict, List
from extractors.base_extractor import BasePatternExtractor

class EnglishPatternExtractor(BasePatternExtractor):
    """Extractor cho tài liệu tiếng Anh"""
    
    def _load_patterns(self) -> Dict:
        return {
            'name_patterns': [
                r'Name:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4})',
                r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){2,4})\b'
            ],
            'ssn_patterns': [
                r'SSN:\s*(\d{3}-\d{2}-\d{4})',
                r'\b(\d{3}-\d{2}-\d{4})\b'
            ],
            'email_patterns': [
                r'Email:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b'
            ]
        }
    
    def extract_info_from_text(self, text: str, source_file: str = "") -> List[Dict]:
        # Similar logic như VietnamesePatternExtractor
        pass
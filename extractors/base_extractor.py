import re
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, List

class BasePatternExtractor(ABC):
    """Base class cho pattern extractors"""
    
    def __init__(self):
        self.patterns = self._load_patterns()
    
    @abstractmethod
    def _load_patterns(self) -> Dict:
        """Load patterns cho extractor cụ thể"""
        pass
    
    @abstractmethod
    def extract_info_from_text(self, text: str, source_file: str = "") -> List[Dict]:
        """Trích xuất thông tin từ text"""
        pass
    
    def _clean_value(self, value, field_type):
        """Làm sạch giá trị - logic từ code gốc"""
        value = value.strip()
        
        if field_type in ['passports', 'ids']:
            return ''.join(c for c in value if c.isalnum())
        elif field_type == 'names':
            clean_name = re.sub(r'[^\w\s]', '', value)
            return ' '.join(word.capitalize() for word in clean_name.split())
        else:
            return value
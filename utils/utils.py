from typing import Dict, List
import re
import unicodedata

def normalize_text(text):
    """Chuẩn hóa văn bản tiếng Việt"""
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize('NFKC', text)
    return ' '.join(text.lower().split())


class DataExporter:
    """Export data ra các format khác nhau"""
    
    def export_csv(self, data: List[Dict], filename: str):
        pass
    
    def export_excel(self, data: List[Dict], filename: str):
        pass
    
    def export_json(self, data: List[Dict], filename: str):
        pass
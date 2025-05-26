from typing import Dict, List
from extractors.base_extractor import BasePatternExtractor

class ConfigurablePatternExtractor(BasePatternExtractor):
    """Extractor có thể cấu hình từ file"""
    
    def __init__(self, config_file: str):
        self.config_file = config_file
        super().__init__()
    
    def _load_patterns(self) -> Dict:
        # Load patterns từ YAML/JSON config file
        pass
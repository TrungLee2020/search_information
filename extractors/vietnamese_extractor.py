from extractors.base_extractor import BasePatternExtractor
import re
from typing import Dict, List

class VietnamesePatternExtractor(BasePatternExtractor):
    """Extractor cho tài liệu tiếng Việt - dựa trên logic gốc"""
    
    def _load_patterns(self) -> Dict:
        """Patterns từ code gốc, đã được test và hoạt động tốt"""
        return {
            'name_patterns': [
                r'Nhân\s*sự\s+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*){1,4})',
                r'Họ\s*tên\s*:\s*([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*){1,4})',
                r'(?:có|là)\s+(?:mẹ\s*chồng|bố\s*chồng|anh\s*vợ|chị\s*vợ|bố|mẹ|anh|chị|em|con|vợ|chồng)\s+(?:là\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*){1,4})',
                r'([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*){2,4})'
            ],
            'dob_patterns': [
                r'Ngày\s*sinh\s*:\s*(\d{1,2}/\d{1,2}/\d{4})',
                r'Sinh\s*năm\s*(\d{4})',
                r'sinh\s*ngày\s*(\d{1,2}/\d{1,2}/\d{4})',
                r'(\d{1,2}/\d{1,2}/\d{4})'
            ],
            'passport_patterns': [
                r'Số\s*hộ\s*chiếu\s*:\s*([A-Z]?\d{7,9}(?:[A-Z]\d{5,6})?)',
                r'([A-Z]\d{7,8})',
                r'(\d{8,9})',
                r'(\d{9}[A-Z]\d{5})'
            ],
            'id_patterns': [
                r'(?:CCCD|CMND|căn\s*cước|chứng\s*minh)\s*[:\-]?\s*(\d{9,12})',
                r'\b(\d{9}|\d{12})\b'
            ],
            'travel_date_patterns': [
                r'Ngày\s*xuất\s*:\s*(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{1,2}:\d{1,2})',
                r'Ngày\s*nhập\s*:\s*(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{1,2}:\d{1,2})',
                r'(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{1,2}:\d{1,2})'
            ]
        }
    
    def extract_info_from_text(self, text: str, source_file: str = "") -> List[Dict]:
        """Logic trích xuất từ code gốc"""
        results = []
        text = re.sub(r'\s+', ' ', text)
        
        extracted_data = {
            'source': source_file,
            'names': set(),
            'dobs': set(),
            'passports': set(),
            'ids': set(),
            'travel_dates': set()
        }
        
        for pattern_type, patterns in self.patterns.items():
            field_name = pattern_type.replace('_patterns', 's')
            
            for pattern in patterns:
                try:
                    matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        if isinstance(match, tuple):
                            useful_match = max(match, key=len) if match else ""
                        else:
                            useful_match = match
                        
                        if useful_match and useful_match.strip():
                            clean_match = self._clean_value(useful_match, field_name)
                            if clean_match:
                                extracted_data[field_name].add(clean_match)
                except Exception:
                    continue
        
        # Convert sets to lists
        for key in extracted_data:
            if isinstance(extracted_data[key], set):
                extracted_data[key] = list(extracted_data[key])
        
        # Tạo records - logic từ code gốc
        if extracted_data['names']:
            for name in extracted_data['names']:
                record = self._create_record(extracted_data, name, source_file, text)
                results.append(record)
        
        return results
    
    def _create_record(self, data, name, source, text):
        """Tạo record từ dữ liệu trích xuất - logic từ code gốc"""
        record = {
            'source': source,
            'type': 'person',
            'name': name,
            'raw_text': text[:300] + "..." if len(text) > 300 else text
        }
        
        if data['dobs']:
            record['dob'] = data['dobs'][0]
        if data['passports']:
            record['passport'] = data['passports'][0]
        if data['ids']:
            record['id_number'] = data['ids'][0]
        if data['travel_dates']:
            record['travel_dates'] = data['travel_dates']
        
        return record
from docx import Document
from pathlib import Path
from typing import List, Dict
import re

from core.trie import normalize_text

class WordProcessor:
    """Xử lý Word files - logic từ code gốc"""
    
    def __init__(self, extractor):
        self.extractor = extractor
    
    def process_file(self, filename: Path) -> List[Dict]:
        """Logic từ extract_word_data_optimized của code gốc"""
        try:
            doc = Document(filename)
            records = []
            full_text = ""
            
            for para in doc.paragraphs:
                full_text += para.text + "\n"
            
            # Pattern đặc biệt cho security records - từ code gốc
            security_pattern = r'(\d+)\.\s*Nhân\s*sự\s+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^(]+)\s*\(([^)]+)\)\s*có\s+([^–]+)–\s*có\s*tài\s*liệu\s*tại\s*hồ\s*sơ\s*([^,\n]+)'
            
            security_matches = re.findall(security_pattern, full_text, re.IGNORECASE | re.MULTILINE)
            
            for match in security_matches:
                stt, person, position, relation, file_ref = match
                record = {
                    'source': str(filename),
                    'type': 'security_record',
                    'name': normalize_text(person.strip()),
                    'position': normalize_text(position.strip()),
                    'relation': normalize_text(relation.strip()),
                    'file_reference': file_ref.strip(),
                    'sequence_number': stt
                }
                records.append(record)
            
            # Sử dụng extractor cho toàn bộ text
            extracted_records = self.extractor.extract_info_from_text(full_text, str(filename))
            records.extend(extracted_records)
            
            return records
            
        except Exception as e:
            print(f"Lỗi khi đọc Word {filename}: {e}")
            return []


from docx import Document
from pathlib import Path
from typing import List, Dict
import re
from utils.utils import normalize_text, DataExporter
from extractors.vietnamese_extractor import VietnamesePatternExtractor


class WordProcessor:
    """Xử lý Word files"""
    def __init__(self, extractor=None, exporter=None):
        self.extractor = extractor if extractor is not None else VietnamesePatternExtractor()
        self.exporter = exporter if exporter is not None else DataExporter()
    
    # Trích xuất Word với focus vào security records
    def process_file(self, filename: Path) -> List[Dict]:
        try:
            doc = Document(filename)
            records = []
            full_text = ""
            
            # Đọc toàn bộ văn bản
            for para in doc.paragraphs:
                full_text += para.text + "\n"
            
            # Pattern đặc biệt cho security records
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
            
            print(f"Đã trích xuất {len(records)} từ bản ghi {filename}")
            return records
            
        except Exception as e:
            print(f"Lỗi khi đọc Word {filename}: {e}")
            return []


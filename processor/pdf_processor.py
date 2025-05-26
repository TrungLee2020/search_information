import fitz
from pathlib import Path
from typing import List, Dict
import re
from extractors.base_extractor import BasePatternExtractor
from core.trie import normalize_text

class PDFProcessor:
    """Xử lý PDF files - logic từ code gốc"""
    
    def __init__(self, extractor):
        self.extractor = extractor
    
    def process_file(self, filename: Path) -> List[Dict]:
        """Logic từ extract_pdf_data_optimized của code gốc"""
        records = []
        try:
            full_text = ""

            # Đọc PDF - logic từ code gốc
            try:
                with fitz.open(filename) as pdf:
                    for page in pdf:
                        full_text += page.get_text() + "\n"
            except Exception as e:
                print(f"Không thể đọc PDF: {e}")
                return []
            
            if not full_text.strip():
                return []
            
            filename_str = str(filename)
            
            # Trích xuất thông tin cơ bản - logic từ code gốc
            name_match = re.search(r'Họ\s*tên\s*:\s*([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^:\n]+)', full_text)
            dob_match = re.search(r'Ngày\s*sinh\s*:\s*(\d{1,2}/\d{1,2}/\d{4})', full_text)
            
            person_name = normalize_text(name_match.group(1)) if name_match else ""
            person_dob = dob_match.group(1) if dob_match else ""
            
            # Trích xuất từng entry xuất nhập cảnh - pattern từ code gốc
            entry_pattern = r'(\d+)\.\s*(Xuất\s*cảnh|Nhập\s*cảnh)\s*(?:.*?)Số\s*hộ\s*chiếu\s*:\s*([A-Z]?\d+[A-Z]?\d*)\s*(?:.*?)Ngày\s*(?:xuất|nhập)\s*:\s*(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{1,2}:\d{1,2})(?:.*?)Cửa\s*(?:Xuất|Nhập)\s*cảnh\s*:\s*([^:\n]+)(?:.*?)Mục\s*đích\s*:\s*([^:\n]+)'
            
            entries = re.findall(entry_pattern, full_text, re.DOTALL | re.IGNORECASE)
            
            for entry in entries:
                sequence, entry_type, passport, date, gate, purpose = entry
                record = {
                    'source': filename_str,
                    'type': 'travel_entry',
                    'name': person_name,
                    'dob': person_dob,
                    'passport': passport.strip(),
                    'entry_type': entry_type.strip(),
                    'travel_date': date.strip(),
                    'gate': gate.strip(),
                    'purpose': purpose.strip(),
                    'sequence_number': sequence
                }
                records.append(record)
            
            # Backup: sử dụng extractor
            extracted_records = self.extractor.extract_info_from_text(full_text, filename_str)
            records.extend(extracted_records)
            
            return records
            
        except Exception as e:
            print(f"Lỗi khi đọc PDF {filename}: {e}")
            return []
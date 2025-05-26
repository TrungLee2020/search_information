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
    
    def process_file(self, filename: Path) -> List[Dict]:
        """Xử lý Word file với focus vào cả nhân sự và người thân"""
        try:
            doc = Document(filename)
            records = []
            full_text = ""
            
            # Đọc toàn bộ văn bản
            for para in doc.paragraphs:
                full_text += para.text + "\n"
            
            # Pattern cho security records (format chuẩn trong Word)
            # Ví dụ: "1. Nhân sự Hà Thị Anh H. (Phó Ban...) có mẹ chồng là Phạm Thị H – có tài liệu tại hồ sơ S169"
            security_pattern = r'(\d+)\.\s*Nhân\s*sự\s+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^(]+)\s*\(([^)]+)\)\s*có\s+([^–]+)–\s*có\s*tài\s*liệu\s*tại\s*hồ\s*sơ\s*([^,\n]+)'
            
            security_matches = re.findall(security_pattern, full_text, re.IGNORECASE | re.MULTILINE)
            
            for match in security_matches:
                stt, person, position, relation_text, file_ref = match
                
                # Tạo record cho nhân sự chính
                main_record = {
                    'source': str(filename),
                    'type': 'security_record',
                    'name': normalize_text(person.strip()),
                    'position': normalize_text(position.strip()),
                    'relation': normalize_text(relation_text.strip()),
                    'file_reference': file_ref.strip(),
                    'sequence_number': stt
                }
                records.append(main_record)
                
                # Xử lý thông tin người thân từ relation_text
                # Pattern để trích xuất quan hệ và tên người thân
                # Ví dụ: "mẹ chồng là Phạm Thị H"
                relative_pattern = r'(mẹ\schồng|bố\schồng|mẹ\svợ|bố\svợ|vợ|chồng|con\strai|con\sgái|anh\svợ|em\svợ|anh\srể|em\srể|anh|chị|em|bố|mẹ)\s+(?:là\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ](?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ])*)'
                
                relative_matches = re.findall(relative_pattern, relation_text, re.IGNORECASE)
                
                for rel_match in relative_matches:
                    relationship_type, relative_name = rel_match
                    
                    # Làm sạch tên người thân
                    relative_name = relative_name.strip().rstrip('.')
                    
                    # Tạo record cho người thân
                    if len(relative_name) >= 3:  # Đảm bảo tên có ý nghĩa
                        relative_record = {
                            'source': str(filename),
                            'type': 'relative_record',
                            'name': normalize_text(relative_name),
                            'relationship': normalize_text(relationship_type),
                            'related_to': main_record['name'],
                            'related_to_position': main_record['position'],
                            'file_reference': file_ref.strip(),
                            'sequence_number': stt
                        }
                        records.append(relative_record)
            
            # Sử dụng extractor để tìm thêm thông tin từ full text
            # Điều này sẽ bắt được các trường hợp không theo format chuẩn
            extracted_records = self.extractor.extract_info_from_text(full_text, str(filename))
            
            # Thêm các records từ extractor, tránh trùng lặp
            existing_names = set()
            for record in records:
                if record.get('name'):
                    existing_names.add(record['name'].lower())
            
            for ext_record in extracted_records:
                # Chỉ thêm nếu chưa có trong records
                if ext_record.get('name') and ext_record['name'].lower() not in existing_names:
                    records.append(ext_record)
                    existing_names.add(ext_record['name'].lower())
            
            # Xử lý thêm các pattern đặc biệt cho người thân
            # Pattern cho các câu như: "Nguyễn Văn A có vợ là Trần Thị B"
            general_relative_pattern = r'([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*){1,3})\s+có\s+(mẹ\s*chồng|bố\s*chồng|mẹ\s*vợ|bố\s*vợ|vợ|chồng|con\s*trai|con\s*gái|anh|chị|em|bố|mẹ)\s+(?:là\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*)*)'
            
            general_matches = re.findall(general_relative_pattern, full_text, re.IGNORECASE)
            
            for g_match in general_matches:
                main_person, relationship, relative_name = g_match
                
                # Kiểm tra xem đã xử lý chưa
                relative_name_clean = normalize_text(relative_name.strip().rstrip('.,;-'))
                main_person_clean = normalize_text(main_person.strip())
                
                # Tạo key unique để check trùng
                rel_key = f"{relative_name_clean}_{relationship}_{main_person_clean}"
                
                # Kiểm tra xem đã có record này chưa
                already_exists = False
                for existing_record in records:
                    if (existing_record.get('name', '').lower() == relative_name_clean.lower() and
                        existing_record.get('relationship', '').lower() == relationship.lower() and
                        existing_record.get('related_to', '').lower() == main_person_clean.lower()):
                        already_exists = True
                        break
                
                if not already_exists and len(relative_name_clean) >= 3:
                    # Tạo record cho người thân
                    relative_record = {
                        'source': str(filename),
                        'type': 'relative_record',
                        'name': relative_name_clean,
                        'relationship': normalize_text(relationship),
                        'related_to': main_person_clean,
                        'raw_text': f"{main_person} có {relationship} là {relative_name}"
                    }
                    records.append(relative_record)
            
            print(f"✅ Đã trích xuất {len(records)} bản ghi từ {filename}")
            
            # Debug: In ra một số record mẫu
            if records:
                print("📋 Mẫu records:")
                for i, record in enumerate(records[:3]):
                    print(f"   {i+1}. Type: {record['type']}, Name: {record.get('name', 'N/A')}")
                    if record['type'] == 'relative_record':
                        print(f"      -> {record.get('relationship', 'N/A')} của {record.get('related_to', 'N/A')}")
            
            return records
            
        except Exception as e:
            print(f"❌ Lỗi khi đọc Word {filename}: {e}")
            return []
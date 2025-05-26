from extractors.base_extractor import BasePatternExtractor
import re
from typing import Dict, List
from utils.utils import normalize_text

class VietnamesePatternExtractor(BasePatternExtractor):
    """Extractor cho tài liệu tiếng Việt"""
    
    def _load_patterns(self) -> Dict:
        """Patterns từ code gốc, đã được test và hoạt động tốt"""
        return {
            # Họ tên - cải tiến để bắt được tên từ các tài liệu thực tế
            'name_patterns': [
                # Từ Word: "Nhân sự Hà Thị Anh H."
                r'Nhân\s*sự\s+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*){1,4})',
                # Từ PDF: "Họ tên: Phạm Thị Hải Hà"
                r'Họ\s*tên\s*:\s*([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*){1,4})',
                # Quan hệ gia đình: "có mẹ chồng là Phạm Thị H"
                r'(?:có|là)\s+(?:mẹ\s*chồng|bố\s*chồng|anh\s*vợ|chị\s*vợ|bố|mẹ|anh|chị|em|con|vợ|chồng)\s+(?:là\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*){1,4})',
                # Tên chung
                r'([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*){2,4})'
            ],
            
            # Ngày sinh - cải tiến dựa trên PDF
            'dob_patterns': [
                r'Ngày\s*sinh\s*:\s*(\d{1,2}/\d{1,2}/\d{4})',
                r'Sinh\s*năm\s*(\d{4})',
                r'sinh\s*ngày\s*(\d{1,2}/\d{1,2}/\d{4})',
                r'(\d{1,2}/\d{1,2}/\d{4})'
            ],
            
            # Số hộ chiếu - dựa trên PDF thực tế
            'passport_patterns': [
                # Từ PDF: "Số hộ chiếu: 060564488", "Số hộ chiếu: B9102661"
                r'Số\s*hộ\s*chiếu\s*:\s*([A-Z]?\d{7,9}(?:[A-Z]\d{5,6})?)',
                r'([A-Z]\d{7,8})',
                r'(\d{8,9})',
                # Hộ chiếu có mã thêm: "060564488H05858"
                r'(\d{9}[A-Z]\d{5})'
            ],
            
            # CCCD/CMND
            'id_patterns': [
                r'(?:CCCD|CMND|căn\s*cước|chứng\s*minh)\s*[:\-]?\s*(\d{9,12})',
                r'\b(\d{9}|\d{12})\b'
            ],
            
            # Ngày xuất/nhập cảnh
            'travel_date_patterns': [
                r'Ngày\s*xuất\s*:\s*(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{1,2}:\d{1,2})',
                r'Ngày\s*nhập\s*:\s*(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{1,2}:\d{1,2})',
                r'(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{1,2}:\d{1,2})'
            ],
            
            # Cửa khẩu
            'gate_patterns': [
                r'Cửa\s*(?:Xuất|Nhập)\s*cảnh\s*:\s*([^:\n]+)',
                r'(?:SBQT|Lào\s*Cai|Nội\s*Bài)',
                r'(Lào\s*Cai|SBQT\s*Nội\s*Bài)'
            ],
            
            # Mục đích
            'purpose_patterns': [
                r'Mục\s*đích\s*:\s*([^:\n]+)',
                r'(thương\s*mại|du\s*lịch|mục\s*đích\s*khác)'
            ],
            
            # Chức vụ từ Word
            'position_patterns': [
                r'\(([^)]*(?:Phó|Chủ\s*tịch|Chánh\s*án|Giáo\s*viên)[^)]*)\)',
                r'(Phó\s*Ban[^,\n]*)',
                r'(Chánh\s*án[^,\n]*)',
                r'(Chủ\s*tịch[^,\n]*)',
                r'(Giáo\s*viên[^,\n]*)'
            ],
            
            # Hồ sơ reference từ Word
            'file_ref_patterns': [
                r'hồ\s*sơ\s*([A-Z]?\d+[/A-Z\d]*)',
                r'(S\d+[A-Z]*)',
                r'(\d+/\d+[A-Z])',
                r'(N\d+/\d+)'
            ]
        }
    
    def extract_info_from_text(self, text: str, source_file: str = "") -> List[Dict]:
        """Trích xuất thông tin từ văn bản với focus vào các pattern thực tế"""
        results = []
        text = re.sub(r'\s+', ' ', text)
        
        extracted_data = {
            'source': source_file,
            'names': set(),
            'dobs': set(),
            'passports': set(),
            'ids': set(),
            'travel_dates': set(),
            'gates': set(),
            'purposes': set(),
            'positions': set(),
            'file_refs': set()
        }
        
        # Trích xuất theo từng pattern group
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
                                
                except Exception as e:
                    continue
        
        # Convert sets to lists
        for key in extracted_data:
            if isinstance(extracted_data[key], set):
                extracted_data[key] = list(extracted_data[key])
        
        # Tạo records từ dữ liệu trích xuất
        if extracted_data['names']:
            for name in extracted_data['names']:
                record = self._create_record(extracted_data, name, source_file, text)
                results.append(record)
        
        # Nếu có thông tin xuất nhập cảnh mà không có tên, tạo record riêng
        if extracted_data['passports'] and not extracted_data['names']:
            record = self._create_record(extracted_data, "", source_file, text)
            record['type'] = 'travel_record'
            results.append(record)
        
        return results
    
    def _clean_value(self, value, field_type):
        """Làm sạch giá trị"""
        value = value.strip()
        
        if field_type in ['passports', 'ids']:
            return ''.join(c for c in value if c.isalnum())
        elif field_type == 'names':
            # Loại bỏ ký tự đặc biệt, chỉ giữ chữ cái và khoảng trắng
            clean_name = re.sub(r'[^\w\s]', '', value)
            return ' '.join(word.capitalize() for word in clean_name.split())
        else:
            return value
    
    def _extract_relative_names(self, text):
        """Trích xuất tên thân nhân từ text thông tin thân nhân"""
        if not text or len(text.strip()) < 3:
            return []
        
        relative_names = []
        
        # Pattern để tìm tên trong text thân nhân
        # Ví dụ: "Phạm Thị H", "Nguyễn Văn A", "Trương Quốc T"
        name_patterns = [
            # Tên đầy đủ hoặc viết tắt
            r'([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*\s+(?:Thị|Văn|Xuân|Minh|Hoàng|Ngọc|Tuyết|Anh)\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]\.?)',
            # Tên họ + tên đệm + tên viết tắt
            r'([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]+\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]\.?)',
            # Tên đầy đủ 2-4 từ
            r'([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*){1,3})'
        ]
        
        for pattern in name_patterns:
            try:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0]
                    
                    clean_name = match.strip().rstrip('.')
                    if len(clean_name) >= 4:  # Tên tối thiểu 4 ký tự
                        # Loại bỏ các từ không phải tên
                        skip_words = ['hồ sơ', 'tài liệu', 'pv06', 'công an', 'tỉnh', 'lưu tại', 'phản ánh']
                        if not any(skip in clean_name.lower() for skip in skip_words):
                            relative_names.append(clean_name)
            except:
                continue
        
        # Loại bỏ trùng lặp và sắp xếp
        unique_names = []
        for name in relative_names:
            if name not in unique_names:
                unique_names.append(name)
        
        return unique_names[:5]  # Giới hạn tối đa 5 tên

    def _extract_family_relationships(self, text):
        """Trích xuất chi tiết mối quan hệ gia đình từ text"""
        if not text:
            return []
        
        relationships = []
        
        # Định nghĩa các mối quan hệ gia đình với pattern tương ứng
        relationship_patterns = {
            # Gia đình ruột
            'bố ruột': r'(?:có\s+)?(?:bố|cha)\s+(?:ruột\s+)?(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'mẹ ruột': r'(?:có\s+)?(?:mẹ|má)\s+(?:ruột\s+)?(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'con trai': r'(?:có\s+)?con\s+trai\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'con gái': r'(?:có\s+)?con\s+gái\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'anh ruột': r'(?:có\s+)?anh\s+(?:ruột\s+)?(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'chị ruột': r'(?:có\s+)?chị\s+(?:ruột\s+)?(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'em ruột': r'(?:có\s+)?em\s+(?:ruột\s+)?(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            
            # Gia đình vợ/chồng
            'bố chồng': r'(?:có\s+)?bố\s+chồng\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'mẹ chồng': r'(?:có\s+)?mẹ\s+chồng\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'bố vợ': r'(?:có\s+)?bố\s+vợ\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'mẹ vợ': r'(?:có\s+)?mẹ\s+vợ\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'chồng': r'(?:có\s+)?chồng\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'vợ': r'(?:có\s+)?vợ\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            
            # Anh chị em dâu/rể
            'anh vợ': r'(?:có\s+)?anh\s+vợ\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'chị vợ': r'(?:có\s+)?chị\s+vợ\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'em vợ': r'(?:có\s+)?em\s+vợ\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'anh chồng': r'(?:có\s+)?anh\s+chồng\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'chị chồng': r'(?:có\s+)?chị\s+chồng\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'em chồng': r'(?:có\s+)?em\s+chồng\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            
            # Con dâu/con rể
            'con dâu': r'(?:có\s+)?con\s+dâu\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'con rể': r'(?:có\s+)?con\s+rể\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            
            # Ông bà
            'ông nội': r'(?:có\s+)?ông\s+(?:nội|ngoại)\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})',
            'bà nội': r'(?:có\s+)?bà\s+(?:nội|ngoại)\s+(?:là\s+|tên\s+)?([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,\n\-\.]{3,30})'
        }
        
        for relationship_type, pattern in relationship_patterns.items():
            try:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        name = match[0]
                    else:
                        name = match
                    
                    # Làm sạch tên
                    clean_name = name.strip().rstrip('.,;-–')
                    
                    # Loại bỏ các từ không phải tên
                    skip_words = ['hồ sơ', 'tài liệu', 'pv06', 'công an', 'tỉnh', 'lưu tại', 'phản ánh']
                    if not any(skip in clean_name.lower() for skip in skip_words) and len(clean_name) >= 4:
                        relationships.append({
                            'relationship': relationship_type,
                            'name': normalize_text(clean_name),
                            'raw_text': match
                        })
            except Exception as e:
                continue
        
        return relationships
    
    def _create_record(self, data, name, source, text):
        """Tạo record từ dữ liệu trích xuất"""
        record = {
            'source': source,
            'type': 'person',
            'name': name,
            'raw_text': text[:300] + "..." if len(text) > 300 else text
        }
        
        # Thêm thông tin khác
        if data['dobs']:
            record['dob'] = data['dobs'][0]
        if data['passports']:
            record['passport'] = data['passports'][0]
        if data['ids']:
            record['id_number'] = data['ids'][0]
        if data['travel_dates']:
            record['travel_dates'] = data['travel_dates']
        if data['gates']:
            record['gates'] = data['gates']
        if data['purposes']:
            record['purposes'] = data['purposes']
        if data['positions']:
            record['position'] = data['positions'][0]
        if data['file_refs']:
            record['file_reference'] = data['file_refs'][0]
        
        return record
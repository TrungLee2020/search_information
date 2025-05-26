import pandas as pd
from pathlib import Path
from typing import List, Dict
from utils.utils import normalize_text, DataExporter
from extractors.vietnamese_extractor import VietnamesePatternExtractor
class ExcelProcessor:
    """Xử lý Excel files"""
    
    def __init__(self, extractor=None, exporter=None):
        self.extractor = extractor if extractor is not None else VietnamesePatternExtractor()
        self.exporter = exporter if exporter is not None else DataExporter()
    
    def process_file(self, filename: Path) -> List[Dict]:
        """Logic từ extract_excel_data_optimized của code gốc"""
        try:
            excel_file = pd.ExcelFile(filename)
            records = []

            for sheet_name in excel_file.sheet_names:
                try:
                    df = pd.read_excel(filename, sheet_name=sheet_name)
                    
                    # Tìm các cột theo tên cụ thể
                    nhan_su_col = None
                    vi_tri_col = None
                    than_nhan_col = None
                    
                    # Mapping các tên cột có thể có
                    column_mappings = {
                        'nhan_su': ['nhân sự', 'nhan su', 'personnel', 'staff', 'tên', 'họ tên', 'name'],
                        'vi_tri': ['vị trí nhân sự', 'vi tri nhan su', 'chức vụ', 'chuc vu', 'position', 'title'],
                        'than_nhan': ['thân nhân có tài liệu', 'than nhan co tai lieu', 'thân nhân', 'than nhan', 'relative']
                    }
                    
                    # Tìm cột tương ứng
                    for col in df.columns:
                        col_lower = str(col).lower().strip()
                        
                        if not nhan_su_col:
                            for keyword in column_mappings['nhan_su']:
                                if keyword in col_lower:
                                    nhan_su_col = col
                                    break
                        
                        if not vi_tri_col:
                            for keyword in column_mappings['vi_tri']:
                                if keyword in col_lower:
                                    vi_tri_col = col
                                    break
                        
                        if not than_nhan_col:
                            for keyword in column_mappings['than_nhan']:
                                if keyword in col_lower:
                                    than_nhan_col = col
                                    break
                    
                    # Debug thông tin cột tìm thấy
                    print(f"📊 Sheet '{sheet_name}' - Tìm thấy cột:")
                    if nhan_su_col:
                        print(f"   👤 Nhân sự: '{nhan_su_col}'")
                    if vi_tri_col:
                        print(f"   💼 Vị trí: '{vi_tri_col}'")
                    if than_nhan_col:
                        print(f"   👨‍👩‍👧‍👦 Thân nhân: '{than_nhan_col}'")

                    # Group data để xử lý merged cells và multiple rows cho cùng nhân sự
                    personnel_data = {}
                    # Pass 1: Thu thập tất cả dữ liệu
                    for index, row in df.iterrows():
                        # Bỏ qua hàng trống hoặc hàng header
                        if index == 0 or row.isna().all():
                            continue

                        # Lấy thông tin nhân sự                    
                        current_personnel = None
                        current_position = None
                        current_relatives = None
                        
                        if nhan_su_col and pd.notna(row[nhan_su_col]):
                            personnel_text = str(row[nhan_su_col]).strip()
                            if personnel_text and len(personnel_text) > 2 and personnel_text.lower() not in ['nhân sự', 'tên', 'họ tên', 'name']:
                                current_personnel = normalize_text(personnel_text)
                        
                        if vi_tri_col and pd.notna(row[vi_tri_col]):
                            position_text = str(row[vi_tri_col]).strip()
                            if position_text and len(position_text) > 2:
                                current_position = normalize_text(position_text)
                        
                        if than_nhan_col and pd.notna(row[than_nhan_col]):
                            relatives_text = str(row[than_nhan_col]).strip()
                            if relatives_text and len(relatives_text) > 2:
                                current_relatives = relatives_text
                        
                        # Xử lý logic grouping
                        if current_personnel:
                            # Nếu có nhân sự mới.
                            if current_personnel not in personnel_data:
                                personnel_data[current_personnel] = {
                                    'name': current_personnel,
                                    'position': current_position,
                                    'relatives_info_list': [],
                                    'row_numbers': []
                                }
                            else:
                                # Cập nhật position nếu chưa có hoặc row hiện tại có position
                                if current_position and not personnel_data[current_personnel]['position']:
                                    personnel_data[current_personnel]['position'] = current_position

                            # Thêm thông tin thân nhân
                            if current_relatives:
                                personnel_data[current_personnel]['relatives_info_list'].append(current_relatives)
                                personnel_data[current_personnel]['row_numbers'].append(index + 1)

                        elif current_relatives and personnel_data:
                            # Không có nhân sự mới, nhưng có thông tin của nhân thân
                            # Gán cho nhân sự gần nhất
                            last_personnel = list(personnel_data.keys())[-1] if personnel_data else None
                            if last_personnel:
                                personnel_data[last_personnel]['relatives_info_list'].append(current_relatives)
                                personnel_data[last_personnel]['row_numbers'].append(index + 1)
                    
                    # Pass 2: Tạo records từ personnel_data
                    for personnel_name, personnel_info in personnel_data.items():
                        main_record = {
                            'source': f"{filename}#{sheet_name}",
                            'type': 'excel_personnel',
                            'name': personnel_info['name'],
                            'row_numbers': personnel_info['row_numbers']
                        }
                        
                        if personnel_info['position']:
                            main_record['position'] = personnel_info['position']
                        
                        # Gôp thông tin thân nhân
                        if personnel_info['relatives_info_list']:
                            all_relatives_info = ' | '.join(personnel_info['relatives_info_list'])
                            main_record['relatives_info'] = all_relatives_info
                        
                            # Trích xuất thông tin thân nhân
                            all_relative_names = set()
                            all_family_relationships = []

                            for relatives_text in personnel_info['relatives_info_list']:
                                # Trích xuất tên thân nhân
                                relative_names = self.extractor._extract_relative_names(relatives_text)
                                all_relative_names.update(relative_names)

                                # Trichs xuất mối quan hệ gia đình
                                family_relationships = self.extractor._extract_family_relationships(relatives_text)
                                all_family_relationships.extend(family_relationships)
                            
                            if all_relative_names:
                                main_record['relative_names'] = list(all_relative_names)
                            if all_family_relationships:
                                main_record['family_relationships'] = all_family_relationships
                            
                            main_record['relatives_count'] = len(personnel_info['relatives_info_list'])

                        records.append(main_record)

                        # Tạo record cho từng thân nhân
                        if main_record.get('family_relationships'):
                            for rel_info in main_record['family_relationships']:
                                rel_record = {
                                    'source': f"{filename}#{sheet_name}",
                                    'type': 'excel_relative',
                                    'name': rel_info['name'],
                                    'relationship': rel_info['relationship'],
                                    'related_to': main_record['name'],
                                    'related_to_position': main_record.get('position', ''),
                                    'row_numbers': personnel_info['row_numbers'],
                                    'relatives_info': all_relatives_info,
                                    'raw_relationship_text': rel_info['raw_text']
                                }
                                records.append(rel_record)
                    
                    # Method 2: Full text search nếu không tìm thấy cột chuẩn
                    if not nhan_su_col and not vi_tri_col and not than_nhan_col:
                        print(f"⚠️  Không tìm thấy cột chuẩn, sử dụng full text extraction")
                        full_text = df.to_string()
                        extracted_records = self.extractor.extract_info_from_text(full_text, f"{filename}#{sheet_name}")
                        records.extend(extracted_records)
                
                except Exception as e:
                    print(f"Lỗi khi đọc sheet '{sheet_name}': {e}")
                    continue
            print(f"✅ Đã xử lý {len(records)} bản ghi từ file {filename}")
            return records
            
        except Exception as e:
            print(f"Lỗi khi đọc Excel {filename}: {e}")
            return []

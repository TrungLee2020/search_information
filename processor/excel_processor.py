import pandas as pd
from pathlib import Path
from typing import List, Dict
from core.trie import normalize_text

class ExcelProcessor:
    """Xử lý Excel files - dựa trên logic optimized từ code gốc"""
    
    def __init__(self, extractor):
        self.extractor = extractor
    
    def process_file(self, filename: Path) -> List[Dict]:
        """Logic từ extract_excel_data_optimized của code gốc"""
        try:
            excel_file = pd.ExcelFile(filename)
            records = []
            
            for sheet_name in excel_file.sheet_names:
                try:
                    df = pd.read_excel(filename, sheet_name=sheet_name)
                    
                    # Tìm các cột theo tên cụ thể - logic từ code gốc
                    nhan_su_col = None
                    vi_tri_col = None
                    than_nhan_col = None
                    
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
                    
                    # Xử lý data theo logic từ code gốc
                    personnel_data = {}
                    
                    for index, row in df.iterrows():
                        if index == 0 or row.isna().all():
                            continue
                        
                        current_personnel = None
                        current_position = None
                        current_relatives = None
                        
                        if nhan_su_col and pd.notna(row[nhan_su_col]):
                            personnel_text = str(row[nhan_su_col]).strip()
                            if personnel_text and len(personnel_text) > 2:
                                current_personnel = normalize_text(personnel_text)
                        
                        if vi_tri_col and pd.notna(row[vi_tri_col]):
                            position_text = str(row[vi_tri_col]).strip()
                            if position_text and len(position_text) > 2:
                                current_position = normalize_text(position_text)
                        
                        if than_nhan_col and pd.notna(row[than_nhan_col]):
                            relatives_text = str(row[than_nhan_col]).strip()
                            if relatives_text and len(relatives_text) > 2:
                                current_relatives = relatives_text
                        
                        # Logic grouping từ code gốc
                        if current_personnel:
                            if current_personnel not in personnel_data:
                                personnel_data[current_personnel] = {
                                    'name': current_personnel,
                                    'position': current_position,
                                    'relatives_info_list': [],
                                    'row_numbers': []
                                }
                            
                            if current_relatives:
                                personnel_data[current_personnel]['relatives_info_list'].append(current_relatives)
                                personnel_data[current_personnel]['row_numbers'].append(index + 1)
                    
                    # Tạo records
                    for personnel_name, personnel_info in personnel_data.items():
                        main_record = {
                            'source': f"{filename}#{sheet_name}",
                            'type': 'excel_personnel',
                            'name': personnel_info['name'],
                            'row_numbers': personnel_info['row_numbers']
                        }
                        
                        if personnel_info['position']:
                            main_record['position'] = personnel_info['position']
                        
                        if personnel_info['relatives_info_list']:
                            all_relatives_info = ' | '.join(personnel_info['relatives_info_list'])
                            main_record['relatives_info'] = all_relatives_info
                        
                        records.append(main_record)
                    
                    # Fallback: full text extraction
                    if not nhan_su_col and not vi_tri_col and not than_nhan_col:
                        full_text = df.to_string()
                        extracted_records = self.extractor.extract_info_from_text(full_text, f"{filename}#{sheet_name}")
                        records.extend(extracted_records)
                
                except Exception as e:
                    print(f"Lỗi khi đọc sheet '{sheet_name}': {e}")
                    continue
            
            return records
            
        except Exception as e:
            print(f"Lỗi khi đọc Excel {filename}: {e}")
            return []

import argparse
import datetime
from pathlib import Path
from collections import defaultdict
from extractors.vietnamese_extractor import VietnamesePatternExtractor
from processor.excel_processor import ExcelProcessor
from processor.word_processor import WordProcessor
from processor.pdf_processor import PDFProcessor
from search.search_engine import SearchEngine
import re
from typing import List, Dict, Any


class DocumentSearchSystem:
    """Main application class - tích hợp tất cả modules"""
    
    def __init__(self):
        self.extractor = VietnamesePatternExtractor()
        self.excel_processor = ExcelProcessor(self.extractor)
        self.word_processor = WordProcessor(self.extractor)
        self.pdf_processor = PDFProcessor(self.extractor)
        self.search_engine = SearchEngine()
        self.data = []
    
    def load_data(self, data_dir: Path):
        """Load dữ liệu từ thư mục"""
        self.data = []
        
        if not data_dir.exists():
            print(f"❌ Thư mục 'data' không tồn tại: {data_dir}")
            return 0
        
        print(f"📁 Đang quét thư mục: {data_dir}")
        
        all_files = list(data_dir.iterdir())
        if not all_files:
            print("❌ Thư mục 'data' trống.")
            return []
        
        print("📋 Files được tìm thấy:")
        for file in all_files:
            print(f"  - {file.name}")        

        # Excel files
        for file in data_dir.iterdir():
            if file.suffix.lower() in ['.xlsx', '.xls']:
                print(f"📊 Xử lý Excel: {file.name}")
                records = self.excel_processor.process_file(file)
                self.data.extend(records)
        
        # Word files  
        for file in data_dir.iterdir():
            if file.suffix.lower() in ['.docx', '.doc']:
                print(f"📄 Xử lý Word: {file.name}")
                records = self.word_processor.process_file(file)
                self.data.extend(records)
        
        # PDF files
        for file in data_dir.iterdir():
            if file.suffix.lower() == '.pdf':
                print(f"📑 Xử lý PDF: {file.name}")
                records = self.pdf_processor.process_file(file)
                self.data.extend(records)
        
        # Build search index
        if self.data:
            print("🔍 Đang xây dựng search index...")
            self.search_engine.build_index(self.data)
        
        print(f"✅ Tổng cộng: {len(self.data)} bản ghi")
        return len(self.data)
    
    def search(self, query, field=None, threshold=70):
        """Tìm kiếm đơn giản"""
        return self.search_engine.search(query, field, threshold)
    
    def smart_search(self, query, threshold=70):
        """Smart search với auto-detection"""
        query = query.strip()
        if not query:
            return []

        if re.match(r'^\d{9}$|^\d{12}$', query):
            return self.search(query, 'id_number', threshold)
        elif re.match(r'^[A-Z]?\d{7,9}$', query):
            return self.search(query, 'passport', threshold)
        elif re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', query):
            try:
                datetime.strptime(query, "%d/%m/%Y")
                return self.search(query, 'dob', threshold)
            except ValueError:
                return []
        elif len(query.split()) >= 2 and not re.search(r'\d', query):
            return self.search(query, 'name', threshold)
        else:
            return self.search(query, None, threshold)
    
    def get_statistics(self):
        """Thống kê dữ liệu"""
        stats = {
            'total_records': len(self.data),
            'sources': defaultdict(int),
            'types': defaultdict(int),
            'fields': defaultdict(int)
        }
        
        for record in self.data:
            source = record.get('source', 'unknown')
            stats['sources'][Path(source).name] += 1
            
            record_type = record.get('type', 'unknown')
            stats['types'][record_type] += 1
            
            for field in record.keys():
                if field not in ['source', 'type', 'raw_text']:
                    stats['fields'][field] += 1
        
        return dict(stats)

def display_results(results, max_results=50):
    """Hiển thị kết quả"""
    if not results:
        print("Không tìm thấy kết quả.")
        return
    
    # Group results by type
    grouped = defaultdict(list)
    for result in results:
        record_type = result['record'].get('type', 'unknown')
        grouped[record_type].append(result)
    
    print(f"\n🔍 Tìm thấy {len(results)} kết quả:")
    print("=" * 80)
    
    displayed_count = 0
    for record_type, type_results in grouped.items():
        if displayed_count >= max_results:
            break
            
        # icon = type_icons.get(record_type, '📄')
        print(f"\n{record_type.upper().replace('_', ' ')} ({len(type_results)} kết quả)")
        print("-" * 40)
        
        for i, result in enumerate(type_results[:min(5, max_results - displayed_count)], 1):
            record = result['record']
            
            print(f"\n{displayed_count + 1}. Điểm: {result['score']:.1f} | Field: {result['matched_field']}")
            print(f"   Nguồn: {record['source']}")
            
            if record.get('name'):
                print(f"   Tên: {record['name']}")
            
            if record.get('dob'):
                print(f"   Sinh: {record['dob']}")
                
            if record.get('passport'):
                print(f"   Hộ chiếu: {record['passport']}")
                
            if record.get('id_number'):
                print(f"   CCCD: {record['id_number']}")
                
            if record.get('travel_date'):
                print(f"   Ngày: {record['travel_date']}")
                
            if record.get('entry_type'):
                print(f"   Loại: {record['entry_type']}")
                
            if record.get('gate'):
                print(f" Cửa khẩu: {record['gate']}")
                
            if record.get('purpose'):
                print(f" Mục đích: {record['purpose']}")
                
            if record.get('position'):
                print(f" Chức vụ: {record['position']}")
                
            if record.get('file_reference'):
                print(f" Hồ sơ: {record['file_reference']}")
            
            # Thông tin đặc biệt cho Excel records
            if record.get('relationship'):
                print(f" Quan hệ: {record['relationship']}")
            
            if record.get('related_to'):
                print(f" Liên quan đến: {record['related_to']}")
            
            if record.get('related_to_position'):
                print(f"Chức vụ người liên quan: {record['related_to_position']}")
            
            if record.get('relatives_info'):
                print(f"Thông tin thân nhân: {record['relatives_info'][:100]}...")
            
            if record.get('relative_names'):
                print(f"Tên thân nhân: {', '.join(record['relative_names'])}")
            
            if record.get('family_relationships'):
                print(f"Chi tiết quan hệ gia đình:")
                for rel in record['family_relationships'][:3]:  # Hiển thị tối đa 3 quan hệ
                    print(f"      • {rel['relationship']}: {rel['name']}")
            
            if record.get('row_number'):
                print(f"Hàng số: {record['row_number']}")
            
            displayed_count += 1
            if displayed_count >= max_results:
                break
        
        if displayed_count >= max_results:
            break
    
    if len(results) > max_results:
        print(f"\n... và {len(results) - max_results} kết quả khác")


def show_statistics(stats):
    """Hiển thị thống kê"""
    print("\n📊 THỐNG KÊ DỮ LIỆU")
    print("=" * 50)
    
    print("📈 Theo loại:")
    for record_type, count in sorted(stats['types'].items()):
        print(f"  • {record_type}: {count}")
    
    print(f"\n📁 Theo nguồn:")
    for source, count in sorted(stats['sources'].items()):
        print(f"  • {source}: {count}")
    
    # Count records with key fields
    print(f"\n📝 Thống kê fields:")
    for field, count in sorted(stats['fields'].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  • {field}: {count}")

def create_cli():
    """Tạo CLI đơn giản"""
    parser = argparse.ArgumentParser(
        description="🔍 Document Search System v2.0",
        epilog="""
Ví dụ sử dụng:
    python main.py --query "Nguyễn Văn A"
    python main.py --query "123456789" --smart
    python main.py --query "Phạm Thị" --field name
    python main.py --stats
        """
    )
    
    parser.add_argument('--query', help='Từ khóa tìm kiếm')
    parser.add_argument('--field', help='Trường cụ thể (name, passport, id_number, dob)')
    parser.add_argument('--threshold', type=int, default=70, help='Ngưỡng similarity (0-100)')
    parser.add_argument('--max-results', type=int, default=50, help='Số kết quả tối đa')
    parser.add_argument('--stats', action='store_true', help='Hiển thị thống kê dữ liệu')
    parser.add_argument('--smart', action='store_true', help='Tìm kiếm thông minh')
    parser.add_argument('--date-range', help='Tìm theo khoảng ngày: start_date,end_date')
    parser.add_argument('--data-dir', type=Path, default=Path('data'), help='Thư mục dữ liệu')
    
    return parser

def main():
    """Main function đơn giản và rõ ràng"""
    parser = create_cli()
    args = parser.parse_args()
    
    print("🚀 Khởi động Document Search System v2.0...")
    
    # Khởi tạo system
    search_system = DocumentSearchSystem()
    
    # Load data
    record_count = search_system.load_data(args.data_dir)
    if record_count == 0:
        print("❌ Không có dữ liệu để xử lý.")
        return
    
    # Hiển thị thống kê nếu được yêu cầu
    if args.stats:
        stats = search_system.get_statistics()
        show_statistics(stats)
        if not args.query:
            return

    # if args.date_range:
    #     # Date range search
    #     dates = args.date_range.split(',')
    #     if len(dates) == 2:
    #         start_date, end_date = dates
    #         print(f"Tìm kiếm theo khoảng thời gian: {start_date} → {end_date}")
    #         results = search_system.search_by_date_range(args.query, start_date.strip(), end_date.strip())
    #     else:
    #         print("Format ngày không đúng. Sử dụng: start_date,end_date")
    #         return    
    # Thực hiện tìm kiếm
    if args.query:
        print(f"\n🔍 Tìm kiếm: '{args.query}'")
        
        if args.smart:
            print("🧠 Sử dụng smart search")
            results = search_system.smart_search(args.query, args.threshold)
        else:
            if args.field:
                print(f"📂 Trong field: {args.field}")
            results = search_system.search(args.query, args.field, args.threshold)
        
        # Hiển thị kết quả
        display_results(results, args.max_results)
    
    else:
        print("\n💡 Sử dụng:")
        print("  python main.py --query 'Nguyễn Văn A'")
        print("  python main.py --query '123456789' --smart")
        print("  python main.py --stats")

if __name__ == '__main__':
    main()
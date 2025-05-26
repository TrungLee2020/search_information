# 🔍 Document Search System v2.0

Hệ thống tìm kiếm thông tin thông minh từ các tài liệu (Excel, Word, PDF) với khả năng trích xuất và tìm kiếm nâng cao cho văn bản tiếng Việt.

## 📋 Tính năng chính

### 🚀 Tính năng nổi bật
- **Đa định dạng**: Hỗ trợ Excel (.xlsx, .xls), Word (.docx, .doc), PDF
- **Trích xuất thông minh**: Tự động nhận diện và trích xuất thông tin quan trọng
- **Tìm kiếm mạnh mẽ**: Sử dụng nhiều thuật toán similarity (Fuzzy, Levenshtein, Jaro-Winkler)
- **Hỗ trợ tiếng Việt**: Xử lý tốt văn bản tiếng Việt có dấu
- **Smart Search**: Tự động nhận diện loại thông tin cần tìm

### 📊 Thông tin được trích xuất
- **Thông tin cá nhân**: Họ tên, ngày sinh, CCCD/CMND, hộ chiếu
- **Quan hệ gia đình**: Thân nhân, mối quan hệ (bố, mẹ, vợ, chồng, con...)
- **Thông tin công việc**: Chức vụ, vị trí
- **Thông tin xuất nhập cảnh**: Ngày, cửa khẩu, mục đích
- **Tài liệu tham chiếu**: Số hồ sơ, nguồn tài liệu

## 🛠️ Cài đặt

### Yêu cầu hệ thống
- Python 3.8 trở lên
- RAM: Tối thiểu 4GB (khuyến nghị 8GB cho file lớn)

### Cài đặt dependencies

```bash
# Clone repository
git clone https://github.com/TrungLee2020/search_information.git
cd search_information

# Tạo virtual environment (khuyến nghị)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### Cấu trúc thư mục

```
search_information/
├── data/                   # Thư mục chứa files cần xử lý
├── config/                 # Cấu hình hệ thống
│   └── settings.py
├── core/                   # Core components
│   └── trie.py
├── extractors/             # Modules trích xuất thông tin
│   ├── base_extractor.py
│   ├── vietnamese_extractor.py
│   └── english_extractor.py
├── processor/              # Xử lý các loại file
│   ├── excel_processor.py
│   ├── word_processor.py
│   └── pdf_processor.py
├── search/                 # Engine tìm kiếm
│   ├── search_engine.py
│   └── advanced_search.py
├── utils/                  # Tiện ích
│   └── utils.py
├── main.py                 # Entry point
└── requirements.txt
```

## 💻 Sử dụng

### 1. Chuẩn bị dữ liệu
Đặt các file cần xử lý vào thư mục `data/`:
```bash
mkdir data
# Copy các file Excel, Word, PDF vào thư mục data/
```

### 2. Sử dụng cơ bản

```bash
# Tìm kiếm theo tên
python main.py --query "Nguyễn Văn A"

# Tìm kiếm thông minh (tự động nhận diện loại dữ liệu)
python main.py --query "123456789" --smart

# Tìm kiếm trong field cụ thể
python main.py --query "B9102661" --field passport

# Xem thống kê dữ liệu
python main.py --stats
```

### 3. Tùy chọn nâng cao

```bash
# Điều chỉnh ngưỡng similarity (0-100)
python main.py --query "Phạm Thị" --threshold 80

# Giới hạn số kết quả
python main.py --query "Nguyễn" --max-results 20

# Chỉ định thư mục dữ liệu khác
python main.py --query "test" --data-dir /path/to/data

# Kết hợp nhiều tùy chọn
python main.py --query "Hà Thị" --field name --threshold 85 --stats
```

## 📖 Ví dụ sử dụng

### Tìm kiếm thông tin cá nhân
```bash
# Tìm theo tên
python main.py --query "Phạm Thị Hải Hà"

# Tìm theo CCCD
python main.py --query "123456789012"

# Tìm theo hộ chiếu
python main.py --query "B9102661"
```

### Tìm kiếm thông tin quan hệ
```bash
# Tìm người có quan hệ với nhân sự cụ thể
python main.py --query "Nguyễn Văn A" --field related_to

# Tìm theo loại quan hệ
python main.py --query "mẹ chồng" --field relationship
```

### Smart Search (Tự động nhận diện)
```bash
# Hệ thống tự nhận diện đây là số CCCD
python main.py --query "123456789" --smart

# Tự nhận diện đây là ngày sinh
python main.py --query "15/03/1990" --smart
```

## 🔧 Cấu hình

### Điều chỉnh settings (config/settings.py)
```python
class Settings:
    DEFAULT_THRESHOLD = 70          # Ngưỡng similarity mặc định
    MAX_RESULTS = 100              # Số kết quả tối đa
    SUPPORTED_EXTENSIONS = ['.xlsx', '.xls', '.docx', '.doc', '.pdf']
    
    # Trọng số cho scoring
    FIELD_WEIGHTS = {
        'name': 2.0,
        'passport': 1.8,
        'id_number': 1.8,
        'dob': 1.5,
        'position': 1.2
    }
```

## 📊 Định dạng dữ liệu

### Excel files
Hệ thống tự động nhận diện các cột:
- Nhân sự / Họ tên / Name
- Vị trí / Chức vụ / Position
- Thân nhân có tài liệu / Relatives

### Word files
Hỗ trợ các định dạng:
- Danh sách nhân sự với format: `1. Nhân sự [Tên] ([Chức vụ]) có [quan hệ]...`
- Văn bản tự do chứa thông tin cá nhân

### PDF files
- Hồ sơ xuất nhập cảnh
- Tài liệu scan chứa thông tin cá nhân

## 🚀 Hiệu năng

- **Xử lý nhanh**: Trie structure cho tìm kiếm tên hiệu quả
- **Index thông minh**: Inverted index cho tìm kiếm full-text
- **Tối ưu bộ nhớ**: Xử lý file lớn theo batch
- **Multi-threading**: Có thể mở rộng cho xử lý song song

## 🐛 Xử lý lỗi

Hệ thống xử lý các lỗi phổ biến:
- File không tồn tại hoặc bị lỗi
- Định dạng dữ liệu không chuẩn
- Encoding không đúng (tự động detect UTF-8)
- Memory overflow với file quá lớn

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:
1. Fork repository
2. Tạo branch mới (`git checkout -b feature/New_Feature`)
3. Commit changes (`git commit -m 'Add some New_Feature'`)
4. Push to branch (`git push origin feature/New_Feature`)
5. Tạo Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Liên hệ

- Email: trungx1204@gmail.com
- Project Link: [https://github.com/TrungLee2020/search_information.git](https://github.com/TrungLee2020/search_information.git)

## 🙏 Acknowledgments

- [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) - Fuzzy string matching
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - PDF processing
- [python-docx](https://github.com/python-openxml/python-docx) - Word processing
- [pandas](https://pandas.pydata.org/) - Excel processing
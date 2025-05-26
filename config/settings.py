class Settings:
    """Cấu hình cho hệ thống"""
    
    DEFAULT_THRESHOLD = 70
    MAX_RESULTS = 100
    SUPPORTED_EXTENSIONS = ['.xlsx', '.xls', '.docx', '.doc', '.pdf', '.txt', '.csv']
    
    # Field weights cho scoring
    FIELD_WEIGHTS = {
        'name': 2.0,
        'passport': 1.8,
        'id_number': 1.8,
        'dob': 1.5,
        'position': 1.2
    }
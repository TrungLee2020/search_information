from rapidfuzz import fuzz
from Levenshtein import distance as levenshtein_distance
from jellyfish import jaro_winkler_similarity
import datetime
from collections import defaultdict
from utils.utils import normalize_text
from core.trie import Trie
from typing import List, Dict, Any

class SearchEngine:
    """Search Engine"""
    
    def __init__(self, similarity_threshold=70):
        self.similarity_threshold = similarity_threshold
        self.trie = Trie()
        self.inverted_index = defaultdict(list)
        # self.data = []
    
    def build_index(self, data):
        """Build index"""
        self.data = data
        # self.trie = Trie()
        # self.inverted_index = defaultdict(list)
        
        for record in data:
            # Index tên chính
            if record.get('name'):
                self.trie.insert(record['name'], record)
                self.inverted_index['name'].append((record['name'], record))
            
            # Index tên thân nhân nếu có
            if record.get('relative_names'):
                for rel_name in record['relative_names']:
                    self.trie.insert(rel_name, record)
                    self.inverted_index['name'].append((rel_name, record))
            
            # Index tên người liên quan và quan hệ
            if record.get('related_to'):
                self.inverted_index['related_to'].append((record['related_to'], record))
            
            if record.get('relationship'):
                self.inverted_index['relationship'].append((record['relationship'], record))
            
            # Index các field quan trọng
            key_fields = ['passport', 'id_number', 'dob', 'travel_date', 'position']
            for field in key_fields:
                if record.get(field):
                    self.inverted_index[field].append((record[field], record))
            
            # Index travel_dates nếu là list
            if record.get('travel_dates') and isinstance(record['travel_dates'], list):
                for date in record['travel_dates']:
                    self.inverted_index['travel_date'].append((date, record))
            
            # Index thông tin thân nhân
            if record.get('relatives_info'):
                # Tách từ để index
                words = record['relatives_info'].lower().split()
                for word in words:
                    if len(word) > 2:  # Chỉ index từ có ý nghĩa
                        self.inverted_index['relatives_info'].append((word, record))
            
            # Index family relationships
            if record.get('family_relationships'):
                for rel in record['family_relationships']:
                    self.inverted_index['family_name'].append((rel['name'], record))
                    self.inverted_index['family_relationship'].append((rel['relationship'], record))
    
    def search(self, query, field=None, threshold=None):
        """Tìm kiếm"""
        if threshold is None:
            threshold = self.similarity_threshold
            
        query_normalized = normalize_text(query)
        results = []
        
        # Exact search trong inverted index
        if field and field in self.inverted_index:
            for key, record in self.inverted_index[field]:
                if query_normalized == normalize_text(key):
                    results.append({'record': record, 'score': 100.0, 'matched_field': field})
        elif not field:
            # Tìm trong tên qua Trie
            trie_results = self.trie.search(query_normalized)
            for record in trie_results:
                results.append({'record': record, 'score': 100.0, 'matched_field': 'name'})
        
        # Fuzzy search nếu chưa có kết quả
        if len(results) < 5:
            for record in self.data:
                max_score = 0
                matched_field = None
                
                search_fields = ['name', 'passport', 'id_number', 'dob', 'position', 'file_reference']
                if field:
                    search_fields = [field] if field in search_fields else []
                
                for search_field in search_fields:
                    if record.get(search_field):
                        value_normalized = normalize_text(str(record[search_field]))
                        score = self._calculate_similarity(query_normalized, value_normalized)
                        
                        if score > max_score:
                            max_score = score
                            matched_field = search_field
                
                if max_score >= threshold:
                    # Kiểm tra xem record đã có trong kết quả chưa: kiểm tra trùng lặp
                    existing = any(r['record'] == record for r in results)
                    if not existing:
                        results.append({
                            'record': record, 
                            'score': max_score, 
                            'matched_field': matched_field
                        })
        
        return sorted(results, key=lambda x: x['score'], reverse=True)
    
    def _calculate_similarity(self, query, value):
        """Tính similarity - logic từ code gốc"""
        if not query or not value:
            return 0
        
        scores = []
        scores.extend([
            fuzz.ratio(query, value),
            fuzz.partial_ratio(query, value),
            fuzz.token_sort_ratio(query, value),
            fuzz.token_set_ratio(query, value)
        ])
        
        # Levenshtein distance
        max_len = max(len(query), len(value))
        if max_len > 0:
            lev_dist = levenshtein_distance(query, value)
            lev_score = ((max_len - lev_dist) / max_len) * 100
            scores.append(lev_score)
        
        # Jaro-Winkler
        try:
            jaro_score = jaro_winkler_similarity(query, value) * 100
            scores.append(jaro_score)
        except:
            pass
        
        return max(scores) if scores else 0
    
    def _search_by_date_range(self, data, start_date, end_date):
        """Tìm kiếm theo khoảng thời gian"""
        results = []
        
        def parse_date(date_str):
            """Parse ngày từ string"""
            try:
                # Thử nhiều format để tìm kiếm theo khoảng thời gian
                formats = ['%d/%m/%Y', '%d/%m/%Y %H:%M:%S', '%Y-%m-%d', '%d-%m-%Y']
                for fmt in formats:
                    try:
                        return datetime.strptime(date_str.strip(), fmt)
                    except:
                        continue
                return None
            except:
                return None
        
        start_dt = parse_date(start_date) if start_date else None
        end_dt = parse_date(end_date) if end_date else None
        
        for record in data:
            record_dates = []
            
            # Lấy các ngày từ record
            if record.get('dob'):
                record_dates.append(record['dob'])
            if record.get('travel_date'):
                record_dates.append(record['travel_date'])
            if record.get('travel_dates'):
                record_dates.extend(record['travel_dates'])
            
            for date_str in record_dates:
                date_obj = parse_date(date_str)
                if date_obj:
                    match = True
                    if start_dt and date_obj < start_dt:
                        match = False
                    if end_dt and date_obj > end_dt:
                        match = False
                    
                    if match:
                        results.append({
                            'record': record,
                            'matched_date': date_str,
                            'score': 100.0,
                            'matched_field': 'date'
                        })
                        break
        
        return results
    
    # Multi-field search
    def _multi_field_search(self, data, trie, inverted_index, criteria_dict, threshold=70):
        """
        Tìm kiếm đa trường
        criteria_dict: {'name': 'Phạm Thị Hải Hà', 'passport': '060564488'}
        """
        all_results = []
        
        for field, query in criteria_dict.items():
            field_results = SearchEngine.search(data, trie, inverted_index, query, field, threshold)
            all_results.extend(field_results)
        
        # Group by record và tính điểm trung bình
        record_scores = defaultdict(list)
        for result in all_results:
            record_id = id(result['record'])
            record_scores[record_id].append(result)
        
        # Lọc records khớp với nhiều tiêu chí
        final_results = []
        for record_id, results_list in record_scores.items():
            if len(results_list) >= max(1, len(criteria_dict) // 2):  # Khớp ít nhất 50% tiêu chí
                avg_score = sum(r['score'] for r in results_list) / len(results_list)
                final_results.append({
                    'record': results_list[0]['record'],
                    'score': avg_score,
                    'matched_field': f"multi_criteria({len(results_list)})",
                    'matched_criteria': len(results_list)
                })
        
        return sorted(final_results, key=lambda x: x['score'], reverse=True)


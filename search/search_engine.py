from rapidfuzz import fuzz
from Levenshtein import distance as levenshtein_distance
from jellyfish import jaro_winkler_similarity

from collections import defaultdict
from core.trie import Trie, normalize_text
from typing import List, Dict, Any

class SearchEngine:
    """Search Engine dựa trên logic tốt từ code gốc"""
    
    def __init__(self, similarity_threshold=70):
        self.similarity_threshold = similarity_threshold
        self.trie = Trie()
        self.inverted_index = defaultdict(list)
        self.data = []
    
    def build_index(self, data):
        """Build index - logic từ code gốc"""
        self.data = data
        self.trie = Trie()
        self.inverted_index = defaultdict(list)
        
        for record in data:
            # Index tên chính
            if record.get('name'):
                self.trie.insert(record['name'], record)
                self.inverted_index['name'].append((record['name'], record))
            
            # Index các field quan trọng - theo logic code gốc
            key_fields = ['passport', 'id_number', 'dob', 'travel_date', 'position']
            for field in key_fields:
                if record.get(field):
                    self.inverted_index[field].append((record[field], record))
            
            # Index travel_dates nếu là list
            if record.get('travel_dates') and isinstance(record['travel_dates'], list):
                for date in record['travel_dates']:
                    self.inverted_index['travel_date'].append((date, record))
    
    def search(self, query, field=None, threshold=None):
        """Tìm kiếm - logic từ search_data_enhanced của code gốc"""
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
        
        # Fuzzy search nếu chưa có kết quả - logic từ code gốc
        if len(results) < 5:
            for record in self.data:
                max_score = 0
                matched_field = None
                
                search_fields = ['name', 'passport', 'id_number', 'dob', 'position']
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
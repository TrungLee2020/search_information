# -*- coding: utf-8 -*-
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.records = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, name, record):
        node = self.root
        for char in name:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.records.append(record)

    def search(self, query):
        node = self.root
        for char in query:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_records(node)

    def _collect_records(self, node):
        records = []
        if node.is_end:
            records.extend(node.records)
        for child in node.children.values():
            records.extend(self._collect_records(child))
        return records

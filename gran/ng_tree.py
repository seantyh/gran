from typing import Dict, Tuple, List

Frequency = int
Character = str

class NGramBP:
    def __init__(self, charac: str, index: int):
        self.charac = charac
        self.index = index

class Node:
    def __init__(self, charac):
        self.charac: str = charac
        self.freq_data: Dict[NGramBP, Frequency] = {}
        self.bp_index = -1

    def new_index(self):
        self.bp_index += 1
        return self.bp_index

    def traceback(self, bp_key):
        if bp_key not in self.freq_data:
    
    def __contains__(self, item):
        return item in self.freq_data

class NGramGraph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
    
    def instantiate_node(self, charac):
        if charac not in self.nodes:
            self.nodes[charac] = Node(charac)
        
        return self.nodes[charac]

    def encode(self, ngram: str, freq: Frequency):
        for gram_x in ngram[::-1]:
            

    def decode(self, ngram: str):
        pass
import pandas as pd
import pickle
from opencc import OpenCC
from .lex_pattern import LexPattern
from typing import List

class Lexicon:
    def __init__(self):
        self.__nword = 0
        self.nword_dirty = True
        self.word_list = {}
        self.annotations = {}

    def __repr__(self):
        return f"<Lexicon: {self.nword} words>"

    @property
    def nword(self):
        if self.nword_dirty:
            self.nword_dirty = False
            self.__nword = sum(len(x) for x in self.word_list.values())
        return self.__nword    
        
    def add_word(self, word, use_regex=False, annot=None):
        if not word: return
        w0 = word[0]
        wlist_x = self.word_list.setdefault(w0, [])        
        wlist_x.append(LexPattern(word, use_regex))   

        if annot:
            self.annotations[word] = annot            
                                
        self.nword_dirty = True
    
    def find_prefixes(self, chars) -> List[LexPattern]:
        candids = set()
        for ch_x in chars:
            candids.update(self.word_list.get(ch_x, []))
        return candids
    
    def get_annotation(self, lu):
        return self.annotations.get(lu, {})

class AnnotFrameAdaptor:
    def __init__(self, lexicon, fpath):
        self.lexicon = lexicon
        self.fpath = fpath
        self.load(fpath)
    
    def __repr__(self):
        return f"<AnnotFrameAdaptor: {self.fpath}>"

    def load(self, fpath):
        frame = pd.read_csv(fpath)
        for ridx, row in frame.iterrows():
            annot_dict = row.to_dict()
            annot_dict.pop("lexical_unit")
            annot_dict.pop("index")
            use_regex = annot_dict.get("form") == '3.2'
            self.lexicon.add_word(row.lexical_unit, use_regex, row.to_dict())

class PmiNgramAdaptor:
    def __init__(self, lexicon, fpath):
        self.lexicon = lexicon
        self.fpath = fpath
        self.load(fpath)
    
    def __repr__(self):
        return f"<PmiNgramAdaptor: {self.fpath}>"

    def load(self, fpath):
        with open(fpath, "rb") as fin:
            data = pickle.load(fin)
        
        wlist = []
        cc_inst = OpenCC('s2t')
        s2t = cc_inst.convert

        for word in data.keys():
            word_new = s2t(word.replace("|", ""))
            self.lexicon.add_word(word_new)
        



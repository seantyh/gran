from ..utils import *
import jieba
from .lexicon import Lexicon

class Segmenter:
    def __init__(self, lexicon):
        self.lexicon: Lexicon = lexicon

    def preprocess_matches(self, matches):
        matches = sorted(matches, key=lambda x: (x[0], -x[1]))
        start_idx_set = []
        preproc_mat = []
        for start_idx, nchar in matches:
            if start_idx in [x[0] for x in preproc_mat]:
                continue
            if preproc_mat and start_idx < preproc_mat[-1][0] + preproc_mat[-1][1]:
                continue
            else:
                preproc_mat.append((start_idx, nchar))
        return preproc_mat

    def segment(self, text):
        candids = self.lexicon.find_prefixes(text)
        matches = []
        annot_data = {}
        for pat_x in candids:
            candid_matches = pat_x.findall(text)
            if candid_matches:
                pat_text = pat_x.pattern
                annot_data[pat_text] = self.lexicon.get_annotation(pat_text)
            matches.extend(candid_matches)
        
        # partition the text
        matches = self.preprocess_matches(matches)
        segments = []
        cursor = 0
        while cursor < len(text):
            if matches and cursor == matches[0][0]:
                nchar = matches[0][1]
                segments.append(text[cursor:cursor+nchar])
                cursor += nchar
                matches = matches[1:]
            else:
                if matches:
                    end_idx = matches[0][0]
                else:
                    end_idx = len(text)
                segments.extend(jieba.cut(text[cursor:end_idx]))
                cursor = end_idx
        return segments, annot_data



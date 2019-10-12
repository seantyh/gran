from ..utils import *
import jieba
from .lexicon import Lexicon
import logging

class Segmenter:
    def __init__(self, lexicon):
        self.lexicon: Lexicon = lexicon
        self.logger = logging.getLogger("Segmenter")
        self.logger.setLevel("DEBUG")

    def preprocess_matches(self, matches):
        matches = sorted(matches, key=lambda x: (-x[1], x[0]))
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

    def find_best_route(self, matches):        
        best_route = None
        best_score = 0
        for mat_x in matches:
            self.logger.debug(f"Start: {mat_x}")
            route, route_score = self.select_route(mat_x, matches)
            self.logger.debug(f"route: {route}")
            self.logger.debug(f"route_score: {route_score}")
            if route_score < best_score:
                best_route = route
                best_score = route_score

        return best_route, best_score

    def select_route(self, start_match, matches):

        def score_func(match_x):
            # use length as match score
            return match_x[1]

        buffer = matches.copy()
        route = [start_match]
        route_score = score_func(start_match)        

        while buffer:
            
            current = route[-1]
            current_score_max = 0
            best_match = None
            for match_x in buffer:                                 
                cur_end = current[0] + current[1]
                if match_x == current:                
                    buffer.remove(match_x)
                    continue
                elif match_x[0] < cur_end:
                    buffer.remove(match_x)
                    continue
                elif match_x[0] >= cur_end:                    
                    cur_score = score_func(match_x)                    
                    if current_score_max < cur_score:
                        self.logger.debug(f"Route(score): {match_x}({cur_score})")
                        best_match = match_x
                        current_score_max = cur_score

            if best_match:
                buffer.remove(best_match)
                route.append(best_match)
                route_score += current_score_max                

        return route, route_score

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



from ..utils import *
import jieba
from .lexicon import Lexicon
import logging
from typing import List, Tuple

MatchStart = int
MatchLength = int
Matches = Tuple[MatchStart, MatchLength]

class Segmenter:
    def __init__(self, lexicon):
        self.lexicon: Lexicon = lexicon
        self.logger = logging.getLogger("Segmenter")
        self.logger.setLevel("DEBUG")

    def preprocess_matches(self, matches):
        matches = sorted(matches, key=lambda x: (x[0], -x[1]))        
        return matches

    def find_best_route(self, matches):
        best_route = None
        best_score = 0
        for mat_x in matches:
            self.logger.debug(f"Start: {mat_x}")
            route, route_score = self.select_route([mat_x], matches)
            if best_score < route_score:
                best_route = route
                best_score = route_score

        return best_route, best_score

    def select_route(self, prev_route:List[Matches], matches: List[Matches]):

        DEBUG_INDENT = len(prev_route) * "  " + "->"
        def score_func(matches:List[Matches]):
            # use length as match score            
            return sum([x[1] for x in matches])

        buffer = matches.copy()                        
        prev_route_score = score_func(prev_route)

        best_next_score = prev_route_score
        best_next_route = prev_route.copy()

        for match_x in matches:
            current = prev_route[-1]            
            cur_end = current[0] + current[1]

            if match_x == current:
                buffer.remove(match_x)
                continue
            elif match_x[0] < cur_end:
                buffer.remove(match_x)
                continue
            elif match_x[0] >= cur_end:
                next_route = prev_route + [match_x]
                new_route, new_route_score = self.select_route(next_route, buffer)
                                    
                if best_next_score < new_route_score:
                    self.logger.debug(f"{DEBUG_INDENT}Route(score): {new_route}({new_route_score})")                        
                    best_next_score = new_route_score
                    best_next_route = new_route        

        return best_next_route, best_next_score

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
        route, route_score = self.find_best_route(matches)
        self.logger.debug("Best Route: " + str(route))
        segments = []
        cursor = 0
        while cursor < len(text):
            if matches and cursor == route[0][0]:
                nchar = route[0][1]
                segments.append(text[cursor:cursor+nchar])
                cursor += nchar
                route = route[1:]
            else:
                if matches:
                    end_idx = route[0][0]
                else:
                    end_idx = len(text)
                segments.extend(jieba.cut(text[cursor:end_idx]))
                cursor = end_idx
        return segments, annot_data



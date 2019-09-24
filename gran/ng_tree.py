from collections import namedtuple
from functools import reduce
from typing import Dict, Tuple, List, Set
from . import utils

Frequency = int
Character = str

NgTag = namedtuple("NgTag", ["charac", "offset"])

class NgTagSet:
    def __init__(self):
        self.tag_map = {}

    def __len__(self):
        return sum([len(x) for x in self.tag_map.values()])

    @property
    def n_charac(self):
        return len(self.tag_map)

    def __contains__(self, item: NgTag):
        if isinstance(item, NgTag):
            charac = item.charac
            offset = item.offset
            if charac in self.tag_map:
                if offset in self.tag_map[charac]:
                    return True
            return False
        if isinstance(item, str):
            return item in self.tag_map
        raise TypeError("unsupported item type, expect NgTag or str")

    def add(self, item: NgTag):
        offsets = self.tag_map.setdefault(item[0], [])
        offsets.append(item[1])
        return item

    def get_offsets(self, charac: str):
        return sorted(self.tag_map.get(charac, []))


class NgNode:
    def __init__(self, charac):
        self.charac: str = charac
        self.tags: NgTagSet = NgTagSet()

    def __repr__(self):
        return f"<NgNode: {self.charac}, with {len(self.tags)} tags>"

    def register(self, charac: str, offset: int):
        tag = NgTag(charac, offset)
        self.tags.add(tag)

class NgGraph:
    def __init__(self, window_size = 3):
        self.nodes: Dict[str, NgNode] = {}
        self.win = window_size + 1
    
    def instantiate_node(self, charac):
        if charac not in self.nodes:
            self.nodes[charac] = NgNode(charac)
        
        return self.nodes[charac]

    def encode(self, ngram: str):
        win = self.win
        delims = utils.get_word_boundary_index(ngram)
        chseq = ngram.replace('|', '')
        for base_i in range(len(chseq)):
            base_ch = chseq[base_i]
            base_node = self.instantiate_node(base_ch)
            for offset_i in range(-win, win):
                if offset_i == 0: continue
                cur_idx = base_i + offset_i
                if not (0 <= cur_idx < len(chseq)):
                    continue
                ch_x = chseq[cur_idx]
                base_node.register(ch_x, offset_i)

    def decode(self, ngram: str):
        entry_node = self.nodes.get(ngram[0])
        if not entry_node:
            return False

        if len(ngram) == 1:
            return True

        buf = [1]
        while buf:
            offset = buf.pop()
            charac = ngram[offset]
            
            tag_x = NgTag(charac, offset)
            hasTag = tag_x in entry_node.tags
            if not hasTag:
                return False
            
            if offset+1 < len(ngram):
                buf.append(offset+1)
        return True
                
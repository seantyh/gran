import pytest
from gran import Lexicon, LexPattern, Segmenter

def test_segment():
    lex = Lexicon()
    lex.add_word("不知道")
    lex.add_word("!+", True, {"form": "3.2"})
    seg = Segmenter(lex)    
    segs, anno_data = seg.segment("我不知道你要不知道的知道!!!!")    
    assert segs == ['我', '不知道', '你', '要', '不知道', '的', '知道', '!!!!']
    assert anno_data == {'不知道': {}, '!+': {'form': '3.2'}}

def test_segment_conflict():
    lex = Lexicon()    
    lex.add_word("知不知道", True, {"form": "3.2"})
    lex.add_word("不知道的知道", True, {"form": "3.2"})
    lex.add_word("!+", True, {"form": "3.2"})
    seg = Segmenter(lex)
    segs, anno_data = seg.segment("我不知道你知不知道的知道!!!!")    
    print(segs, anno_data)
    assert segs == ['我', '不', '知道', "你", "知", "不知道的知道", '!!!!']    

def test_segment_conflict2():
    lex = Lexicon()    
    lex.add_word("不知道", True, {"form": "3.2"})
    lex.add_word("不知道的知道", True, {"form": "3.2"})
    lex.add_word("!+", True, {"form": "3.2"})
    seg = Segmenter(lex)
    segs, anno_data = seg.segment("我不知道你不知道的知道!!!!")    
    print(segs, anno_data)
    assert segs == ['我', '不知道', "你", "不知道的知道", '!!!!']    

def test_segment_best_route():
    lex = Lexicon()    
    seg = Segmenter(lex)
    route, score = seg.find_best_route([(0,2), (0,3), (2,5), (3,2), (5,4), (7,2)])    
    assert route == [(0,2), (2,5), (7,2)] 
    route, score = seg.find_best_route([(0,2), (0,3), (2,5), (3,2), (5,8), (7,2)])
    assert route == [(0,3), (3,2), (5,8)] 

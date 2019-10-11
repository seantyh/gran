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


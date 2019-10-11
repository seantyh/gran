import pytest
from gran import LexPattern

def test_lex_pattern():
    lex_pat = LexPattern("123")
    mat = lex_pat.findall("123456")
    assert mat == [(0, 3)]
    mat = lex_pat.findall("123456123")
    assert mat == [(0, 3), (6, 3)]

def test_lex_regexPattern():
    lex_pat = LexPattern.from_regex("1.3")
    mat = lex_pat.findall("123456133")
    assert mat == [(0, 3), (6, 3)]


    
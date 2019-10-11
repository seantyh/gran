import pytest
from gran import Lexicon

def test_lexicon():
    lex = Lexicon()
    lex.add_word("123")
    lex.add_word("1.3")
    lex.add_word("456", False, {"test_data": "aaa"})
    word_set = lex.find_prefixes("1")
    words = [x.pattern for x in word_set]
    assert len(words) == 2
    assert "123" in words
    assert "1.3" in words
    assert lex.get_annotation("456")["test_data"] == "aaa"


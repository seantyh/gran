import pytest
from gran import NgNode, NgGraph, NgTag

def test_node():
    node = NgNode("測")
    assert node

def test_graph():
    graph = NgGraph()
    assert graph

def test_word_boudary():
    test_str = "蘋果|電腦|有|梨子"
    test_str_2 = "沒有|人|會|來|救|你|的"
    ng = NgGraph()
    delims = ng.get_word_boundary_index(test_str)
    delims2 = ng.get_word_boundary_index(test_str_2)
    assert delims == [2, 4, 5]
    assert delims2 == [2, 3, 4, 5, 6, 7]

def test_add_ngram():
    graph = NgGraph()
    ngram1 = "蘋果電腦"
    ngram2 = "果粉表示"
    freq = 100
    graph.encode(ngram1)
    graph.encode(ngram2)
    n1 = graph.instantiate_node('果')
    print(n1.tags)
    assert NgTag("蘋", -1) in n1.tags
    assert NgTag("電", 1) in n1.tags
    assert NgTag("腦", 2) in n1.tags
    assert NgTag("粉" ,1) in n1.tags
    assert NgTag("表", 2) in n1.tags
    assert NgTag("示", 3) in n1.tags 

def test_decode_ngram():
    graph = NgGraph()
    ngram1 = "蘋果電腦"
    ngram2 = "果粉表示"
    freq = 100
    graph.encode(ngram1)
    graph.encode(ngram2)

    assert graph.decode("果電腦") == True
    assert graph.decode("蘋果電") == True
    assert graph.decode("蘋果") == True
    assert graph.decode("粉表") == True
    assert graph.decode("果表示") == False
    assert graph.decode("電腦示") == False
    assert graph.decode("沒有人") == False

    
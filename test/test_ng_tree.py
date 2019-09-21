import pytest
from gran import NgNode, NgGraph

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
    ngram = "蘋果電腦"
    freq = 100
    graph.encode(ngram)
    n1 = graph.instantiate_node('果')
    print(n1.tags)
    # assert graph.decode(ngram)
    
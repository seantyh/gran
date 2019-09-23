import gran
import pytest

def test_ngTagSet():
    tag_set = gran.ng_tree.NgTagSet()
    with pytest.raises(TypeError):
        assert tag_set.add(3)
    assert tag_set.add(gran.NgTag("我", 2))
    assert tag_set.add(gran.NgTag("我", 1))
    assert tag_set.add(gran.NgTag("她", -1))
    assert "我" in tag_set
    assert gran.NgTag("我", 1) in tag_set
    assert tag_set.get_offsets("我") == [1,2]
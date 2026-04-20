from app.core.containers import (
    count_words,
    create_chain_map,
    create_deque,
    create_ordered_dict,
    create_point,
    group_by_category,
)


class TestCounter:
    def test_count_words_basic(self):
        text = "apple banana apple cherry banana apple"
        result = count_words(text)
        assert result["apple"] == 3
        assert result["banana"] == 2
        assert result["cherry"] == 1

    def test_count_words_most_common(self):
        text = "a b c a b a"
        result = count_words(text)
        assert result.most_common(1) == [("a", 3)]

    def test_count_words_empty(self):
        result = count_words("")
        assert len(result) == 0


class TestDefaultdict:
    def test_group_by_category(self):
        items = [
            {"name": "apple", "category": "fruit"},
            {"name": "carrot", "category": "vegetable"},
            {"name": "banana", "category": "fruit"},
        ]
        result = group_by_category(items, "category")
        assert result["fruit"] == ["apple", "banana"]
        assert result["vegetable"] == ["carrot"]

    def test_group_by_missing_key(self):
        items = [{"name": "item1"}, {"name": "item2"}]
        result = group_by_category(items, "category")
        assert result["missing"] == ["item1", "item2"]


class TestNamedTuple:
    def test_create_point(self):
        point = create_point(3, 4)
        assert point.x == 3
        assert point.y == 4

    def test_point_distance(self):
        point = create_point(3, 4)
        assert point.distance() == 5.0

    def test_point_is_namedtuple(self):
        point = create_point(1, 2)
        assert point._fields == ("x", "y")


class TestDeque:
    def test_create_deque(self):
        d = create_deque([1, 2, 3], maxlen=5)
        assert list(d) == [1, 2, 3]
        assert d.maxlen == 5

    def test_deque_append_left(self):
        d = create_deque([2, 3])
        d.appendleft(1)
        assert list(d) == [1, 2, 3]

    def test_deque_rotate(self):
        d = create_deque([1, 2, 3, 4, 5])
        d.rotate(2)
        assert list(d) == [4, 5, 1, 2, 3]


class TestOrderedDict:
    def test_create_ordered_dict(self):
        items = [("c", 3), ("a", 1), ("b", 2)]
        od = create_ordered_dict(items)
        assert list(od.keys()) == ["c", "a", "b"]

    def test_move_to_end(self):
        od = create_ordered_dict([("a", 1), ("b", 2), ("c", 3)])
        od.move_to_end("a")
        assert list(od.keys()) == ["b", "c", "a"]

    def test_popitem_last(self):
        od = create_ordered_dict([("a", 1), ("b", 2)])
        key, value = od.popitem()
        assert key == "b"
        assert value == 2


class TestChainMap:
    def test_create_chain_map(self):
        dict1 = {"a": 1, "b": 2}
        dict2 = {"b": 3, "c": 4}
        cm = create_chain_map(dict1, dict2)
        assert cm["a"] == 1
        assert cm["b"] == 2
        assert cm["c"] == 4

    def test_chain_map_update(self):
        cm = create_chain_map({"a": 1}, {"b": 2})
        cm["a"] = 10
        assert cm["a"] == 10
        assert cm.maps[0]["a"] == 10

    def test_chain_map_new_child(self):
        cm = create_chain_map({"a": 1})
        child = cm.new_child({"a": 2})
        assert child["a"] == 2

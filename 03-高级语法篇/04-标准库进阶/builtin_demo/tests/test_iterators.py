from app.core.iterators import (
    accumulate_sum,
    cartesian_product,
    chain_iterators,
    cycle_iterator,
    drop_while,
    generate_combinations,
    generate_permutations,
    repeat_value,
    slice_iterator,
    take_while,
    zip_longest_merge,
)


class TestChain:
    def test_chain_basic(self):
        result = list(chain_iterators([1, 2], [3, 4]))
        assert result == [1, 2, 3, 4]

    def test_chain_empty(self):
        result = list(chain_iterators())
        assert result == []

    def test_chain_multiple(self):
        result = list(chain_iterators([1], [2, 3], [4, 5, 6]))
        assert result == [1, 2, 3, 4, 5, 6]


class TestCombinations:
    def test_combinations_basic(self):
        result = list(generate_combinations([1, 2, 3], 2))
        assert result == [(1, 2), (1, 3), (2, 3)]

    def test_combinations_length_one(self):
        result = list(generate_combinations(["a", "b"], 1))
        assert result == [("a",), ("b",)]

    def test_combinations_full_length(self):
        result = list(generate_combinations([1, 2], 2))
        assert result == [(1, 2)]


class TestPermutations:
    def test_permutations_basic(self):
        result = list(generate_permutations([1, 2, 3], 2))
        assert result == [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

    def test_permutations_full_length(self):
        result = list(generate_permutations([1, 2], None))
        assert result == [(1, 2), (2, 1)]


class TestProduct:
    def test_product_basic(self):
        result = list(cartesian_product([1, 2], ["a", "b"]))
        assert result == [(1, "a"), (1, "b"), (2, "a"), (2, "b")]

    def test_product_repeat(self):
        result = list(cartesian_product([0, 1], repeat=2))
        assert result == [(0, 0), (0, 1), (1, 0), (1, 1)]


class TestCycle:
    def test_cycle_basic(self):
        c = cycle_iterator([1, 2])
        result = [next(c) for _ in range(5)]
        assert result == [1, 2, 1, 2, 1]

    def test_cycle_single(self):
        c = cycle_iterator(["x"])
        result = [next(c) for _ in range(3)]
        assert result == ["x", "x", "x"]


class TestRepeat:
    def test_repeat_times(self):
        result = list(repeat_value("a", 3))
        assert result == ["a", "a", "a"]

    def test_repeat_infinite(self):
        r = repeat_value(1)
        assert next(r) == 1
        assert next(r) == 1


class TestSlice:
    def test_slice_basic(self):
        result = list(slice_iterator(range(10), 5))
        assert result == [0, 1, 2, 3, 4]

    def test_slice_with_start(self):
        result = list(slice_iterator(range(10), 2, 5))
        assert result == [2, 3, 4]


class TestTakewhileDropwhile:
    def test_take_while(self):
        result = list(take_while(lambda x: x < 5, [1, 2, 3, 4, 5, 6, 7]))
        assert result == [1, 2, 3, 4]

    def test_drop_while(self):
        result = list(drop_while(lambda x: x < 5, [1, 2, 3, 4, 5, 6, 7]))
        assert result == [5, 6, 7]


class TestAccumulate:
    def test_accumulate_sum(self):
        result = list(accumulate_sum([1, 2, 3, 4]))
        assert result == [1, 3, 6, 10]

    def test_accumulate_empty(self):
        result = list(accumulate_sum([]))
        assert result == []


class TestZipLongest:
    def test_zip_longest_basic(self):
        result = list(zip_longest_merge([1, 2], ["a", "b", "c"]))
        assert result == [(1, "a"), (2, "b"), (None, "c")]

    def test_zip_longest_fillvalue(self):
        result = list(zip_longest_merge([1, 2, 3, 4], ["a", "b"], fillvalue="X"))
        assert result == [(1, "a"), (2, "b"), (3, "X"), (4, "X")]

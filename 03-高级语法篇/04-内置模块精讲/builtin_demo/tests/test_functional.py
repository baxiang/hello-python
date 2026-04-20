from app.core.functional import (
    cached_property_demo,
    clear_cache,
    create_comparable_point,
    create_multiplier,
    fibonacci_cached,
    get_cache_info,
    multiply_all,
    preserve_decorator_info,
    process_data,
)


class TestLRUCache:
    def test_fibonacci_cached(self):
        assert fibonacci_cached(10) == 55
        assert fibonacci_cached(10) == 55

    def test_cache_info(self):
        fibonacci_cached(5)
        fibonacci_cached(5)
        info = get_cache_info()
        assert info.hits >= 1
        assert info.misses >= 1

    def test_clear_cache(self):
        fibonacci_cached(7)
        clear_cache()
        info = get_cache_info()
        assert info.hits == 0
        assert info.misses == 0


class TestPartial:
    def test_create_multiplier(self):
        double = create_multiplier(2)
        assert double(5) == 10
        triple = create_multiplier(3)
        assert triple(5) == 15

    def test_partial_with_multiple_args(self):
        from functools import partial

        def add(a, b, c):
            return a + b + c

        add_five = partial(add, 5)
        assert add_five(3, 2) == 10


class TestReduce:
    def test_multiply_all(self):
        result = multiply_all([1, 2, 3, 4, 5])
        assert result == 120

    def test_multiply_all_empty(self):
        result = multiply_all([], initial=1)
        assert result == 1

    def test_multiply_all_with_initial(self):
        result = multiply_all([2, 3], initial=10)
        assert result == 60


class TestWraps:
    def test_preserve_decorator_info(self):
        @preserve_decorator_info
        def my_func():
            """My docstring"""
            pass

        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "My docstring"


class TestTotalOrdering:
    def test_create_comparable_point(self):
        p1 = create_comparable_point(1, 1)
        p2 = create_comparable_point(2, 2)
        assert p1 < p2
        assert p2 > p1
        assert p1 <= p2
        assert p2 >= p1
        assert p1 != p2

    def test_comparable_point_equal(self):
        p1 = create_comparable_point(1, 1)
        p2 = create_comparable_point(1, 1)
        assert p1 == p2
        assert p1 <= p2
        assert p1 >= p2


class TestSingledispatch:
    def test_process_int(self):
        result = process_data(42)
        assert result == "Integer: 42"

    def test_process_str(self):
        result = process_data("hello")
        assert result == "String: hello"

    def test_process_list(self):
        result = process_data([1, 2, 3])
        assert result == "List with 3 items"

    def test_process_default(self):
        result = process_data(3.14)
        assert result == "Unknown type: float"


class TestCachedProperty:
    def test_cached_property_demo(self):
        obj = cached_property_demo()
        assert obj.call_count == 0
        _ = obj.expensive_value
        assert obj.call_count == 1
        _ = obj.expensive_value
        assert obj.call_count == 1

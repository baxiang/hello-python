from collections.abc import Callable, Iterator
from itertools import (
    accumulate,
    chain,
    combinations,
    cycle,
    dropwhile,
    islice,
    permutations,
    product,
    repeat,
    takewhile,
    zip_longest,
)
from typing import Any


def chain_iterators(*iterables: list) -> Iterator:
    return chain.from_iterable(iterables)


def generate_combinations(iterable: list, r: int) -> Iterator:
    return combinations(iterable, r)


def generate_permutations(iterable: list, r: int | None = None) -> Iterator:
    return permutations(iterable, r)


def cartesian_product(*iterables: list, repeat: int = 1) -> Iterator:
    return product(*iterables, repeat=repeat)


def cycle_iterator(iterable: list) -> Iterator:
    return cycle(iterable)


def repeat_value(value: Any, times: int | None = None) -> Iterator:
    if times is None:
        return repeat(value)
    return repeat(value, times)


def slice_iterator(iterable: Iterator, start: int, stop: int | None = None) -> Iterator:
    if stop is None:
        return islice(iterable, start)
    return islice(iterable, start, stop)


def take_while(predicate: Callable, iterable: list) -> Iterator:
    return takewhile(predicate, iterable)


def drop_while(predicate: Callable, iterable: list) -> Iterator:
    return dropwhile(predicate, iterable)


def accumulate_sum(iterable: list) -> Iterator:
    return accumulate(iterable)


def zip_longest_merge(*iterables: list, fillvalue: Any = None) -> Iterator:
    return zip_longest(*iterables, fillvalue=fillvalue)

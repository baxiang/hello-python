"""标准库示例"""

from collections import Counter, defaultdict, namedtuple
from itertools import chain, combinations, product
from functools import reduce, partial
from typing import Any
import json
import datetime


def collections_examples() -> dict[str, Any]:
    """collections 示例"""
    # Counter
    counter = Counter("hello world")
    
    # defaultdict
    d = defaultdict(list)
    d["fruits"].append("apple")
    
    # namedtuple
    Point = namedtuple("Point", ["x", "y"])
    p = Point(1, 2)
    
    return {
        "counter": dict(counter),
        "defaultdict": dict(d),
        "namedtuple": p._asdict()
    }


def itertools_examples() -> dict[str, Any]:
    """itertools 示例"""
    return {
        "chain": list(chain([1, 2], [3, 4])),
        "combinations": list(combinations([1, 2, 3], 2)),
        "product": list(product([1, 2], ["a", "b"]))
    }


def functools_examples() -> dict[str, Any]:
    """functools 示例"""
    # reduce
    sum_result = reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
    
    # partial
    def power(base, exp):
        return base ** exp
    
    square = partial(power, exp=2)
    
    return {
        "reduce": sum_result,
        "partial": square(5)
    }


def datetime_examples() -> dict[str, Any]:
    """datetime 示例"""
    now = datetime.datetime.now()
    return {
        "now": now.isoformat(),
        "date": now.date().isoformat(),
        "time": now.time().isoformat()
    }
import math
from collections import ChainMap, Counter, OrderedDict, defaultdict, deque, namedtuple


def count_words(text: str) -> Counter:
    words = text.split()
    return Counter(words)


def group_by_category(items: list[dict], key: str) -> defaultdict:
    grouped = defaultdict(list)
    for item in items:
        category = item.get(key, "missing")
        grouped[category].append(item["name"])
    return grouped


Point = namedtuple("Point", ["x", "y"])


class Point(Point):
    def distance(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)


def create_point(x: int, y: int) -> Point:
    return Point(x, y)


def create_deque(iterable: list | None = None, maxlen: int | None = None) -> deque:
    return deque(iterable or [], maxlen=maxlen)


def create_ordered_dict(items: list[tuple]) -> OrderedDict:
    return OrderedDict(items)


def create_chain_map(*dicts: dict) -> ChainMap:
    return ChainMap(*dicts)

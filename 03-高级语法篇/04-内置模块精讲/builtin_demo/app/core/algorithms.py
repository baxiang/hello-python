import bisect
import heapq
from collections.abc import Iterator
from typing import Any


def push_to_heap(heap: list, item: Any) -> None:
    heapq.heappush(heap, item)


def pop_from_heap(heap: list) -> Any:
    return heapq.heappop(heap)


def heapify_list(lst: list) -> list:
    result = lst.copy()
    heapq.heapify(result)
    return result


def get_n_smallest(iterable: list, n: int) -> list:
    return heapq.nsmallest(n, iterable)


def get_n_largest(iterable: list, n: int) -> list:
    return heapq.nlargest(n, iterable)


def merge_sorted(*iterables: list) -> Iterator:
    return heapq.merge(*iterables)


def binary_search_left(arr: list, target: Any) -> int:
    return bisect.bisect_left(arr, target)


def binary_search_right(arr: list, target: Any) -> int:
    return bisect.bisect_right(arr, target)


def insert_sorted(arr: list, item: Any) -> None:
    bisect.insort(arr, item)


class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0

    def push(self, item: Any, priority: int = 0) -> None:
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self) -> tuple | None:
        if not self._heap:
            return None
        priority, _, item = heapq.heappop(self._heap)
        return (item, priority)

    def peek(self) -> tuple | None:
        if not self._heap:
            return None
        priority, _, item = self._heap[0]
        return (item, priority)

    def is_empty(self) -> bool:
        return len(self._heap) == 0


class TaskScheduler:
    def __init__(self):
        self._pq = PriorityQueue()

    def add_task(self, task: str, priority: int = 0) -> None:
        self._pq.push(task, priority)

    def run_next(self) -> str | None:
        result = self._pq.pop()
        return result[0] if result else None

    def run_all(self) -> list[str]:
        results = []
        while not self._pq.is_empty():
            result = self._pq.pop()
            if result:
                results.append(result[0])
        return results

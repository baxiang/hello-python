from collections import defaultdict
from collections.abc import Callable
from typing import Any

from app.core.data import DataRecord


class DataPipeline:
    def __init__(self, data: list[DataRecord] | None = None):
        self.data: list[DataRecord] = data or []

    @classmethod
    def from_list(cls, records: list[DataRecord]) -> "DataPipeline":
        return cls(records)

    def filter(self, predicate: Callable[[DataRecord], bool]) -> "DataPipeline":
        self.data = [r for r in self.data if predicate(r)]
        return self

    def map(self, func: Callable[[DataRecord], Any]) -> "DataPipeline":
        self._mapped_data = [func(r) for r in self.data]
        return self

    def reduce(self, func: Callable[[Any, DataRecord], Any], initial: Any) -> Any:
        result = initial
        for r in self.data:
            result = func(result, r)
        return result

    def group_by(self, key: str) -> defaultdict:
        grouped = defaultdict(list)
        for r in self.data:
            grouped[getattr(r, key)].append(r)
        return grouped

    def sort_by(self, key: str, reverse: bool = False) -> "DataPipeline":
        self.data = sorted(self.data, key=lambda r: getattr(r, key), reverse=reverse)
        return self

    def batch(self, size: int) -> list[list[DataRecord]]:
        return [self.data[i : i + size] for i in range(0, len(self.data), size)]

    def execute(self) -> list[DataRecord] | list[Any]:
        if hasattr(self, "_mapped_data"):
            return self._mapped_data
        return self.data

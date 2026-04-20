from collections import namedtuple
from typing import Any

DataRecord = namedtuple("DataRecord", ["id", "name", "category", "value", "timestamp"])


class DataRecord(DataRecord):
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "value": self.value,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DataRecord":
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            category=data.get("category", "default"),
            value=data.get("value", 0),
            timestamp=data.get("timestamp", ""),
        )


def create_record(
    id: int,
    name: str,
    category: str,
    value: Any,
    timestamp: str,
) -> DataRecord:
    return DataRecord(id, name, category, value, timestamp)

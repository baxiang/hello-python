import weakref
from typing import Any


class DataObject:
    def __init__(self, data: Any):
        self.data = data

    def __repr__(self):
        return f"DataObject({self.data})"


def create_weak_reference(obj: Any) -> weakref.ref:
    return weakref.ref(obj)


class WeakValueCache:
    def __init__(self):
        self._cache: weakref.WeakValueDictionary = weakref.WeakValueDictionary()

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value

    def get(self, key: str) -> Any | None:
        return self._cache.get(key)

    def contains(self, key: str) -> bool:
        return key in self._cache


class WeakKeyCache:
    def __init__(self):
        self._cache: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()

    def set(self, key: Any, value: Any) -> None:
        self._cache[key] = value

    def get(self, key: Any) -> Any | None:
        return self._cache.get(key)

    def __len__(self) -> int:
        return len(self._cache)


class ResourceTracker:
    def __init__(self):
        self._resources: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        self._cleanup_count = 0

    def track(self, name: str, resource: Any) -> None:
        self._resources[name] = resource

        def on_finalize():
            self._cleanup_count += 1

        weakref.finalize(resource, on_finalize)

    def get(self, name: str) -> Any | None:
        return self._resources.get(name)

    def cleanup_count(self) -> int:
        return self._cleanup_count


class CircularNode:
    def __init__(self, value: Any):
        self.value = value
        self.next: CircularNode | None = None
        self.prev: weakref.ref | None = None


def create_circular_demo() -> tuple[CircularNode, CircularNode]:
    node_a = CircularNode("A")
    node_b = CircularNode("B")
    node_a.next = node_b
    node_b.prev = weakref.ref(node_a)
    return node_a, node_b

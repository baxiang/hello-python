from typing import Any


def flatten_nested(nested: list[list[Any]]) -> list[Any]:
    return [item for sublist in nested for item in sublist]


def chunk_list(lst: list[Any], size: int) -> list[list[Any]]:
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def safe_get(data: dict, key: str, default: Any = None) -> Any:
    return data.get(key, default)


def merge_dicts(*dicts: dict) -> dict:
    result = {}
    for d in dicts:
        result.update(d)
    return result


def unique_values(lst: list[Any]) -> list[Any]:
    return list(dict.fromkeys(lst))


def partition_by(lst: list[Any], predicate: callable) -> tuple[list, list]:
    true_list = []
    false_list = []
    for item in lst:
        if predicate(item):
            true_list.append(item)
        else:
            false_list.append(item)
    return true_list, false_list

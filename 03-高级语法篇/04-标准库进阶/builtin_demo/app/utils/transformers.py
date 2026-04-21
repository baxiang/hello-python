from app.core.data import DataRecord, create_record


def to_record(data: dict) -> DataRecord:
    return create_record(
        id=data.get("id", 0),
        name=data.get("name", ""),
        category=data.get("category", "default"),
        value=data.get("value", 0),
        timestamp=data.get("timestamp", ""),
    )


def records_to_dicts(records: list[DataRecord]) -> list[dict]:
    return [r.to_dict() for r in records]


def dicts_to_records(data_list: list[dict]) -> list[DataRecord]:
    return [to_record(d) for d in data_list]


def transform_values(records: list[DataRecord], field: str, func: callable) -> list:
    return [func(getattr(r, field)) for r in records]


def normalize_values(records: list[DataRecord], field: str) -> list[DataRecord]:
    values = [getattr(r, field) for r in records]
    if not values:
        return records
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val if max_val != min_val else 1

    return [
        create_record(
            r.id,
            r.name,
            r.category,
            (getattr(r, field) - min_val) / range_val,
            r.timestamp,
        )
        for r in records
    ]


def aggregate_by_key(
    records: list[DataRecord], key_field: str, value_field: str, agg_func: callable
) -> dict:
    from collections import defaultdict

    groups = defaultdict(list)
    for r in records:
        key = getattr(r, key_field)
        groups[key].append(getattr(r, value_field))

    return {k: agg_func(v) for k, v in groups.items()}

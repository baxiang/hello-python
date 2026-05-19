from app.core.data import DataRecord, create_record
from app.core.pipeline import DataPipeline


class TestDataRecord:
    def test_create_record(self):
        record = create_record(
            id=1, name="test", category="cat1", value=100, timestamp="2024-01-01"
        )
        assert record.id == 1
        assert record.name == "test"

    def test_record_to_dict(self):
        record = create_record(
            id=1, name="test", category="cat1", value=100, timestamp="2024-01-01"
        )
        d = record.to_dict()
        assert d["id"] == 1
        assert d["name"] == "test"

    def test_record_from_dict(self):
        d = {"id": 1, "name": "test", "category": "cat1", "value": 100}
        record = DataRecord.from_dict(d)
        assert record.id == 1
        assert record.name == "test"


class TestDataPipeline:
    def test_from_list(self):
        records = [
            create_record(1, "a", "cat1", 10, "2024-01-01"),
            create_record(2, "b", "cat2", 20, "2024-01-02"),
        ]
        pipeline = DataPipeline.from_list(records)
        assert len(pipeline.data) == 2

    def test_filter(self):
        records = [
            create_record(1, "a", "cat1", 10, "2024-01-01"),
            create_record(2, "b", "cat2", 20, "2024-01-02"),
            create_record(3, "c", "cat1", 30, "2024-01-03"),
        ]
        pipeline = DataPipeline.from_list(records)
        result = pipeline.filter(lambda r: r.category == "cat1").execute()
        assert len(result) == 2

    def test_map(self):
        records = [
            create_record(1, "a", "cat1", 10, "2024-01-01"),
        ]
        pipeline = DataPipeline.from_list(records)
        result = pipeline.map(lambda r: r.value * 2).execute()
        assert result == [20]

    def test_reduce(self):
        records = [
            create_record(1, "a", "cat1", 10, "2024-01-01"),
            create_record(2, "b", "cat2", 20, "2024-01-02"),
        ]
        pipeline = DataPipeline.from_list(records)
        result = pipeline.reduce(lambda acc, r: acc + r.value, 0)
        assert result == 30

    def test_group_by(self):
        records = [
            create_record(1, "a", "cat1", 10, "2024-01-01"),
            create_record(2, "b", "cat1", 20, "2024-01-02"),
            create_record(3, "c", "cat2", 30, "2024-01-03"),
        ]
        pipeline = DataPipeline.from_list(records)
        result = pipeline.group_by("category")
        assert len(result["cat1"]) == 2
        assert len(result["cat2"]) == 1

    def test_sort_by(self):
        records = [
            create_record(1, "a", "cat1", 30, "2024-01-01"),
            create_record(2, "b", "cat2", 10, "2024-01-02"),
            create_record(3, "c", "cat1", 20, "2024-01-03"),
        ]
        pipeline = DataPipeline.from_list(records)
        result = pipeline.sort_by("value").execute()
        assert result[0].value == 10
        assert result[2].value == 30

    def test_batch(self):
        records = [
            create_record(i, f"item{i}", "cat", i * 10, f"2024-01-{i}")
            for i in range(1, 10)
        ]
        pipeline = DataPipeline.from_list(records)
        batches = pipeline.batch(3)
        assert len(batches) == 3
        assert len(batches[0]) == 3

    def test_chain_operations(self):
        records = [
            create_record(1, "a", "cat1", 10, "2024-01-01"),
            create_record(2, "b", "cat2", 20, "2024-01-02"),
            create_record(3, "c", "cat1", 30, "2024-01-03"),
        ]
        pipeline = DataPipeline.from_list(records)
        result = (
            pipeline.filter(lambda r: r.category == "cat1")
            .sort_by("value", reverse=True)
            .execute()
        )
        assert len(result) == 2
        assert result[0].value == 30

    def test_empty_pipeline(self):
        pipeline = DataPipeline.from_list([])
        result = pipeline.filter(lambda r: True).execute()
        assert result == []

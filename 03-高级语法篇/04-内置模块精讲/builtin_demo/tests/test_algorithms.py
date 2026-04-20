from app.core.algorithms import (
    PriorityQueue,
    TaskScheduler,
    binary_search_left,
    binary_search_right,
    get_n_largest,
    get_n_smallest,
    heapify_list,
    insert_sorted,
    merge_sorted,
    pop_from_heap,
    push_to_heap,
)


class TestHeapOperations:
    def test_push_pop(self):
        heap = []
        push_to_heap(heap, 3)
        push_to_heap(heap, 1)
        push_to_heap(heap, 2)
        assert pop_from_heap(heap) == 1
        assert pop_from_heap(heap) == 2

    def test_heapify_list(self):
        result = heapify_list([3, 1, 4, 1, 5])
        assert result[0] == 1

    def test_n_smallest(self):
        result = get_n_smallest([5, 1, 4, 2, 3], 3)
        assert result == [1, 2, 3]

    def test_n_largest(self):
        result = get_n_largest([5, 1, 4, 2, 3], 3)
        assert result == [5, 4, 3]

    def test_merge_sorted(self):
        result = list(merge_sorted([1, 3, 5], [2, 4, 6]))
        assert result == [1, 2, 3, 4, 5, 6]


class TestBisectOperations:
    def test_binary_search_left(self):
        arr = [1, 2, 2, 2, 3]
        result = binary_search_left(arr, 2)
        assert result == 1

    def test_binary_search_right(self):
        arr = [1, 2, 2, 2, 3]
        result = binary_search_right(arr, 2)
        assert result == 4

    def test_insert_sorted(self):
        arr = [1, 2, 4, 5]
        insert_sorted(arr, 3)
        assert arr == [1, 2, 3, 4, 5]

    def test_binary_search_not_found(self):
        arr = [1, 3, 5]
        result = binary_search_left(arr, 2)
        assert result == 1


class TestPriorityQueue:
    def test_basic_operations(self):
        pq = PriorityQueue()
        pq.push("task1", priority=2)
        pq.push("task2", priority=1)
        pq.push("task3", priority=3)
        assert pq.pop() == ("task2", 1)
        assert pq.pop() == ("task1", 2)

    def test_empty_queue(self):
        pq = PriorityQueue()
        assert pq.is_empty()
        assert pq.pop() is None

    def test_peek(self):
        pq = PriorityQueue()
        pq.push("task", priority=1)
        assert pq.peek() == ("task", 1)
        assert pq.pop() == ("task", 1)


class TestTaskScheduler:
    def test_schedule_tasks(self):
        scheduler = TaskScheduler()
        scheduler.add_task("high", priority=1)
        scheduler.add_task("low", priority=3)
        scheduler.add_task("medium", priority=2)
        result = scheduler.run_all()
        assert result == ["high", "medium", "low"]

    def test_empty_scheduler(self):
        scheduler = TaskScheduler()
        result = scheduler.run_all()
        assert result == []

    def test_run_single(self):
        scheduler = TaskScheduler()
        scheduler.add_task("task1", priority=2)
        scheduler.add_task("task2", priority=1)
        result = scheduler.run_next()
        assert result == "task2"
        assert scheduler.run_next() == "task1"

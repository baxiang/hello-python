import gc

from app.core.weak_ref import (
    DataObject,
    ResourceTracker,
    WeakKeyCache,
    WeakValueCache,
    create_circular_demo,
    create_weak_reference,
)


class TestWeakReference:
    def test_create_weak_reference(self):
        obj = DataObject("value")
        ref = create_weak_reference(obj)
        assert ref() is obj

    def test_weak_reference_gone(self):
        obj = DataObject("value")
        ref = create_weak_reference(obj)
        del obj
        gc.collect()
        assert ref() is None


class TestWeakValueCache:
    def test_set_get(self):
        cache = WeakValueCache()
        obj = DataObject("test")
        cache.set("key", obj)
        assert cache.get("key") is obj

    def test_weak_value_cleanup(self):
        cache = WeakValueCache()
        obj = DataObject("data")
        cache.set("key", obj)
        del obj
        gc.collect()
        assert cache.get("key") is None

    def test_contains(self):
        cache = WeakValueCache()
        obj = DataObject("value")
        cache.set("key", obj)
        assert cache.contains("key")
        assert not cache.contains("missing")


class TestWeakKeyCache:
    def test_set_get(self):
        cache = WeakKeyCache()
        key = DataObject("key_obj")
        cache.set(key, "value")
        assert cache.get(key) == "value"

    def test_weak_key_cleanup(self):
        cache = WeakKeyCache()
        key = DataObject("key_obj")
        cache.set(key, "value")
        del key
        gc.collect()
        assert len(cache) == 0


class TestResourceTracker:
    def test_track_and_cleanup(self):
        tracker = ResourceTracker()
        resource = DataObject("important")
        tracker.track("res1", resource)
        assert tracker.get("res1") is resource

    def test_cleanup_on_deletion(self):
        tracker = ResourceTracker()
        resource = DataObject("important")
        tracker.track("res1", resource)
        del resource
        gc.collect()
        assert tracker.get("res1") is None
        assert tracker.cleanup_count() >= 1


class TestCircularReference:
    def test_create_circular_demo(self):
        node_a, node_b = create_circular_demo()
        assert node_a.next is node_b
        assert node_b.prev() is node_a
        assert node_a.value == "A"
        assert node_b.value == "B"

    def test_circular_cleanup(self):
        node_a, node_b = create_circular_demo()
        import weakref

        ref_a = weakref.ref(node_a)
        ref_b = weakref.ref(node_b)
        del node_a, node_b
        gc.collect()
        assert ref_a() is None
        assert ref_b() is None

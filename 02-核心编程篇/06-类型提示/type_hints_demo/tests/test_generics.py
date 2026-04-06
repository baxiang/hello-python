"""泛型测试"""

from app.core.generics import (
    first,
    reverse,
    get_middle,
    double,
    add_numbers,
    Stack,
    Repository,
    Entity,
)


def test_first():
    assert first([1, 2, 3]) == 1
    assert first(["a", "b", "c"]) == "a"


def test_reverse():
    assert reverse([1, 2, 3]) == [3, 2, 1]
    assert reverse(["a", "b"]) == ["b", "a"]


def test_get_middle():
    assert get_middle([1, 2, 3]) == 2
    assert get_middle(["a", "b", "c"]) == "b"


def test_double():
    assert double(5) == 10
    assert double(5.0) == 10.0


def test_add_numbers():
    assert add_numbers(1, 2) == 3
    assert add_numbers(1.5, 2.5) == 4.0


def test_stack():
    stack: Stack[int] = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)

    assert stack.pop() == 3
    assert stack.peek() == 2
    assert not stack.is_empty()

    assert stack.pop() == 2
    assert stack.pop() == 1
    assert stack.is_empty()


def test_stack_with_strings():
    stack: Stack[str] = Stack()
    stack.push("a")
    stack.push("b")

    assert stack.pop() == "b"
    assert stack.peek() == "a"


def test_repository():
    repo: Repository[Entity] = Repository()

    entity = Entity(id=1)
    index = repo.add(entity)

    assert index == 0
    assert repo.get(0) == entity
    assert len(repo.get_all()) == 1


def test_repository_operations():
    repo: Repository[Entity] = Repository()

    e1 = Entity(id=1)
    e2 = Entity(id=2)

    repo.add(e1)
    repo.add(e2)

    assert repo.update(0, Entity(id=10)) == True
    assert repo.get(0) is not None
    assert repo.get(0).id == 10

    assert repo.delete(1) == True
    assert len(repo.get_all()) == 1

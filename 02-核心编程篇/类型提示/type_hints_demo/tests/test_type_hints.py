"""类型提示测试"""

from app.core.type_hints import (
    greet,
    find_user,
    process,
    User,
    Stack,
    Circle,
    Square,
    render,
    apply,
    add,
    multiply,
)
from app.utils.helpers import first, reverse, count_words, safe_get


def test_greet():
    assert greet("张三", 25) == "Hello 张三, you are 25 years old"
    assert greet("李四", 30) == "Hello 李四, you are 30 years old"


def test_find_user():
    user = find_user(1)
    assert user is not None
    assert user["name"] == "张三"

    user = find_user(999)
    assert user is None


def test_process():
    assert process(5) == "整数: 10"
    assert process("hello") == "字符串: HELLO"


def test_user():
    user = User(1, "张三", "test@example.com", 25)
    assert user.id == 1
    assert user.name == "张三"
    assert user.to_dict()["name"] == "张三"


def test_stack():
    stack: Stack[int] = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)

    assert stack.pop() == 3
    assert stack.peek() == 2
    assert not stack.is_empty()


def test_render():
    circle = Circle()
    square = Square()

    render(circle)
    render(square)


def test_apply():
    result = apply(add, 5, 3)
    assert result == 8

    result = apply(multiply, 5, 3)
    assert result == 15


def test_first():
    assert first([1, 2, 3]) == 1
    assert first(["a", "b", "c"]) == "a"


def test_reverse():
    assert reverse([1, 2, 3]) == [3, 2, 1]
    assert reverse(["a", "b"]) == ["b", "a"]


def test_count_words():
    result = count_words("hello world hello")
    assert result["hello"] == 2
    assert result["world"] == 1


def test_safe_get():
    data = {"name": "张三", "age": "25"}
    assert safe_get(data, "name") == "张三"
    assert safe_get(data, "email") is None

"""第 1 章测试 — 函数是一等公民"""

from app.decorators.ch01_first_class import (
    dispatch,
    execute,
    get_operation,
    greet,
    say_hello,
)


class TestFirstClassFunctions:
    """测试函数的四大能力"""

    def test_assign_to_variable(self):
        """能力 1: 函数可以赋值给变量"""
        assert say_hello("Alice") == "Hello, Alice!"
        assert say_hello is greet  # 赋值是引用，指向同一对象
        assert say_hello("Bob") == greet("Bob")  # 行为完全相同

    def test_pass_as_argument(self):
        """能力 2: 函数可以作为参数传递"""
        result = execute(greet, "World")
        assert result == "Hello, World!"

    def test_return_as_value(self):
        """能力 3: 函数可以作为返回值"""
        add = get_operation("add")
        assert add(3, 5) == 8

        sub = get_operation("sub")
        assert sub(10, 4) == 6

        mul = get_operation("mul")
        assert mul(3, 7) == 21

        unknown = get_operation("unknown")
        assert unknown(1, 2) == 0

    def test_store_in_data_structure(self):
        """能力 4: 函数可以存储在数据结构中"""
        result = dispatch("/users", {})
        assert result == {"users": ["Alice", "Bob", "Charlie"]}

        result = dispatch("/products", {})
        assert result == {"products": ["Apple", "Banana"]}

        result = dispatch("/orders", {})
        assert result == {"orders": [{"id": 1, "user": "Alice"}]}

    def test_dispatch_unknown_path(self):
        """未知路径返回 None"""
        assert dispatch("/unknown", {}) is None

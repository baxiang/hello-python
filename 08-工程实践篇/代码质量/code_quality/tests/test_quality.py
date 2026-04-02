"""代码质量测试"""

from app.core.quality import calculate_average, Calculator, User


def test_calculate_average():
    assert calculate_average([1, 2, 3]) == 2.0
    assert calculate_average([10, 20, 30, 40]) == 25.0


def test_calculator():
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.subtract(10, 4) == 6
    assert calc.multiply(3, 4) == 12


def test_user():
    user = User(1, "张三", "test@example.com")
    assert user.id == 1
    assert user.to_dict()["name"] == "张三"
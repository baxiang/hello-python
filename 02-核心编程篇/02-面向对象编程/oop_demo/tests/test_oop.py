"""面向对象测试"""

from app.core.classes import Person, Student, Circle, Point


def test_person():
    p = Person("张三", 25)
    assert p.name == "张三"
    assert p.age == 25
    assert "张三" in p.introduce()


def test_student():
    s = Student("李四", 18, "高三")
    assert s.grade == "高三"
    assert "高三" in s.introduce()


def test_circle():
    c = Circle(5)
    assert c.radius == 5
    assert c.area > 75


def test_point():
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    assert p1.distance_to(p2) == 5.0
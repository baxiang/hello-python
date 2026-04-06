"""协议测试"""

from app.core.protocols import (
    Circle,
    Square,
    render,
    Person,
    User,
    Serializable,
    UserDict,
    create_user,
    find_max,
)


def test_render():
    circle = Circle()
    square = Square()

    render(circle)
    render(square)


def test_person_compare():
    p1 = Person("张三", 25)
    p2 = Person("李四", 18)

    assert p1.compare_to(p2) > 0
    assert p2.compare_to(p1) < 0

    p3 = Person("王五", 25)
    assert p1.compare_to(p3) == 0


def test_serializable():
    user = User("张三", 25)

    assert isinstance(user, Serializable)
    json_str = user.to_json()
    assert "张三" in json_str
    assert "25" in json_str


def test_user_dict():
    user_data: UserDict = {
        "id": 1,
        "name": "张三",
        "email": "test@example.com",
        "age": None,
    }

    result = create_user(user_data)
    assert result["id"] == 1
    assert result["name"] == "张三"


def test_find_max():
    people = [Person("张三", 25), Person("李四", 18), Person("王五", 30)]

    max_person = find_max(people)
    assert max_person.name == "王五"
    assert max_person.age == 30

"""异常测试"""

from app.core.exceptions import divide, validate_age, ValidationError, AgeError


def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(10, 0) is None


def test_validate_age():
    assert validate_age(25) is True
    
    try:
        validate_age(-5)
    except AgeError:
        pass
    
    try:
        validate_age(200)
    except AgeError:
        pass
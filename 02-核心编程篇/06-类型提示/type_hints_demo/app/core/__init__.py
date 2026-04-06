"""类型提示核心模块"""

from app.core.basics import (
    count_words,
    find_user,
    parse_value,
    apply_operation,
)
from app.core.generics import (
    first,
    reverse,
    Stack,
    Repository,
    Entity,
)
from app.core.protocols import (
    Drawable,
    Circle,
    Square,
    render,
    Person,
    User,
    UserDict,
)
from app.core.advanced import (
    log_call,
    Config,
    is_string_list,
)

__all__ = [
    "count_words",
    "find_user",
    "parse_value",
    "apply_operation",
    "first",
    "reverse",
    "Stack",
    "Repository",
    "Entity",
    "Drawable",
    "Circle",
    "Square",
    "render",
    "Person",
    "User",
    "UserDict",
    "log_call",
    "Config",
    "is_string_list",
]

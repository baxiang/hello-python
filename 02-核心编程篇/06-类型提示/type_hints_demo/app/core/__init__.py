"""类型提示核心模块"""

from app.core.advanced import (
    Config,
    is_string_list,
    log_call,
)
from app.core.basics import (
    apply_operation,
    count_words,
    find_user,
    parse_value,
)
from app.core.generics import (
    Entity,
    Repository,
    Stack,
    first,
    reverse,
)
from app.core.protocols import (
    Circle,
    Drawable,
    Person,
    Square,
    User,
    UserDict,
    render,
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

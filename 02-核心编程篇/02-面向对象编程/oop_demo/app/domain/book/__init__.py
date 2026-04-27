"""图书领域 — BookItem 层次结构"""

from app.domain.book.mixins import DigitalMixin
from app.domain.book.model import AudioBook, BookItem, EBook, PhysicalBook

__all__ = [
    "BookItem",
    "PhysicalBook",
    "EBook",
    "AudioBook",
    "DigitalMixin",
]

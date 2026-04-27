"""通知服务接口 — Protocol 实现依赖倒置原则（DIP）

覆盖：ch06 依赖倒置、开放封闭原则
"""

from __future__ import annotations

from typing import Protocol


class NotificationService(Protocol):
    """通知服务协议

    任何实现了 notify(member, message) 的对象都满足此接口。
    Library 依赖此抽象而非具体实现 → DIP。
    """

    def notify(self, member, message: str) -> None:  # type: ignore[reportUnknownParameterType]
        ...

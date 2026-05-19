"""通知服务实现

覆盖：ch06 依赖注入、开放封闭原则（新增通知方式无需改 Library）
"""

from __future__ import annotations

from app.domain.member import Member
from app.ports.notification import NotificationService


class ConsoleNotification:
    """控制台通知 — 默认实现"""

    def notify(self, member: Member, message: str) -> None:
        print(f"[通知] {member.name}: {message}")


class SilentNotification:
    """静默通知 — 测试用，不输出任何内容，但记录消息"""

    def __init__(self) -> None:
        self.messages: list[tuple[str, str]] = []

    def notify(self, member: Member, message: str) -> None:
        self.messages.append((member.name, message))


class EmailNotification:
    """邮件通知 — 模拟实现（不真正发送邮件）"""

    def __init__(self) -> None:
        self.sent_emails: list[tuple[str, str, str]] = []

    def notify(self, member: Member, message: str) -> None:
        self.sent_emails.append((member.email, member.name, message))

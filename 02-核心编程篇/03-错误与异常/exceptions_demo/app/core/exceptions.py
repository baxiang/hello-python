"""异常示例 — 覆盖第01-04章（错误与异常）

场景：银行账户操作系统

章节对应：
  ch01  异常类层次：BankError → InsufficientFundsError / AccountLockedError
        try/except 捕获、except 多个异常
  ch02  try/except/else/finally 完整结构
        捕获具体异常 vs 宽泛异常
  ch03  raise 抛出异常；raise ... from ... 异常链
        自定义 __init__ 携带额外上下文
  ch04  上下文管理器：__enter__ / __exit__；contextlib.contextmanager
"""

from __future__ import annotations

import contextlib
from collections.abc import Generator

# ---------------------------------------------------------------------------
# ch01 / ch03: 自定义异常层次
# ---------------------------------------------------------------------------

class BankError(Exception):
    """银行业务基础异常（ch01：自定义异常基类）"""

    def __init__(self, message: str, account_id: str = "") -> None:
        super().__init__(message)
        self.account_id = account_id   # 额外上下文字段

    def __str__(self) -> str:
        prefix = f"[账户 {self.account_id}] " if self.account_id else ""
        return f"{prefix}{super().__str__()}"


class InsufficientFundsError(BankError):
    """余额不足（ch01：异常继承）"""

    def __init__(self, account_id: str, required: float, available: float) -> None:
        super().__init__(
            f"余额不足：需要 {required:.2f}，可用 {available:.2f}",
            account_id,
        )
        self.required = required
        self.available = available


class AccountLockedError(BankError):
    """账户已锁定（ch01：异常继承）"""


class InvalidAmountError(BankError):
    """金额无效（ch01：参数校验类异常）"""


# ---------------------------------------------------------------------------
# ch01 / ch02: try / except / else / finally
# ---------------------------------------------------------------------------

class BankAccount:
    """银行账户（ch01-02：异常处理完整示例）"""

    def __init__(self, account_id: str, balance: float = 0.0) -> None:
        self.account_id = account_id
        self._balance: float = balance
        self._locked: bool = False
        self._transaction_log: list[str] = []

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def locked(self) -> bool:
        return self._locked

    def lock(self) -> None:
        self._locked = True

    def unlock(self) -> None:
        self._locked = False

    def deposit(self, amount: float) -> float:
        """存款（ch02：try/except/else/finally 完整结构）

        Raises:
            AccountLockedError: 账户已锁定时抛出
            InvalidAmountError: 金额无效时抛出

        else  → 仅在 try 无异常时执行（记录日志）
        finally → 无论成功/失败都执行（可在此做资源清理）
        """
        try:
            if self._locked:
                raise AccountLockedError("账户已锁定，无法存款", self.account_id)
            if amount <= 0:
                raise InvalidAmountError(f"存款金额必须大于 0，收到 {amount}", self.account_id)
            self._balance += amount
        except (AccountLockedError, InvalidAmountError):
            raise                              # 重新抛出，让调用方处理
        else:
            self._transaction_log.append(f"+{amount:.2f}")   # ch02: else
        finally:
            self._transaction_log.append("deposit:cleanup")   # ch02: finally（演示清理逻辑）
        return self._balance

    def withdraw(self, amount: float) -> float:
        """取款（ch02/ch03：多异常类型 + raise）"""
        if self._locked:
            raise AccountLockedError("账户已锁定，无法取款", self.account_id)
        if amount <= 0:
            raise InvalidAmountError(f"取款金额必须大于 0，收到 {amount}", self.account_id)
        if amount > self._balance:
            raise InsufficientFundsError(self.account_id, amount, self._balance)
        self._balance -= amount
        self._transaction_log.append(f"-{amount:.2f}")
        return self._balance

    def transfer(self, target: BankAccount, amount: float) -> None:
        """转账（ch03：raise ... from ... 异常链）"""
        try:
            self.withdraw(amount)
        except InsufficientFundsError as e:
            # ch03: raise ... from ... 保留原始异常上下文
            raise BankError(
                f"转账失败：{self.account_id} → {target.account_id}",
                self.account_id,
            ) from e
        target.deposit(amount)

    def get_log(self) -> list[str]:
        return list(self._transaction_log)


def safe_parse_amount(text: str) -> float:
    """安全解析金额字符串（ch02：捕获多种内置异常）"""
    try:
        value = float(text)
    except (ValueError, TypeError) as e:
        raise InvalidAmountError(f"无效金额格式: {text!r}") from e
    if value < 0:
        raise InvalidAmountError(f"金额不能为负数: {value}")
    return value


# ---------------------------------------------------------------------------
# ch04: 上下文管理器
# ---------------------------------------------------------------------------

class TransactionContext:
    """事务上下文管理器（ch04：__enter__ / __exit__）

    with TransactionContext(account) as txn:
        account.deposit(100)

    正常退出 → 提交事务（记录快照差值）
    异常退出 → 回滚（恢复余额到进入前的状态）
    """

    def __init__(self, account: BankAccount) -> None:
        self._account = account
        self._snapshot: float = 0.0

    def __enter__(self) -> TransactionContext:
        self._snapshot = self._account.balance   # 保存进入时余额
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> bool:
        if exc_type is not None:
            # 发生异常 → 回滚
            self._account._balance = self._snapshot
            self._account._transaction_log.append("ROLLBACK")
            return False   # 不吞掉异常，继续向上传播
        # 正常退出 → 提交（什么都不需要做，状态已就绪）
        self._account._transaction_log.append("COMMIT")
        return False

    @property
    def delta(self) -> float:
        """本次事务余额变化量"""
        return self._account.balance - self._snapshot


@contextlib.contextmanager
def audit_log(account: BankAccount, operation: str) -> Generator[None, None, None]:
    """审计日志上下文管理器（ch04：@contextmanager 装饰器方式）

    yield 之前 = __enter__；yield 之后 = __exit__
    """
    account._transaction_log.append(f"BEGIN:{operation}")
    try:
        yield
    except BankError as e:
        account._transaction_log.append(f"ERROR:{operation}:{e}")
        raise
    else:
        account._transaction_log.append(f"END:{operation}")

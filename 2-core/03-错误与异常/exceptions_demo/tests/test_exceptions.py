"""异常篇测试套件 — 银行账户操作系统，覆盖第01-04章"""

import pytest

from app.core.exceptions import (
    AccountLockedError,
    BankAccount,
    BankError,
    InsufficientFundsError,
    InvalidAmountError,
    TransactionContext,
    audit_log,
    safe_parse_amount,
)


# ===========================================================================
# ch01: 错误与异常基础 — 自定义异常层次
# ===========================================================================
class TestExceptionHierarchy:
    """ch01: 自定义异常继承、isinstance 检查、额外字段"""

    def test_bank_error_is_exception(self):
        err = BankError("测试", "ACC001")
        assert isinstance(err, Exception)
        assert err.account_id == "ACC001"

    def test_insufficient_funds_is_bank_error(self):
        err = InsufficientFundsError("ACC001", 200.0, 100.0)
        assert isinstance(err, BankError)
        assert err.required == 200.0
        assert err.available == 100.0

    def test_account_locked_is_bank_error(self):
        err = AccountLockedError("账户已锁定", "ACC001")
        assert isinstance(err, BankError)

    def test_bank_error_str_includes_account_id(self):
        err = BankError("余额不足", "ACC001")
        assert "ACC001" in str(err)

    def test_bank_error_str_without_account_id(self):
        err = BankError("通用错误")
        assert "通用错误" in str(err)

    def test_catch_by_base_class(self):
        """捕获基类可以捕获所有子类异常"""
        account = BankAccount("ACC001", 50.0)
        with pytest.raises(BankError):
            account.withdraw(200.0)   # InsufficientFundsError 也是 BankError


# ===========================================================================
# ch02: 异常处理 — try/except/else/finally
# ===========================================================================
class TestExceptionHandling:
    """ch02: try/except 多异常类型；else 只在无异常时执行；finally 总执行"""

    def test_deposit_success_logs_in_else(self):
        """else 分支：成功存款后日志被记录"""
        account = BankAccount("ACC001")
        account.deposit(100.0)
        assert "+100.00" in account.get_log()

    def test_deposit_invalid_amount_no_log(self):
        """异常发生时 else 不执行，交易日志不被记录，但 finally 清理日志会被记录"""
        account = BankAccount("ACC001")
        with pytest.raises(InvalidAmountError):
            account.deposit(-10.0)
        # else 分支未执行 → 没有 "+..." 记录
        assert not any(e.startswith("+") for e in account.get_log())
        # finally 分支总是执行 → 有清理记录
        assert "deposit:cleanup" in account.get_log()

    def test_withdraw_insufficient_funds(self):
        account = BankAccount("ACC001", 50.0)
        with pytest.raises(InsufficientFundsError) as exc_info:
            account.withdraw(200.0)
        assert exc_info.value.required == 200.0
        assert exc_info.value.available == 50.0

    def test_withdraw_locked_account(self):
        account = BankAccount("ACC001", 100.0)
        account.lock()
        with pytest.raises(AccountLockedError):
            account.withdraw(50.0)

    def test_deposit_locked_account(self):
        account = BankAccount("ACC001")
        account.lock()
        with pytest.raises(AccountLockedError):
            account.deposit(100.0)

    def test_safe_parse_amount_valid(self):
        assert safe_parse_amount("99.5") == pytest.approx(99.5)

    def test_safe_parse_amount_invalid_string(self):
        with pytest.raises(InvalidAmountError):
            safe_parse_amount("abc")

    def test_safe_parse_amount_negative(self):
        with pytest.raises(InvalidAmountError):
            safe_parse_amount("-10")

    def test_withdraw_zero_amount(self):
        account = BankAccount("ACC001", 100.0)
        with pytest.raises(InvalidAmountError):
            account.withdraw(0)


# ===========================================================================
# ch03: 抛出异常 — raise / raise from / 异常链
# ===========================================================================
class TestRaisingExceptions:
    """ch03: raise 显式抛出；raise ... from ... 异常链；__cause__"""

    def test_transfer_insufficient_raises_bank_error(self):
        """raise BankError from InsufficientFundsError"""
        src = BankAccount("SRC", 50.0)
        dst = BankAccount("DST", 0.0)
        with pytest.raises(BankError):
            src.transfer(dst, 200.0)

    def test_transfer_exception_chain_preserved(self):
        """raise X from Y → X.__cause__ 是 Y"""
        src = BankAccount("SRC", 50.0)
        dst = BankAccount("DST", 0.0)
        with pytest.raises(BankError) as exc_info:
            src.transfer(dst, 200.0)
        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, InsufficientFundsError)

    def test_safe_parse_exception_chain(self):
        """safe_parse_amount 中的 raise X from Y"""
        with pytest.raises(InvalidAmountError) as exc_info:
            safe_parse_amount("not_a_number")
        assert exc_info.value.__cause__ is not None   # 原始 ValueError 被保留

    def test_transfer_success(self):
        src = BankAccount("SRC", 200.0)
        dst = BankAccount("DST", 0.0)
        src.transfer(dst, 100.0)
        assert src.balance == pytest.approx(100.0)
        assert dst.balance == pytest.approx(100.0)


# ===========================================================================
# ch04: 上下文管理器 — __enter__ / __exit__ / @contextmanager
# ===========================================================================
class TestContextManager:
    """ch04: TransactionContext（类方式）；audit_log（@contextmanager 方式）"""

    def test_transaction_context_commit(self):
        """正常退出 → COMMIT 被记录"""
        account = BankAccount("ACC001", 200.0)
        with TransactionContext(account):
            account.deposit(50.0)
        assert "COMMIT" in account.get_log()
        assert account.balance == pytest.approx(250.0)

    def test_transaction_context_rollback_on_exception(self):
        """异常退出 → 余额回滚到进入前，ROLLBACK 被记录"""
        account = BankAccount("ACC001", 200.0)
        with pytest.raises(InvalidAmountError), TransactionContext(account):
            account.deposit(-50.0)   # 触发异常
        assert account.balance == pytest.approx(200.0)   # 回滚
        assert "ROLLBACK" in account.get_log()

    def test_transaction_context_delta(self):
        account = BankAccount("ACC001", 100.0)
        with TransactionContext(account) as txn:
            account.deposit(50.0)
        assert txn.delta == pytest.approx(50.0)

    def test_context_manager_enter_exit_called(self):
        """__enter__ 返回 TransactionContext 实例"""
        account = BankAccount("ACC001", 100.0)
        with TransactionContext(account) as ctx:
            assert isinstance(ctx, TransactionContext)

    def test_audit_log_contextmanager_success(self):
        """@contextmanager：正常退出 → BEGIN/END 被记录"""
        account = BankAccount("ACC001", 100.0)
        with audit_log(account, "deposit"):
            account.deposit(50.0)
        log = account.get_log()
        assert any(e.startswith("BEGIN:deposit") for e in log)
        assert any(e.startswith("END:deposit") for e in log)

    def test_audit_log_contextmanager_error(self):
        """@contextmanager：异常退出 → BEGIN/ERROR 被记录，异常继续传播"""
        account = BankAccount("ACC001", 50.0)
        with pytest.raises(InsufficientFundsError):
            with audit_log(account, "withdraw"):
                account.withdraw(200.0)
        log = account.get_log()
        assert any(e.startswith("BEGIN:withdraw") for e in log)
        assert any(e.startswith("ERROR:withdraw") for e in log)

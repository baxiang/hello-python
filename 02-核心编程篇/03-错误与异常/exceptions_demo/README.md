# 错误与异常

Python 异常处理示例项目，覆盖第 01-04 章（异常层次 → try/except/else/finally → raise/异常链 → 上下文管理器）。

## 场景

银行账户操作系统：通过 BankAccount 的存款、取款、转账操作，演示异常创建、捕获、抛出和上下文管理的完整流程。

## 项目结构

```
exceptions_demo/
├── pyproject.toml
├── app/
│   ├── __init__.py
│   ├── core/
│   │   └── exceptions.py   # ch01-04: 异常层次、try/except、raise from、上下文管理器
│   └── utils/
│       └── helpers.py      # safe_execute 安全执行上下文
└── tests/
    └── test_exceptions.py  # 20 个测试
```

## 安装

```bash
uv sync
```

## 使用示例

```python
from app.core.exceptions import (
    BankAccount, BankError, InsufficientFundsError,
    TransactionContext, audit_log, safe_parse_amount
)

# ch01-02: 异常处理
account = BankAccount("ACC001", 100.0)
account.deposit(50.0)           # → 150.0
account.withdraw(200.0)         # → 抛出 InsufficientFundsError

# ch03: 异常链
src = BankAccount("SRC", 50.0)
dst = BankAccount("DST", 0.0)
src.transfer(dst, 200.0)        # → 抛出 BankError，__cause__ 为 InsufficientFundsError

# ch04: 上下文管理器（自动回滚）
with TransactionContext(account) as txn:
    account.deposit(50.0)
# 正常退出 → COMMIT；异常退出 → ROLLBACK（余额回滚）

# ch04: @contextmanager 审计日志
with audit_log(account, "deposit"):
    account.deposit(100.0)
# 日志: BEGIN:deposit → END:deposit（或 ERROR:deposit:...）
```

## 运行测试

```bash
uv run pytest               # 全部测试
uv run pytest -k "context"  # 只运行上下文管理器测试
uv run pytest -k "chain"    # 只运行异常链测试
```

## 章节映射

| 代码文件 | 对应章节 | 核心内容 |
|---------|---------|---------|
| `exceptions.py` | ch01-02 | BankError 层次、try/except/else/finally 完整结构 |
| `exceptions.py` | ch03 | raise、raise from 异常链、自定义异常 __init__ |
| `exceptions.py` | ch04 | TransactionContext（__enter__/__exit__）、audit_log（@contextmanager） |
| `helpers.py` | ch04 | safe_execute 安全执行上下文 |

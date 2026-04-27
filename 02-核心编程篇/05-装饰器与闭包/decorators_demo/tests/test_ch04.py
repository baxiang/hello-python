"""第 4 章测试 — 带参数装饰器"""

import pytest

from app.decorators.ch04_parameterized import (
    create_rate_limiter,
    repeat,
    require_role,
    retry,
)


class TestParameterizedDecorators:
    """测试带参数装饰器"""

    def test_repeat_executes_multiple_times(self):
        call_count = 0

        @repeat(times=3)
        def increment():
            nonlocal call_count
            call_count += 1

        increment()
        assert call_count == 3

    def test_require_role_allows_correct_role(self):
        @require_role("admin")
        def admin_action(request=None):
            return {"status": 200}

        class MockRequest:
            role = "admin"

        result = admin_action(request=MockRequest())
        assert result == {"status": 200}

    def test_require_role_denies_wrong_role(self):
        @require_role("admin")
        def admin_action(request=None):
            return {"status": 200}

        class MockRequest:
            role = "guest"

        result = admin_action(request=MockRequest())
        assert result["status"] == 403
        assert result["required"] == "admin"

    def test_retry_succeeds_first_attempt(self):
        @retry(max_attempts=3)
        def always_ok():
            return "ok"

        assert always_ok() == "ok"

    def test_retry_retries_on_failure(self):
        call_count = 0

        @retry(max_attempts=3, exceptions=(ValueError,))
        def unstable():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("暂时失败")
            return "success"

        result = unstable()
        assert result == "success"
        assert call_count == 3

    def test_retry_raises_after_max(self):
        @retry(max_attempts=2, exceptions=(RuntimeError,))
        def always_fail():
            raise RuntimeError("持续失败")

        try:
            always_fail()
            pytest.fail("应该抛出异常")
        except RuntimeError:
            pass

    def test_rate_limiter_allows_within_limit(self):
        limiter = create_rate_limiter(3)

        @limiter
        def api_call():
            return "ok"

        assert api_call() == "ok"
        assert api_call() == "ok"
        assert api_call() == "ok"

    def test_rate_limiter_blocks_over_limit(self):
        limiter = create_rate_limiter(2)

        @limiter
        def api_call():
            return "ok"

        api_call()
        api_call()
        try:
            api_call()
            pytest.fail("应该抛出异常")
        except RuntimeError:
            pass

    def test_rate_limiter_reset(self):
        limiter = create_rate_limiter(1)

        @limiter
        def api_call():
            return "ok"

        api_call()
        api_call.reset()  # type: ignore[attr-defined]
        assert api_call() == "ok"

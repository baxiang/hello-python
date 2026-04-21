"""请求日志中间件"""

import logging
import time
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """处理请求并记录日志"""
        start_time = time.time()

        method = request.method
        path = request.url.path

        response = await call_next(request)

        duration = time.time() - start_time
        status_code = response.status_code

        logger.info(f"{method} {path} - {status_code} - {duration:.3f}s")

        return response
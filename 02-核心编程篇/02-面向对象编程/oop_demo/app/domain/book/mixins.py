"""图书领域 Mixin — 为多重继承提供数字内容能力"""

from __future__ import annotations


class DigitalMixin:
    """数字内容 Mixin

    通过多重继承为子类提供文件信息展示能力。
    自身不继承 Catalogable，只关注"数字内容"这一横切关注点。
    """

    _file_size_mb: float
    _format: str

    def download_info(self) -> str:
        return f"{self._format} | {self._file_size_mb:.1f} MB"

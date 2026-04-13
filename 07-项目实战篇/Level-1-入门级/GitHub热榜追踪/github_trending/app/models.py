from dataclasses import dataclass, asdict


@dataclass
class TrendingRepo:
    """GitHub Trending 项目数据模型"""

    name: str
    description: str
    language: str
    stars: int
    forks: int
    stars_today: int
    url: str

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return asdict(self)

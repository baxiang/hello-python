"""版本管理"""

from dataclasses import dataclass


@dataclass
class Version:
    """版本号"""
    major: int = 0
    minor: int = 1
    patch: int = 0
    
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
    
    def bump_major(self) -> "Version":
        return Version(self.major + 1, 0, 0)
    
    def bump_minor(self) -> "Version":
        return Version(self.major, self.minor + 1, 0)
    
    def bump_patch(self) -> "Version":
        return Version(self.major, self.minor, self.patch + 1)
    
    @classmethod
    def parse(cls, version_str: str) -> "Version":
        """解析版本字符串"""
        parts = version_str.split(".")
        return cls(
            major=int(parts[0]) if len(parts) > 0 else 0,
            minor=int(parts[1]) if len(parts) > 1 else 0,
            patch=int(parts[2]) if len(parts) > 2 else 0
        )
# 项目管理示例

"""
项目管理示例
包含：配置管理、依赖管理、版本控制
"""

import os
import json
import tomllib
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


# 1. 配置管理
@dataclass
class Config:
    """应用配置"""
    app_name: str = "MyApp"
    version: str = "0.1.0"
    debug: bool = False
    database_url: str = "sqlite:///app.db"
    secret_key: str = "dev-secret-key"
    
    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量加载"""
        return cls(
            app_name=os.getenv("APP_NAME", "MyApp"),
            version=os.getenv("APP_VERSION", "0.1.0"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            database_url=os.getenv("DATABASE_URL", "sqlite:///app.db"),
            secret_key=os.getenv("SECRET_KEY", "dev-secret-key")
        )
    
    @classmethod
    def from_file(cls, filepath: str) -> "Config":
        """从文件加载"""
        path = Path(filepath)
        
        if path.suffix == ".json":
            with open(path) as f:
                data = json.load(f)
        elif path.suffix in (".toml", ".lock"):
            with open(path, "rb") as f:
                data = tomllib.load(f)
        else:
            raise ValueError(f"不支持的配置文件格式: {path.suffix}")
        
        return cls(**data)


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self._config: Optional[Config] = None
        self._overrides: Dict[str, Any] = {}
    
    def load(self, config: Config) -> None:
        """加载配置"""
        self._config = config
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        if key in self._overrides:
            return self._overrides[key]
        if self._config and hasattr(self._config, key):
            return getattr(self._config, key)
        return default
    
    def set(self, key: str, value: Any) -> None:
        """设置配置项"""
        self._overrides[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        if not self._config:
            return {}
        result = {
            "app_name": self._config.app_name,
            "version": self._config.version,
            "debug": self._config.debug,
            "database_url": self._config.database_url,
        }
        result.update(self._overrides)
        return result


# 2. 版本管理
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


# 3. 项目结构
class ProjectStructure:
    """项目结构管理"""
    
    def __init__(self, root: str = "."):
        self.root = Path(root)
    
    def create_structure(self) -> None:
        """创建标准项目结构"""
        directories = [
            "src",
            "tests",
            "docs",
            "config",
            "scripts",
            ".github/workflows"
        ]
        
        for directory in directories:
            path = self.root / directory
            path.mkdir(parents=True, exist_ok=True)
        
        # 创建基础文件
        self._create_file("README.md", "# Project\n")
        self._create_file(".gitignore", "*.pyc\n__pycache__/\n.env\n")
        self._create_file("pyproject.toml", self._get_pyproject_template())
    
    def _create_file(self, name: str, content: str) -> None:
        """创建文件"""
        path = self.root / name
        if not path.exists():
            path.write_text(content)
    
    def _get_pyproject_template(self) -> str:
        """获取 pyproject.toml 模板"""
        return """[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""


# 4. 依赖管理
class DependencyManager:
    """依赖管理器"""
    
    def __init__(self, pyproject_path: str = "pyproject.toml"):
        self.pyproject_path = Path(pyproject_path)
    
    def get_dependencies(self) -> Dict[str, str]:
        """获取依赖"""
        if not self.pyproject_path.exists():
            return {}
        
        with open(self.pyproject_path, "rb") as f:
            data = tomllib.load(f)
        
        return data.get("project", {}).get("dependencies", [])
    
    def add_dependency(self, package: str, version: str = "") -> None:
        """添加依赖"""
        deps = self.get_dependencies()
        dep_str = f"{package}{version}" if version else package
        
        if dep_str not in deps:
            deps.append(dep_str)
            self._update_dependencies(deps)
    
    def _update_dependencies(self, deps: list) -> None:
        """更新依赖"""
        # 简化实现，实际需要修改文件
        pass


# 5. 环境管理
class Environment:
    """环境管理"""
    
    DEV = "development"
    STAGING = "staging"
    PROD = "production"
    
    def __init__(self, env: str = None):
        self.env = env or os.getenv("ENV", self.DEV)
    
    def is_dev(self) -> bool:
        return self.env == self.DEV
    
    def is_staging(self) -> bool:
        return self.env == self.STAGING
    
    def is_prod(self) -> bool:
        return self.env == self.PROD
    
    def get_config_file(self) -> str:
        """获取配置文件"""
        return f"config/{self.env}.json"


if __name__ == "__main__":
    print("=" * 40)
    print("项目管理示例")
    print("=" * 40)
    
    # 配置管理
    print("\n【配置管理】")
    config = Config.from_env()
    print(f"应用名: {config.app_name}")
    print(f"版本: {config.version}")
    print(f"调试模式: {config.debug}")
    
    # 版本管理
    print("\n【版本管理】")
    version = Version.parse("1.2.3")
    print(f"当前版本: {version}")
    print(f"升级 minor: {version.bump_minor()}")
    print(f"升级 major: {version.bump_major()}")
    
    # 环境管理
    print("\n【环境管理】")
    env = Environment("development")
    print(f"当前环境: {env.env}")
    print(f"是开发环境: {env.is_dev()}")
    print(f"配置文件: {env.get_config_file()}")
    
    # 项目结构
    print("\n【项目结构】")
    print("标准目录结构:")
    print("  src/          - 源代码")
    print("  tests/        - 测试代码")
    print("  docs/         - 文档")
    print("  config/       - 配置文件")
    print("  scripts/      - 脚本")
    print("  .github/      - GitHub 配置")